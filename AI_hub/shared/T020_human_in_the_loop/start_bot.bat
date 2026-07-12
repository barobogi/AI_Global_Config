@echo off
chcp 65001 >nul
cd /d %~dp0

for /f "tokens=2 delims== " %%i in ('findstr "APPROVAL_BOT_TOKEN" D:\Dev\n8n_start.bat') do set APPROVAL_BOT_TOKEN=%%i

if "%APPROVAL_BOT_TOKEN%"=="" (
    echo [ERROR] APPROVAL_BOT_TOKEN을 D:\Dev\n8n_start.bat에서 찾을 수 없습니다.
    pause
    exit /b 1
)

set PATH=D:\Dev\nodejs;%PATH%
python n8n_telegram_bot.py
