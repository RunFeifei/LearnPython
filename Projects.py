import logging
import os
import subprocess

from Config import *
from Snapshots import getListSnapshotDepends

# 此文件负责远端工程clone到本地
# getstatusoutput 同步执行

# 凡是package.gradle文件中以-SNAPSHOT为结尾的包都是待发布的包
# snack   : 'com.keruyun.osmobile:snack:2.9.2-SNAPSHOT',
# 以快餐为例 2.9.2-SNAPSHOT是扫描到的版本号,需要cd到snack目录下,修改gradle文件中的版本号为2.9.2,然后执行打包脚本,然后commit&push
# 然后修改storage下的package.gradle目录,把snack:2.9.2-SNAPSHOT修改为snack:2.9.2


# package.gradle文件禁止有注释行 禁止在行末尾进行注释 禁止在每一组的依赖中间有空行

# 拿到
from Storage import PACKAGE_GRADLE_PATH


def pre_process_upload_data():
    snap_shots = getListSnapshotDepends(PACKAGE_GRADLE_PATH)
    list_upload_data = []
    for snap in snap_shots:
        for x, y in snap.items():
            try:
                repo = REPOS_DICT[x]
            except KeyError:
                logging.error(' 没有在Config.py中找到配置信息-->' + x)
                pass
            else:
                list_upload_data.append(repo)
    return list_upload_data


def clone_codes():
    if os.path.exists(LOCAL_GIT_REPOS.strip()):
        status, output = subprocess.getstatusoutput('rm -rf' + LOCAL_GIT_REPOS)
        if status != 0:
            raise RuntimeError('rm -rf LOCAL_GIT_REPOS failed')

    status, output = subprocess.getstatusoutput('mkdir' + LOCAL_GIT_REPOS)
    if status != 0:
        raise RuntimeError('mkdir LOCAL_GIT_REPOS failed')
    list_upload_data = pre_process_upload_data()
    # print(list_upload_data)
    for upload_data in list_upload_data:
        path = get_clone_file_path(upload_data)
        if os.path.exists(path.strip()):
            continue
        order = 'git clone -b develop ' + upload_data[0] + path
        status, output = subprocess.getstatusoutput(order)
        print(output)
        if status != 0:
            raise RuntimeError('clone ' + upload_data[0] + ' fail !!!!!')


# 检查所有拉下来的项目是否都依赖的同一个配置文件
def check_pros():
    list_upload_data = pre_process_upload_data()
    for upload_data in list_upload_data:
        path = get_clone_file_path(upload_data)
        packagePath = path + '/gradle.properties'
        # print(packagePath)
        with open(packagePath.strip(), 'r') as packageGradle:
            for line in packageGradle.readlines():
                if line.startswith('PACKAGE_GRADLE_FILE') or line.startswith('#PACKAGE_GRADLE_FILE'):
                    package_cfg = line.replace('\n', '').strip()
                    package_cfg = package_cfg[package_cfg.rindex('/') + 1:]
                    if package_cfg != get_package_file_name():
                        raise RuntimeError(get_module_gradle_path(upload_data)
                                           + '-->PACKAGE_GRADLE_FILE 和 Config.PACKAGE_GRADLE_PATH配置不一致')


def main():
    clone_codes()
    check_pros()


if __name__ == "__main__":
    main()
