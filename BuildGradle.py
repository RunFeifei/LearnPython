from Shell import *
from Snapshots import get_snaps_key


# 遍历多叉树
# https://www.jianshu.com/p/dee8284b2dc4

class BaseSnapError(Exception):
    pass


root_snap_shots = get_snaps_key(PACKAGE_GRADLE_PATH)


# 获取所有module的build.gradle文件的目录
def get_list_module_build_gradle_files():
    list_module_build_gradle_files = []
    list_upload_data = pre_process_upload_data()
    for upload_data in list_upload_data:
        buildPath = get_module_gradle_path(upload_data)
        # print(buildPath)
        if not os.path.exists(buildPath.strip()):
            raise RuntimeError(buildPath + ' 不存在')
        list_module_build_gradle_files.append(buildPath.strip())
    return list_module_build_gradle_files


# 通过递归进行遍历多叉树 拿到最底层snap开始上传
def recursion(module_gradle_path):
    if module_gradle_path is None:
        child = get_list_module_build_gradle_files()
    else:
        try:
            child = get_child_snap(module_gradle_path)
        except BaseSnapError:
            # 去执行上传
            # 上传完成后怎么去父亲节点上传呢
            pass
    for module_gradle_path in child:
        recursion(module_gradle_path)


# 遍历某一个module下面的的build.gradle找出该module所依赖的更底层snapshot依赖
# 返回底层snapshot依赖路径
def get_child_snap(module_gradle_path):
    snap_shots = []
    with open(module_gradle_path.strip(), 'r') as gradle:
        for line in gradle.readlines():
            if line.startswith('//'):
                continue
            for snap in root_snap_shots:
                if snap in line:
                    snap_shots.append(get_module_gradle_path(REPOS_DICT[snap]))
    if snap_shots:
        return snap_shots
    else:
        raise BaseSnapError('got base snap already')


def main():
    recursion(None)


if __name__ == "__main__":
    main()
