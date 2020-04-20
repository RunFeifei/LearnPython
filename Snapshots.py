from pip._vendor.msgpack.fallback import xrange

from Storage import PACKAGE_GRADLE_PATH


def get_snaps_key(packagePath):
    keys = []
    for snap in getListSnapshotDepends(packagePath):
        for x, y in snap.items():
            keys.append(x)
    return keys


# packagePath package.gradle文件磁盘地址
# return 返回package.gradle文件中所有的snapshot依赖
# [{'component_depends.paycenter': 'com.keruyun.mobile:paycenter:2.8.218-SNAPSHOT'}, {'component_depends.paycenter_board': 'com.keruyun.mobile:paycenter-board:2.8.218-SNAPSHOT'}, {'osm_depends.snack': 'com.keruyun.osmobile:snack:2.8.14-SNAPSHOT'}]
def getListSnapshotDepends(packagePath):
    with open(packagePath, 'r') as packageGradle:
        packageGradleStr = packageGradle.read()
    # print(packageGradleStr)
    leftMarkIndex = [i for i in xrange(len(packageGradleStr)) if packageGradleStr.startswith('[', i)]
    # print(leftMarkIndex)
    rightMarkIndex = [i for i in xrange(len(packageGradleStr)) if packageGradleStr.startswith(']', i)]
    # print(rightMarkIndex)

    if len(leftMarkIndex) != len(rightMarkIndex):
        raise RuntimeError('len(leftMarkIndex)!=len(rightMarkIndex)')
    listTypes = getDependType(packagePath)
    # print('type len-->' + str(len(listTypes)))

    preDepends1 = []
    for i in range(0, len(leftMarkIndex)):
        temp = packageGradleStr[leftMarkIndex[i] + 1:rightMarkIndex[i]]
        temp = temp.strip().replace(',', '')
        preDepends1.append(temp.splitlines())
    # print('type len-->' + str(len(preDepends1)))

    listDependsMaps = []
    for i in range(0, len(preDepends1)):
        for depend in preDepends1[i]:
            # 这里防止有空行 防止有maven地址
            if len(depend) > 0 and (not depend.startswith('//')) and ('http' not in depend):
                temp = depend.replace(' ', '').replace('\'', '')
                temp = listTypes[i] + '.' + temp
                listDependsMaps.append(temp)

    listDepends = []
    for depend in listDependsMaps:
        # 这里去掉注释行
        # print(depend)
        if not depend.startswith('//'):
            key = depend[0:depend.index(':')]
            value = depend[depend.index(':') + 1:]
            # 这里防止末尾有注释
            if '//' in value:
                value = value[0:value.index('//')]
            listDepends.append({key: value})

    listDependsSnap = []
    for depend in listDepends:
        # print(depend)
        for x, y in depend.items():
            if y.endswith("-SNAPSHOT"):
                listDependsSnap.append({x: y})

    return listDependsSnap


def getDependType(packagePath):
    with open(packagePath, 'r') as packageGradle:
        packageGradleStr = packageGradle.read()
    leftBraceIndex = [i for i in xrange(len(packageGradleStr)) if packageGradleStr.startswith('{', i)]
    leftMarkIndex = [i for i in xrange(len(packageGradleStr)) if packageGradleStr.startswith('[', i)]
    rightMarkIndex = [i for i in xrange(len(packageGradleStr)) if packageGradleStr.startswith(']', i)]
    listTypes = []
    for i in range(0, len(leftMarkIndex)):
        if i == 0:
            listTypes.append(
                packageGradleStr[leftBraceIndex[1] + 1:leftMarkIndex[0] - 1]
                    .replace(' ', '')
                    .replace('=', '')
                    .replace('\n', ''))
        else:
            listTypes.append(
                packageGradleStr[rightMarkIndex[i - 1] + 1: leftMarkIndex[i] - 1]
                    .replace(' ', '')
                    .replace('=', '')
                    .replace('\n', ''))

    return listTypes


def main():
    for snap in getListSnapshotDepends(PACKAGE_GRADLE_PATH):
        for x, y in snap.items():
            print(x, y)


if __name__ == "__main__":
    main()
