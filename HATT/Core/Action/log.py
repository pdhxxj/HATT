__author__ = 'kasi'
#coding=utf-8
import tempfile

from Core.Utils.adb_interface import AdbInterface
from Core.Action.app import LocalAction


adb=AdbInterface()
l=LocalAction()
class Log(object):
    """
    打印日志
    """
    def __init__(self):
        self.tempFile = tempfile.gettempdir()

    def __getLog(self,vtype,btype,count):
         adb.SendCommand("logcat -v "+vtype+" -b "+btype+" -t "+str(count)+" -f /sdcard/"+btype+".log")



    def clearLog(self):
        """
        清除logcat日志
        usage: clearLog()
        """
        adb.SendCommand("logcat -c")

    def getMainLog(self,count=2000):
        """
        打印logcat主日志
         args:
        - count -: 条数
        usage: getMainLog() or getMainLog(2000)
        """
        self.__getLog("threadtime","main",count)

    def getSystemLog(self,count=2000):
        """
        打印logcat系统日志
         args:
        - count -: 条数
        usage: getSystemLog(2000) or getSystemLog()
        """
        self.__getLog("threadtime","system",count)

    def getRadioLog(self,count=2000):
        """
        打印logcat音频日志
         args:
        - count -: 条数
        usage: getRadioLog(2000) or getRadioLog()
        """
        self.__getLog("threadtime","radio",count)

    def getEventsLog(self,count=2000):
        """
        打印logcat事件日志
         args:
        - count -: 条数
        usage: getEventsLog(2000) or getEventsLog()
        """
        self.__getLog("threadtime","event",count)

