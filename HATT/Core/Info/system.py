__author__ = 'kasi'
#coding=utf-8
import re

from Core.Utils.Cmd.adb_interface import AdbInterface

shell=AdbInterface()


class SystemInfo(object):
    def __init__(self):
        pass

    def getDeviceState(self):
        """
        获取设备状态： offline | bootloader | device
         usage: getDeviceState()
        """
        return shell.SendCommand("get-state").split("\n")[0]

    def getDeviceID(self):
        """
        获取设备id号，return serialNo
         usage: getDeviceID()
        """
        return shell.SendCommand("get-serialno").split("\n")[0]

    def getDeviceIDlist(self):
        """
        获取设备id号，return list(serialNo)
         usage: getDeviceIDlist()
        """
        l=[]
        tmp=[]
        l=shell.SendCommand("devices").split("\r\n")
        del l[0]
        for x in l:
            if x!="":
                tmp.append(x.split("\t")[0])
        return tmp

    def getAppList(self):
        """
        获取设备中安装的应用包名列表
         usage: getAppList()
        """
        app=[]
        for packages in shell.SendShellCommand("pm list packages").split():
            app.append(packages.split(":")[1])

        return app


    def getSystemAppList(self):
        """
        获取设备中安装的系统应用包名列表
         usage: getSystemAppList()
        """
        sysApp = []
        for packages in shell.SendShellCommand("pm list packages -s").split():
            sysApp.append(packages.split(":")[1])

        return sysApp

    def getThirdAppList(self):
        """
        获取设备中安装的第三方应用包名列表
         usage: getThirdAppList()
        """
        thirdApp = []
        for packages in shell.SendShellCommand("pm list packages -3").split():
            thirdApp.append(packages.split(":")[1])

        return thirdApp

    def getMatchingAppList(self, keyword):
        """
        模糊查询与keyword匹配的应用包名列表
         args:
        - keyword -: 关键字
        usage: getMatchingAppList("qq")
        """
        matApp = []
        for packages in shell.SendShellCommand("pm list packages " + keyword).split():
            matApp.append(packages.split(":")[1])
        return matApp

    def getAppAddressFromPname(self,packagename):
        """
        根据包名查询应用地址
        args:
        - packagename -: 包名
        usage: getAppAddressFromPname("com.android.test")
        """
        address=shell.SendShellCommand("pm list packages -f ^|grep "+packagename)
        return  address.split(":")[1].split("=")[0]

    def getAppAddressFromKeyList(self,key):
        """
        根据关键字查找应用地址
        args:
        - key -: 关键字
        usage: getAppAddressFromKeyList("android")
        """
        l=[]
        tmp=[]
        l=shell.SendShellCommand("pm list packages -f ^|grep "+key).split("\n")
        for x in l:
            if x!="":
                tmp.append(x.split(":")[1].split("=")[0])
        return tmp

    def getAppAddressList(self):
        """
        获取安装应用地址
        usage: getAppAddressList()
        """
        l=[]
        tmp=[]
        l=shell.SendShellCommand("pm list packages -f").split("\n")
        for x in l:
            if x!="":
                tmp.append(x.split(":")[1].split("=")[0])
        return tmp

    def getAppNo(self):
        """
        获取应用数量
        usage: getAppNo()
        """
        return len(self.getAppList())

    def getSysAppNo(self):
        """
        获取系统应用数量
        usage: getSysAppNo()
        """
        return len(self.getSystemAppList())

    def getThirdAppNo(self):
        """
        获取第三方应用数量
        usage: getThirdAppNo()
        """
        return len(self.getThirdAppList())

    def getSdkVersion(self):
        """
        得到sdk版本号
        usage: getSdkVersion()
        """
        return shell.SendShellCommand("getprop ro.build.version.sdk").split("\r\n")[0]

    def getCurHandle(self):
        """
        得到当前的handle
        usage: getCurHandle()
        """
        l=[]
        fname=[]
        l=shell.SendShellCommand("dumpsys SurfaceFlinger").split("\r\n")
        n=0
        z=0
        for x in l:
            n=n+1
            if "----------+-" in x:
                fname=l[n-2].split("|")
                break
        for y in fname:
            z=z+1
            if "handle" in y:
                handle=[]
                handle=l[n].split("|")
                return handle[z-1]

    def getScreenResolution(self):
        """
        获取设备屏幕分辨率，return (width, high)
        usage: getScreenResolution()
        """
        pattern = re.compile(r"\d+")
        out = shell.SendShellCommand("dumpsys display | findstr PhysicalDisplayInfo")
        display = pattern.findall(out)

        return (int(display[0]), int(display[1]))


