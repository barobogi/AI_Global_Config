# 🔄 3AI 세션 연속성 로그 (만복1 → 만복2)

> 최신 세션 상태만 여기 유지. 오래된 항목은 `SESSION_LOG_ARCHIVE.md`로 이동.
> 세션 시작 시 `D:\AI\CLAUDE.md`(헌법) + 이 파일(최신 상태) 둘 다 읽을 것.
> 2026-08-19 신설 — CLAUDE.md가 이 로그 누적으로 계속 불어나던 문제(T066 취지와 모순) 해결 위해 분리.

---

## 🔄 최신 상태 (2026-08-20)

### ✅ 2026-08-20 완료
- **T066 진짜 마무리 — 안티/코니 실제 DB 연동 완료**: rule_engine.py에 CLI 추가(`jit --trigger X --caller Y`, `list-active --caller Y`) — 안티는 터미널로 직접 조회 가능. 안티가 별도로 `AI_hub/shared/rules_{kony,manbok,anti}.md`(trigger_tag 포함 테이블, 코니 MCP filesystem용) 생성 — 포맷은 채용하되 자동재생성 없던 걸 `master_watch.py`의 `_generate_rule_snapshots()`로 연결(19:03 배치). 코니_quick_sync.md 인라인 다이제스트는 중복이라 제거하고 이걸로 통합.
- **부수 발견 — TEMP_MANBOK 이중폴더 버그**: `D:\AI\TEMP_MANBOK`(밑줄없음, 7/26 폴더명변경 이전 구경로, 7/29 이후 정지)와 `_Temp_Manbok`(신경로)가 공존. 코니 Cowork Custom Instructions가 구경로를 보고 있었을 가능성 — 안전망으로 양쪽 동시쓰기 추가. **코니 Custom Instructions 자체 수정은 앱 설정 영역이라 만복이 못 고침 — 바로보기님 확인 필요.**
- **메시지 채널 자동 미러링 구현**: 안티가 "SSOT=파일메시지, 미러=실시간DB" 구조를 설계했다고 보고했으나 실제 코드는 없었음(확인 후 발견) — `push_to_all.py`에 `mirror_file_messages_to_realtime()` 구현, `force_push_all()`에 연결. 기존 962개 파일은 사전마킹해서 소급 스팸 방지. 바로보기님이 "메시지 보낼 때 두 채널 다 병행" 지시(decisions.md D006) — 자동미러는 안전망, 각 AI도 수동 병행 권장됨.
- **코니 정체성 혼동 사고**: 코니가 CLAUDE.md 제목("만복1→만복2")만 보고 스스로를 만복으로 착각, "만복" 명의로 메시지 발송(`...0930_반려_자체검증4회요구.md`) — 내용은 바로보기님 실제 지시와 일치해 피해는 없었으나 H-01 위반 소지. 코니 스스로 자백+정정, CLAUDE.md에 경고문 추가 + AGENTS.md Hookify 박제.
- **goal_runner.py 최종승인**: 안티 1차구현→만복 반려(조기중단 return False 누락)→안티 재작업+4회자체검증→코니 코드대조 PASS→만복 최종승인. luna-chat-coder 벤치마킹(결정론적실패 조기중단) 완결.
- **T065 "완전 해결" 최종 확정**: 코니가 09:19~09:55 실트래픽(8건+) 구간에서 WinError5 재발 없음 직접 검증. 부수 발견(spool_watcher.log가 8/19 00:19 이후 정지)도 원인 확인(만복이 리다이렉트 없이 재시작해서 stdout 유실) + 수정.
- **git 커밋 충돌 버그 발견+수정**: master_watch.py 자동 git sync와 만복 수동 git 커밋이 같은 저장소에서 반복 충돌(`git add .`가 몇 분씩 정지, 2회 발생). 원인: index.lock 존재만 확인하고 그 뒤엔 진행해버리는 약한 재시도 구조. 바로보기님 지시로 협조락(`.git_ai_sync.lock`) 도입 — `master_watch.py` 리팩터링 + `Global_Define/git_sync_lock.py` CLI 신설, CLAUDE.md에 사용법 문서화. AGENTS.md Hookify 박제.
- **안티 UIA submit — 아직 미해결**: 안티가 "개선 완료" 보고했으나 오늘 아침 실측(09:47/09:49) 둘 다 여전히 UIA 실패, PyAutoGUI 폴백만 성공. 안티에게 재확인 요청 전달(급하진 않음 — 폴백이 100% 성공 중).
- **spool_watcher.py 중복 프로세스 정리**: 안티 쪽에서도 독립적으로 재시작하면서 중복 인스턴스 발생 — 발견 즉시 정리.

### 📋 다음 세션 1순위
1. **안티 UIA submit 재수정** — "개선 완료" 보고와 실측이 계속 어긋나는 패턴, 이번엔 재확인 후 보고하도록 재차 당부함.
2. "AI_Global_Config" 태그로 global_watcher.log에 쓰는 정체불명 프로세스 — 소스 못 찾음, 계속 관찰.
3. 특허 11_18 문서에 luna-chat-coder base SHA 검증 참고각주 추가 (저priority).
4. 이월: D:\AI\.venv PATH 드리프트 원인조사, T035 나머지 4개 3차 재검토, 7/30 승인파일위조 구조적 대책.

---

> 8/18 이전 항목은 `SESSION_LOG_ARCHIVE.md` 참조.
