# 오늘뭐하지 Android 앱 — 빌드 디버깅 및 트러블슈팅 이력 (DEBUG_LOG)

본 문서는 Android Studio 로컬 환경에서 APK 빌드 중 발생한 에러 원인과 해결 조치 내역을 기록한 엔지니어링 로그입니다.

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
