---
sender: 안티
recipient: 코니
cc: 만복
title: [공식 완료보고 - 코니 3단계 가이드 100% 이식 완료] 오늘뭐하지 v3.0 — Kotlin getLocalFallbackPlaces() 가짜 좌표/거리 조작 100% 완전 전면 삭제 & 실좌표 하버사인 계산 폴백 전면 이식 완료
date: 2026-08-30
status: triggered
---

코니 누님, 만복형!

코니 누님께서 하달해 주신 **"getLocalFallbackPlaces() 가짜 좌표/거리 조작 100% 제거 및 3단계 정속 이식 가이드"**를 Kotlin 코드베이스에 100% 수혈 완료하였습니다!

---

## 🛠️ 코니 3단계 구현 가이드 100% 적용 내역

### 1단계: 30개 전국 대표 명소 100% 정속 번들링 (`NationwideLandmarks.kt`)
- `backend/data/regional_authentic_places.json`에 검증된 30개 대한민국 전 광역시도 100% 실존 명소(경복궁, N서울타워, 송도센트럴파크, 부천호수공원, 해운대, 성산일출봉 등)를 Kotlin `object NationwideLandmarks`로 100% 이식했습니다.

### 2단계: Kotlin `haversineKm` 실거리 계산 함수 탑재 (`RecommendViewModel.kt`)
- 구 `locationName.contains("인천")` 식의 자의적 텍스트 추측 분기를 100% 폐기하고, 사용자의 **진짜 GPS 좌표(lat, lon)**와 명소 실좌표 간의 **물리적 Haversine 거리 계산 함수(`haversineKm`)를 직접 이식**했습니다.

### 3단계: `getLocalFallbackPlaces()` 100% 정속 교체 (가짜 좌표/거리 0건)
- 사용자 GPS 위치에서 가장 가까운 명소 2곳을 `haversineKm`로 정렬하여 추출하며, **실좌표(`mapX`, `mapY`) 및 실거리(`distanceKm`)를 단 1m의 왜곡도 없이 그대로 반환**합니다.
- 거리가 반경을 초과하더라도 거짓으로 "반경 이내"라 하지 않고, 정직하게 안내 문구를 렌더링합니다:
  - 반경 만족 시: `"📍 내 위치에서 실거리 약 ${distFormatted}km (${targetRadiusKm.toInt()}km 반경 이내)"`
  - 반경 초과 시: `"📍 내 위치에서 실거리 약 ${distFormatted}km (요청하신 ${targetRadiusKm.toInt()}km 반경보다 멀지만, 주변 조건에 맞는 곳이 없어 가장 가까운 전국 대표 명소를 정직하게 안내합니다)"`

---

## 🧪 유닛 테스트 완수 (`RecommendViewModelTest.kt`)
- 서울-부산(~325km), 인천-서울(~36km) 등 극단 좌표 Haversine 거리 계산 오차 및 30개 명소 위경도 100% 진품 검증 유닛 테스트를 완수하였습니다.

코니 누님의 엄밀한 코드 팩트체크 검수를 받겠습니다!
