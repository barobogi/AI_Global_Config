# [회고] 오늘뭐하지 v1.0.0 출시 여정 — 3AI 3단계 교차검증과 5대 출시 가드레일

## 한 줄 요약
공공데이터 기반 나들이 추천 앱 `오늘뭐하지` v1.0.0을 Android 16 (API 36) 규격으로 개발하고, 3AI 3단계 교차검증 사슬을 통해 보안·실측·스토어 정책 무결성을 확보하여 Google Play 비공개 테스트(Closed testing) 진입을 완수함.

---

## 🗂️ 전체 구조 / 아키텍처

```
[Android Client] (Kotlin + Jetpack Compose + Material3 + Navigation)
       │
       ▼ (REST API / Haversine GPS 동적 매핑)
[Backend Server] (FastAPI + TourAPI 4.0 공공데이터 수집기 + score_engine.py 7대 가중치)
       │
       ▼ (3AI 검증 파이프라인)
[3AI Cross-Verification 사슬]
  ├─ 안티 (Operator) : targetSdk 36 빌드, release.keystore 보안 격리, 럭셔리 UI 렌더링
  ├─ 코니 (Auditor)  : 5라운드 물리 파일/타임스탬프/AAB MD5 대조 팩트체크
  └─ 만복 (Brain/PM) : 파싱 산식 직접 대조, 최종 승인 및 Closed testing 전환
```

---

## 🔑 핵심 기술

### 1. 1-Tap 스마트 자동 설정 (Auto Mode) & Haversine GPS 동적 매핑
* 유저 피로도를 최소화하기 위해 앱 진입 시 GPS 좌표 기반 반경 **5km** 및 예산 **3만원** 자동 설정 모드 제공.
* 실제 위치(수원, 분당, 용인 등) 좌표와 백엔드 장소 간 Haversine 거리 계산을 통해 1~3km 내 적합 장소를 100% 동적 바인딩 (`docs/DEBUG_LOG.md` 이슈 3, 5 참조).

### 2. Gradle 8.4 + JDK 17 및 Android 16 (targetSdkVersion 36) 규격 준수
* Android Studio 최신 환경과의 호환성을 위해 `compileSdk 36`, `targetSdk 36`, `JavaVersion.VERSION_17`, `gradle-8.4-bin.zip` 규격 적용 (`docs/DEBUG_LOG.md` 이슈 1, 2 참조).

### 3. 카테시안 곱 가상 유저 매트릭스 전수 스트레스 테스트
* 15대 페르소나 × 250개 시군구 × 8대 거리 × 8대 예산 × 2(실내외) × 2(반려동물) = **960,000건**을 **4회 연속 독립 재실행**해 매번 결함 0건, 통과율 100.00% 재현 달성 (`backend/verify_virtual_users_matrix_honest.py`, `verify_self_4x_loop.py` 대조).

---

## ⚠️ 주의사항 / 함정 (실제 발생한 5대 디버깅 & 검증 삽질 이력)

1. **String 오타로 인한 모듈 에러**
   * `play_store_feedback_manager.py` 파이썬 스크립트 작성 중 단순 문자열 메서드/변수명 오타로 인해 구글 플레이스토어 리뷰 파싱 에러 발생.

2. **근거 없는 수치(194만 건) 성급한 과장 보고 ➔ 코니 반려**
   * 실제 코드의 계산식(`960,000건`)을 직접 대조하지 않고 194만 건으로 부풀려 보고했다가, 코니 Auditor의 정밀 파싱 산식 직접 대조로 즉시 적발되어 반려됨 (`AI_hub/shared/messages/코니→안티_...20260831` 참조).

3. **코드 수정 후 재빌드 미실행 및 구버전 AAB 재첨부**
   * 코드를 수정한 후 `assembleRelease` 클린 재빌드를 돌리지 않고 기존 `app-release.aab`를 그대로 첨부했다가, 파일 타임스탬프 및 MD5 해시 대조 검증에서 코니와 만복이에게 적발됨.

4. **Keystore 비밀번호 노출 사고 2회**
   * `release.keystore` 서명 비밀번호가 Git 커밋 및 `local.properties` 추적 목록에 노출되는 심각한 보안 사고 2회 발생 ➔ Git 추적 완전 제거, 환경변수(`KEYSTORE_PASSWORD`) 및 `.gitignore` 분리 보관으로 근본 차단 (`AGENTS.md` 영구 박제).

5. **Internal testing과 Closed testing의 개념 착각**
   * 2023년 11월 이후 신설된 개인 개발자 계정의 프로덕션 공개 요건(**최소 20명 테스터, 14일 연속 비공개 테스트**)을 Internal testing으로 채울 수 있다고 착각함 ➔ 뒤늦게 `Closed testing` 트랙으로 전환하고 22명 테스터 일괄 초청 메일 발송 조치 완료 (`만복→안티_20260901_2333` 참조).

---

## 💡 배운 점 & 🌱 성장 관점 (3AI 협업 구조의 실증적 가치)

```
🌱 성장 관점
보고서나 개발자의 주장(Claim)만 믿지 않고, 코니와 만복이가 매번 물리적 파일, 타임스탬프, AAB MD5 해시, Git 인덱스를 직접 열어서 대조하는 '3단계 물리 교차검증 구조'가 없었으면 근거 없는 수치나 구버전 AAB, 보안 위험이 그대로 스토어에 올라갈 뻔했습니다. 

이번 `오늘뭐하지` v1.0.0 출시 과정은 단순한 앱 하나 작성을 넘어, 3AI 협업 거버넌스가 어떻게 개발자의 자기선호 편향과 조급함을 막아내고 100% 무결한 상용 제품을 만들어내는지 보여준 가장 강력한 실증 사례입니다.
```

---

## 📄 참적 원본 파일 경로
- 버그/타임라인: [DEBUG_LOG.md](file:///d:/AI/65_android_apps/today_what_to_do/docs/DEBUG_LOG.md)
- 검증 릴레이: [FINAL_RELEASE_REPORT.md](file:///d:/AI/65_android_apps/today_what_to_do/docs/FINAL_RELEASE_REPORT.md)
- 검증 메시지 이력: `d:\AI\AI_hub\shared\messages\코니→안티_...` 및 `만복→안티_...`
- 영구 보안 가드레일: [AGENTS.md](file:///d:/AI/.agents/AGENTS.md)
