# Python 3.12 기반 이미지 사용
FROM python:3.12

# 작업 디렉토리 설정
WORKDIR /app

# 소스 코드 복사
COPY . /app

# .env 파일도 복사 (환경변수 로딩을 위해)
COPY .env /app/.env

# service_account.json 파일도 복사 (Vision API 인증용)
COPY service_account.json /app/service_account.json

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 포트 노출
EXPOSE 8000

# 앱 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
