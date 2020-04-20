# 次文件负责管理mobile-storage下的配置文件

import os
import subprocess

# return ' ./AndroidProjects/mobile-storage/package_gradle/osmobile/package_2.8.13'
from Config import get_clone_file_path, REPOS_STORAGE, PACKAGE_GRADLE_NAME

# 最新的待发布的package.gradle文件路径
PACKAGE_GRADLE_PATH = ''


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
    key = key[key.index('.')+1:]




def main():
    modify_pkg_and_push('osm_depends.snack')


if __name__ == "__main__":
    main()
