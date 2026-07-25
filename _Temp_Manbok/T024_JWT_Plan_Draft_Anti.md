# [1차 기획안] VibeCoding 웹앱 제너레이터(T024) JWT 인증 표준화 가이드

**작성자**: 안티 (Anti)
**작성일**: 2026-07-14
**상태**: 코니/만복 검토 대기 중 (Draft)

## 1. 추진 배경 및 도입 목적
* **AI 생성 코드의 보안 취약성 방어**: AI(LLM)에게 로그인 구현을 요청하면 LocalStorage에 Access Token을 노출시키는 코드를 짤 확률이 높음. 이를 방지하기 위함.
* **무상태(Stateless) 서버 지향**: 세션 기반 방식 대비 서버(로드밸런서) 분산 및 확장이 용이한 JWT 구조를 표준으로 채택.

## 2. JWT 인증 표준 아키텍처 (보안 철칙)
1. **Access Token과 Refresh Token 분리**
2. **토큰 저장 위치 분리 (핵심)**:
   * Access Token: 메모리에 보관.
   * Refresh Token: 프론트엔드의 LocalStorage 저장을 엄격히 금지하며, 반드시 `Secure, HttpOnly, SameSite=Strict 쿠키`에 저장해 XSS 취약점을 방어.
3. **검증 및 로그아웃**: 모든 Protected Route에 토큰 검증 로직 필수 적용 및 로그아웃 시 쿠키 완전 만료 처리.

## 3. 구현 방식
* **프롬프트 인젝터**: AI가 코드를 짜기 직전, 이 규칙을 주입할 프롬프트 템플릿(`jwt_auth_rule.md`) 파일 신설.
* **스니펫(Snippet)**: Httponly Cookie를 통해 Refresh Token을 안전하게 처리하는 기본 서버 인증 스니펫(FastAPI/Express.js 등) 제공.

> **만복(PM) & 코니님 피드백 요청사항**:
> VibeCoding용 기본 템플릿 언어/프레임워크 스택(Python FastAPI vs Node Express)을 확정해 주시면, 맞춤형 스니펫을 준비하여 2차(최종) 기획안으로 대체하겠습니다.
