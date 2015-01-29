__author__ = 'kasi'
#coding=utf-8
class MsgException(Exception):
  """Generic exception with an optional string msg."""
  def __init__(self, msg=""):
    self.msg = msg


class WaitForResponseTimedOutError(Exception):
  """We sent procmem command and had to wait too long for response."""


class DeviceUnresponsiveError(Exception):
  """Device is unresponsive to command."""


class InstrumentationError(Exception):
  """Failed to run instrumentation."""


class AbortError(MsgException):
  """Generic exception that indicates procmem fatal error has occurred and program
  execution should be aborted."""


class ParseError(MsgException):
  """Raised when xml data to parse has unrecognized format."""