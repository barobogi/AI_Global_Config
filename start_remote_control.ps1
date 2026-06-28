# 만복이 Remote Control 시작
# 모바일 Claude 앱에서 만복이 세션에 접속 가능!

$claude = "C:\Users\82102\.vscode\extensions\anthropic.claude-code-2.1.185-win32-x64\resources\native-binary\claude.exe"

Write-Host "🚀 만복이 Remote Control 시작 중..." -ForegroundColor Cyan
Write-Host "📱 모바일 Claude 앱 → 우측 상단 메뉴 → Remote Sessions 에서 접속하세요" -ForegroundColor Yellow
Write-Host ""

Set-Location "D:\AI"
& $claude remote-control --name "만복이_데스크탑"
