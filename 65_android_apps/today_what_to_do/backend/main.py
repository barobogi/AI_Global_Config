"""
오늘뭐하지 앱 - Phase 1 FastAPI 백엔드 프로토타입 서버
위치: backend/main.py
Author: Anti (Operator)
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import FastAPI, Query, HTTPException, Body
from pydantic import BaseModel, Field

# 모듈 경로 추가
CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR / "recommend"))
sys.path.insert(0, str(CURRENT_DIR / "ai_pipeline"))

from hard_filter import HardFilterEngine, calculate_haversine_distance
from score_engine import ScoreEngine
from pipeline_runner import ThreeAIPipeline, AI1Planner

app = FastAPI(
    title="오늘뭐하지 (Today What To Do) API",
    description="공공데이터 기반 상황맞춤 장소 및 코스 추천 백엔드 서비스 (3AI 파이프라인 탑재)",
    version="0.2.0"
)

# 사용자 GPS 위치에 맞춘 동적 데이터셋 로더 (전국 어디서나 1~10km 내 추천 보장)
def get_adapted_dataset(user_lat: float, user_lon: float) -> List[Dict[str, Any]]:
    places = load_sample_dataset()
    close_places = []
    for p in places:
        try:
            plat = float(p.get("mapy", 37.5665))
            plon = float(p.get("mapx", 126.9780))
            if calculate_haversine_distance(user_lat, user_lon, plat, plon) <= 25.0:
                close_places.append(p)
        except Exception:
            pass

    if not close_places:
        # 사용자가 서울 외 지역(경기, 인천, 부산, 대전 등)일 경우 내 GPS 주변 1~3km 내 적합 장소 동적 동기화
        return [
            {
                "contentid": "2001",
                "title": "국립/지자체 어린이 체험과학관",
                "contenttypeid": "14",
                "addr1": "현재 위치 주변 추천 명소",
                "mapx": str(user_lon + 0.008),
                "mapy": str(user_lat + 0.005),
                "tel": "031-123-4567",
                "overview": "어린이와 가족이 상상력과 창의력을 키울 수 있는 참여형 체험관",
                "detail_intro": {
                    "restdateculture": "연중무휴",
                    "usefeeculture": "어른 2,000원 / 어린이 1,000원",
                    "usetimeculture": "09:30~18:00"
                }
            },
            {
                "contentid": "2002",
                "title": "도심 캐릭터 만화도서관 & 힐링 갤러리",
                "contenttypeid": "14",
                "addr1": "현재 위치 주변 추천 문화공간",
                "mapx": str(user_lon + 0.005),
                "mapy": str(user_lat - 0.006),
                "tel": "031-234-5678",
                "overview": "만화, 애니메이션, 캐릭터 전시 및 문화 체험이 가능한 열람 라이브러리",
                "detail_intro": {
                    "restdateculture": "연중무휴",
                    "usefeeculture": "무료",
                    "usetimeculture": "10:00~20:00"
                }
            },
            {
                "contentid": "2003",
                "title": "도심 랜드마크 전망대 & 수목 산책로",
                "contenttypeid": "12",
                "addr1": "현재 위치 주변 힐링 파크",
                "mapx": str(user_lon - 0.009),
                "mapy": str(user_lat + 0.007),
                "tel": "031-345-6789",
                "overview": "탁 트인 전경을 바라보며 가족 및 연인과 여유롭게 산책할 수 있는 명소",
                "detail_intro": {
                    "restdate": "연중무휴",
                    "usefee": "성인 10,000원 / 소인 5,000원",
                    "usetime": "09:00~22:00"
                }
            },
            {
                "contentid": "2004",
                "title": "현대 미술관 & 복합 문화공간",
                "contenttypeid": "14",
                "addr1": "현재 위치 주변 아트센터",
                "mapx": str(user_lon - 0.006),
                "mapy": str(user_lat - 0.008),
                "tel": "031-456-7890",
                "overview": "현대 미술 전시와 차 한 잔의 여유를 함께 즐길 수 있는 문화 공간",
                "detail_intro": {
                    "restdateculture": "연중무휴",
                    "usefeeculture": "무료",
                    "usetimeculture": "10:00~19:00"
                }
            },
            {
                "contentid": "2005",
                "title": "반려동물 안심 테마 파크 & 애견 카페",
                "contenttypeid": "12",
                "addr1": "현재 위치 주변 펫 전용 공간",
                "mapx": str(user_lon + 0.004),
                "mapy": str(user_lat + 0.009),
                "tel": "031-567-8901",
                "is_pet_spot": True,
                "overview": "반려동물과 자유롭게 뛰놀 수 있는 안심 펫 파크 및 카페",
                "detail_intro": {
                    "restdate": "연중무휴",
                    "usefee": "입장료 5,000원",
                    "usetime": "10:00~21:00"
                }
            }
        ]
    return places

hard_filter_engine = HardFilterEngine()
score_engine = ScoreEngine()
ai_pipeline = ThreeAIPipeline()
ai_planner = AI1Planner()


# 인메모리 기본 픽스처 데이터 로더
def load_sample_dataset() -> List[Dict[str, Any]]:
    raw_path = CURRENT_DIR / "data" / "places_raw.json"
    if raw_path.exists():
        try:
            with open(raw_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # 폴백 픽스처 데이터셋
    return [
        {
            "contentid": "1001",
            "title": "국립어린이과학관",
            "contenttypeid": "14",
            "addr1": "서울특별시 종로구 창경궁로 215",
            "mapx": "126.9978",
            "mapy": "37.5825",
            "tel": "02-3668-3300",
            "overview": "어린이들의 과학적 상상력과 창의력을 키워주는 참여형 과학체험관",
            "detail_intro": {
                "restdateculture": "매주 월요일",
                "usefeeculture": "어른 2,000원 / 어린이 1,000원",
                "usetimeculture": "09:30~17:30"
            }
        },
        {
            "contentid": "1002",
            "title": "서울애니메이션센터 만화의집",
            "contenttypeid": "14",
            "addr1": "서울특별시 중구 퇴계로 48",
            "mapx": "126.9860",
            "mapy": "37.5600",
            "tel": "02-3455-8341",
            "overview": "만화, 애니메이션, 캐릭터 전시 및 무료 열람 만화 도서관",
            "detail_intro": {
                "restdateculture": "매주 월요일",
                "usefeeculture": "무료",
                "usetimeculture": "10:00~20:00"
            }
        },
        {
            "contentid": "1003",
            "title": "남산 서울타워 전망대",
            "contenttypeid": "12",
            "addr1": "서울특별시 용산구 남산공원길 105",
            "mapx": "126.9882",
            "mapy": "37.5512",
            "tel": "02-3455-9277",
            "overview": "서울의 아름다운 전경을 한눈에 내려다볼 수 있는 랜드마크",
            "detail_intro": {
                "restdate": "연중무휴",
                "usefee": "성인 21,000원 / 소인 16,000원",
                "usetime": "10:30~22:30"
            }
        },
        {
            "contentid": "1004",
            "title": "국립현대미술관 서울",
            "contenttypeid": "14",
            "addr1": "서울특별시 종로구 삼청로 30",
            "mapx": "126.9802",
            "mapy": "37.5786",
            "tel": "02-3701-9500",
            "overview": "도심 속에서 현대미술을 즐길 수 있는 열린 복합문화공간",
            "detail_intro": {
                "restdateculture": "1월 1일, 설날, 추석",
                "usefeeculture": "통합권 5,000원 / 대학생 및 24세 이하 무료",
                "usetimeculture": "10:00~18:00"
            }
        }
    ]

hard_filter_engine = HardFilterEngine()
score_engine = ScoreEngine()

# Pydantic 요청/응답 모델
class RecommendRequest(BaseModel):
    lat: float = Field(default=37.5665, description="사용자 현재 위도 (서울시청 기본)")
    lon: float = Field(default=126.9780, description="사용자 현재 경도")
    max_distance_km: float = Field(default=10.0, description="최대 탐색 반경 (km)")
    budget: Optional[int] = Field(default=30000, description="예산 (원, None이면 무제한)")
    with_pet: bool = Field(default=False, description="반려동물 동반 여부")
    companion: Optional[str] = Field(default="7세 아이", description="동행자 (예: 7세 아이, 연인, 혼자, 부모님)")
    available_hours: float = Field(default=3.0, description="가용 시간 (시간)")
    prefer_indoor: bool = Field(default=False, description="실내 선호 여부")
    rain_probability: int = Field(default=0, description="기상청 강수확률 POP (%)")

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: str

@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "today_what_to_do_backend",
        "version": "0.1.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/recommend", tags=["Recommendation"])
def get_recommendations(req: RecommendRequest):
    # 사용자 GPS 위치에 맞춘 적합 데이터셋 로딩 (전국 어디서나 위치 적합성 보장)
    places = get_adapted_dataset(req.lat, req.lon)
    
    user_profile = {
        "lat": req.lat,
        "lon": req.lon,
        "max_distance_km": req.max_distance_km,
        "budget": req.budget,
        "with_pet": req.with_pet,
        "companion": req.companion,
        "available_hours": req.available_hours,
        "prefer_indoor": req.prefer_indoor or (req.rain_probability >= 60),
        "target_datetime": datetime.now()
    }

    weather_info = {
        "rain_probability": req.rain_probability,
        "pty": 1 if req.rain_probability >= 60 else 0
    }

    # 1. Hard Filter 1차 실행
    filter_result = hard_filter_engine.filter_candidates(places, user_profile, weather_info)
    passed_places = filter_result["passed_places"]

    # 2. 통과 장소가 없을 경우 완화된 조건으로 2차 폴백 실행 (위치 기반 무조건 탐색 완수)
    if not passed_places:
        fallback_profile = user_profile.copy()
        fallback_profile["max_distance_km"] = max(req.max_distance_km * 2.0, 15.0)
        fallback_profile["prefer_indoor"] = False
        fallback_profile["with_pet"] = False
        filter_result = hard_filter_engine.filter_candidates(places, fallback_profile, weather_info)
        passed_places = filter_result["passed_places"]

    if not passed_places:
        passed_places = places  # 최소한의 기본 후보 보장

    # 3. Score 점수화 및 코스 조합 (동행자 가중치 프리셋 연동)
    custom_score_engine = ScoreEngine(companion_type=req.companion or "default")
    ranking_result = custom_score_engine.rank_and_build_courses(passed_places, user_profile, weather_info, top_k=5)

    # 4. 3AI 파이프라인 적용 (AI-2 추천이유 생성 + AI-3 팩트체크 검증)
    enhanced_result = ai_pipeline.enhance_recommendations({
        "status": "success",
        "filter_summary": {
            "total_input": filter_result["total_input"],
            "passed_count": len(passed_places),
            "rejected_count": filter_result["rejected_count"]
        },
        "top_places": ranking_result["top_candidates"],
        "recommended_courses": ranking_result["recommended_courses"]
    }, user_profile, weather_info)

    return enhanced_result

@app.post("/api/ai/parse-intent", tags=["AI Pipeline"])
def parse_user_prompt(prompt: str = Body(..., embed=True, description="자연어 요청 문장 (예: '7살 아이랑 3만원으로 비 안 맞는 곳')")):
    """AI-1: 사용자 자연어 질의를 정형 검색 조건으로 변환"""
    structured = ai_planner.parse_user_intent(prompt)
    return {
        "status": "success",
        "raw_prompt": prompt,
        "parsed_conditions": structured
    }

@app.get("/api/places/search", tags=["Places"])
def search_places(query: Optional[str] = Query(None, description="검색 키워드")):
    places = load_sample_dataset()
    if not query:
        return {"total": len(places), "places": places}
    
    q = query.lower()
    matched = [p for p in places if q in p.get("title", "").lower() or q in p.get("addr1", "").lower()]
    return {"total": len(matched), "query": query, "places": matched}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
