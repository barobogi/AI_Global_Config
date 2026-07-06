@echo off
REM start_telegram.bat -- 텔레그램 만복2 세션 시작
REM 기존 bun 프로세스 종료 후 D:\AI 기준으로 --channels 세션 단독 실행

cd /d D:\AI

echo [start_telegram] 기존 bun 프로세스 종료 중...
taskkill /F /IM bun.exe 2>nul
timeout /t 2 /nobreak > nul

echo [start_telegram] 텔레그램 세션 시작 (D:\AI CLAUDE.md 자동 로드)
claude --channels plugin:telegram@claude-plugins-official
