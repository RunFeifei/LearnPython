class NoChildSnapError(Exception):
    pass


# module_gradle_path=./AndroidProjects/Snack/snack/build.gradle
# return ./AndroidProjects/Snack/gradle.properties
def to_project_gradle_properties_path(module_gradle_path):
    module_gradle_path = module_gradle_path.replace('/build.gradle', '')
    module_gradle_path = module_gradle_path[:module_gradle_path.rindex('/') + 1]
    return module_gradle_path + 'gradle.properties'


# module_gradle_path=./AndroidProjects/Snack/snack/build.gradle
# return snack
def to_module_name(module_gradle_path):
    module_gradle_path = module_gradle_path.replace('/build.gradle', '')
    module_gradle_path = module_gradle_path[module_gradle_path.rindex('/') + 1:]
    return module_gradle_path


def main():
    print(to_module_name('./AndroidProjects/Snack/snack/build.gradle'))


if __name__ == "__main__":
    main()
