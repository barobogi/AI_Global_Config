# [최종 기획안] VibeCoding 웹앱 제너레이터(T024) JWT 인증 표준화 가이드

**작성자**: 안티 (Anti)
**작성일**: 2026-07-14
**상태**: 최종 확정안

## 1. 추진 배경 및 도입 목적
* **AI 생성 코드의 보안 취약성 방어**: AI(LLM)에게 로그인 구현을 요청하면 LocalStorage에 Access Token을 노출시키는 코드를 짤 확률이 높습니다. 이를 원천 차단합니다.
* **무상태(Stateless) 서버 지향**: 세션 기반 방식 대신 로드밸런싱 및 분산 환경에 유리한 JWT 구조를 표준으로 채택합니다.

## 2. JWT 인증 표준 아키텍처 (보안 철칙)
1. **Access Token과 Refresh Token 분리**
2. **토큰 저장 위치 분리 (핵심)**:
   * Access Token: 프론트엔드의 메모리(상태 변수 등)에만 보관.
   * Refresh Token: 프론트엔드의 LocalStorage 저장을 엄격히 금지. 반드시 서버에서 `Secure, HttpOnly, SameSite=Strict` 옵션을 적용한 쿠키로 발급하여 XSS 취약점을 방어.
3. **검증 및 로그아웃**: 
   * 모든 Protected Route 호출 시 토큰 검증 로직 필수 적용.
   * 로그아웃 시 서버 측에서 쿠키 완전 만료 처리(Set-Cookie로 만료일 과거로 설정).

## 3. 시스템 편입: VibeCoding 프롬프트 템플릿 (`jwt_auth_rule.md`)
이 규칙을 VibeCoding용 시스템 프롬프트에 주입하여, AI가 코드를 생성할 때 보안 원칙을 강제하도록 합니다.

```markdown
# VibeCoding JWT Auth Security Rule
When implementing authentication, you MUST follow these security rules:
1. NEVER store JWT tokens (Access or Refresh) in LocalStorage or SessionStorage.
2. The server MUST issue the Refresh Token as an `HttpOnly`, `Secure`, `SameSite=Strict` cookie.
3. The frontend MUST store the Access Token only in memory (e.g., React state) and use it in the Authorization header.
4. Implement a `/refresh` endpoint to issue a new Access Token using the HttpOnly Refresh Token cookie.
5. Implement a `/logout` endpoint that clears the HttpOnly Refresh Token cookie.
```

## 4. 백엔드 구현 스니펫 가이드

### Option A: Python (FastAPI)
```python
from fastapi import APIRouter, Response, Depends, HTTPException
from datetime import timedelta

router = APIRouter()

@router.post("/login")
def login(response: Response):
    # (인증 로직 후 토큰 생성)
    access_token = "..."
    refresh_token = "..."
    
    # HttpOnly 쿠키로 Refresh Token 설정
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,          # HTTPS 필수
        samesite="strict",
        max_age=7 * 24 * 60 * 60  # 7일
    )
    
    # Access Token은 JSON 바디로 반환 (메모리 저장용)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="refresh_token", httponly=True, secure=True, samesite="strict")
    return {"message": "Logged out successfully"}
```

### Option B: Node.js (Express)
```javascript
const express = require('express');
const router = express.Router();

router.post('/login', (req, res) => {
    // (인증 로직 후 토큰 생성)
    const accessToken = "...";
    const refreshToken = "...";

    // HttpOnly 쿠키로 Refresh Token 설정
    res.cookie('refresh_token', refreshToken, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production', // HTTPS 필수
        sameSite: 'Strict',
        maxAge: 7 * 24 * 60 * 60 * 1000 // 7일
    });

    // Access Token은 JSON 바디로 반환 (메모리 저장용)
    res.json({ accessToken });
});

router.post('/logout', (req, res) => {
    res.clearCookie('refresh_token', { httpOnly: true, secure: true, sameSite: 'Strict' });
    res.json({ message: 'Logged out successfully' });
});
```
