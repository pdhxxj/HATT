__author__ = 'kasi'
#coding=utf-8
from Core.Utils.adb_interface import AdbInterface
from Core.Info.system import SystemInfo
import Core.Info.keycode as key
shell=AdbInterface()
s=SystemInfo()
class Action(object):

    def __init__(self):
        self.display = s.getScreenResolution()
        self.width = self.display[0]
        self.high = self.display[1]

    def sendKeyEvent(self, keycode):
        """
        发送一个按键事件
        args:
        - keycode -:
        http://developer.android.com/reference/android/view/KeyEvent.html
        usage: sendKeyEvent(keycode.HOME)
        """
        shell.SendShellCommand("input keyevent " + str(keycode))

    def longPressKey(self, keycode):
        """
        发送一个按键长按事件，Android 4.4以上
        usage: longPressKey(keycode.HOME)
        """
        shell.SendShellCommand("input keyevent --longpress " + str(keycode))

    def touch(self, e=None, x=None, y=None):
        """
        触摸事件
        usage: touch(e), touch(x=0.5,y=0.5)
        """
        if(e != None):
            x = e[0]
            y = e[1]
        if(0< x < 1):
            x = x * self.width
        if(0<y<1):
            y = y * self.high

        shell.SendShellCommand("input tap " + str(x) + " " + str(y))

    def touchByElement(self, element):
        """
        点击元素
        usage: touchByElement(Element().findElementByName(u"计算器"))
        """
        shell.SendShellCommand("input tap " + str(element[0]) + " " + str(element[1]))

    def touchByRatio(self, ratioWidth, ratioHigh):
        """
        通过比例发送触摸事件
        args:
        - ratioWidth -:width占比, 0<ratioWidth<1
        - ratioHigh -: high占比, 0<ratioHigh<1
        usage: touchByRatio(0.5, 0.5) 点击屏幕中心位置
        """
        shell.SendShellCommand("input tap "+ str(ratioWidth * self.width) + " " + str(ratioHigh * self.high))


    def swipeByCoord(self, start_x, start_y, end_x, end_y, duration = " "):
        """
        滑动事件，Android 4.4以上可选duration(ms)
        usage: swipe(800, 500, 200, 500)
        """
        shell.SendShellCommand("input swipe " + str(start_x) + " " + str(start_y) + \
              " " + str(end_x) + " " + str(end_y) + " " + str(duration))

    def swipe(self, e1=None, e2=None, start_x=None, start_y=None, end_x=None, end_y=None, duration=" "):
        """
        滑动事件，Android 4.4以上可选duration(ms)
        usage: swipe(e1, e2)
               swipe(e1, end_x=200, end_y=500)
               swipe(start_x=0.5, start_y=0.5, e2)
        """
        if(e1 != None):
            start_x = e1[0]
            start_y = e1[1]
        if(e2 != None):
            end_x = e2[0]
            end_y = e2[1]
        if(0< start_x < 1):
            start_x = start_x * self.width
        if(0<start_y<1):
            start_y = start_y * self.high
        if(0<end_x<1):
            end_x = end_x * self.width
        if(0<end_y<1):
            end_y = end_y * self.high

        shell.SendShellCommand("input swipe " + str(start_x) + " " + str(start_y) + \
              " " + str(end_x) + " " + str(end_y) + " " + str(duration))

    def swipeByRatio(self, start_ratioWidth, start_ratioHigh, end_ratioWidth, end_ratioHigh, duration = " "):
        """
        通过比例发送滑动事件，Android 4.4以上可选duration(ms)
        usage: swipeByRatio(0.9, 0.5, 0.1, 0.5) 左滑
        """
        shell.SendShellCommand("input swipe " + str(start_ratioWidth * self.width) + " " + str(start_ratioHigh * self.high) + \
              " " + str(end_ratioWidth * self.width) + " " + str(end_ratioHigh * self.high) + " " +\
             str(duration))

    def swipeToLeft(self):
        """
        左滑屏幕
        usage: swipeToLeft()
        """
        self.swipeByRatio(0.8, 0.5, 0.2, 0.5)

    def swipeToRight(self):
        """
        右滑屏幕
         usage: swipeToRight()
        """
        self.swipeByRatio(0.2, 0.5, 0.8, 0.5)

    def swipeToUp(self):
        """
        上滑屏幕
         usage: swipeToUp()
        """
        self.swipeByRatio(0.5, 0.8, 0.5, 0.2)

    def swipeToDown(self):
        """
        下滑屏幕
         usage: swipeToDown()
        """
        self.swipeByRatio(0.5, 0.2, 0.5, 0.8)

    def longPress(self, e=None, x=None, y=None):
        """
        长按屏幕的某个坐标位置, Android 4.4
        usage: longPress(e)
               longPress(x=0.5, y=0.5)
        """
        self.swipe(e1=e, e2=e, start_x=x, start_y=y, end_x=x, end_y=y, duration=2000)

    def longPressElement(self, e):
        """
       长按元素, Android 4.4
        usage: longPressElement(e)
        """
        shell.SendShellCommand("input swipe " + str(e[0]) + " " + str(e[1]) + " "  + str(e[0]) + " " + str(e[1]) + str(2000))

    def longPressByRatio(self, ratioWidth, ratioHigh):
        """
        通过比例长按屏幕某个位置, Android.4.4
        usage: longPressByRatio(0.5, 0.5) 长按屏幕中心位置
        """
        self.swipeByRatio(ratioWidth, ratioHigh, ratioWidth, ratioHigh, duration=2000)

    def sendText(self, string):
        """
        发送一段文本，只能包含英文字符和空格，多个空格视为一个空格
        usage: sendText("i am unique")
        """
        text = str(string).split(" ")
        out = []
        for i in text:
            if i != "":
                out.append(i)
        length = len(out)
        for i in xrange(length):
            shell.SendShellCommand("input text " + out[i])
            if i != length - 1:
                self.sendKeyEvent(key.SPACE)