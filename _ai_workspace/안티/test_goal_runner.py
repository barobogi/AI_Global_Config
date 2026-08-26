import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Path setup
sys.path.insert(0, r"D:\AI\Global_Define")
from goal_runner import GoalRunner

class TestGoalRunnerComprehensive(unittest.TestCase):
    def setUp(self):
        self.test_task_id = "TEST_GOAL_RUNNER_4CASES"

    # Case 1: 정상 성공 케이스
    @patch("goal_runner.subprocess.Popen")
    @patch("time.sleep", return_value=None)
    def test_1_successful_run(self, mock_sleep, mock_popen):
        runner = GoalRunner(
            task_id=self.test_task_id,
            command="echo 'success'",
            proof_command="echo 'proof ok'",
            max_turns=5
        )
        runner._run_subproc = MagicMock(return_value=(True, "ok", ""))
        
        success = runner.execute()
        self.assertTrue(success)
        self.assertEqual(runner.turn, 1)
        self.assertEqual(runner.consecutive_fails, 0)
        self.assertFalse(runner._consecutive_escalated)
        print("[CASE 1 PASS] 정상 성공 케이스 (Turn 1 완료)")

    # Case 2: 비결정론적 실패 -> 3턴까지 재시도 후 에스컬레이션
    @patch("goal_runner.subprocess.Popen")
    @patch("time.sleep", return_value=None)
    def test_2_nondeterministic_failure_escalates_on_turn_3(self, mock_sleep, mock_popen):
        runner = GoalRunner(
            task_id=self.test_task_id,
            command="flaky_command",
            max_turns=5
        )
        side_effects = [
            (False, "", "Transient Error 1: socket timeout"),
            (False, "", "Transient Error 2: connection reset"),
            (False, "", "Transient Error 3: busy lock"),
            (False, "", "Transient Error 4: memory low"),
            (False, "", "Transient Error 5: out of turns")
        ]
        runner._run_subproc = MagicMock(side_effect=side_effects)
        
        escalate_calls = []
        orig = runner._escalate
        runner._escalate = lambda r: escalate_calls.append((runner.turn, r)) or orig(r)
        
        success = runner.execute()
        self.assertFalse(success)
        self.assertGreaterEqual(len(escalate_calls), 1)
        first_turn, first_reason = escalate_calls[0]
        self.assertEqual(first_turn, 3, f"Expected escalation at Turn 3, but got {first_turn}")
        self.assertIn("3회 연속 실패", first_reason)
        # Should have continued past turn 2
        self.assertEqual(runner.turn, 5)
        print(f"[CASE 2 PASS] 비결정론적 실패 케이스 (Turn {first_turn} 에스컬레이션, Turn 5까지 정상 시도 완료)")

    # Case 3: 결정론적 실패 (Command phase) -> 2턴만에 즉시 return False 및 1회 에스컬레이션
    @patch("goal_runner.subprocess.Popen")
    @patch("time.sleep", return_value=None)
    def test_3_deterministic_command_early_abort_on_turn_2(self, mock_sleep, mock_popen):
        runner = GoalRunner(
            task_id=self.test_task_id,
            command="invalid_python_script",
            max_turns=20
        )
        runner._run_subproc = MagicMock(return_value=(False, "", "SyntaxError: invalid syntax in line 10"))
        
        escalate_calls = []
        orig = runner._escalate
        runner._escalate = lambda r: escalate_calls.append((runner.turn, r)) or orig(r)
        
        success = runner.execute()
        self.assertFalse(success)
        self.assertEqual(len(escalate_calls), 1, "Expected exactly 1 escalation call")
        first_turn, first_reason = escalate_calls[0]
        self.assertEqual(first_turn, 2)
        self.assertIn("결정론적 실패", first_reason)
        # Verify that loop stopped immediately at Turn 2 and did not run to 20 turns
        self.assertEqual(runner.turn, 2, f"Expected loop to stop at Turn 2, but ran {runner.turn} turns")
        print(f"[CASE 3 PASS] 결정론적 실패 Command 케이스 (Turn {first_turn} 감지 즉시 return False 중단 성공)")

    # Case 4: 결정론적 실패 Proof phase 및 Phase 교차 검증
    @patch("goal_runner.subprocess.Popen")
    @patch("time.sleep", return_value=None)
    def test_4_deterministic_proof_phase_and_phase_mismatch(self, mock_sleep, mock_popen):
        # 4-A. Proof phase 동일 에러 2회 연속 -> Turn 2 조기 중단
        runner = GoalRunner(
            task_id=self.test_task_id,
            command="echo 'ok'",
            proof_command="verify_proof_cmd",
            max_turns=20
        )
        def mock_subproc(cmd):
            if "verify_proof_cmd" in cmd:
                return (False, "", "AssertionError: Proof validation failed: result mismatch")
            return (True, "cmd ok", "")
            
        runner._run_subproc = MagicMock(side_effect=mock_subproc)
        
        escalate_calls = []
        orig = runner._escalate
        runner._escalate = lambda r: escalate_calls.append((runner.turn, r)) or orig(r)
        
        success = runner.execute()
        self.assertFalse(success)
        self.assertEqual(runner.turn, 2)
        self.assertEqual(len(escalate_calls), 1)
        self.assertIn("Proof 검증", escalate_calls[0][1])
        print(f"[CASE 4-A PASS] 결정론적 실패 Proof 케이스 (Turn {runner.turn} 감지 즉시 중단 성공)")

        # 4-B. Phase 교차 (Command 실패 후 Proof 실패) -> 서로 다른 phase이므로 오탐 없이 정상 3회 로직 유지
        runner_cross = GoalRunner(
            task_id=self.test_task_id,
            command="cmd",
            proof_command="proof",
            max_turns=5
        )
        cross_side_effects = [
            (False, "", "Error 100"),  # Turn 1: Command fails with Error 100
            (True, "ok", ""),          # Turn 2: Command succeeds
            (False, "", "Error 100"),  # Turn 2: Proof fails with Error 100 (same error string, but different phase)
            (False, "", "Error 100"),  # Turn 3: Command fails with Error 100
            (False, "", "Error 100"),
            (False, "", "Error 100")
        ]
        runner_cross._run_subproc = MagicMock(side_effect=cross_side_effects)
        runner_cross.execute()
        # In turn 2, Proof failed with Error 100, but last failure was Command -> not deterministic -> continues
        self.assertGreater(runner_cross.turn, 2)
        print(f"[CASE 4-B PASS] Phase 교차 회귀 방지 검증 완료 (오탐 없이 지속)")

if __name__ == "__main__":
    unittest.main()
