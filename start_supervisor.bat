@echo off
chcp 65001 >nul
echo [%date% %time%] Supervisor 시작 >> D:\AI\Global_Define\supervisor.log
C:\hb\python.exe D:\AI\Global_Define\supervisor.py
