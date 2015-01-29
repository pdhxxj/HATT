__author__ = 'kasi'
#coding=utf-8
import os
import re
from Core.Utils.adb_interface import AdbInterface
from Core.Action.app import LocalAction
shell=AdbInterface()
l=LocalAction()
busyboxPath=os.path.join(os.path.abspath(".."),"Core","Lib","busybox")
class Crash(object):
    def __init__(self):
        self.pattern = re.compile(r"\d+")
        self.__install()

    def __install(self):
        l.pullFile(busyboxPath,"/system/bin/")
        shell.SendShellCommand("chmod 755 /system/bin/busybox")

    def __getData(self,key):
        return shell.SendShellCommand("ls /data/system/dropbox ^|grep "+key)

    def __getdata(self,key):
         return self.pattern.findall(
             shell.SendShellCommand("ls /data/system/dropbox ^|grep "+key+" ^|busybox wc -l"))[0]

    def Check(self):
        crash=self.__getData("crash")
        anr=self.__getData("anr")
        tomstone=self.__getData("tomstone")
        apanic=self.__getData("apanic")
        if crash=="" and anr=="" and tomstone=="" and apanic=="":
            return True
        else:
            return False

    def getCrashNo(self):
        return self.__getdata("crash")

    def getAnrNo(self):
        return self.__getdata("anr")

    def getTomstoneNo(self):
        return self.__getdata("tomstone")

    def getApanicNo(self):
        return self.__getdata("apanic")