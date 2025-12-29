# AI Infrastructure Setup Guide (GPT-OSS-20B)

이 문서는 Local Arch-Copilot의 핵심 엔진인 GPT-OSS-20B 모델을 로컬(WSL2) 환경에서 구동하기 위한 설치 절차를 설명합니다.

## 📋 요구 사항
- Windows 11
- NVIDIA RTX 5070 Ti (16GB VRAM) 이상
- NVIDIA Driver 570.xx+
- WSL2 (Ubuntu 24.04 권장)

## 🛠️ 단계별 설치 가이드

### 1. WSL2 Ubuntu 설정
Windows Terminal에서 다음 명령어를 실행합니다:
```bash
wsl --install -d Ubuntu-24.04
```

### 2. CUDA Toolkit 설치 (WSL2 내부)
WSL2 터미널 접속 후:
```bash
wget https://developer.download.nvidia.com/compute/cuda/12.8.0/local_installers/cuda_12.8.0_570.86.10_linux.run
sudo sh cuda_12.8.0_570.86.10_linux.run
```

### 3. Python 가상환경 및 vLLM 설치
```bash
conda create -n arch-copilot python=3.12 -y
conda activate arch-copilot
pip install vllm>=0.4.0
```

### 4. 모델 다운로드 및 실행
`scripts/start_vllm_server.sh`를 실행합니다. 모델은 처음 실행 시 자동으로 HuggingFace에서 다운로드됩니다.
```bash
chmod +x scripts/start_vllm_server.sh
./scripts/start_vllm_server.sh
```

### 5. Ollama 연동 (Optional for API Proxy)
Ollama를 다운로드하고 vLLM API를 연동하여 관리할 수 있습니다.

## 🧪 검증 방법
프로젝트 루트에서 다음 테스트를 실행하여 인프라가 정상인지 확인합니다:
```bash
pytest tests/integration/test_vllm_infrastructure.py
```
