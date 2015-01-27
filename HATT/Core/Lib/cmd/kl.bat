@echo off

for /f "tokens=2" %%i in ('adb shell ps ^|findstr "logcat"') do adb shell kill %%i
