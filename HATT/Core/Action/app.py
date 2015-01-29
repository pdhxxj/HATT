__author__ = 'kasi'
#coding=utf-8
from Core.Utils.adb_interface import AdbInterface
shell=AdbInterface()


class LocalAction(object):
    def __init__(self):
        pass

    def pullFile(self,spathfile,dpath):
        """
        pull文件
        args:
        - spathfile -: 源地址文件
        - dpath -: 目标地址
        usage: pullFile("/sdcard/1.txt","e:\\")
        """
        shell.SendCommand("pull "+spathfile+" "+dpath)

    def pushFile(self,dpathfile,spath):
        """
        push文件
        args:
         - spath -: 源地址
        - dpathfile -: 目标地址文件
        usage: pushFile("e:\\1.txt","/sdcard/")
        """
        shell.SendCommand("push "+dpathfile+" "+spath)


    def installApp(self, appFile):
        """
        安装app，app名字不能含中文字符
        args:
        - appFile -: app路径
        usage: install("d:\\apps\\Weico.apk")
        """
        shell.SendCommand("install " + appFile)

    def removeApp(self, packageName):
        """
        卸载应用
        args:
        - packageName -:应用包名，非apk名
        usage: removeApp("com.example.apidemo")
        """
        shell.SendCommand("uninstall " + packageName)

    def clearAppData(self, packageName):
        """
        清除应用用户数据
        usage: clearAppData("com.android.contacts")
        """
        if "Success" in shell.SendShellCommand("pm clear " + packageName).splitlines():
            return "clear user data success "
        else:
            return "make sure package exist"

    def quitApp(self, packageName):
        """
        退出app，类似于kill掉进程
        usage: quitApp("com.android.settings")
        """
        shell.SendShellCommand("am force-stop " + packageName)

    def startActivity(self, component):
        """
        启动一个Activity
        usage: startActivity(component = "com.android.settinrs/.Settings")
        """
        shell.SendShellCommand("am start -n " + component)