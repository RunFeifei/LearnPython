from Test import getListSnapshotDepends


# 凡是package.gradle文件中以-SNAPSHOT为结尾的包都是待发布的包
# snack   : 'com.keruyun.osmobile:snack:2.9.2-SNAPSHOT',
# 以快餐为例 2.9.2-SNAPSHOT

def main():
    listDependsSnap = getListSnapshotDepends('/Users/fei/Codes/PYTHON/Package/package.gradle')
    for snap in listDependsSnap:
        for x, y in snap.items():
            print(x, y)


if __name__ == "__main__":
    main()
