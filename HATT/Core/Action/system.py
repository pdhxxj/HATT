__author__ = 'kasi'
#coding=utf-8
from Core.Utils.adb_interface import AdbInterface
from Core.Info.app import AppInfo
from Core.Action.app import LocalAction

shell=AdbInterface()

appinfo=AppInfo()
l=LocalAction()
class SystemAction(object):
    def __init__(self):
        pass

    def searchFile(self,filePath,fileName):
        """
        查找文件返回布尔值
        args:
        - filePath -:地址
        - fileName -:文件名
        usage: searchFile("sdcard","log.txt")
        """
        rezult=shell.SendShellCommand("ls "+filePath+"/"+fileName)
        if "No such file or directory" in rezult:
            return False
        else:
            return True

    def delFile(self,filePath,fileName):
        """
        删除文件
        args:
        - filePath -:地址
        - fileName -:文件名
        usage: delFile("sdcard","log.txt")
        """
        shell.SendShellCommand("rm -f "+filePath+"/"+fileName)

    def defFileDic(self,filePath):
        """
        删除文件夹，包括子文件夹
        args:
        - filePath -:地址
        usage: defFileDic("sdcard")
        """
        shell.SendShellCommand("rm -Rf "+filePath)


    def killProcess(self, pid):
        """
        杀死应用进程
        args:
        - pid -: 进程pid值
        usage: killProcess(154)
        注：杀死系统应用进程需要root权限
        """
        if shell.SendShellCommand("kill " + str(pid)).split(": ")[-1] == "":
            return "kill success"
        else:
            return shell.SendShellCommand("kill " + str(pid)).split(": ")[-1]


    def resetCurrentApp(self):
        """
        重置当前应用
        usage: resetCurrentApp()
        """
        packageName = appinfo.getCurrentPackageName()
        component = appinfo.getFocusedPackageAndActivity()
        l.clearAppData(packageName)
        l.startActivity(component)

    def startWebpage(self, url):
        """
        使用系统默认浏览器打开一个网页
        usage: startWebpage("http://www.baidu.com")
        """
        shell.SendShellCommand("am start -procmem android.intent.action.VIEW -d " + url)

    def callPhone(self, number):
        """
        启动拨号器拨打电话
        usage: callPhone(10086)
        """
        shell.SendShellCommand("am start -procmem android.intent.action.CALL -d tel:" + str(number))

    def resetSystem(self):
        """
        重置系统
        usage: resetSystem()
        """
        shell.SendShellCommand("am broadcast -procmem android.intent.action.MASTER_CLEAR")

    def reboot(self):
        """
        重启设备
        usage: reboot()
        """
        shell.SendCommand("reboot")

    def fastboot(self):
        """
        进入fastboot模式
        usage: fastboot()
        """
        shell.SendCommand("reboot bootloader")

    def isRoot(self):
        result=shell.SendShellCommand("remount")
        if "Permission denied" in result:
            return False
        else:
            return True