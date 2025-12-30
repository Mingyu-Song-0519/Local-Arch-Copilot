# Multi-Provider LLM & Dynamic Model Configuration

사용자가 Settings 페이지에서 직접 LLM 공급자(Ollama, LMStudio, Gemini 등)를 선택하고, 로컬 환경의 경우 설치된 모델 목록을 실시간으로 가져와 선택할 수 있는 기능을 구현합니다.

## User Review Required

> [!IMPORTANT]
> **API Key 보안**: 입력된 API Key는 로컬 `.env` 파일에 저장됩니다. 공용 PC에서 사용 시 주의가 필요합니다.
> **인터넷 연결**: Gemini나 OpenAI 등 외부 공급자 선택 시 인터넷 연결이 필수적입니다.

## Proposed Changes

### 1. Domain & Configuration Layer

계층화된 설정을 지원하고 변경 사항을 영구 저장할 수 있도록 설정을 확장합니다.

#### [MODIFY] [i_config.py](file:///d:/Developing%20works/Local%20Arch-Copilot/arch_copilot/domain/config/i_config.py)
- 다음 속성 추가: `llm_provider`, `llm_base_url`, `llm_api_key`, `llm_model`.
- 설정 업데이트 및 저장을 위한 `update_settings(settings_dict)` 메서드 정의.

#### [MODIFY] [config.py](file:///d:/Developing%20works/Local%20Arch-Copilot/arch_copilot/infrastructure/config/config.py)
- Pydantic 모델에 새로운 LLM 필드 추가.
- `.env` 파일에 설정을 다시 쓰는 `persist()` 로직 재구현.

---

### 2. Infrastructure Layer (LLM Clients)

다양한 API 공급자에 대응하기 위해 클라이언트 구조를 유연하게 변경합니다.

#### [NEW] `LLMClientFactory`
- 설정된 `provider`에 따라 적절한 클라이언트 객체를 반환합니다.

#### [MODIFY] `VLLMClient`
- 범용 OpenAI 호환 클라이언트로 개량하여 Ollama, LMStudio, OpenAI 본사를 모두 처리할 수 있게 합니다.

#### [NEW] `GeminiClient`
- Google Gemini API 전용 클라이언트를 추가합니다 (필요 시).

---

### 3. Presentation Layer (NiceGUI Settings Page)

이미지에서 제시된 것과 유사한 동적 설정을 구현합니다.

#### [MODIFY] [settings_page.py](file:///d:/Developing%20works/Local%20Arch-Copilot/arch_copilot/presentation/nicegui_app/pages/settings_page.py)
- **공급자 선택 드롭다운**: (Ollama, LMStudio, Gemini, OpenAI, Anthropic 등).
- **조건부 입력창**:
  - Ollama/LMStudio 선택 시: **Base URL** 입력창 노출.
  - Gemini/OpenAI 선택 시: **API Key** 입력창 노출.
- **모델 동적 로드**:
  - "REFRESH MODELS" 버튼 추가.
  - 클릭 시 선택된 URL 또는 API를 통해 실제 사용 가능한 모델 목록을 비동기로 로드.
  - 로드된 결과를 'Model' 드롭다운에 반영.
- **저장 시스템**: 변경 즉시 `.env`에 반영하고 애플리케이션 상태를 갱신.

---

### 4. Application Layer

#### [MODIFY] [analyze_project.py](file:///d:/Developing%20works/Local%20Arch-Copilot/arch_copilot/application/use_cases/analyze_project.py)
- `IAIAnalyzer`가 `VLLMAnalyzer` 고정 방식에서 벗어나, 현재 설정된 클라이언트를 주입받아 작동하도록 수정.

## Verification Plan

### Automated Tests
- 설정 저장 및 로드 로직 단위 테스트 수행.
- Ollama/LMStudio 모킹(Mock) 서버를 통해 모델 목록 가져오기 기능 검증.

### Manual Verification
1.  **Settings** 페이지 진입.
2.  **API Provider**를 'Ollama'로 변경 -> Base URL 입력창이 정상적으로 나타나는지 확인.
3.  **Base URL** 입력 후 (또는 기본값 사용) **REFRESH MODELS** 클릭 -> 로컬 Ollama에 설치된 실제 모델들(예: `mistral-24b`, `llama3` 등)이 드롭다운에 표시되는지 확인.
4.  다른 모델 선택 후 **Dashboard**에서 분석 수행 -> 바뀐 모델로 분석이 진행되는지 확인.
5.  **Gemini** 선택 시 API Key 창이 나타나고 모델 목록이 Gemini 라인업으로 바뀌는지 확인.
