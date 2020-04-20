# 次文件负责管理mobile-storage下的配置文件

import os
import subprocess

# return ' ./AndroidProjects/mobile-storage/package_gradle/osmobile/package_2.8.13'
from Config import get_clone_file_path, REPOS_STORAGE, PACKAGE_GRADLE_NAME

# 最新的待发布的package.gradle文件路径
# /Users/fei/Codes/PYTHON/Package/AndroidProjects/mobile-storage/package_gradle/osmobile/package_2.8.14.gradle
PACKAGE_GRADLE_PATH = './package.gradle'


# return
# /Users/fei/Codes/PYTHON/Package/AndroidProjects/mobile-storage/package_gradle/osmobile/package_2.8.14.gradle
def get_latest_package_gradle_file():
    global PACKAGE_GRADLE_PATH
    if PACKAGE_GRADLE_PATH == '':
        PACKAGE_GRADLE_PATH = get_storage_package_gradle()
    return PACKAGE_GRADLE_PATH


# 获取最新的待发布的package.gradle文件路径
def get_storage_package_gradle():
    path = get_clone_file_path(REPOS_STORAGE)
    if os.path.exists(path.strip()):
        status, output = subprocess.getstatusoutput('cd' + path + ' & git pull')
        print('git pull mobile-storage--> ' + output)
        if status != 0:
            raise RuntimeError('git pull mobile-storage failed')
        return path + '/package_gradle/osmobile/' + PACKAGE_GRADLE_NAME

    order = 'git clone -b master ' + REPOS_STORAGE[0] + path
    status, output = subprocess.getstatusoutput(order)
    print(output)
    if status != 0:
        raise RuntimeError('clone ' + REPOS_STORAGE[0] + ' fail !!!!!')
    return path + '/package_gradle/osmobile/' + PACKAGE_GRADLE_NAME


# key=osm_depends.snack
def modify_pkg_and_push(key):
    key = key[key.index('.') + 1:]
    with open(PACKAGE_GRADLE_PATH, 'r') as packageGradle:
        packageGradleStr = packageGradle.readlines()

    status = 0
    for i in range(0, len(packageGradleStr)):
        line = packageGradleStr[i].strip()
        if line.startswith(key):
            status = -1
            packageGradleStr[i] = packageGradleStr[i].replace('-SNAPSHOT', '')
            with open(PACKAGE_GRADLE_PATH, 'w') as packageGradle:
                packageGradle.writelines(packageGradleStr)
                packageGradle.close()
                # status=-1 表示key匹配成功并且文件修改成功
                status = -2

    if status == 0:
        raise RuntimeError(key + ' 没有匹配成功')
    if status == -1:
        raise RuntimeError(PACKAGE_GRADLE_PATH + ' 文件写入失败')

    # status, output = subprocess.getstatusoutput(')
    # if status != 0:
    #     raise RuntimeError('mkdir LOCAL_GIT_REPOS failed')


def main():
    path = get_clone_file_path(REPOS_STORAGE)
    path = ' ./'
    key = 'test'
    commit = '\"OS_自动打包 更新{}\"'.format(key)
    key = 'cd{} && git pull && git add -A && git commit -a -m {} && git push origin'.format(path, commit)
    status, output = subprocess.getstatusoutput(key)
    if status != 0:
        raise RuntimeError('mkdir LOCAL_GIT_REPOS failed')
    print(output)


if __name__ == "__main__":
    main()
