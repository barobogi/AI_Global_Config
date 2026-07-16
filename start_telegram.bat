@echo off
if "%1"=="standalone" goto run
start cmd /k "%~f0" standalone
exit
:run
taskkill /F /IM bun.exe 2>nul
timeout /t 2 /nobreak > nul
cd /d D:\AI
FOR /D %%G IN ("C:\Users\82102\.vscode\extensions\anthropic.claude-code-*-win32-x64") DO SET EXT_DIR=%%G

echo [%TIME%] 텔레그램 플러그인 시작...
"%EXT_DIR%\resources\native-binary\claude.exe" --channels plugin:telegram@claude-plugins-official
echo [%TIME%] 플러그인 종료됨.
