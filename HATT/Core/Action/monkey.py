__author__ = 'kasi'
#coding=utf-8
import os
import time
import tempfile

from Core.Utils.adb_interface import AdbInterface
from Core.Action.system import SystemAction
from Core.Action.log import Log
from Core.Action.app import LocalAction

shell=AdbInterface()
s=SystemAction()
l=Log()
la=LocalAction()
killMonkeyPath=os.path.join(os.path.abspath(".."),"Core","Lib","cmd","km.bat")
killLogcatPath=os.path.join(os.path.abspath(".."),"Core","Lib","cmd","kl.bat")
class Monkey(object):

    def __init__(self):
        self.tempFile = tempfile.gettempdir()
        #self.__before()
       # self.__launchLog()


    def __before(self):
        #clear caches
        shell.SendShellCommand("echo 3>/proc/sys/vm/drop_caches")
        #clear logcat
        l.clearLog()
        #clear logs
        shell.SendShellCommand("rm -r /data/system/dropbox/*.*")
        shell.SendShellCommand("rm -r /data/anr/*.*")
        shell.SendShellCommand("rm -r /data/dontpanic/*.*")
        shell.SendShellCommand("rm -r /data/tombstone/*.*")

    def __launchLog(self):
        shell.SendCommand("logcat -v threadtime -b main -f /sdcard/main.log")
        time.sleep(0.3)
        shell.SendCommand("logcat -v threadtime -b system -f /sdcard/system.log")
        time.sleep(0.3)
        shell.SendCommand("logcat -v threadtime -b radio -f /sdcard/radio.log")
        time.sleep(0.3)
        shell.SendCommand("logcat -v threadtime -b events -f /sdcard/events.log")

    def StartOne(self,packagename,seed,throttletime,count,logversion="-v -v -v",runflag="--hprof",custompercent=""):
        shell.SendShellCommand("monkey -p "+packagename
                        +" -s "+str(seed)
                        +" --throttle "+str(throttletime)
                        +" "+logversion+" "+runflag+" "+custompercent+" "+str(count)+" >"+self.tempFile+"\Monkey.log")


    def StartMul(self,packages,seed,throttletime,count,logversion="-v -v -v",runflag="--hprof",custompercent=""):
        shell.SendShellCommand("monkey "+packages
                        +" -s "+seed
                        +" --throttle "+throttletime
                        +" "+logversion+" "+runflag+" "+custompercent+" "+str(count)+" >"+self.tempFile+"\Monkey.log")

    def Stop(self):
        #kill monkey and logcat
        os.popen(killMonkeyPath)
        os.popen(killLogcatPath)
        #pull log
        la.pullFile("/data/system/dropbox",self.tempFile)
        la.pullFile("/data/anr/",self.tempFile)
        la.pullFile("/data/dontpanic",self.tempFile)
        la.pullFile("/data/tombstone",self.tempFile)
        la.pullFile("/sdcard/main.log",self.tempFile)
        la.pullFile("/sdcard/system.log",self.tempFile)
        la.pullFile("/sdcard/events.log",self.tempFile)
        la.pullFile("/sdcard/radio.log",self.tempFile)
        #dumplog
        shell.SendShellCommand("dmsg >"+self.tempFile+"\dmsg.txt")
        shell.SendShellCommand("dumpsys >"+self.tempFile+"\dumpsys.txt")
        shell.SendShellCommand("dumpstate >"+self.tempFile+"\dumpstate.txt")
