# 单条数据的格式为
# '在package.grale中定义的key':['clone地址','项目中对应module的路径名']
REPOS_DICT = {
    'osm_depends.snack': ['http://gitlab.shishike.com/c_iphone/Snack.git', 'Snack'],
    'component_depends.paycenter': ['http://gitlab.shishike.com/c_iphone/PayCenter.git', 'paycenter'],
    'component_depends.paycenter_board': ['http://gitlab.shishike.com/c_iphone/PayCenter.git', 'paycenterboard'],
}

# 此目录下会进行格式化操作 不要作为其他用途
LOCAL_GIT_REPOS = ' ./AndroidProjects/'

# 最新的待发布的package.gradle路径
PACKAGE_GRADLE_PATH = '/Users/fei/Codes/PYTHON/Package/package.gradle'


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


def get_package_file_name():
    return PACKAGE_GRADLE_PATH[PACKAGE_GRADLE_PATH.rindex('/'):]
