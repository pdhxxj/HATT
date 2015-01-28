__author__ = 'kasi'
#coding=utf-8
import re
import os
import platform
system = platform.system()


if system is "Windows":
    acomond=os.path.join(os.path.abspath(".."),"Core","Lib","aapt.exe")
else:
    acomond=os.path.join(os.path.abspath(".."),"Core","Lib","aapt")

#aapt 命令
def aapt(args):
    return os.popen(acomond+" "+str(args))

class AAPT(object):

    def __init__(self):
        self.pattern = re.compile(r"\d+")

    def __getRes(self,path):
        return aapt("d badging "+path).read().split()

    def getApkPname(self,path):
        """
        获取apk包名
        args:
        - path -: apk文件地址
        usage: getApkPname("e:\\tt\\procmem.apk")
        """
        count=0
        print self.__getRes(path)
        for pname in self.__getRes(path):
            count+=1
            if "package:" in pname:
                return self.__getRes(path)[count].split("=")[1].strip('\'')

    def getApkVersionCode(self,path):
        """
        获取apk内部版本号
        args:
        - path -: apk文件地址
        usage: getApkVersionCode("e:\\tt\\procmem.apk")
        """
        for code in self.__getRes(path):
            if "versionCode=" in code:
                return code.split("=")[1].strip('\'')

    def getApkVersionName(self,path):
        """
        获取apk版本号
        args:
        - path -: apk文件地址
        usage: getApkVersionName("e:\\tt\\procmem.apk")
        """
        for name in self.__getRes(path):
            if "versionName=" in name:
                return name.split("=")[1].strip('\'')


    def getSuportMinSdkVersion(self,path):
        """
        获取apk支持的最小SDK版本号
        args:
        - path -: apk文件地址
        usage: getSuportMinSdkVersion("e:\\tt\\procmem.apk")
        """
        for minversion in self.__getRes(path):
            if "sdkVersion:" in minversion:
                return minversion.split(":")[1].strip('\'')


    def getSuportMaxSdkVersion(self,path):
        """
        获取apk支持的最大SDK版本号
        args:
        - path -: apk文件地址
        usage: getSuportMaxSdkVersion("e:\\tt\\procmem.apk")
        """
        for maxversion in self.__getRes(path):
            if "targetSdkVersion:" in maxversion:
                return maxversion.split(":")[1].strip('\'')


    def getLaunchActivity(self,path):
        """
        获取apk启动activity
        args:
        - path -: apk文件地址
        usage: getLaunchActivity("e:\\tt\\procmem.apk")
        """
        count=0
        print self.__getRes(path)
        for activity in self.__getRes(path):
            count+=1
            if "launchable-activity:" in activity:
                return self.__getRes(path)[count].split("=")[1].strip('\'')

    def supportAnyDensity(self,path):
        """
        判断应用是否支持适配
        args:
        - path -: apk文件地址
        usage: supportAnyDensity("e:\\tt\\procmem.apk")
        """
        count=0
        print self.__getRes(path)
        for sad in self.__getRes(path):
            count+=1
            if "supports-any-density:" in sad:
                if self.__getRes(path)[count].strip('\'')=='true':
                    return True
                else:
                    return False

    def getIconAdress(self,path):
        """
        获取apk图标地址
        args:
        - path -: apk文件地址
        usage: getIconAdress("e:\\tt\\procmem.apk")
        """
        for icon in self.__getRes(path):
            if "icon=:" in icon:
                return icon.split("=")[1].strip('\'')

    def getApkPermisson(self,path):
        """
        获取apk权限清单
        args:
        - path -: apk文件地址
        usage: getApkPermisson("e:\\tt\\procmem.apk")
        """
        permisson=[]
        for pm in self.__getRes(path):
            if "uses-permission:" in pm:
                permisson.append(pm.split(":")[1].strip('\''))
        return permisson


    def getApkPermissonNo(self,path):
        """
        获取apk权限条数
        args:
        - path -: apk文件地址
        usage: getApkPermissonNo("e:\\tt\\procmem.apk")
        """
        return len(self.getApkPermisson(path))