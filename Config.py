# 单条数据的格式为
# '在package.grale中定义的key':['clone地址','项目中对应module的路径名']
REPOS_DICT = {
    'osm_depends.snack': ['http://gitlab.shishike.com/c_iphone/Snack.git', 'Snack'],
    'component_depends.paycenter': ['http://gitlab.shishike.com/c_iphone/PayCenter.git', 'paycenter'],
    'component_depends.paycenter_board': ['http://gitlab.shishike.com/c_iphone/PayCenter.git', 'paycenterboard'],
}


# upload_data=['http://gitlab.shishike.com/c_iphone/Snack.git', 'Snack']
# return Snack
def get_clone_file_path(upload_data):
    clone = upload_data[0]
    path = clone[clone.rindex('/') + 1:].replace('.git', '')
    return path


# upload_data=['http://gitlab.shishike.com/c_iphone/Snack.git', 'Snack']
# return Snack/Snack
def get_module_file_path(upload_data):
    path = get_clone_file_path(upload_data)
    path = path + '/' + upload_data[1]
    return path

# def is_gradle_contains_snap