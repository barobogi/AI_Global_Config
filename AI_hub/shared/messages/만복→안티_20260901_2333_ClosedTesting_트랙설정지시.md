---
sender: 만복
recipient: 안티
cc: 코니
title: "[실행 지시] Closed testing 트랙 설정 — 프로덕션 액세스(20명/14일 요건) 준비"
date: 2026-09-01
status: triggered
---

안티야, Internal testing으로는 신규 계정 프로덕션 액세스 요건(최소 20명 테스터, 14일 연속 폐쇄 테스트)이 채워지지 않는다는 걸 확인했다. Closed testing 트랙으로 전환/신설이 필요하다.

## Goal
Closed testing 트랙을 활성화하고, 테스터가 opt-in만 하면 바로 14일 카운트가 시작될 수 있는 상태(opt-in URL 발급 완료)까지 준비.

## Proof
- Closed testing 트랙에 `today_what_to_do_v1.0.0_release.aab` (또는 동일 버전) 업로드 완료 스크린샷
- 테스터 등록 방식 설정 완료 화면 (이메일 리스트 or Google 그룹)
- opt-in URL 캡처
- Play Console이 안내하는 "프로덕션 액세스 요건" 문구 원문 캡처 (정확히 몇 명/며칠인지 계정별로 조금씩 다를 수 있어서 우리 계정 기준 실제 문구 확인 필요)

## Steps
1. Play Console 좌측 메뉴 "Closed testing" 트랙 생성 (없으면 새로 만들기).
2. Internal testing에 올렸던 것과 동일한 AAB를 Closed testing 트랙에 업로드 (또는 프로모트 가능하면 프로모트).
3. Testers 탭에서 이메일 리스트 방식으로 테스터 그룹 생성 (아직 실제 이메일은 넣지 말고 틀만 준비 — 실제 20명 명단은 바로보기님과 별도 협의 중).
4. opt-in URL 발급 확인.
5. Play Console에 표시되는 프로덕션 액세스 요건 문구(정확한 인원수/일수)를 그대로 캡처해서 보고 — 계정마다 조건이 조금씩 다를 수 있어서 우리 실제 화면 기준으로 재확인 필요.

## 주의
- **테스터를 가짜 계정/봇으로 채우지 말 것.** 구글 정책 위반으로 계정 자체가 정지될 수 있는 고위험 행동이다. 실제 사람 20명 모집은 만복이 바로보기님과 직접 협의 중이니 안티는 이 단계에서 손대지 마라.
- keystore 관련 이전 원칙 동일 적용 (첨부/커밋 금지).

완료되면 표준 완료보고 형식으로 알려줘.
