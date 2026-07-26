@echo off
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'claude.exe' -and $_.CommandLine -like '*channels*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
taskkill /F /IM bun.exe >nul 2>&1
ping -n 3 127.0.0.1 > nul
cd /d D:\AI
FOR /D %%G IN ("C:\Users\82102\.vscode\extensions\anthropic.claude-code-*-win32-x64") DO SET EXT_DIR=%%G

for /f "delims=" %%T in (D:\AI\.secrets\telegram_oauth_token.txt) do set CLAUDE_CODE_OAUTH_TOKEN=%%T

echo [%TIME%] 텔레그램 플러그인 시작 (OAuth 토큰 인증)...
"%EXT_DIR%\resources\native-binary\claude.exe" --channels plugin:telegram@claude-plugins-official
echo [%TIME%] 플러그인 종료됨.
