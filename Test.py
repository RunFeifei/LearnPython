class NoChildSnapError(Exception):
    pass


# module_gradle_path=./AndroidProjects/Snack/snack/build.gradle
# return ./AndroidProjects/Snack/gradle.properties
def to_project_gradle_properties_path(module_gradle_path):
    module_gradle_path = module_gradle_path.replace('/build.gradle', '')
    module_gradle_path = module_gradle_path[:module_gradle_path.rindex('/') + 1]
    return module_gradle_path + 'gradle.properties'


def main():
    # try:
    #     raise NoChildSnapError('1232323232323' + '# 该节点已经没有儿子Snap节点')
    # except NoChildSnapError as e:
    #     print(e.args[0][:e.args[0].index('#')])
    print(to_project_gradle_properties_path('./AndroidProjects/Snack/snack/build.gradle'))


if __name__ == "__main__":
    main()
