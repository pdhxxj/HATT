@echo off

for /f "tokens=2" %%i in ('adb shell ps ^|findstr "monkey"') do adb shell kill %%i
