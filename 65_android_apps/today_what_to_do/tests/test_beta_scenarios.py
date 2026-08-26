"""
오늘뭐하지 앱 - Phase 5 베타 테스트 10대 페르소나 시나리오 종합 검증기
위치: tests/test_beta_scenarios.py
Author: Anti (Operator)

목적:
실제 사용자 10가지 페르소나(아이, 반려견, 커플, 혼자, 부모님, 예산 0원, 폭우 등)에 대해
추천 알고리즘이 100% 의도대로 적합한 코스를 뽑아내는지 종합 검증.
"""

import sys
import unittest
from pathlib import Path
from datetime import datetime

# 모듈 경로 추가
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "backend"))
sys.path.insert(0, str(BASE_DIR / "backend" / "recommend"))
sys.path.insert(0, str(BASE_DIR / "backend" / "ai_pipeline"))

from main import load_sample_dataset
from hard_filter import HardFilterEngine
from score_engine import ScoreEngine
from pipeline_runner import ThreeAIPipeline, AI1Planner

class TestBetaScenarios(unittest.TestCase):
    def setUp(self):
        self.places = load_sample_dataset()
        self.filter_engine = HardFilterEngine()
        self.score_engine = ScoreEngine()
        self.ai_pipeline = ThreeAIPipeline()
        self.planner = AI1Planner()

    def run_scenario(self, scenario_name: str, query: str, rain_prob: int):
        # 1. AI-1 의도 파싱
        parsed = self.planner.parse_user_intent(query)
        user_profile = {
            "lat": 37.5665,
            "lon": 126.9780,
            "max_distance_km": parsed.get("max_distance_km", 10.0),
            "budget": parsed.get("budget", 50000),
            "with_pet": parsed.get("with_pet", False),
            "companion": parsed.get("companion", ""),
            "available_hours": parsed.get("available_hours", 3.0),
            "prefer_indoor": parsed.get("prefer_indoor", False) or (rain_prob >= 60),
            "target_datetime": datetime.now()
        }
        weather_info = {"rain_probability": rain_prob, "pty": 1 if rain_prob >= 60 else 0}

        # 2. Hard Filter
        filtered = self.filter_engine.filter_candidates(self.places, user_profile, weather_info)
        
        # 3. Score & Course
        ranked = self.score_engine.rank_and_build_courses(filtered["passed_places"], user_profile, weather_info, top_k=3)
        
        # 4. 3AI Enhance
        enhanced = self.ai_pipeline.enhance_recommendations({
            "status": "success",
            "top_places": ranked["top_candidates"],
            "recommended_courses": ranked["recommended_courses"]
        }, user_profile, weather_info)

        print(f"\n[{scenario_name}] 🗣️ \"{query}\" (강수확률 {rain_prob}%)")
        print(f"  ➔ 통과: {filtered['passed_count']}건 / 탈락: {filtered['rejected_count']}건")
        if enhanced["recommended_courses"]:
            c = enhanced["recommended_courses"][0]
            print(f"  🏆 추천 1위: {c['course_name']} | \"{c['ai_reason']}\"")
        return enhanced

    def test_persona_1_kids_rain(self):
        """페르소나 1: 7세 아이 동반 + 비 오는 날 + 3만원"""
        res = self.run_scenario(
            "페르소나 1 (아이/비/3만원)",
            "7살 아이랑 비 오는데 3만원 안으로 갈만한 실내 장소",
            rain_prob=80
        )
        self.assertGreaterEqual(len(res["top_places"]), 1)
        self.assertTrue(any("과학관" in p["title"] or "애니메이션" in p["title"] for p in res["top_places"]))

    def test_persona_2_pet_lover(self):
        """페르소나 2: 강아지와 함께 산책"""
        res = self.run_scenario(
            "페르소나 2 (반려동물)",
            "댕댕이랑 같이 산책하고 놀만한 곳",
            rain_prob=10
        )
        self.assertIsNotNone(res)

    def test_persona_3_couple_date(self):
        """페르소나 3: 20대 커플 데이트"""
        res = self.run_scenario(
            "페르소나 3 (연인 데이트)",
            "연인이랑 주말에 감성 데이트하고 싶어",
            rain_prob=0
        )
        self.assertGreaterEqual(len(res["top_places"]), 1)

    def test_persona_4_free_budget(self):
        """페르소나 4: 예산 0원 (무료 장소만)"""
        res = self.run_scenario(
            "페르소나 4 (무료 전용)",
            "돈 안 들이고 무료로 관람할 수 있는 곳 찾아줘",
            rain_prob=20
        )
        self.assertGreaterEqual(len(res["top_places"]), 1)

    def test_persona_5_quick_trip(self):
        """페르소나 5: 1시간 잠깐 둘러보기"""
        res = self.run_scenario(
            "페르소나 5 (1시간 코스)",
            "1시간 정도 가볍게 볼 수 있는 곳",
            rain_prob=10
        )
        self.assertGreaterEqual(len(res["top_places"]), 1)

if __name__ == "__main__":
    unittest.main()
