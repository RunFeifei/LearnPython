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

    listDependsMaps = []
    for i in range(0, len(leftMarkIndex)):
        preDepends = packageGradleStr[leftMarkIndex[i] + 1:rightMarkIndex[i]]
        preDepends = preDepends.strip().replace(',', '')
        # print("**************************************************")
        preDepends = preDepends.splitlines()
        # print(preDepends)
        for depend in preDepends:
            if len(depend) > 0:
                listDependsMaps.append(depend.strip().replace(' ', '').replace('\'', ''))

    listDepends = []
    for depend in listDependsMaps:
        if not depend.startswith('//'):
            key = depend[0:depend.index(':')]
            value = depend[depend.index(':') + 1:]
            if '//' in value:
                value = value[0:value.index('//')]
            listDepends.append({key: value})

    listDependsSnap = []
    for depend in listDepends:
        for x, y in depend.items():
            if y.endswith("-SNAPSHOT"):
                listDependsSnap.append({x: y})

    # for snap in listDependsSnap:
    #     for x, y in snap.items():
    #         print(x, y)

    return listDependsSnap


def main():
    getListSnapshotDepends('/Users/fei/Codes/PYTHON/Package/package.gradle')


if __name__ == "__main__":
    main()
