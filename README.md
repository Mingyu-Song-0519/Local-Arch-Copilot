# 🔍 Local Arch-Copilot

**"클린 코드를 넘어, 클린 아키텍처로 가는 가장 빠른 길"**

Local Arch-Copilot은 Python 프로젝트의 **Clean Architecture** 준수 여부를 분석하고, 순환 참조를 탐지하며, AI를 통해 리팩토링 가이드를 제공하는 로컬 AI 기반 아키텍처 진단 도구입니다.

---

## 🚀 Key Features

- 🤖 **멀티 공급자 LLM 지원 (Full Stack)**
  - Ollama, Gemini, OpenAI, Anthropic, LMStudio, vLLM 완벽 지원
  - 각 인프라별 전용 클라이언트를 통한 실시간 모델 목록 동기화
- 🔍 **초고속 프로젝트 스캔 & 분석**
  - Python AST(Abstract Syntax Tree) 기반의 비파괴적 정적 분석
  - 4계층(Domain, Application, Infrastructure, Presentation) 규칙 자동 검증
- 📊 **인터랙티브 신경망 시각화**
  - Vis.js 기반의 고성능 그래프 렌더링 (170+ 노드 대응)
  - 아키텍처 위반 의존성(Red Edges) 실시간 강조
- ⚡ **실시간 시스템 헬스 체크**
  - AI 엔진의 연결 상태 및 가동 여부를 대시보드에서 즉시 확인
- 📂 **엔터프라이즈 리포트 생성**
  - AI가 제안하는 리팩토링 가이드를 마크다운 리포트로 즉시 저장

---

## 🧠 Supported AI Engines

| 공급자 | 유형 | 특징 |
| :--- | :--- | :--- |
| **Ollama** | Local | 가장 대중적인 로컬 모델 서빙 도구 |
| **Gemini** | Cloud | Google의 고성능 멀티모달 AI (API Key 필요) |
| **OpenAI** | Cloud | GPT-4o 등 업계 표준 AI (API Key 필요) |
| **Anthropic** | Cloud | Claude 3.5 Sonnet 등 정교한 추론 AI (API Key 필요) |
| **LMStudio** | Local | GUI 기반의 로컬 모델 테스트 환경 |
| **vLLM** | Local/Server | 엔터프라이즈급 고성능 추론 엔진 |

---

## 🛠️ Quick Start

### 1. 환경 구성
Python 3.12 이상의 환경이 필요합니다.

```bash
# 저장소 복제
git clone https://github.com/Mingyu-Song-0519/Local-Arch-Copilot.git
cd Local-Arch-Copilot

# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Linux/WSL
# .venv\Scripts\activate  # Windows

# 필수 패키지 설치
pip install -e "."
pip install google-generativeai anthropic openai  # 클라우드 AI 사용 시
```

### 2. 실행
```bash
python arch_copilot/main.py
```
실행 후 브라우저에서 `http://localhost:8080`에 접속하세요.

---

## ⚙️ Configuration

1. 대시보드 상단의 **SETTINGS** 버튼을 클릭합니다.
2. 사용하고자 하는 **API Provider**를 선택합니다.
3. 로컬 공급자의 경우 **Base URL**을, 클라우드 공급자의 경우 **API Key**를 입력합니다.
4. **VALIDATE** 또는 **Refresh** 버튼을 눌러 모델 목록을 가져옵니다.
5. 분석에 사용할 모델을 선택하고 **SAVE CHANGES**를 누르면 즉시 앱에 반영됩니다.

---

## 🏗️ Architecture

이 프로젝트는 스스로 **Clean Architecture**를 준수하여 설계되었습니다.

```
arch_copilot/
├── domain/           # 핵심 비즈니스 로직 및 인터페이스
├── application/      # 유스케이스 (분석 실행, 결과 집계)
├── infrastructure/   # 세부 구현 (AST Parser, AI Clients, Config)
└── presentation/     # UI 레이어 (NiceGUI, 동적 컴포넌트)
```

---

## 📄 License

이 프로젝트는 MIT License를 따릅니다.
