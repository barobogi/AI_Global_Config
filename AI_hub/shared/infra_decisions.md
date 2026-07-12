# 인프라 결정 고정 저장소 (compact 생존용)

> 세션 시작 시 반드시 읽을 것. /compact 후에도 이 파일은 유지됨.
> AI가 내린 환경/인프라 결정만 기록. 코드·프로젝트 내용 X.

---

## D001 — n8n 설치 위치 및 포트 (2026-07-12 확정)
- **결정**: n8n = `C:\n8n` v1.123.63 (SSD 전용)
- **이유**: D드라이브(HDD)는 IOPS 부족으로 설치 반복 실패
- **포트**: 10678 (5678은 System PID4 점유로 사용 불가)
- **데이터 경로**: `D:\Dev\n8n_data` (N8N_USER_FOLDER)
- **시작 명령**: `D:\Dev\n8n_start.bat` (안티 작성, 환경변수 포함)
- **UI**: http://localhost:10678
- **계정**: barobogi79@gmail.com
- **⚠️ D드라이브 재설치 절대 금지** — compact 후 기억 리셋되어도 이 파일 읽으면 됨

## D002 — Python 경로 (확정)
- **결정**: `C:\hb\python.exe` (심볼릭 링크 C:\hb → D:\hb)
- **pip 캐시**: D:\Dev\pip_cache

## D003 — master_watch.py 실행 (확정)
- **결정**: 부팅 시 자동 시작 / 재시작 명령:
```powershell
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like "*master_watch*"} | Stop-Process -Force
Start-Process "C:\hb\python.exe" -ArgumentList "D:\AI\Global_Define\master_watch.py" -WindowStyle Hidden
```
- **로그**: `D:\AI\Global_Define\global_watcher.log`

## D004 — Hall 삼진아웃제 유예 (2026-07-11 확정)
- **결정**: 2026-07-11 ~ 2026-08-11 만복 수정안 운영 (Hall → CLAUDE.md 예방 룰 추가)
- **전환 조건**: 개선 없으면 2026-08-11 즉시 삼진아웃제 시행

---

*이 파일은 코니 감독관 제안으로 신설 (2026-07-11). compact 생존 목적.*
