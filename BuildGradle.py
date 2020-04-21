from Projects import *
from Snapshots import get_snaps_key

# 遍历多叉树
# https://www.jianshu.com/p/dee8284b2dc4
from Storage import PACKAGE_GRADLE_PATH


class NoChildSnapError(Exception):
    pass


root_snap_shots = get_snaps_key(PACKAGE_GRADLE_PATH)
# 上传完成的包记录
module_upload_ed = []


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
    child = []
    if module_gradle_path is None:
        child = get_list_module_build_gradle_files()
    else:
        try:
            child = get_child_snap(module_gradle_path)
        except NoChildSnapError as e:
            # 去执行上传
            # 上传完成后怎么去父亲节点上传呢
            upload_module_archive(e.args[0][:e.args[0].index('#')])
            print(e)
    for module_gradle_path in child:
        # 如果已经上传过则略过
        if module_gradle_path in module_upload_ed:
            continue
        recursion(module_gradle_path)
    # 这里是儿子节点全部遍历完成?
    upload_module_archive(module_gradle_path)


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
        raise NoChildSnapError(module_gradle_path + '# 该节点已经没有儿子Snap节点')


def upload_module_archive(module_gradle_path):
    # 先去修改gradle.properties
    modify_gradle_properties(module_gradle_path)

    module_path = module_gradle_path.replace('/build.gradle', '')
    status, output = subprocess.getstatusoutput(
        'cd ' + module_path + ' && ' + '../gradlew clean build uploadArchives')
    if status != 0:
        raise RuntimeError('upload_moddule_archive failed')
    module_upload_ed.append(module_gradle_path)


def modify_gradle_properties(module_gradle_path):
    module_name = to_module_name(module_gradle_path)
    project_gradle_properties_path = to_project_gradle_properties_path(module_gradle_path)
    project_gradle_properties_path = project_gradle_properties_path.strip()

    file_changed = False
    # 先读取
    with open(project_gradle_properties_path, 'r') as packageGradle:
        packageGradleStr = packageGradle.readlines()

    for i in range(0, len(packageGradleStr)):
        line = packageGradleStr[i].strip()
        # 把#PACKAGE_GRADLE_FILE的开关打开,以便拉取最新的配置文件
        if line.startswith('#PACKAGE_GRADLE_FILE'):
            packageGradleStr[i] = packageGradleStr[i].replace('#PACKAGE_GRADLE_FILE', 'PACKAGE_GRADLE_FILE')
            file_changed = True
        # 更改版本号码,去掉-SNAPSHOT
        if line.startswith('VERSION_NAME'):
            packageGradleStr[i] = packageGradleStr[i].replace('-SNAPSHOT', '')
            file_changed = True

    # 把文件的更改写入
    if file_changed:
        with open(project_gradle_properties_path, 'w') as packageGradle:
            packageGradle.writelines(packageGradleStr)
            packageGradle.close()

    # path = get_clone_file_path(REPOS_STORAGE)
    # commit = '\"OS_自动打包 更新{}\"'.format(key)
    # key = 'cd{} && git pull && git add -A && git commit -a -m {} && git push origin'.format(path, commit)
    # status, output = subprocess.getstatusoutput(key)
    # if status != 0:
    #     raise RuntimeError('commit&push {} failed'.format(REPOS_STORAGE[0]))
    # print(output)


def main():
    recursion(None)


if __name__ == "__main__":
    main()
