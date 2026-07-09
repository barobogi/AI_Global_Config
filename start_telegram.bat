@echo off
if "%1"=="standalone" goto run
start cmd /k "%~f0" standalone
exit
:run
taskkill /F /IM bun.exe 2>nul
timeout /t 2 /nobreak > nul
cd /d D:\AI
FOR /D %%G IN ("C:\Users\82102\.vscode\extensions\anthropic.claude-code-*-win32-x64") DO SET EXT_DIR=%%G
"%EXT_DIR%\resources\native-binary\claude.exe" --channels plugin:telegram@claude-plugins-official
