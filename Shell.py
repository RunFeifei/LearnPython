# getstatusoutput 同步执行
import logging
import os
import subprocess

from Config import REPOS_DICT
from Snapshots import getListSnapshotDepends

# 凡是package.gradle文件中以-SNAPSHOT为结尾的包都是待发布的包
# snack   : 'com.keruyun.osmobile:snack:2.9.2-SNAPSHOT',
# 以快餐为例 2.9.2-SNAPSHOT是扫描到的版本号,需要cd到snack目录下,修改gradle文件中的版本号为2.9.2,然后执行打包脚本,然后commit&push
# 然后修改storage下的package.gradle目录,把snack:2.9.2-SNAPSHOT修改为snack:2.9.2

# list字典
snap_shots = getListSnapshotDepends('/Users/fei/Codes/PYTHON/Package/package.gradle')


def main():
    print(pre_process_upload_data())
    status, output = subprocess.getstatusoutput('git status')
    print(status)
    print(output)


def pre_process_upload_data():
    list_upload_data = []
    for snap in snap_shots:
        for x, y in snap.items():
            try:
                repo = REPOS_DICT[x]
            except KeyError:
                logging.error('    没有在Config.py中找到配置信息-->' + x)
                pass
            else:
                list_upload_data.append(repo)
    return list_upload_data


def cloneCodes():
    if os.path.exists('./AndroidProjects'):
        status, output = subprocess.getstatusoutput('rm -rf ./AndroidProjects')
        if status != 0:
            raise RuntimeError('rm -rf ./AndroidProjects failed')

    status, output = subprocess.getstatusoutput('mkdir AndroidProjects')
    if status != 0:
        raise RuntimeError('mkdir AndroidProjects failed')
    status, output = subprocess.getstatusoutput('cd ./AndroidProjects')
    if status != 0:
        raise RuntimeError('cd ./AndroidProjects failed')
    list_upload_data = pre_process_upload_data()
    print(list_upload_data)
    for upload_data in list_upload_data:
        path = get_clone_file_path(upload_data)
        if os.path.exists('./AndroidProjects/' + path):
            continue
        order = 'git clone -b develop ' + upload_data[0] + ' ./AndroidProjects/' + path
        status, output = subprocess.getstatusoutput(order)
        print(output)
        if status != 0:
            raise RuntimeError('clone ' + upload_data[0] + ' fail !!!!!')


def get_clone_file_path(upload_data):
    clone = upload_data[0]
    path = clone[clone.rindex('/') + 1:].replace('.git', '')
    return path


if __name__ == "__main__":
    cloneCodes()
