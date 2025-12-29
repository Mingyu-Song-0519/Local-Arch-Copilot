# Dockerfile for Local Arch-Copilot

# 빌드 및 실행을 위한 베이스 이미지 (Python 3.12)
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 프로젝트 파일 복사
COPY . /app

# Python 의존성 설치
RUN pip install --no-cache-dir -e .

# NiceGUI 포트 노출
EXPOSE 8080

# 애플리케이션 실행
CMD ["python", "arch_copilot/main.py"]
