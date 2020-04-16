from pip._vendor.msgpack.fallback import xrange


# 返回list字典
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

    for snap in listDependsSnap:
        for x, y in snap.items():
            print(x, y)

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
    getListSnapshotDepends('/Users/fei/Codes/PYTHON/Package/package.gradle')


if __name__ == "__main__":
    main()
