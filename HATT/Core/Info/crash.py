__author__ = 'kasi'
#coding=utf-8
from Core.Utils.Cmd.adb_interface import AdbInterface
shell=AdbInterface()

class Crash(object):
    def __init__(self):
        pass

    def __getData(self,key):
        return shell.SendShellCommand("ls /data/system/dropbox ^|grep "+key).read()

    def __getdata(self,key):
         return shell.SendShellCommand("ls /data/system/dropbox ^|grep "+key+" |wc -l").read()

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