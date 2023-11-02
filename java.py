import shutil
import winreg
import os
import subprocess

# 定义用于获取注册表值的函数
def getzcb(HKEY, path, z=''):
    try:
        with winreg.OpenKey(HKEY, path) as key:
            try:
                return True, winreg.QueryValueEx(key, z)
            except FileNotFoundError:
                return True, ''
    except FileNotFoundError:
        print(f"注册表项不存在")
        return False, ''
    except PermissionError:
        print("没有足够的权限访问注册表")
        return False, ''

# 定义用于设置注册表值的函数
def setzcb(HKEY, path, j='', z='',l=winreg.REG_SZ):
    try:
        with winreg.CreateKey(HKEY, path) as key:
            try:
                winreg.SetValueEx(key, j, 0, l, z)
                print("值已写入注册表")
            except FileNotFoundError:
                return True, ''
    except FileNotFoundError:
        print(f"注册表项不存在")
        return False, ''
    except PermissionError:
        print("没有足够的权限访问注册表")
        return False, ''

# 定义要操作的注册表键和路径
HKEY = winreg.HKEY_LOCAL_MACHINE
path = r'SOFTWARE\Classes\jarfile'
# 获取计算机上的所有JDK目录
jdk=input('全部jdk目录：')
ml = [f1 for f1 in os.listdir(jdk) if (os.path.isdir(f'{jdk}\\{f1}') and f1.startswith('jdk-'))]
# 遍历每个JDK目录并执行以下操作
for f1 in ml:
    if not os.path.isfile(f'{jdk}\\{f1}\\bin\\java.exe'):
        print('无java.exe文件')
        exit
    # 获取JDK版本号
    bb1 = subprocess.getoutput(f'{jdk}\\{f1}\\bin\\java.exe -version').split('\n')[0][:-1].split('"')[1]
    bb=bb1.split('.')
    if bb[0] == '1':
        bb = bb[1]
    else:
        bb = bb[0]
    # 复制java.exe文件到j{版本号}.exe
    shutil.copyfile(f'{jdk}\\{f1}\\bin\\java.exe',f'{jdk}\\{f1}\\bin\\j{bb}.exe')
    # 操作注册表来关联.jar文件的打开方式
    if getzcb(winreg.HKEY_LOCAL_MACHINE, rf'SOFTWARE\Classes\jarfile{bb}')[0]:
        getzcb(HKEY, rf'SOFTWARE\Classes\jarfile{bb}')
        setzcb(HKEY, rf'SOFTWARE\Classes\jarfile{bb}', j='', z=f'可执行 Jar-{bb} 文件')
        getzcb(HKEY, rf'SOFTWARE\Classes\jarfile{bb}\shell\open\command')
        setzcb(HKEY, rf'SOFTWARE\Classes\jarfile{bb}\shell\open\command', j='', z=rf'{jdk}\{f1}\bin\j{bb}.exe -jar "%1" %*')
    else:
        setzcb(HKEY, rf'SOFTWARE\Classes\jarfile{bb}', j='', z=f'可执行 Jar-{bb} 文件')
        setzcb(HKEY, rf'SOFTWARE\Classes\jarfile{bb}\shell\open\command', j='', z=rf'{jdk}\{f1}\bin\j{bb}.exe -jar "%1" %*')
    # 设置其他相关注册表项
    setzcb(winreg.HKEY_USERS, rf'S-1-5-21-1738001706-3578771923-927531698-1001\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.jar\OpenWithProgids', j=f'jarfile{bb}', z=b'',l=winreg.REG_BINARY)
    setzcb(winreg.HKEY_USERS, rf'S-1-5-21-1738001706-3578771923-927531698-1001\SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache', j=f'{jdk}\\{f1}\\bin\\j{bb}.exe.FriendlyAppName', z=f'java-{bb1}',l=winreg.REG_SZ)
input('完成，回车结束')