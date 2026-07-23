@echo off
echo [1] kill start >> D:\AI\_debug_telegram.log
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'claude.exe' -and $_.CommandLine -like '*channels*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }" >> D:\AI\_debug_telegram.log 2>&1
echo [2] taskkill >> D:\AI\_debug_telegram.log
taskkill /F /IM bun.exe >> D:\AI\_debug_telegram.log 2>&1
echo [3] timeout done >> D:\AI\_debug_telegram.log
timeout /t 2 /nobreak > nul
cd /d D:\AI
echo [4] cd done, finding ext dir >> D:\AI\_debug_telegram.log
FOR /D %%G IN ("C:\Users\82102\.vscode\extensions\anthropic.claude-code-*-win32-x64") DO SET EXT_DIR=%%G
echo [5] EXT_DIR=%EXT_DIR% >> D:\AI\_debug_telegram.log
echo [6] about to launch claude.exe >> D:\AI\_debug_telegram.log
echo done >> D:\AI\_debug_telegram.log
