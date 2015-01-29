__author__ = 'kasi'
#coding=utf-8
import re
import platform

from Core.Utils.adb_interface import AdbInterface
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
            string = shell.SendShellCommand("ps ^| grep " + packageName + "$")
        else:
            string = shell.SendShellCommand("ps ^| grep -w " + packageName)

        if string == '':
            return "the process doesn't exist."

        result = string.split(" ")
        result.remove(result[0])

        return  self.pattern.findall(" ".join(result))[0]

    def getFocusedPackageAndActivity(self):
        """
        获取当前应用界面的包名和Activity，返回的字符串格式为：packageName/activityName
        usage: getFocusedPackageAndActivity()
        """
        pa = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
        out = shell.SendShellCommand("dumpsys window w ^| grep \/ ^| grep name=")
        return pa.findall(out)[0]

    def getCurrentPackageName(self):
        """
        获取当前运行的应用的包名
        usage: getCurrentPackageName()
        """
        return self.getFocusedPackageAndActivity().split("/")[0]

    def getCurrentCompont(self):
        """
        获取当前运行应用的compont
        usage: getCurrentCompont()
        """
        rezult=shell.SendShellCommand("dumpsys activity top ^|grep ACTIVITY").split()
        if len(rezult)==4:
            return rezult[1]
        else:
            return None

    def getCurrentPid(self):
        """
        获取当前运行应用的pid
        usage: getCurrentPid()
        """
        rezult=shell.SendShellCommand("dumpsys activity top ^|grep ACTIVITY").split()
        if len(rezult)==4:
            return rezult[3].split("=")[1]
        else:
            return None

    def getCurrentHandle(self):
        """
        获取当前运行应用的handle
        usage: getCurrentHandle()
        """
        rezult=shell.SendShellCommand("dumpsys activity top ^|grep ACTIVITY").split()
        if len(rezult)==4:
            return rezult[2]
        else:
            return None

    def getcurrentActivity(self):
        """
        获取当前运行应用的activity
        usage: getCurrentActivity()
        """
        rezult=self.getCurrentCompont()
        if rezult!=None:
            return rezult.split("/")[1]
        else:
            return None

    def getcurrentPackageName(self):
        """
        获取当前运行应用的包名
        usage: getcurrentPackageName()
        """
        rezult=self.getCurrentCompont()
        if rezult!=None:
            return rezult.split("/")[0]
        else:
            return None

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


