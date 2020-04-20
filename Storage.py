# 次文件负责管理mobile-storage下的配置文件

import os
import subprocess

from Config import get_clone_file_path, REPOS_STORAGE, PACKAGE_GRADLE_NAME


# ' ./AndroidProjects/mobile-storage'
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


def main():
    get_storage_package_gradle()


if __name__ == "__main__":
    main()
