@echo off
chcp 65001 >nul 2>&1
set PATH=C:\Users\82102\.bun\bin;%PATH%
cd /d D:\AI

:loop
echo [%date% %time%] Telegram session start >> D:\AI\telegram_session.log 2>&1
"C:\Users\82102\.vscode\extensions\anthropic.claude-code-2.1.195-win32-x64\resources\native-binary\claude.exe" --channels "plugin:telegram@claude-plugins-official"
echo [%date% %time%] Telegram session ended (code: %ERRORLEVEL%). Restarting in 30s >> D:\AI\telegram_session.log 2>&1
ping -n 31 127.0.0.1 >nul 2>&1
goto loop
