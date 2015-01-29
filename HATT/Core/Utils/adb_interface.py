__author__ = 'kasi'
#coding=utf-8
import run_command
import Core.Utils.logger as logger

class AdbInterface:
    _target_arg = ""

    def SendCommand(self,command_string, timeout_time=1, retry_count=3):
        """
        发送adb命令行
         args:
        - command_string -: 命令字符串
        - timeout_time -: 延迟
        - retry_count -: 重试次数
         usage: SendCommand("devices")
        """
        adb_cmd = "adb %s %s" % (self._target_arg, command_string)
        logger.SilentLog("about to run %s" % adb_cmd)
        return run_command.RunCommand(adb_cmd, timeout_time=timeout_time, retry_count=retry_count)

    def SendShellCommand(self, cmd, timeout_time=1, retry_count=3):
        """
        发送adb shell命令行
         args:
        - cmd -: 命令字符串
        - timeout_time -: 延迟
        - retry_count -: 重试次数
         usage: SendShellCommand("dumpsys")
        """
        return self.SendCommand("shell %s" % cmd, timeout_time=timeout_time,retry_count=retry_count)


