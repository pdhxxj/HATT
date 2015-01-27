__author__ = 'kasi'
#coding=utf-8
import re
import platform

from Core.Utils.Cmd.adb_interface import AdbInterface
from system import SystemInfo

shell=AdbInterface()

system = platform.system()
s=SystemInfo()
class AppInfo(object):
    """
    获取部分app信息
    """
    def __init__(self):
        self.pattern = re.compile(r"\d+")

    def getUid(self,packagename):
        """
        获取UID
         args:
        - packagename -: 包名
         usage: getUid("com.android.test")
        """
        return self.pattern.findall(shell.SendShellCommand("dumpsys package "+packagename+" ^|grep userId"))[0]

    def getPid(self, packageName):
        """
        获取进程pid
        args:
        - packageName -: 应用包名
        usage: getPid("com.android.settings")
        """
        if system is "Windows":
            string = shell.SendShellCommand("ps | findstr " + packageName + "$")

        string = shell.SendShellCommand("ps | grep -w " + packageName)

        if string == '':
            return "the process doesn't exist."

        pattern = re.compile(r"\d+")
        result = string.split(" ")
        result.remove(result[0])

        return  pattern.findall(" ".join(result))[0]

    def getFocusedPackageAndActivity(self):
        """
        获取当前应用界面的包名和Activity，返回的字符串格式为：packageName/activityName
        usage: getFocusedPackageAndActivity()
        """
        pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
        out = shell.SendShellCommand("dumpsys window w | findstr \/ | findstr name=")
        return pattern.findall(out)[0]

    def getCurrentPackageName(self):
        """
        获取当前运行的应用的包名
        usage: getCurrentPackageName()
        """
        return self.getFocusedPackageAndActivity().split("/")[0]

    def getCurrentActivity(self):
        """
        获取当前运行应用的activity
        usage: getCurrentActivity()
        """
        return self.getFocusedPackageAndActivity().split("/")[-1]

    def isInstall(self, packageName):
        """
        判断应用是否安装，已安装返回True，否则返回False
        usage: isInstall("com.example.apidemo")
        """
        if s.getMatchingAppList(packageName):
            return True
        else:
            return False


