# 1. 경량 Python 3.11 슬림 이미지 사용
FROM python:3.11-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 시스템 의존성 및 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 4. 파이썬 패키지 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 백엔드 전체 소스코드 복사
COPY . .

# 6. 포트 노출 (FastAPI 기본 8000)
EXPOSE 8000

# 7. Uvicorn 프로덕션 서버 실행 (0.0.0.0 바인딩)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
