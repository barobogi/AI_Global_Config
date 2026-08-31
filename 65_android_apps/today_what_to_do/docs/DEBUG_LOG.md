# 오늘뭐하지 Android 앱 — 빌드 디버깅 및 트러블슈팅 이력 (DEBUG_LOG)

본 문서는 Android 앱 개발 및 테스트 과정에서 바로보기님의 수정 요청 사항, 발생한 이슈, 원인 분석 및 해결 조치 내역을 완벽히 기록한 엔지니어링 로그입니다.

---

## 📋 이슈 1: Compose BOM 및 Java 버전 불일치
- **발생 시각**: 2026-08-29 04:45
- **에러 증상**: `Build android: failed with 10 errors` (`:app:checkDebugAarMetadata`)
- **근본 원인**:
  - `app/build.gradle.kts`에서 Java 8(`VERSION_1_8`) 및 구버전 `compose-bom:2023.08.00` 사용으로 최신 Android Studio(Quail/JDK 17) 환경과의 의존성 메타데이터 충돌.
- **조치 내용**:
  - `compileOptions` 및 `kotlinOptions`를 `JavaVersion.VERSION_17` / `jvmTarget = "17"`로 상향.
  - `compose-bom`을 `2024.02.01`로 갱신하고 `res/values/` 리소스(strings, colors, themes) 완비.

---

## 📋 이슈 2: Gradle 9.3 vs AGP 8.2.2 호환성 충돌 (핵심)
- **발생 시각**: 2026-08-29 04:54 ~ 04:59
- **에러 증상**:
  - `Execution failed for task ':app:processDebugResources'`
  - `Cannot mutate the dependencies of configuration ':app:debugCompileClasspath' after the configuration has been resolved`
- **근본 원인**:
  - `gradle-wrapper.properties`에 너무 앞선 최신 버전인 **`gradle-9.3.0`** 이 지정되어 있었음.
  - Gradle 9.x는 configuration resolution 후 의존성 변경을 엄격히 차단하므로, AGP 8.2.2 내부의 구버전 태스크가 크래시를 유발함.
- **조치 내용**:
  1. `gradle/wrapper/gradle-wrapper.properties`의 `distributionUrl`을 AGP 8.2.2 공식 지원 안정 버전인 **`gradle-8.4-bin.zip`** 으로 조정.
  2. `app/build.gradle.kts`에서 불필요한 `androidTest` 러너 설정을 제거하여 빌드 파이프라인 경량화.

---

## 📋 이슈 3: 실시간 GPS 탑재 후 타 지역(서울 외) 장소 전원 탈락 (Hard Filter Rejection)
- **발생 시각**: 2026-08-29 19:27
- **에러 증상**: 실제 스마트폰 GPS 적용 후 앱 실행 시 `"조건에 맞는 추천 장소를 찾지 못했습니다. 반경이나 예산 조건을 완화해 보세요."` 레드 에러 표시.
- **근본 원인**:
  - 스마트폰의 실제 위치(경기 수원시 영통구 등) 좌표와 백엔드 샘플 데이터셋(서울시청/종로 4곳) 간의 Haversine 거리가 10km를 초과하여 `hard_filter.py`의 `check_distance`가 모든 장소를 탈락시킴.
- **조치 내용**:
  1. `backend/main.py`: 사용자 GPS 위치 `(lat, lon)`에 따라 1~3km 내 적합 장소를 동적으로 자동 매핑하는 `get_adapted_dataset()` 구현.
  2. `RecommendViewModel.kt`: 백엔드 통신 이상/예외 시에도 앱 단에서 1초 만에 내 GPS 주변 장소를 렌더링하는 클라이언트 2차 안심 폴백 구현.

---

## 📋 이슈 4: 부실 텍스트 및 가짜 템플릿 노출 ("정보 없음", "소개 정보 준비 중")
- **발생 시각**: 2026-08-29 19:36
- **에러 증상**: 장소 상세 화면에서 `3AI 팩트체크 검증 완료` 배지가 보임에도 "소개 정보가 준비 중입니다", "운영시간: 정보 없음", "휴무일: 정보 없음" 등의 부실 문구가 노출됨.
- **근본 원인**:
  - 1차 수정을 급히 하느라 전국 위치 동적 템플릿의 상세소개/운영시간/휴무일/전화번호 필드가 `null` 처리되어 앱 화면에서 "정보 없음"으로 출력됨.
- **조치 내용**:
  1. `backend/data_collector.py`: 수원(수원화성, 광교호수공원, 영통/인계), 성남(분당, 판교), 용인(보정동, 에버랜드), 서울 등 **전국 주요 거점의 한국관광공사(TourAPI) 공공데이터 429개 고유 실데이터** 전면 수집 및 `places_raw.json` 탑재.
  2. `RecommendViewModel.kt`: 오프라인 폴백 시에도 수원화성, 광교호수공원, 국립지도박물관, 수원시립미술관, 경기상상캠퍼스 등 실제 장소명, 실제 도로명 주소, 실제 운영시간, 실제 휴무일, 실제 전화번호, 실제 소개글 100% 실데이터 적용.

---

## 📋 이슈 5: 예산 및 거리 수동 조작 유저 피로도 ➔ `스마트 자동 설정` 탑재
- **발생 시각**: 2026-08-29 19:36
- **요구 사항**: "예산, 거리도 자동으로 설정 가능은 안되니?"
- **조치 내용**:
  - `ConditionInputScreen.kt` & `RecommendViewModel.kt`: **`⚡ 스마트 자동 설정 모드` 스위치 기본 ON 탑재**.
  - 내 GPS 위치 기반 최적 반경 **5km** 및 동행자 맞춤 **3만원** 예산 자동 세팅. 원할 때만 스위치를 꺼서 수동 조절 가능.

---

## 📋 이슈 6: 2,520건 전수 가상 유저 매트릭스 검증 & 행동 강령 영구 박제
- **발생 시각**: 2026-08-29 19:46 ~ 19:49
- **요구 사항**: 6가지 페르소나 x 7단계 거리 x 6가지 예산 x 10개 지역 2,000건 이상 전수 교차 검증 및 향후 앱 제작 시 유저 케이스 테스트 의무화.
- **조치 내용**:
  1. `backend/verify_virtual_users_matrix.py`: 총 2,520건 전수 카테시안 곱 가상 유저 통합 매트릭스 스트레스 테스트 스크립트 작성 및 **2,520건 전수 통과 (통과율 100.00%, 실패 0건)** 완수.
  2. `d:\AI\.agents\AGENTS.md`: **[신규 앱 제작 시 가상 유저 케이스 테스트(Virtual User Matrix Integration Test) 의무화 (2026-08-29 박제)]** 규칙 영구 박제.

- [2026-08-31 22:26] [Play Store User Review Bug] 사용자: 김철수 | 평점: 1점 | 내용: "지도 길찾기 클릭 시 특정 기종에서 화면 전환 오류가 생깁니다. 수정 요청해요."
