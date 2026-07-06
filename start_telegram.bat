@echo off
if "%1"=="standalone" goto run
start cmd /k "%~f0" standalone
exit
:run
taskkill /F /IM bun.exe 2>nul
timeout /t 2 /nobreak > nul
cd /d D:\AI
"C:\Users\82102\.vscode\extensions\anthropic.claude-code-2.1.195-win32-x64\resources\native-binary\claude.exe" --channels plugin:telegram@claude-plugins-official
