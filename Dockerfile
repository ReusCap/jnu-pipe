# 로컬이 3.13이라. 이전 버전이면 거기에 맞춰서 수정 (3.11이 가장 안정적이라고 함)
FROM python:3.13-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN  pip install --no-cache-dir -r requirements.txt

# 소스 복사
COPY . .

# Render에서 PORT 환경 변수를 제공하며, 로컬 기본값은 10000으로 설정
ENV PORT=10000
EXPOSE 10000

# 실행 명령
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]