# Bug Fix & Enhancement: Multi-Provider LLM UI Stability

현재 Settings 페이지에서 발생하고 있는 UI 반응성 문제와 조건부 렌더링 오류를 해결하고, 모든 공급자에게 동일한 모델 선택 경험을 제공합니다.

## User Review Required

> [!NOTE]
> **반응형 바인딩**: NiceGUI의 `bind_value`, `bind_options`를 전면 도입하여 수동 갱신(`ui.update`) 없이 상태가 UI에 즉시 반영되도록 개선합니다.
> **모델 목록 초기화**: 공급자가 변경될 때 이전 모델 목록이 남아있지 않도록 즉시 초기화 로직을 추가합니다.

## Current Issues & Solutions

### 1. 모델 목록 표시 오류 (Ollama 등)
- **증상**: "Found 9 models" 알림은 뜨지만 드롭다운 메뉴가 비어있음.
- **원인**: NiceGUI `ui.select`의 `options` 속성을 수동으로 바꾼 후 UI 갱신이 누락되었거나, 비동기 호출 시 객체 참조가 어긋남.
- **해결**: `bind_options`를 사용하여 `state['available_models']` 배열과 드롭다운을 동기화합니다.

### 2. 조건부 입력창 상시 노출 오류
- **증상**: Gemini/OpenAI 선택 시에도 Base URL이 보임.
- **원인**: `@ui.refreshable` 내부의 조건문 로직이 이전 상태를 완전히 초기화하지 못함.
- **해결**: 공급자별로 명확한 `with ui.column().bind_visibility_from(...)` 구조를 사용하여 레이아웃 수준에서 가시성을 제어합니다.

### 3. 전역 모델 선택 기능 보장
- **증상**: 일부 공급자에서 모델 선택이 원활하지 않음.
- **해결**: 모든 공급자 클라이언트(Gemini, Ollama 등)의 `list_models()` 메서드를 표준화하고, 데이터 로드 성공 시 즉시 선택 가능하도록 보장합니다.

## Proposed Changes

### 1. Presentation Layer (UI Refactoring)

#### [MODIFY] [settings_page.py](file:///d:/Developing%20works/Local%20Arch-Copilot/arch_copilot/presentation/nicegui_app/pages/settings_page.py)
- **상태 관리 객체화**: 단순 `dict` 대신 `AppState`와 유사한 반응형 클래스 혹은 명확한 바인딩 구조 사용.
- **가시성 바인딩**: `ui.input().bind_visibility_from(state, 'provider', backward=lambda p: p in [...])` 사용.
- **드롭다운 바인딩**: 
  - `model_dropdown.bind_options(state, 'available_models')`
  - `model_dropdown.bind_value(state, 'model')`

### 2. Infrastructure Layer (Client Cleanup)

#### [MODIFY] [gemini_client.py](file:///d:/Developing%20works/Local%20Arch-Copilot/arch_copilot/infrastructure/ai_client/gemini_client.py)
- `list_models()`의 예외 처리를 강화하고, 빈 리스트 대신 기본 모델명을 포함한 결과를 반환하여 UI 먹통 방지.

#### [MODIFY] [ollama_client.py](file:///d:/Developing%20works/Local%20Arch-Copilot/arch_copilot/infrastructure/ai_client/ollama_client.py)
- URL 끝에 `/v1`이 붙어있을 경우 자동으로 정규화하여 API 호출 실패 방지.

## Verification Plan

### Manual Verification
1.  **Ollama 선택** -> 'Base URL'만 나타나는지 확인.
2.  **Refresh** 클릭 -> 드롭다운에 실제 모델 목록이 나타나고 선택 가능한지 확인.
3.  **Gemini 선택** -> 'Base URL'은 **즉시 사라지고** 'API Key' 필드만 나타나는지 확인.
4.  **Save** 후 대시보드에서 분석 수행하여 선택한 모델이 실제 로그에 찍히는지 확인.
