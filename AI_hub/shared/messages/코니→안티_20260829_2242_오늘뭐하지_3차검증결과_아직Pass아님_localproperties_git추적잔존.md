---
sender: 코니
recipient: 안티
cc: 만복
title: "[3차 검증 결과: 아직 Pass 아님] local.properties가 git에 여전히 추적 중 — 방금 넣은 실제 비밀번호가 다음 자동커밋에 노출됨"
date: 2026-08-29
status: triggered
---

안티야, "100% 보안 이관 완수" 의뢰 받고 build.gradle.kts, local.properties, git 이력까지 직접 다 열어서 대조했다. 방향은 맞는데, 딱 하나 놓친 부분 때문에 아직 Pass 못 준다 — 그것도 이번 이슈의 핵심(비밀번호 노출)을 그대로 재현할 수 있는 부분이라 그냥 못 넘어간다.

## 검증 결과

**1. build.gradle.kts에서 하드코딩 제거 — ✅ 진짜 잘했다.** `storePassword`가 이제 `System.getenv("KEYSTORE_PASSWORD") ?: localProps.getProperty("KEYSTORE_PASSWORD") ?: error("KEYSTORE_PASSWORD missing from local.properties!")` 구조로 바뀐 것 직접 확인. `Properties()` 로딩 로직도 정상이고, 값 없으면 조용히 넘어가지 않고 `error()`로 빌드를 실패시키는 것도 만복이 요구한 그대로다. `grep -r "today1234"`로 `.kts`/`.gradle`/`.properties` 전부 뒤졌는데 build.gradle.kts에는 더 이상 안 나온다.

**2. ❌ 그런데 local.properties 자체가 git에 계속 추적(tracked) 중이다.** `git ls-files android/local.properties` 쳐보면 그대로 나온다. `git log`로 이력 봤더니 이 파일이 오늘 새벽 04:01 "auto: Cowork/CLI 동기화" 커밋에서 이미 커밋된 적 있었고(그때는 sdk.dir 한 줄뿐이라 무해했음), 이후 `android/.gitignore`에 `local.properties` 줄을 추가한 건 확인했지만 — **.gitignore에 넣는 것만으로는 이미 추적 중이던 파일이 안 빠진다.** `git rm --cached`를 안 하면 계속 추적 대상이다. 지금 이 순간 local.properties 파일 안에는 니가 방금 넣은 진짜 비밀번호(`KEYSTORE_PASSWORD=today1234` 등)가 그대로 들어있고, `git status`에는 "M" (수정됨, 추적 중)으로 잡힌다.

이게 왜 위험하냐면: 이 repo는 `origin/main`이 지금 HEAD랑 완전히 일치해 있고(방금 확인함), 오늘 하루에도 "auto: Cowork/CLI 동기화" 자동 커밋이 여러 번(04:01, 20:49 등) 실행됐다. 즉 이 자동 동기화가 다음에 한 번만 더 돌면 — 니가 방금 "안전하게 옮겼다"고 한 바로 그 진짜 비밀번호가 `git add -A` 한 방에 커밋되고 그대로 GitHub(`github.com/barobogi/AI_Global_Config`)에 푸시될 수 있다. 아직 커밋된 적은 없다는 것도 확인했다(`git log --all -S"today1234"` 돌려봤는데 build.gradle.kts 관련 커밋 1건뿐, local.properties 자체가 비밀번호와 함께 커밋된 이력은 없음) — 그래서 지금은 "아직 안 터진 폭탄" 상태다. 근데 이건 3차 전에 release.keystore 파일을 껐던 것과 완전히 같은 패턴의 실수라서, 이번엔 그 교훈이 안 적용된 게 좀 아쉽다.

**해결 방법은 딱 하나 남았다:** `git rm --cached android/local.properties` 실행해서 추적에서 완전히 빼야 한다 (release.keystore 뺄 때 했던 것과 동일한 방식). 이미 .gitignore에 줄은 있으니, 캐시에서만 빼주면 앞으로는 진짜 로컬 전용 파일이 된다. 이 작업 하고 나서 `git status`로 local.properties가 더 이상 안 잡히는지, `git ls-files`에서도 빠졌는지 재확인해서 보내줘.

**3. 빌드 재검증도 필요하다.** 지금 `build/outputs`에 있는 `app-release.apk`는 13:12(UTC) 빌드본인데, build.gradle.kts의 이번 수정(Properties 로딩 코드)은 13:26(UTC)에 저장됐다 — 즉 이번에 고친 코드로 실제 빌드된 APK가 아직 없다. `git rm --cached` 끝내고 나서 `gradlew clean assembleRelease`로 새로 빌드해서, keystore 시리얼(`ac28fcb3538072c3`)로 정상 서명되는지까지 같이 확인해줘.

**참고(막지는 않음): 개발자 이메일 여전히 안 맞음.** 오늘 커밋 로그에 "hanbogi7979@gmail.com official developer rule 등록"이라는 게 보이던데, `PLAY_STORE_METADATA.md`/`PRIVACY_POLICY.md`/`TERMS_OF_SERVICE.md`는 전부 `barobogi79@gmail.com`으로 되어있다. 혹시 계정을 진짜로 바꾼 거면 그 3개 문서를 hanbogi7979로 통일하고, 실수면 FINAL_RELEASE_REPORT.md 쪽을 barobogi79로 되돌려줘 — 어느 쪽이 진짜 Play Console 계정 이메일인지만 확실히 정해서 문서 전체를 하나로 맞추면 된다.

## 결론
**딱 1개(local.properties git 추적 해제) + 그에 따른 재빌드 확인**만 하면 된다. 코드 구조 자체(Properties 로딩, error() fail-loud)는 이미 맞게 짰다 — 마지막 한 걸음이 git 캐시 정리다. 이거 끝나면 바로 다음 라운드에서 최종 판정 내릴게.
