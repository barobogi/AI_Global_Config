"""
오늘뭐하지 앱 - 9.2절 Score 점수화 및 코스 추천 엔진
위치: backend/recommend/score_engine.py
Author: Anti (Operator)

기획서 9.2절 가중치 공식:
recommend_score = (
    0.25 * condition_match +
    0.20 * distance_score +
    0.15 * weather_fit +
    0.15 * time_fit +
    0.10 * budget_fit +
    0.10 * popularity +
    0.05 * novelty
)
"""

import math
from datetime import datetime
from typing import List, Dict, Any, Optional

class ScoreEngine:
    """9.2절 Score 점수화 및 코스 조합 추천 엔진 (상용급 가중치 프리셋 연동)"""
    PRESET_WEIGHTS = {
        "default": {
            "condition_match": 0.25, "distance_score": 0.20, "weather_fit": 0.15,
            "time_fit": 0.15, "budget_fit": 0.10, "popularity": 0.10, "novelty": 0.05
        },
        "가족": {
            "condition_match": 0.20, "distance_score": 0.23, "weather_fit": 0.15,
            "time_fit": 0.15, "budget_fit": 0.15, "popularity": 0.10, "novelty": 0.02
        },
        "아이": {
            "condition_match": 0.20, "distance_score": 0.23, "weather_fit": 0.15,
            "time_fit": 0.15, "budget_fit": 0.15, "popularity": 0.10, "novelty": 0.02
        },
        "연인": {
            "condition_match": 0.20, "distance_score": 0.20, "weather_fit": 0.18,
            "time_fit": 0.15, "budget_fit": 0.07, "popularity": 0.10, "novelty": 0.10
        },
        "친구": {
            "condition_match": 0.17, "distance_score": 0.20, "weather_fit": 0.15,
            "time_fit": 0.15, "budget_fit": 0.10, "popularity": 0.15, "novelty": 0.08
        },
        "혼자": {
            "condition_match": 0.28, "distance_score": 0.20, "weather_fit": 0.15,
            "time_fit": 0.20, "budget_fit": 0.10, "popularity": 0.05, "novelty": 0.02
        }
    }

    def __init__(self, companion_type: str = "default"):
        self.weights = self._select_weights(companion_type)

    def _select_weights(self, companion_type: str) -> Dict[str, float]:
        for key in self.PRESET_WEIGHTS:
            if key in companion_type:
                return self.PRESET_WEIGHTS[key]
        return self.PRESET_WEIGHTS["default"]

    def calculate_place_score(self, place: Dict[str, Any], user_profile: Dict[str, Any], weather_info: Dict[str, Any]) -> Dict[str, Any]:
        """단일 장소에 대한 100점 만점 기준 세부 점수 계산"""
        # 1. condition_match (조건 일치도, 100점 만점)
        companion = user_profile.get("companion", "")
        title = place.get("title", "")
        overview = place.get("overview", "")
        intro = place.get("detail_intro", {})
        
        c_score = 70.0
        bonus = 0.0
        if "아이" in companion or "어린이" in companion:
            if any(k in title or k in overview for k in ["어린이", "아이", "체험", "과학", "애니메이션", "키즈", "박물관"]):
                bonus += 25.0
        if user_profile.get("with_pet"):
            if place.get("is_pet_spot") or "반려" in title or "애견" in title:
                bonus += 25.0
        if "연인" in companion or "데이트" in companion:
            if any(k in title or k in overview for k in ["전망", "미술관", "카페", "야경", "산책"]):
                bonus += 25.0
        
        c_score = min(100.0, c_score + bonus)

        # 2. distance_score (가까울수록 높은 점수, 0~10km)
        dist_km = place.get("calculated_distance_km", 5.0)
        max_dist = user_profile.get("max_distance_km", 10.0)
        # 0km=100점, max_dist=0점 (선형 감점)
        d_score = max(0.0, min(100.0, 100.0 * (1.0 - (dist_km / max(max_dist, 1.0)))))

        # 3. weather_fit (날씨 적합도)
        rain_prob = weather_info.get("rain_probability", 0)
        ctid = str(place.get("contenttypeid", "12"))
        is_indoor = place.get("is_indoor", ctid in ["14", "38", "39"])
        
        if rain_prob >= 60:
            w_score = 100.0 if is_indoor else 30.0
        elif rain_prob >= 30:
            w_score = 90.0 if is_indoor else 70.0
        else:
            w_score = 90.0 if not is_indoor else 80.0  # 맑은 날은 야외 선호 약간 가산

        # 4. time_fit (이용 가능 시간 및 소요시간 적합도)
        available_hours = user_profile.get("available_hours", 3.0)
        t_score = 85.0
        if ctid in ["12", "14"]:
            t_score = 95.0

        # 5. budget_fit (예산 여유도)
        user_budget = user_profile.get("budget", 50000)
        b_score = 80.0
        fee_str = str(intro.get("usefee", "")) + str(intro.get("usefeeculture", ""))
        if "무료" in fee_str or not fee_str.strip() or place.get("estimated_fee", 0) == 0:
            b_score = 100.0
        else:
            b_score = 85.0

        # 6. popularity (대표 이미지 유무 및 기본 인기도)
        p_score = 60.0
        if place.get("firstimage"):
            p_score += 25.0
        if place.get("tel"):
            p_score += 15.0

        # 7. novelty (신선도 기본값)
        n_score = 75.0

        # 가중치 합산 (총 100점 만점)
        total_score = (
            self.weights["condition_match"] * c_score +
            self.weights["distance_score"] * d_score +
            self.weights["weather_fit"] * w_score +
            self.weights["time_fit"] * t_score +
            self.weights["budget_fit"] * b_score +
            self.weights["popularity"] * p_score +
            self.weights["novelty"] * n_score
        )

        place["score_breakdown"] = {
            "total_score": round(total_score, 1),
            "condition_match": round(c_score, 1),
            "distance_score": round(d_score, 1),
            "weather_fit": round(w_score, 1),
            "time_fit": round(t_score, 1),
            "budget_fit": round(b_score, 1),
            "popularity": round(p_score, 1),
            "novelty": round(n_score, 1)
        }
        place["final_score"] = round(total_score, 1)
        return place

    def rank_and_build_courses(self, filtered_places: List[Dict[str, Any]], user_profile: Dict[str, Any], weather_info: Dict[str, Any], top_k: int = 5) -> Dict[str, Any]:
        """필터링된 장소들을 점수화하고 3코스 추천 세트 및 추천 근거 카드(Why Card)를 조합"""
        scored_places = [
            self.calculate_place_score(p, user_profile, weather_info)
            for p in filtered_places
        ]
        # 점수 내림차순 정렬
        scored_places.sort(key=lambda x: x.get("final_score", 0), reverse=True)

        # 카테고리 다양성 보장 로직 (동일 카테고리 쏠림 방지 — 데이트팝 불만 사례 방지)
        top_candidates = []
        seen_categories = {}
        for p in scored_places:
            cat = p.get("cat2") or p.get("contenttypeid") or "etc"
            count = seen_categories.get(cat, 0)
            if count < 2 or len(top_candidates) < 2:
                top_candidates.append(p)
                seen_categories[cat] = count + 1
            if len(top_candidates) >= top_k:
                break
        
        # 보충
        if len(top_candidates) < top_k:
            for p in scored_places:
                if p not in top_candidates:
                    top_candidates.append(p)
                    if len(top_candidates) >= top_k:
                        break
        rain_prob = weather_info.get("rain_probability", 0)

        # 코스 조합 (메인 목적지 + 보조 방문지/휴식)
        recommended_courses = []
        if len(top_candidates) >= 2:
            # 1. 꽉 찬 알찬 코스 (상위 1위 + 2위)
            c1_places = [top_candidates[0], top_candidates[1]]
            c1_fee_total = sum(p.get("estimated_fee", 0) for p in c1_places)
            recommended_courses.append({
                "course_id": "course_1",
                "course_name": "⭐ 베스트 맞춤 코스",
                "places": c1_places,
                "estimated_duration_hours": min(user_profile.get("available_hours", 3.0), 3.5),
                "summary": f"{top_candidates[0]['title']} 중심의 알찬 코스",
                "why_badges": [
                    f"🌧️ 우천 안심 실내 코스" if rain_prob >= 60 else "🌤️ 날씨 최적화",
                    f"💰 총 예상 경비 {c1_fee_total:,}원 (예산 내)",
                    f"📍 {top_candidates[0]['calculated_distance_km']}km 초근접 이동"
                ]
            })
        if len(top_candidates) >= 3:
            # 2. 여유로운 힐링 코스
            c2_places = [top_candidates[0], top_candidates[2]]
            c2_fee_total = sum(p.get("estimated_fee", 0) for p in c2_places)
            recommended_courses.append({
                "course_id": "course_2",
                "course_name": "🌿 여유로운 힐링 코스",
                "places": c2_places,
                "estimated_duration_hours": 2.5,
                "summary": f"{top_candidates[0]['title']} 중심의 편안한 일정",
                "why_badges": [
                    "☕ 여유로운 이동 동선",
                    f"💰 총 예상 경비 {c2_fee_total:,}원",
                    "👶 가족/동행 맞춤 추천"
                ]
            })
        elif top_candidates:
            c3_places = [top_candidates[0]]
            recommended_courses.append({
                "course_id": "course_3",
                "course_name": "📍 핵심 집중 코스",
                "places": c3_places,
                "estimated_duration_hours": 2.0,
                "summary": f"{top_candidates[0]['title']} 단독 집중 방문",
                "why_badges": [
                    "⏱️ 2시간 숏코스",
                    f"💰 {top_candidates[0].get('estimated_fee', 0):,}원"
                ]
            })

        return {
            "top_candidates": top_candidates,
            "recommended_courses": recommended_courses,
            "total_ranked": len(scored_places)
        }
