# Local Arch-Copilot

🔍 Python 프로젝트의 Clean Architecture 준수 여부를 분석하는 로컬 AI 기반 도구

## ✨ Features

- 🤖 **GPT-OSS-20B 기반 아키텍처 분석** - 16GB VRAM에서 40-50 TPS로 동작
- 🔍 **0.1초 이내 초고속 프로젝트 스캔** - Python AST 기반
- 📊 **의존성 그래프 시각화** - NetworkX + Mermaid
- 🎯 **Clean Architecture 위반 자동 탐지** - 4계층 구조 검증
- 🔄 **순환 참조 탐지** - 자동 분석 및 리포트

## 📋 Requirements

- Python 3.12+
- NVIDIA RTX 5070 Ti (16GB VRAM)
- WSL2 Ubuntu 24.04 LTS

## 🚀 Quick Start

```bash
# 가상환경 생성
python -m venv .venv
source .venv/bin/activate  # Linux/WSL
# .venv\Scripts\activate  # Windows

# 의존성 설치
pip install -e ".[dev]"

# 환경 설정
cp .env.example .env

# 애플리케이션 실행
python -m arch_copilot.main
```

## 🏗️ Architecture

Clean Architecture 4계층 구조:

```
arch_copilot/
├── domain/           # 비즈니스 로직 (외부 의존성 0)
├── application/      # Use Cases
├── infrastructure/   # 구체적 구현 (AST, Graph, AI Client)
└── presentation/     # NiceGUI UI
```

## 📖 Documentation

- [설정 가이드](docs/setup/configuration.md)
- [아키텍처 문서](docs/architecture/domain-model.md)
- [사용자 가이드](docs/guides/user-guide.md)

## 🧪 Testing

```bash
# 전체 테스트
pytest tests/ -v --cov=arch_copilot

# 단위 테스트만
pytest tests/unit/ -v

# 통합 테스트만
pytest tests/integration/ -v
```

## 📄 License

MIT License
