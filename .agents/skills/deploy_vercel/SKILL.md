---
name: deploy_vercel
description: 안티가 로컬에서 작성한 웹앱 프로젝트 코드를 GitHub에 푸시하고, Vercel을 통해 클라우드 환경으로 원클릭 원격 배포하는 스킬.
---

# Deploy Vercel Skill

## 용도
- 안티가 작성한 프론트엔드/풀스택 코드를 로컬이 아닌 외부 브라우저(모바일 등)에서 즉시 확인할 수 있도록 클라우드 배포가 필요할 때 사용.

## 작동 절차
1. 코딩이 완료되면 안티는 사용자에게 배포 승인을 요청합니다.
2. 승인이 떨어지면, 동봉된 파이썬 스크립트(`scripts\deploy.py`)를 실행합니다.
3. 스크립트가 알아서 로컬 Git 커밋, GitHub 저장소 Push, 그리고 Vercel CLI를 통한 Production 배포를 순차적으로 자동 실행합니다.
4. 산출된 Live URL을 사용자에게 보고합니다.
