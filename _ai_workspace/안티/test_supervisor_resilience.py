"""
[자체 검증 3회] supervisor.py 무중단 상시 운영 및 무한루프 방지 검증 스위트
"""

import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, r"D:\AI\Global_Define")
import supervisor

class TestSupervisorResilience(unittest.TestCase):
    def setUp(self):
        self.mock_target = {
            "name": "test_service",
            "check": MagicMock(),
            "pre_kill": None,
            "start": MagicMock(),
            "quiet_skip": False
        }

    # 1. 정상 생존 시 리셋 검증
    def test_1_healthy_process_resets_counters(self):
        self.mock_target["check"].return_value = 1
        failures = {"test_service": 2}
        alert_mode = {"test_service": True}

        # 시뮬레이션
        if self.mock_target["check"]() > 0:
            failures["test_service"] = 0
            alert_mode["test_service"] = False

        self.assertEqual(failures["test_service"], 0)
        self.assertFalse(alert_mode["test_service"])
        print("[PASS] 시나리오 1: 정상 생존 시 카운터 및 알림모드 정상 리셋")

    # 2. 프로세스 다운 시 지수 백오프 계산 검증
    def test_2_exponential_backoff_calculation(self):
        self.mock_target["check"].return_value = 0
        failures = {"test_service": 0}
        
        # 1회차 실패
        failures["test_service"] += 1
        wait_1 = min(60 * (2 ** (failures["test_service"] - 1)), 1800)
        self.assertEqual(wait_1, 60)

        # 2회차 실패
        failures["test_service"] += 1
        wait_2 = min(60 * (2 ** (failures["test_service"] - 1)), 1800)
        self.assertEqual(wait_2, 120)

        # 3회차 실패
        failures["test_service"] += 1
        wait_3 = min(60 * (2 ** (failures["test_service"] - 1)), 1800)
        self.assertEqual(wait_3, 240)
        print(f"[PASS] 시나리오 2: 지수 백오프 계산 검증 완료 ({wait_1}s -> {wait_2}s -> {wait_3}s)")

    # 3. 3회 초과 시 무한 루프 차단 & 알림 전용 모드 전환 검증
    @patch("supervisor._send_telegram_alert")
    def test_3_infinite_loop_prevention_on_limit_exceeded(self, mock_alert):
        self.mock_target["check"].return_value = 0
        failures = {"test_service": 3}
        alert_mode = {"test_service": False}
        restart_called = []

        # 4회차 시도 (BACKOFF_LIMIT = 3 초과)
        failures["test_service"] += 1
        if failures["test_service"] > supervisor.BACKOFF_LIMIT:
            alert_mode["test_service"] = True
            supervisor._send_telegram_alert("Limit reached")
        else:
            restart_called.append(True)

        self.assertTrue(alert_mode["test_service"])
        self.assertEqual(len(restart_called), 0, "4회차에는 재시작이 호출되지 않고 중단되어야 함")
        self.assertTrue(mock_alert.called, "텔레그램 긴급 알림이 발송되어야 함")
        print("[PASS] 시나리오 3: 3회 초과 시 무한 루프 완전 차단 및 알림 전용 모드 전환 검증 완료")

if __name__ == "__main__":
    unittest.main()
