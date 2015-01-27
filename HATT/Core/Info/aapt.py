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
        return aapt("d badging "+path).read().split(":")

    def getApkPname(self,path):
        """
        获取apk包名
        args:
        - path -: apk文件地址
        usage: getApkPname("e:\\tt\\procmem.apk")
        """
        l=[]
        l=self.__getRes(path)[1].split("\r\n")
        return l[0].split("=")[1].split(" ")[0]

    def getApkVersionCode(self,path):
        """
        获取apk内部版本号
        args:
        - path -: apk文件地址
        usage: getApkVersionCode("e:\\tt\\procmem.apk")
        """
        l=[]
        l=self.__getRes(path)[1].split("\r\n")
        return  self.pattern.findall(str(l))[0]

    def getApkVersionName(self,path):
        """
        获取apk版本号
        args:
        - path -: apk文件地址
        usage: getApkVersionName("e:\\tt\\procmem.apk")
        """
        l=[]
        ll=[]
        s=""
        l=self.__getRes(path)[1].split("\r\n")
        ll=self.pattern.findall(str(l))
        del ll[0]
        count=0
        for x in ll:
            count+=1
            if count==len(ll):
                s=s+x
                break
            s+=x+"."
        return s

    def getSuportMinSdkVersion(self,path):
        """
        获取apk支持的最小SDK版本号
        args:
        - path -: apk文件地址
        usage: getSuportMinSdkVersion("e:\\tt\\procmem.apk")
        """
        l=[]
        l=self.__getRes(path)[2].split("\r\n")
        return  self.pattern.findall(str(l))[0]

    def getSuportMaxSdkVersion(self,path):
        """
        获取apk支持的最大SDK版本号
        args:
        - path -: apk文件地址
        usage: getSuportMaxSdkVersion("e:\\tt\\procmem.apk")
        """
        l=[]
        l=self.__getRes(path)[3].split("\r\n")
        return  self.pattern.findall(str(l))[0]

    def getLaunchActivity(self,path):
        """
        获取apk启动activity
        args:
        - path -: apk文件地址
        usage: getLaunchActivity("e:\\tt\\procmem.apk")
        """
        l=[]
        l=self.__getRes(path)
        count=0
        for x in l:
            count=count+1
            if "launchable-activity" in x:
                break
        return l[count].split(" ")[1].split("=")[1]

    def getApkPermisson(self,path):
        """
        获取apk权限清单
        args:
        - path -: apk文件地址
        usage: getApkPermisson("e:\\tt\\procmem.apk")
        """
        l=[]
        l=self.__getRes(path)
        tmp=[]
        s=[]
        for x in l:
            if "uses-permission" in x:
                tmp.append(x)
        del tmp[0]
        del tmp[len(tmp)-1]
        for y in tmp:
            s.append(str(y).split("\n")[0].replace("'",""))
        return s

    def getApkPermissonNo(self,path):
        """
        获取apk权限条数
        args:
        - path -: apk文件地址
        usage: getApkPermissonNo("e:\\tt\\procmem.apk")
        """
        return len(self.getApkPermisson(path))