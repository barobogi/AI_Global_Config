"""
오늘뭐하지 앱 - FastAPI 백엔드 엔드포인트 E2E 테스트
위치: backend/test_api_server.py
Author: Anti (Operator)
"""

import sys
import unittest
from pathlib import Path

# 모듈 경로 추가
CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

from main import app, load_sample_dataset
from fastapi.testclient import TestClient

class TestBackendApi(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        resp = self.client.get("/api/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "today_what_to_do_backend")
        print("✅ [Test] /api/health 정상 통과")

    def test_places_search_endpoint(self):
        resp = self.client.get("/api/places/search?query=과학관")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreaterEqual(data["total"], 1)
        self.assertIn("국립어린이과학관", data["places"][0]["title"])
        print("✅ [Test] /api/places/search 검색 정상 통과")

    def test_recommendation_flow(self):
        req_payload = {
            "lat": 37.5665,
            "lon": 126.9780,
            "max_distance_km": 5.0,
            "budget": 30000,
            "with_pet": False,
            "companion": "7세 아이",
            "available_hours": 3.0,
            "prefer_indoor": True,
            "rain_probability": 80
        }
        resp = self.client.post("/api/recommend", json=req_payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertGreaterEqual(len(data["top_places"]), 1)
        self.assertGreaterEqual(len(data["recommended_courses"]), 1)

        print("\n" + "="*60)
        print("🎯 [Test] /api/recommend 실전 추천 E2E 응답 확인:")
        print(f"  • 추천 1순위: {data['top_places'][0]['title']} (점수: {data['top_places'][0]['final_score']}점)")
        print(f"  • 추천 코스명: {data['recommended_courses'][0]['course_name']}")
        print(f"  • 코스 요약: {data['recommended_courses'][0]['summary']}")
        print("="*60)

if __name__ == "__main__":
    unittest.main()
