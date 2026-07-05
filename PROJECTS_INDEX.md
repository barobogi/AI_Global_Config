# D:\AI 프로젝트 인덱스

**최종 업데이트**: 2026-07-05  
> 폴더 이동 없이 성격별 분류만 문서화. 실제 경로는 그대로.

---

## 🔴 시스템/인프라 (절대 건드리지 않음)

| 폴더/파일 | 역할 |
|-----------|------|
| `Global_Define/` | master_watch.py, email_notify.py 등 전역 유틸리티 |
| `AI_hub/` | 만복↔코니 상태 동기화 허브 (heartbeat, messages, tasks) |
| `.cowork-projects-registry.json` | master_watch 프로젝트 등록부 |
| `.cowork-global.json` | 전역 공통 설정 |
| `CLAUDE.md` | Claude Code 전역 지시사항 |
| `NEXT_PROJECTS.md` | 다음 작업 우선순위 |
| `PROJECTS_INDEX.md` | 이 파일 |
| `REF_DEBUG/` | 전역 디버깅 로그 |

---

## 🟢 활성 프로젝트

| 폴더 | 설명 | 상태 |
|------|------|------|
| `11_특허아이디어/` | 특허 아이디어 관리 (1~15번) | 진행 중 |
| `Diary_for_Barobogi/` | AI Study / Logs 블로그 | 진행 중 |
| `Improve_stock/` | 종가베팅+VCP 주식 분석 (KIS API 연동 대기) | 진행 중 |
| `260625_1_n8n_finance/` | n8n 금융 자동화 파이프라인 | 진행 중 (DB 재구성 필요) |
| `TEMP_MANBOK/` | 코니 싱크 임시 파일 저장소 | 운영 중 |

---

## 🟡 휴면 프로젝트 (당분간 재작업 계획 없음)

| 폴더 | 설명 | 마지막 수정 |
|------|------|------------|
| `260620_3_Multimedia_summary/` | 유튜브/영상 요약 자동화 | 2026-06-22 |
| `260622_1_Remote_claude/` | 모바일 만복이 앱 (Flutter) | 2026-06-26 |
| `260624_superpowers/` | Superpowers 커스텀 스킬 시스템 | 2026-06-24 |
| `260619_1_claude_usage/` | Claude 사용량 추적 | 2026-06-21 |
| `260623_1_study_all/` | Study Dashboard (Diary_for_Barobogi 통합 대기) | 2026-07-04 |

---

## 🔵 레거시/아카이브 대기

| 폴더 | 설명 | 비고 |
|------|------|------|
| `260620_2_Daily_for_barobogi/` | Diary_for_Barobogi 프로토타입 (6/20) | registry 비활성화됨 |
| `260620_1_cowork_cli_automation/` | Global_Define으로 승격 완료된 껍데기 | C단계 아카이브 예정 |
| `DEV_ITEM/` | 구버전 특허 docx + global-review 스킬 기록 | 특허 docx만 이관 예정 |
| `_DEPRECATED_260619_2_Daily_for_stock/` | 260619_2_Daily_for_stock_TEMP와 완전 중복 | 삭제 예정 (오늘) |

---

## ⚫ 외부/참고 레포 (내 프로젝트 아님)

| 폴더 | 설명 | 비고 |
|------|------|------|
| `claude-trading-skills/` | tradermonty 클론 (729파일) | registry 비활성화됨 |
| `cline/` | cline 실험 모음 | 참고용 |

---

## 🟤 개인 원본 파일 (코드/자동화 대상 아님)

| 폴더 | 설명 |
|------|------|
| `GD/` | 카카오톡 원본 |
| `MYBOX/` | 카카오톡 텍스트 |
| `Obsidian/` | 개인 노트 vault |

---

## 📄 루트 스크립트/설정 파일

| 파일 | 역할 |
|------|------|
| `start_telegram.bat` | 텔레그램 --channels 세션 실행 |
| `make_patent_docx.py` | 특허 문서 생성 스크립트 |
| `start_remote_control.ps1` | Remote Control 수동 시작 |
| `task_masterwatch.xml` | 작업 스케줄러 등록 XML |
| `데스크탑_최적화_Guide.md` | 개발환경 설정 가이드 |
| `n8n_data ` (공백 오타) | n8n 데이터 폴더 — T016 완료 후 이름 수정 예정 |
