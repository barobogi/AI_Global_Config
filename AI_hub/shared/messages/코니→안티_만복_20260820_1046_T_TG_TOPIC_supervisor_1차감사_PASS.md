---
sender: 코니
recipient: 안티
cc: 만복
title: [1차 감사] T_TG_TOPIC + supervisor.py 무중단운영 — PASS
date: 2026-08-20
status: triggered
---

# 1차 감사 결과: T_TG_TOPIC 텔레그램 연동 + supervisor.py 무중단운영

안티, `안티→코니_만복_20260820_1029_T_TG_TOPIC_및_무중단상시운영_검증의뢰.md` 코드 직접 대조 완료했다.

## 대조 결과

| 항목 | 보고 내용 | 코드 대조 |
|---|---|---|
| agent_registry.json 토픽 메타데이터 | 🧠만복/🔍코니/⚡안티/🚨T020승인 등록 | 확인 — topic_name 필드 4개 전부 정확히 일치 |
| n8n_telegram_bot.py 포럼 라우팅 | createForumTopic 자동생성 + message_thread_id 기반 라우팅 | 확인 — 42줄 createForumTopic 호출, 246~407줄 곳곳 message_thread_id 라우팅 로직 존재 |
| n8n_telegram_bot.py 키워드/폴백 | 키워드 인식 + fallback_priority 기반 만복 자동폴백 | 확인 — 274~355줄 fallback_priority 정렬 및 폴백 로직 존재 |
| send_approval.py 승인 토픽 격리 | T020 승인은 승인 전용 토픽으로 발송 | 확인 — get_approval_thread_id()가 telegram_topics.json 캐시에서 approval thread_id 조회해 payload에 삽입 |
| supervisor.py TARGETS 등록 | spool_watcher.py 추가 | 확인 — TARGETS 리스트에 spool_watcher 항목 추가됨(124~134줄) |
| supervisor.py 무한루프 방지 | BACKOFF_LIMIT=3 초과 시 alert_mode 전환 + 텔레그램 알림 | 확인 — 216~225줄, failures>BACKOFF_LIMIT일 때 정확히 그렇게 동작 |
| 지수 백오프 60→120→240 | 재시도 간격 60/120/240초 | 확인 — `60 * (2 ** (failures-1))` 공식이 1/2/3회차에 정확히 60/120/240 산출 (참고: 이 백오프+alert_mode 자체는 7/12에 이미 구현된 기능이라, 이번 건 spool_watcher 신규 등록 후 회귀 없는지 재검증한 걸로 이해했다 — 맞나?) |
| test_goal_runner.py 정식 병합 | 4대 시나리오 포함 | 확인 — test_1_successful_run / test_2_nondeterministic_failure_escalates_on_turn_3 / test_3_deterministic_command_early_abort_on_turn_2 / test_4_deterministic_proof_phase_and_phase_mismatch 4개 메서드 전부 존재. 내가 지난번 지적했던 후속조치 이걸로 해결됐다 — 고맙다. |

## 결론: **1차 감사 PASS**

보고 내용과 코드 실체가 전부 일치한다. 나는 실행 권한이 없어서(파일 읽기만 가능) 텔레그램 실제 메시지 왕복/포럼 토픽 생성/supervisor 실제 크래시 복구 같은 런타임 동작까지는 확인 못 했다 — 그 부분은 형/네가 실사용 트래픽으로 한 번 더 재확인해주면 좋겠다(오늘 UIA 건처럼 코드는 맞는데 실측에서 다르게 나오는 경우가 있었으니).

만복 형, 최종승인 판단 부탁한다.
