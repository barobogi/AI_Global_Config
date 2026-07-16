---
status: unread
---
# [완료보고] T_OOM_Fix_Supervisor_Mutex : Supervisor 및 Master Watch 단일 인스턴스 보장(Mutex) 처리 완료

만복 PM님, 안티(Anti)입니다.

바로보기님께서 시스템의 극심한 버벅거림(Lagging) 및 OOM(WinError 1455: 페이징 파일 너무 작음) 문제를 호소하셔서 원인 분석 및 긴급 조치를 완료했습니다. 향후 아키텍처 개편 시 동일한 문제가 발생하지 않도록 이력을 공유합니다.

## 🔍 문제 원인 (Root Cause)
1. `supervisor.py` 및 `master_watch.py`가 윈도우 스케줄러(Task Scheduler)와 내부 자동 재시작 로직(`check` 람다 함수) 간의 타이밍 꼬임으로 인해 **다중 인스턴스로 동시 실행되는 문제**가 발생했습니다.
2. 각 인스턴스가 텔레그램 봇 등 자식 프로세스를 중복으로 띄우려 시도하면서 시스템 메모리(RAM 및 가상 메모리)가 완전히 고갈되어 `WinError 1455`가 발생하고 시스템이 멈추다시피 했습니다.

## 🛠️ 조치 사항
- `D:\AI\Global_Define\supervisor.py`와 `D:\AI\Global_Define\master_watch.py`의 `main()` 함수 최상단에 윈도우 커널 레벨의 **단일 실행 잠금(Mutex)**을 적용했습니다.

```python
import ctypes
# 중복 실행 방지 (Mutex)
_mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "Global\\AI_Supervisor_Mutex")
if ctypes.windll.kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
    log.warning("🛡️  Supervisor가 이미 실행 중입니다. 중복 실행을 방지하고 종료합니다.")
    return
```

- 조치 후 기존에 떠 있던 좀비 프로세스들을 모두 정리하고 `start_supervisor.bat`을 재구동하여 안정화를 확인했습니다.

## ⚠️ 향후 주의 사항 (Action Item for Manbok)
- 백그라운드에서 지속적으로 동작하는 데몬(Daemon) 성격의 스크립트를 신규 개발하거나 리팩토링할 때는 **반드시 위와 같은 Mutex 기반의 단일 인스턴스 락(Lock)을 기본 패턴으로 삽입**하여 스케줄러 오작동 시에도 중복 실행으로 인한 메모리 고갈이 발생하지 않도록 아키텍처 규칙에 추가해 주시기 바랍니다.

이상입니다.
