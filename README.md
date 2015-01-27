# HATT
__author__ = 'kasi'
#coding=utf-8
#import moudles
from Core.Utils.surface_collector import SurfaceStatsCollector
from Core.Action.action import Action
from Core.Info.element import Element
from Core.Info.performance import PerformanceInfo
from Core.Action.Monkey.monkey import Monkey
import Core.Info.keycode as key
s=SurfaceStatsCollector()
a=Action()
e=Element()
p=PerformanceInfo()
m=Monkey()
"""
Performance Test
"""
#Fps Test
s.DisableWarningAboutEmptyData()
s.Start()
#steps
for x in range(3):
    a.swipeToUp()
s.Stop()
#print result
for x in s.GetResults():
    if "avg_surface_fps" in x.name:
        print x.name,x.value,x.unit

#Cpu Test
#steps
for x in range(3):
    a.swipeToUp()
    #print result
    cpunInfo=p.getCpuFromDump("com.android.launch")
    #or
    cpunInfo=p.getCpuFromTop("com.android.launch")


# Mem Test
#steps
for x in range(3):
    a.swipeToUp()
    #print result
    memInfo=p.getMemFromDump("com.android.launch")
    #or if you install procrank
    menInfo=p.getMemFromProcrank("com.android.launch")


#LaunchTime Test
#steps
for x in range(3):
    a.swipeToUp()
#print result
startInfo=p.getAppStartTotalTime("com.android.launch/.LaunchActivity")


#Flow Test
#steps
flowInfoBefore=p.getCurFlowFromProc("com.android.launch")
#do something
for x in range(3):
    a.swipeToUp()
flowInfoAfter=p.getCurFlowFromProc("com.android.launch")
#print result
flowInfo=flowInfoAfter-flowInfoBefore

#Battery Test
#steps
batteryInfoBefore=p.getBatteryLevel()
#do something
for x in range(3):
    a.swipeToUp()
batteryInfoAfter=p.getBatteryLevel()
#batteryInfo=(batteryInfoBefore-batteryInfoAfter)*batteryCount


"""
Function Test
"""
#click element
#1.get by class
elm=e.findElementByClass("TextView")
#or by id
elm=e.findElementById("dd")
#or by text
elm=e.findElementByName("tt")
#or by content-desc
elm=e.findElementByContent("tt")
#2.then do something
#click
a.touch(elm)
a.touchByElement(elm)
a.touchByRatio(0.5,0.2)
a.touch(300,400)
#long click
a.longPress(elm)
#send text
a.sendText("dd")
#send keyevent
a.sendKeyEvent(key.BACK)
#swipe
a.swipeToDown()
a.swipeToLeft()
a.swipeToRight()
a.swipeToUp()
a.swipe(elm,elm)
a.swipe(100,100,100,100)

#check currentview hava element
#by class
e.searchForByClass("TextView")
#by name
e.searchForByName("dd")
#by id
e.searchForById("dd")
#by content-desc
e.searchForByContent("dd")


"""
Monkey Test
"""
#steps
m.StartOne("com.android.browser",1000,1000,1000)
#wait for monkey stop or new script and run m.Stop()
#if you see monkey stop you can run
m.Stop()
