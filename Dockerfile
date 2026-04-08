# Slim 버전을 사용하여 이미지 용량 최소화
FROM python:3.10-slim

# Python 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Hugging Face 모델 캐시 디렉터리 지정
ENV HF_HOME=/app/.cache/huggingface

# 작업 디렉터리 설정
WORKDIR /app

# 시스템 의존성 패키지 설치
# 빌드에 필요한 최소한의 패키지만 설치 후 apt 캐시 삭제로 이미지 크기 최적화
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 의존성 목록 복사 및 패키지 설치
# --no-cache-dir 옵션으로 pip 캐시를 제외하여 용량 최적화
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# [최적화 핵심] Docker Build 과정에서 AI 모델을 미리 다운로드!
# 서버가 켜질 때마다 1GB가 넘는 모델을 새로 다운로드하는 것을 방지합니다.
#RUN python -c "from transformers import pipeline; pipeline('summarization', model='sshleifer/distilbart-cnn-12-6')"

# 보안을 위해 컨테이너 내부에서 root가 아닌 생성된 유저 사용
RUN useradd -m appuser

# 애플리케이션 코드 복사
COPY app/ app/

# 생성한 유저에게 폴더 권한 부여 (모델 캐시 폴더 포함 접근 권한)
RUN chown -R appuser:appuser /app

# root -> appuser로 계정 전환
USER appuser

# 포트 노출
EXPOSE 8000

# 컨테이너 실행 명령어
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
