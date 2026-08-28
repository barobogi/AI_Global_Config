"""
오늘뭐하지 앱 - Hard Filter 실전 시나리오 검증 스크립트
위치: backend/recommend/test_hard_filter.py
Author: Anti (Operator)

검증 시나리오:
"7세 아이 동반 / 서울시청 기준 / 오늘 / 3시간 / 예산 30,000원 / 대중교통(5km 이내) / 비(강수확률 80%, 실내선호)"
"""

import os
import sys
import json
import unittest
from datetime import datetime
from pathlib import Path

# 모듈 경로 설정
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hard_filter import HardFilterEngine, calculate_haversine_distance

class TestHardFilterScenarios(unittest.TestCase):
    def setUp(self):
        self.engine = HardFilterEngine()
        
        # 1. 다채로운 테스트 픽스처 데이터셋 (다양한 엣지 케이스 포함)
        self.mock_places = [
            {
                "contentid": "1001",
                "title": "국립어린이과학관 (실내 박물관)",
                "contenttypeid": "14",
                "mapx": "126.9978",
                "mapy": "37.5825",
                "dist": "2500",
                "detail_intro": {
                    "restdateculture": "매주 월요일",
                    "usefeeculture": "성인 2,000원 / 어린이 1,000원",
                    "usetimeculture": "09:30~17:30"
                }
            },
            {
                "contentid": "1002",
                "title": "서울 숲 야외 놀이터 (실외 공원)",
                "contenttypeid": "12",
                "mapx": "127.0374",
                "mapy": "37.5444",
                "dist": "6200",
                "detail_intro": {
                    "restdate": "연중무휴",
                    "usefee": "무료",
                    "usetime": "24시간"
                }
            },
            {
                "contentid": "1003",
                "title": "초호화 VIP 패밀리 테마파크",
                "contenttypeid": "14",
                "mapx": "126.9780",
                "mapy": "37.5665",
                "dist": "500",
                "detail_intro": {
                    "restdateculture": "연중무휴",
                    "usefeeculture": "1인 입장료 90,000원",
                    "usetimeculture": "10:00~20:00"
                }
            },
            {
                "contentid": "1004",
                "title": "성인 전용 나이트 라이브 클럽",
                "contenttypeid": "14",
                "mapx": "126.9780",
                "mapy": "37.5665",
                "dist": "300",
                "detail_intro": {
                    "restdateculture": "연중무휴",
                    "usefeeculture": "10,000원",
                    "usetimeculture": "20:00~04:00"
                }
            },
            {
                "contentid": "1005",
                "title": "월요일 정기휴무 미술관",
                "contenttypeid": "14",
                "mapx": "126.9800",
                "mapy": "37.5670",
                "dist": "800",
                "detail_intro": {
                    "restdateculture": f"매주 {['월','화','수','목','금','토','일'][datetime.now().weekday()]}요일 휴무",
                    "usefeeculture": "무료",
                    "usetimeculture": "10:00~18:00"
                }
            },
            {
                "contentid": "1006",
                "title": "강남 코엑스 아쿠아리움 (실내 수족관)",
                "contenttypeid": "14",
                "mapx": "127.0590",
                "mapy": "37.5126",
                "dist": "8500", # 서울시청에서 약 9km (5km 초과)
                "detail_intro": {
                    "restdateculture": "연중무휴",
                    "usefeeculture": "성인 32,000원 / 어린이 28,000원",
                    "usetimeculture": "10:00~20:00"
                }
            },
            {
                "contentid": "1007",
                "title": "서울애니메이션센터 만화의집 (실내 도서관)",
                "contenttypeid": "14",
                "mapx": "126.9860",
                "mapy": "37.5600",
                "dist": "1200",
                "detail_intro": {
                    "restdateculture": "매주 월요일",
                    "usefeeculture": "무료",
                    "usetimeculture": "10:00~20:00"
                }
            }
        ]

    def test_official_scenario_filtering(self):
        """
        만복 지시서 공식 시나리오:
        - 동행: 7세 아이
        - 기준 위치: 서울시청 (37.5665, 126.9780)
        - 최대 거리: 5km (대중교통 3시간 이내 이동 반경)
        - 예산: 30,000원
        - 날씨: 비 (POP=80%, 실내 선호)
        - 반려동물: 미동반
        """
        user_profile = {
            "lat": 37.5665,
            "lon": 126.9780,
            "max_distance_km": 5.0,
            "budget": 30000,
            "with_pet": False,
            "target_datetime": datetime.now(),
            "prefer_indoor": True,
            "companion": "7세 아이"
        }

        weather_info = {
            "rain_probability": 80,
            "pty": 1 # 비
        }

        result = self.engine.filter_candidates(self.mock_places, user_profile, weather_info)

        print("\n" + "=" * 70)
        print("🎯 [Hard Filter 실전 검증] '7세 아이 / 서울 / 3만원 / 5km / 비(POP 80%)' 시나리오")
        print("=" * 70)
        print(f"📊 전체 입력 후보: {result['total_input']}건")
        print(f"✅ 통과(Passed) 후보: {result['passed_count']}건")
        print(f"❌ 탈락(Rejected) 후보: {result['rejected_count']}건")
        print("-" * 70)

        print("🚫 [탈락 상세 내역]:")
        for r in result["rejected_places"]:
            p = r["place"]
            print(f"  • [{r['stage'].upper()}] '{p['title']}' ➔ 사유: {r['reason']}")

        print("-" * 70)
        print("🏆 [최종 통과 후보]:")
        for p in result["passed_places"]:
            fee = p.get("detail_intro", {}).get("usefeeculture", "무료")
            print(f"  ✨ '{p['title']}' (거리: {p.get('calculated_distance_km')}km, 요금: {fee})")
        print("=" * 70 + "\n")

        # 1. 서울 숲 (야외 공원) -> 우천 실내 선호로 탈락해야 함
        rejected_titles = [r["place"]["title"] for r in result["rejected_places"]]
        self.assertIn("서울 숲 야외 놀이터 (실외 공원)", rejected_titles)

        # 2. 초호화 테마파크 (90,000원) -> 예산 초과(30,000원 초과)로 탈락해야 함
        self.assertIn("초호화 VIP 패밀리 테마파크", rejected_titles)

        # 3. 성인 전용 클럽 -> 연령/동행자 제약으로 탈락해야 함
        self.assertIn("성인 전용 나이트 라이브 클럽", rejected_titles)

        # 4. 코엑스 아쿠아리움 -> 거리 초과(>5km)로 탈락해야 함
        self.assertIn("강남 코엑스 아쿠아리움 (실내 수족관)", rejected_titles)

    def test_nth_week_restdate_parsing(self):
        """매월 N째주 X요일 휴무 패턴 독립 검증"""
        # 2026년 8월 29일은 5주차 토요일
        dt_5th_sat = datetime(2026, 8, 29)
        place_5th_sat = {
            "title": "5주차 토요일 휴무 도서관",
            "detail_intro": {"restdate": "매월 다섯째주 토요일 휴무"}
        }
        from hard_filter import check_is_open
        is_open, reason = check_is_open(place_5th_sat, dt_5th_sat)
        self.assertFalse(is_open)
        self.assertIn("5째주", reason)

        # 다른 주차 토요일은 정상 영업이어야 함
        dt_1st_sat = datetime(2026, 8, 1) # 1주차 토요일
        is_open_1st, _ = check_is_open(place_5th_sat, dt_1st_sat)
        self.assertTrue(is_open_1st)

    def test_budget_child_price_parsing(self):
        """다중 요금 문자열에서 어린이 요금 분리 파싱 검증"""
        place_multi_fee = {
            "title": "가족 체험관",
            "detail_intro": {"usefeeculture": "성인 35,000원 / 어린이 12,000원"}
        }
        from hard_filter import check_budget
        # 예산 20,000원 + 아이 동반 -> 어린이 요금(12,000원) 기준 통과
        ok, msg, fee = check_budget(place_multi_fee, user_budget=20000, is_child=True)
        self.assertTrue(ok)
        self.assertEqual(fee, 12000)

        # 예산 20,000원 + 성인 단독 -> 성인 요금(35,000원) 기준 탈락
        ok_adult, msg_adult, fee_adult = check_budget(place_multi_fee, user_budget=20000, is_child=False)
        self.assertFalse(ok_adult)
        self.assertEqual(fee_adult, 35000)

if __name__ == "__main__":
    unittest.main()
