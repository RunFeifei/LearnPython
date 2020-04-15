import subprocess


# 凡是package.gradle文件中以-SNAPSHOT为结尾的包都是待发布的包
# snack   : 'com.keruyun.osmobile:snack:2.9.2-SNAPSHOT',
# 以快餐为例 2.9.2-SNAPSHOT是扫描到的版本号,需要cd到snack目录下,修改gradle文件中的版本号为2.9.2,然后执行打包脚本,然后commit&push
# 然后修改storage下的package.gradle目录,把snack:2.9.2-SNAPSHOT修改为snack:2.9.2


def main():
    # print(os.popen('git status').read())
    # print(os.system('git status'))
    status, output = subprocess.getstatusoutput('git status')
    print(status)
    print(output)


if __name__ == "__main__":
    main()
