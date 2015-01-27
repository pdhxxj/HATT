__author__ = 'kasi'
#coding=utf-8
import re
import os

from Core.Utils.Cmd.adb_interface import AdbInterface
from Core.Action.Log.log import Log
from Core.Action.System.system import SystemAction
from Core.Action.App.app import LocalAction
from app import AppInfo

shell=AdbInterface()
a=AppInfo()
l=Log()
la=LocalAction()
s=SystemAction()
prank=os.path.join(os.path.abspath(".."),"Core","Lib","procrank")
libso=os.path.join(os.path.abspath(".."),"Core","Lib","libpagemap")
pmem=os.path.join(os.path.abspath(".."),"Core","Lib","procmem")
class PerformanceInfo(object):
    """
    获取部分app性能信息
    """
    def __init__(self):
        self.pattern = re.compile(r"\d+")
        self.__install()


    def __install(self):
        if s.isRoot():
            la.pushFile(prank,"/system/xbin/")
            la.pushFile(pmem,"/system/xbin/")
            la.pushFile(libso,"/system/lib/")
            shell.SendShellCommand("chmod 755 /system/xbin/procrank")
            shell.SendShellCommand("chmod 755 /system/xbin/procmem")
            shell.SendShellCommand("chmod 755 /system/lib/libpagemap")
        else:
            pass

    def getAppStartTotalTime(self, component):
     """
     获取启动应用所花时间
      args:
        - component -: 组件
     usage: getAppStartTotalTime("com.android.settings/.Settings")
     """
     time = shell.SendShellCommand("am start -W " + component + " ^| grep TotalTime") \
        .split(": ")[-1]
     return int(time)

    """
    def getAppStartTime(self,component):
        #l.clearLog()
        #time.sleep(5)
        shell.SendShellCommand("am start -n "+component)
        time.sleep(2)
        tempFile = tempfile.gettempdir()
        shell.SendCommand("adb logcat -s ActivityManager ^|grep Displayed >"+tempFile+"\main.log")
        time.sleep(2)
        f=file(tempFile+"\main.log",'r')
        rezult=f.read().split("\r\n")
        print rezult
        f.close()
        rezults=[]
        for x in rezult:
            if x!="":
                rezults.append(self.pattern.findall(x)[1])
        return rezults
    """



    def getMemFromDump(self,packagename):
        """
        获取应用的内存值-PSS
         args:
        - packagename -: 包名
        usage: getMemFromDump("com.android.settings")
        """
        s=shell.SendShellCommand("dumpsys meminfo "+packagename)
        if "No process found for" in s:
            return "error"
        else:
            l=s.split("\n")
            for x in l:
                if "TOTAL" in x:
                    return self.pattern.findall(x)[0]

    def getMemFromProcrank(self,packagename):
        """
        获取应用的内存值-PSS
         args:
        - packagename -: 包名
        usage: getMemFromProcrank("com.android.settings")
        """
        if s.searchFile("/system/xbin","procrank"):
            l=shell.SendShellCommand("procrank ^|grep "+packagename).split("\n")
            count=0
            for x in l:
                if x!="":
                    count=count+int(self.pattern.findall(x)[3])
            return count
        else:
            return None

    def getCpuFromDump(self,packagename):
        """
        获取应用的cpu值
         args:
        - packagename -: 包名
        usage: getCpuFromDump("com.android.settings")
        """
        l= shell.SendShellCommand("dumpsys cpuinfo ^|grep "+packagename).split(" ")
        while l[0]=="":
            l.remove("")
        return l

    def getCpuFromTop(self,packagename):
        l=shell.SendShellCommand("top -n 1 ^|grep "+packagename).split("\n")
        count=0
        for x in l:
            if x!="":
                count=count+int(self.pattern.findall(x)[2])
        return str(count)+"%"


    def getCurFlowFromProc(self,packagename):
        """
        获取应用的当前流量(只统计tcp)
         args:
        - packagename -: 包名
        usage: getFlowFromProc("com.android.settings")
        """
        uid=a.getUid(packagename)
        tcp_rcv=int(shell.SendShellCommand("cat /proc/uid_stat/"+uid+"/tcp_rcv"))
        tcp_snd=int(shell.SendShellCommand("cat /proc/uid_stat/"+uid+"/tcp_snd"))
        return tcp_rcv+tcp_snd


    def getBatteryLevel(self):
        """
        获取电池电量
        usage: getBatteryLevel()
        """
        level = shell.SendShellCommand("dumpsys battery | findstr level").split(": ")[-1]

        return int(level)

    def getBatteryStatus(self):
        """
        获取电池充电状态
        BATTERY_STATUS_UNKNOWN：未知状态
        BATTERY_STATUS_CHARGING: 充电状态
        BATTERY_STATUS_DISCHARGING: 放电状态
        BATTERY_STATUS_NOT_CHARGING：未充电
        BATTERY_STATUS_FULL: 充电已满
        usage: getBatteryStatus()
        """
        statusDict = {1 : "BATTERY_STATUS_UNKNOWN",
                      2 : "BATTERY_STATUS_CHARGING",
                      3 : "BATTERY_STATUS_DISCHARGING",
                      4 : "BATTERY_STATUS_NOT_CHARGING",
                      5 : "BATTERY_STATUS_FULL"}
        status = shell.SendShellCommand("dumpsys battery | findstr status").split(": ")[-1]

        return statusDict[int(status)]

    def getBatteryTemp(self):
        """
        获取电池温度
        usage: getBatteryTemp()
        """
        temp = shell.SendShellCommand("dumpsys battery | findstr temperature").split(": ")[-1]

        return int(temp) / 10.0