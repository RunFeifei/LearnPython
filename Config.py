# 单条数据的格式为
# '在package.grale中定义的key':['clone地址','项目中对应module的路径名']


REPOS_STORAGE = ['http://gitlab.shishike.com/OSMobile/mobile-storage.git', 'mobile-storage']

REPOS_DICT = {
    'osm_depends.snack': ['http://gitlab.shishike.com/c_iphone/Snack.git', 'Snack'],
    'component_depends.paycenter': ['http://gitlab.shishike.com/c_iphone/PayCenter.git', 'paycenter'],
    'component_depends.paycenter_board': ['http://gitlab.shishike.com/c_iphone/PayCenter.git', 'paycenterboard'],
}

# 此目录下会进行格式化操作 不要作为其他用途
LOCAL_GIT_REPOS = ' ./AndroidProjects/'

# 最新的待发布的package.gradle文件名
PACKAGE_GRADLE_NAME = 'package_2.8.13'

# upload_data=['http://gitlab.shishike.com/c_iphone/Snack.git', 'snack']
# if LOCAL_GIT_REPOS = ' ./AndroidProjects/'
# return ./AndroidProjects/Snack
def get_clone_file_path(upload_data):
    clone = upload_data[0]
    path = clone[clone.rindex('/') + 1:].replace('.git', '')
    return LOCAL_GIT_REPOS + path


# upload_data=['http://gitlab.shishike.com/c_iphone/Snack.git', 'Snack']
# if LOCAL_GIT_REPOS = ' ./AndroidProjects/'
# return ./AndroidProjects/Snack/snack/build.gradle
def get_module_gradle_path(upload_data):
    path = get_clone_file_path(upload_data)
    path = path + '/' + upload_data[1] + '/build.gradle'
    return path


# module_gradle_path=./AndroidProjects/Snack/snack/build.gradle
# return ./AndroidProjects/Snack/gradle.properties
def to_project_gradle_properties_path(module_gradle_path):
    module_gradle_path = module_gradle_path.replace('/build.gradle', '')
    module_gradle_path = module_gradle_path[:module_gradle_path.rindex('/') + 1]
    return module_gradle_path + 'gradle.properties'


def get_package_file_name():
    return PACKAGE_GRADLE_PATH[PACKAGE_GRADLE_PATH.rindex('/'):]
