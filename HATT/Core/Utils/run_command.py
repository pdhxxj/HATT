__author__ = 'kasi'
#coding=utf-8
import time
import subprocess
import threading

import Core.Utils.error as error
import Core.Utils.logger as logger


_abort_on_error=False



def SetAbortOnError(abort=True):
  """Sets behavior of RunCommand to throw AbortError if command process returns
  procmem negative error code"""
  global _abort_on_error
  _abort_on_error = abort

def RunCommand(cmd, timeout_time=None, retry_count=3, return_output=True,
               stdin_input=None):
  """
    运行命令行
     args:
    - cmd -: 命令字符串
    - timeout_time -: 延迟
    - retry_count -: 重试次数
    - return_output -: 输出
    - stdin_input -: 输入
     usage: RunCommand("adb devices")
  """
  result = None
  while True:
    try:
      result = RunOnce(cmd, timeout_time=timeout_time,
                       return_output=return_output, stdin_input=stdin_input)
    except error.WaitForResponseTimedOutError:
      if retry_count == 0:
        raise
      retry_count -= 1
      logger.Log("No response for %s, retrying" % cmd)
    else:
      # Success
      return result

def RunOnce(cmd, timeout_time=None, return_output=True, stdin_input=None):
  start_time = time.time()

  so = []
  pid = []
  global _abort_on_error, error_occurred
  error_occurred = False

  def Run():
    global error_occurred
    if return_output:
      output_dest = subprocess.PIPE
    else:
      # None means direct to stdout
      output_dest = None
    if stdin_input:
      stdin_dest = subprocess.PIPE
    else:
      stdin_dest = None
    pipe = subprocess.Popen(
        cmd,
        #executable='/bin/bash',
        stdin=stdin_dest,
        stdout=output_dest,
        stderr=subprocess.STDOUT,
        shell=True)
    pid.append(pipe.pid)
    try:
      output = pipe.communicate(input=stdin_input)[0]
      if output is not None and len(output) > 0:
        so.append(output)
    except OSError, e:
      logger.SilentLog("failed to retrieve stdout from: %s" % cmd)
      logger.Log(e)
      so.append("ERROR")
      error_occurred = True
    if pipe.returncode:
      logger.SilentLog("Error: %s returned %d error code" %(cmd,
          pipe.returncode))
      error_occurred = True

  t = threading.Thread(target=Run)
  t.start()
  """
  break_loop = False
  while not break_loop:
    #print t.isAlive()
    if not t.isAlive():
      break_loop = True

    # Check the timeout
    #print timeout_time
    if (not break_loop and timeout_time is not None
        and time.time() > start_time + timeout_time):
      try:
         #os.kill(pid[0], signal.SIGKILL)
        os.kill(pid[0], signal.SIGTERM)
      except OSError:
        # process already dead. No action required.
        pass

      logger.SilentLog("about to raise procmem timeout for: %s" % cmd)

      raise error.WaitForResponseTimedOutError
    if not break_loop:
      time.sleep(1)
  """
  t.join()
  output = "".join(so)
  if _abort_on_error and error_occurred:
    raise error.AbortError(msg=output)

  return "".join(so)

