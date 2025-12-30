# Implementation Plan: Multi-Provider LLM UI Stability Bug Fix

**Status**: 🔄 Ready to Implement
**Created**: 2025-12-30
**Last Updated**: 2025-12-30
**Estimated Completion**: 2-3 phases, 3-5 hours

---

**⚠️ CRITICAL INSTRUCTIONS**: After completing each phase:
1. ✅ Check off completed task checkboxes
2. 🧪 Run all quality gate validation commands
3. ⚠️ Verify ALL quality gate items pass
4. 📅 Update "Last Updated" date above
5. 📝 Document learnings in Notes section
6. ➡️ Only then proceed to next phase

⛔ **DO NOT skip quality gates or proceed with failing checks**

---

## 📋 Overview

### Feature Description
Settings 페이지에서 발생하는 NiceGUI 반응성 문제와 조건부 렌더링 오류를 해결하여 모든 LLM 공급자에게 일관된 사용자 경험을 제공합니다.

### Current Issues

1. **모델 목록 표시 오류** (Critical)
   - 증상: "Found 9 models" 알림은 뜨지만 드롭다운 메뉴가 비어있음
   - 원인: `ui.select.options` 수동 변경 후 UI 갱신 누락, 비동기 호출 시 객체 참조 불일치
   - 영향: Ollama, LMStudio 사용자가 모델 선택 불가

2. **조건부 입력창 중복 노출** (High)
   - 증상: Gemini/OpenAI 선택 시에도 Base URL 입력창이 함께 표시됨
   - 원인: `@ui.refreshable` 내부 조건문이 이전 렌더링 상태를 완전히 제거하지 못함
   - 영향: 사용자 혼란, 잘못된 설정 입력 가능성

3. **Provider 변경 시 모델 목록 미초기화** (Medium)
   - 증상: vLLM → Ollama 전환 시 이전 모델 목록이 남아있음
   - 원인: `state['available_models']` 배열이 Provider 변경 시 초기화되지 않음
   - 영향: 잘못된 모델 선택 가능성

### Success Criteria
- [ ] Ollama 선택 시 Base URL 입력창만 표시, API Key 입력창 숨김
- [ ] Gemini 선택 시 API Key 입력창만 표시, Base URL 입력창 숨김
- [ ] REFRESH MODELS 버튼 클릭 시 드롭다운에 실제 모델 목록 표시
- [ ] 모델 선택 가능 (드롭다운 클릭 시 옵션 표시)
- [ ] Provider 변경 시 이전 모델 목록 즉시 초기화
- [ ] 모든 UI 변경사항이 수동 갱신 없이 자동 반영 (Reactive Binding)

### User Impact
- **안정성 향상**: UI 반응성 문제 해결로 설정 변경 과정 원활
- **사용성 개선**: 조건부 입력창 정확한 표시로 사용자 혼란 제거
- **신뢰성 강화**: 모델 목록 정확한 표시로 올바른 모델 선택 보장

---

## 🏗️ Architecture Decisions

| Decision | Rationale | Trade-offs |
|----------|-----------|------------|
| **NiceGUI Reactive Binding 도입** | `bind_value()`, `bind_options()` 사용으로 수동 갱신 제거 | NiceGUI 9.0+ 버전 필요, 기존 코드 대폭 변경 |
| **단일 Reactive State 객체 사용** | 일반 dict 대신 명시적 바인딩 구조로 상태 변경 추적 | 초기 설정 복잡도 증가 |
| **bind_visibility_from으로 조건부 렌더링** | `@ui.refreshable` 대신 선언적 가시성 제어 | 복잡한 조건 로직 구현 어려움 |
| **Provider 변경 시 즉시 초기화** | 모델 목록을 빈 배열로 리셋 후 REFRESH 유도 | 사용자가 수동으로 REFRESH 클릭 필요 |

---

## 🧪 Test Strategy

### Testing Approach
Bug Fix 특성상 수동 테스트 중심, 회귀 방지를 위한 자동화 테스트 추가

### Test Pyramid for This Fix
| Test Type | Coverage Target | Purpose |
|-----------|-----------------|---------|
| **Manual Tests** | Critical paths | UI 반응성 및 조건부 렌더링 검증 |
| **Integration Tests** | Key scenarios | Settings → Provider 변경 → 모델 로드 전체 흐름 |
| **Unit Tests** | Helper functions | 상태 초기화, 모델 목록 파싱 로직 |

### Test File Organization
```
tests/
├── manual/
│   └── MANUAL_TEST_CHECKLIST.md (NEW)
├── integration/
│   └── test_settings_ui_reactivity.py (NEW)
└── unit/
    ├── infrastructure/
    │   ├── test_ollama_client_url_normalization.py (NEW)
    │   └── test_gemini_client_error_handling.py (NEW)
```

---

## 🚀 Implementation Phases

### Phase 1: Presentation Layer - Reactive Binding Refactoring
**Goal**: NiceGUI Reactive Binding 적용으로 UI 반응성 문제 해결
**Estimated Time**: 1.5-2 hours
**Status**: ⏳ Pending

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 1.1**: Settings UI 반응성 테스트
  - File(s): `tests/manual/MANUAL_TEST_CHECKLIST.md` (NEW)
  - Expected: 수동 테스트 체크리스트 생성
  - Details: 테스트 시나리오:
    ```markdown
    ## Manual Test Checklist - Settings UI Reactivity

    ### Test 1: Provider 선택 시 조건부 입력창 표시
    - [ ] **초기 상태**: vLLM 선택됨, Base URL 표시됨
    - [ ] **Ollama 선택**: Base URL 유지, API Key 숨김 확인
    - [ ] **Gemini 선택**: Base URL 즉시 사라짐, API Key 표시 확인
    - [ ] **다시 Ollama 선택**: API Key 즉시 사라짐, Base URL 표시 확인

    ### Test 2: 모델 목록 Refresh 동작
    - [ ] **Ollama 선택 후 REFRESH**: 드롭다운에 모델 목록 표시
    - [ ] **드롭다운 클릭**: 옵션 리스트 정상 표시
    - [ ] **모델 선택**: 선택한 모델명이 드롭다운에 표시

    ### Test 3: Provider 변경 시 모델 목록 초기화
    - [ ] **Ollama 모델 로드 후 Gemini 선택**: 모델 목록 초기화 확인
    - [ ] **경고 메시지**: "Provider changed. Please refresh models." 표시
    ```

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 1.2**: Reactive State 객체 구현
  - File(s): `arch_copilot/presentation/nicegui_app/pages/settings_page.py`
  - Goal: NiceGUI Reactive Binding 지원 상태 객체
  - Details:
    ```python
    from nicegui import ui
    from typing import List

    class SettingsState:
        """Reactive state for Settings page"""
        def __init__(self, config: IConfig):
            # Provider 설정
            self.provider = config.llm_provider

            # URL/API Key 설정
            self.base_url = config.llm_base_url or "http://localhost:11434"
            self.api_key = config.llm_api_key.get_secret_value() if config.llm_api_key else ""

            # 모델 설정
            self.model = config.llm_model
            self.available_models: List[str] = []  # 빈 배열로 시작

        def reset_model_list(self):
            """Provider 변경 시 모델 목록 초기화"""
            self.available_models = []
            self.model = ""  # 빈 문자열로 리셋 (드롭다운 선택 해제)
    ```

- [ ] **Task 1.3**: Provider 선택 드롭다운 Reactive Binding 적용
  - File(s): `arch_copilot/presentation/nicegui_app/pages/settings_page.py`
  - Goal: Provider 변경 시 자동 UI 갱신 및 모델 리스트 초기화
  - Details:
    ```python
    def settings_page():
        container = get_container()
        config = container.resolve(IConfig)

        # Reactive State 객체
        state = SettingsState(config)

        def on_provider_change(new_provider: str):
            """Provider 변경 시 콜백"""
            state.provider = new_provider
            state.reset_model_list()
            ui.notify(f"Switched to {new_provider}. Please refresh models.", type='info')

        with base_layout("System Settings"):
            # ... UI 레이블 ...

            with ui.card().classes('w-full p-8 bg-zinc-900/50 border border-zinc-800 rounded-3xl mt-4'):
                with ui.column().classes('w-full gap-6'):
                    # 1. API Provider (Reactive Binding)
                    ui.label('API Provider').classes('text-sm text-gray-500 mb-1')
                    provider_select = ui.select(
                        options=['vllm', 'ollama', 'lmstudio', 'gemini', 'openai', 'anthropic'],
                        on_change=lambda e: on_provider_change(e.value)
                    ).bind_value(state, 'provider') \
                     .classes('w-full').props('dark outlined color=primary')
    ```

- [ ] **Task 1.4**: 조건부 입력창 Reactive Visibility Binding 적용
  - File(s): `arch_copilot/presentation/nicegui_app/pages/settings_page.py`
  - Goal: `@ui.refreshable` 제거, `bind_visibility_from()` 사용
  - Details:
    ```python
    # 2. Dynamic Inputs (Reactive Visibility)

    # Base URL 입력 (로컬 Provider만 표시)
    with ui.column().classes('w-full') as base_url_container:
        ui.label('Base URL').classes('text-sm text-gray-500 mb-1')
        ui.input(
            placeholder='http://localhost:11434',
        ).bind_value(state, 'base_url') \
         .classes('w-full').props('dark outlined color=primary')

    # Provider가 로컬일 때만 Base URL 컨테이너 표시
    base_url_container.bind_visibility_from(
        state, 'provider',
        backward=lambda p: p in ['vllm', 'ollama', 'lmstudio']
    )

    # API Key 입력 (클라우드 Provider만 표시)
    with ui.column().classes('w-full') as api_key_container:
        ui.label('API Key').classes('text-sm text-gray-500 mb-1')
        ui.input(
            password=True,
            password_toggle_button=True
        ).bind_value(state, 'api_key') \
         .classes('w-full').props('dark outlined color=primary')
        ui.label('⚠️ API Key는 .env 파일에 평문으로 저장됩니다.').classes('text-xs text-yellow-600')

    # Provider가 클라우드일 때만 API Key 컨테이너 표시
    api_key_container.bind_visibility_from(
        state, 'provider',
        backward=lambda p: p in ['gemini', 'openai', 'anthropic']
    )
    ```

- [ ] **Task 1.5**: 모델 드롭다운 Reactive Binding 적용
  - File(s): `arch_copilot/presentation/nicegui_app/pages/settings_page.py`
  - Goal: `state.available_models` 변경 시 자동 UI 갱신
  - Details:
    ```python
    # 3. Model Selection (Reactive Binding)
    ui.label('Model').classes('text-sm text-gray-500 mb-1')
    with ui.row().classes('w-full gap-4 items-center'):
        model_dropdown = ui.select(
            # options 파라미터 제거 (bind_options로 대체)
        ).bind_value(state, 'model') \
         .bind_options(state, 'available_models') \
         .classes('flex-grow').props('dark outlined color=primary')

        ui.button(icon='refresh', on_click=fetch_models) \
            .props('outline round color=primary') \
            .tooltip('Refresh installed models')
    ```

- [ ] **Task 1.6**: fetch_models() 함수 수정
  - File(s): `arch_copilot/presentation/nicegui_app/pages/settings_page.py`
  - Goal: Reactive State 직접 수정으로 자동 UI 갱신
  - Details:
    ```python
    async def fetch_models():
        """선택된 공급자/URL 전용 모델 목록 가져오기"""
        temp_config = type('TempConfig', (), {
            'llm_provider': state.provider,
            'llm_base_url': state.base_url,
            'llm_api_key': SecretStr(state.api_key) if state.api_key else None,
            'llm_model': state.model,
            'vllm_base_url': config.vllm_base_url
        })

        try:
            client = LLMClientFactory.create(temp_config)
            ui.notify(f"Fetching models from {state.provider}...", type='info')
            models = await client.list_models()

            if models:
                # Reactive State 직접 수정 → 자동 UI 갱신
                state.available_models = models

                # 현재 선택된 모델이 목록에 없으면 첫 번째 모델 선택
                if state.model not in models:
                    state.model = models[0]

                ui.notify(f"Found {len(models)} models!", type='positive')
            else:
                ui.notify("No models found. Check your connection/URL.", type='warning')
                state.available_models = []

        except Exception as e:
            ui.notify(f"Failed to load models: {str(e)}", type='negative')
            state.available_models = []
    ```

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 1.7**: 수동 UI 갱신 코드 제거
  - Files: `settings_page.py`
  - Goal: `model_dropdown.options = ...`, `model_dropdown.value = ...` 등 수동 갱신 코드 삭제
  - Checklist:
    - [ ] `model_dropdown.options` 직접 할당 제거
    - [ ] `model_dropdown.value` 직접 할당 제거
    - [ ] `model_dropdown.update()` 호출 제거
    - [ ] `render_inputs.refresh()` 호출 제거 (더 이상 `@ui.refreshable` 사용 안 함)

- [ ] **Task 1.8**: save_all() 함수 Reactive State 적용
  - Files: `settings_page.py`
  - Goal: state 객체 속성 직접 참조
  - Details:
    ```python
    def save_all():
        """설정 영구 저장 및 반영"""
        updates = {
            'llm_provider': state.provider,
            'llm_base_url': state.base_url,
            'llm_api_key': SecretStr(state.api_key) if state.api_key else None,
            'llm_model': state.model
        }
        config.update_settings(updates)
        ui.notify("Settings saved to .env and applied!", type='positive', icon='cloud_done')
    ```

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed to Phase 2 until ALL checks pass**

**Manual Testing**:
- [ ] **Provider 변경**: Ollama ↔ Gemini 전환 시 입력창 즉시 변경
- [ ] **조건부 입력창**: 한 번에 하나의 입력창만 표시 (Base URL 또는 API Key)
- [ ] **모델 목록 초기화**: Provider 변경 시 드롭다운 비어있음 확인
- [ ] **REFRESH 동작**: 모델 목록 정상 표시, 드롭다운 클릭 가능

**Code Quality**:
- [ ] **Linting**: `ruff check arch_copilot/presentation/nicegui_app/pages/`
- [ ] **Type Safety**: `mypy arch_copilot/presentation/nicegui_app/pages/settings_page.py`

**Functionality**:
- [ ] UI 반응성 즉시 동작 (수동 갱신 없이)
- [ ] 이전 상태 잔존 없음 (Provider 변경 시 깨끗한 초기화)

**Validation Commands**:
```bash
# 코드 품질 검증
ruff check arch_copilot/presentation/nicegui_app/pages/settings_page.py
mypy arch_copilot/presentation/nicegui_app/pages/settings_page.py --strict

# 수동 테스트 (애플리케이션 실행)
python -m arch_copilot.main
# Settings 페이지 접속 후 Manual Test Checklist 수행
```

**Manual Test Checklist**:
- [ ] Ollama 선택 시 Base URL만 표시
- [ ] Gemini 선택 시 API Key만 표시
- [ ] REFRESH MODELS 클릭 시 드롭다운에 모델 목록 표시
- [ ] 모델 선택 가능 (드롭다운 정상 동작)
- [ ] Provider 변경 시 모델 목록 즉시 초기화

---

### Phase 2: Infrastructure Layer - Client Error Handling Enhancement
**Goal**: Ollama/Gemini 클라이언트 예외 처리 강화 및 URL 정규화
**Estimated Time**: 1-1.5 hours
**Status**: ⏳ Pending
**Dependencies**: Phase 1 완료

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 2.1**: OllamaClient URL 정규화 테스트
  - File(s): `tests/unit/infrastructure/test_ollama_client_url_normalization.py` (NEW)
  - Expected: URL 정규화 로직 없어서 실패
  - Details: 테스트 케이스:
    ```python
    import pytest
    from arch_copilot.infrastructure.ai_client.ollama_client import OllamaClient

    def test_ollama_client_should_normalize_url_with_v1_suffix():
        """URL 끝에 /v1이 있을 경우 자동 정규화"""
        client = OllamaClient(base_url="http://localhost:11434/v1")
        assert client.base_url == "http://localhost:11434"

    def test_ollama_client_should_normalize_url_with_trailing_slash():
        """URL 끝에 슬래시가 있을 경우 제거"""
        client = OllamaClient(base_url="http://localhost:11434/")
        assert client.base_url == "http://localhost:11434"

    def test_ollama_client_should_handle_url_without_v1():
        """URL에 /v1이 없을 경우 그대로 유지"""
        client = OllamaClient(base_url="http://localhost:11434")
        assert client.base_url == "http://localhost:11434"

    @pytest.mark.asyncio
    async def test_ollama_client_should_append_v1_to_api_calls():
        """API 호출 시 /v1 자동 추가"""
        client = OllamaClient(base_url="http://localhost:11434")
        # Mock httpx 사용하여 실제 URL 확인
        # ... (생략, 실제 구현 시 httpx.AsyncClient를 mock)
    ```

- [ ] **Test 2.2**: GeminiClient 예외 처리 테스트
  - File(s): `tests/unit/infrastructure/test_gemini_client_error_handling.py` (NEW)
  - Expected: 예외 처리 강화 로직 없어서 실패
  - Details: 테스트 케이스:
    ```python
    import pytest
    from unittest.mock import AsyncMock, patch, MagicMock
    from arch_copilot.infrastructure.ai_client.gemini_client import GeminiClient

    @pytest.mark.asyncio
    async def test_gemini_client_should_return_default_models_on_api_failure():
        """API 실패 시 빈 리스트 대신 기본 모델 목록 반환"""
        client = GeminiClient(api_key='test-key')

        with patch('google.generativeai.list_models', side_effect=Exception("API Error")):
            models = await client.list_models()
            # 빈 리스트가 아닌 기본 모델 목록 반환
            assert len(models) > 0
            assert 'gemini-1.5-pro' in models or 'gemini-1.5-flash' in models

    @pytest.mark.asyncio
    async def test_gemini_client_should_handle_empty_api_response():
        """API가 빈 리스트 반환 시 기본 모델 제공"""
        client = GeminiClient(api_key='test-key')

        with patch('google.generativeai.list_models', return_value=[]):
            models = await client.list_models()
            assert len(models) > 0  # 기본 모델 목록 제공
    ```

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 2.3**: OllamaClient URL 정규화 로직 개선
  - File(s): `arch_copilot/infrastructure/ai_client/ollama_client.py`
  - Goal: 이미 구현된 URL 정규화 로직 검증 및 개선
  - Details:
    ```python
    class OllamaClient(ILLMClient):
        def __init__(self, base_url: str, model_name: str = "mistral-24b:latest") -> None:
            # URL 정규화: 끝의 슬래시 제거
            self.base_url = base_url.rstrip('/')

            # /v1 경로가 있으면 제거 (API 호출 시 자동 추가)
            if self.base_url.endswith('/v1'):
                self.base_url = self.base_url[:-3].rstrip('/')

            self.model_name = model_name
            self.timeout = httpx.Timeout(300.0, connect=10.0)

        # NOTE: 현재 구현이 이미 정규화되어 있음, 테스트로 검증만 필요
    ```

- [ ] **Task 2.4**: GeminiClient 예외 처리 강화
  - File(s): `arch_copilot/infrastructure/ai_client/gemini_client.py`
  - Goal: API 실패 시 빈 리스트 대신 기본 모델 목록 반환
  - Details:
    ```python
    class GeminiClient(ILLMClient):
        # 기본 모델 목록 (Fallback)
        DEFAULT_MODELS = [
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-pro",
            "gemini-pro-vision"
        ]

        async def list_models(self) -> List[str]:
            """Gemini에서 지원하는 텍스트 생성 가능 모델 목록 조회"""
            def _sync_list():
                try:
                    models = genai.list_models()
                    # generateContent를 지원하는 모델만 추출
                    available = [
                        m.name.replace("models/", "")
                        for m in models
                        if "generateContent" in m.supported_generation_methods
                    ]

                    # API가 빈 리스트 반환 시 기본 모델 제공
                    return available if available else self.DEFAULT_MODELS

                except Exception as e:
                    print(f"Failed to fetch Gemini models: {e}, returning default models")
                    # API 실패 시 기본 모델 목록 반환 (UI 먹통 방지)
                    return self.DEFAULT_MODELS

            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, _sync_list)
    ```

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 2.5**: 에러 로깅 개선
  - Files: `ollama_client.py`, `gemini_client.py`
  - Goal: 예외 발생 시 상세한 로그 출력
  - Checklist:
    - [ ] 연결 실패 시 URL 포함 로그 출력
    - [ ] API 키 오류 시 마스킹된 키 일부 출력 (디버깅 용이)
    - [ ] 타임아웃 발생 시 소요 시간 출력

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed to Phase 3 until ALL checks pass**

**TDD Compliance**:
- [ ] Tests written FIRST and initially failed
- [ ] Implementation makes tests pass
- [ ] Coverage: Client 예외 처리 ≥80%

**Unit Tests**:
- [ ] OllamaClient URL 정규화 테스트 통과
- [ ] GeminiClient 기본 모델 Fallback 테스트 통과

**Functionality**:
- [ ] Ollama URL `/v1` 자동 정규화
- [ ] Gemini API 실패 시 기본 모델 목록 반환

**Validation Commands**:
```bash
pytest tests/unit/infrastructure/test_ollama_client_url_normalization.py -v
pytest tests/unit/infrastructure/test_gemini_client_error_handling.py -v
pytest tests/unit/infrastructure/ --cov=arch_copilot/infrastructure/ai_client
```

---

### Phase 3: Integration Testing & Documentation
**Goal**: 전체 워크플로우 통합 테스트 및 사용자 가이드 작성
**Estimated Time**: 0.5-1 hour
**Status**: ⏳ Pending
**Dependencies**: Phase 1, 2 완료

#### Tasks

**🔴 RED: Write Failing Integration Tests First**
- [ ] **Test 3.1**: Settings UI 통합 테스트
  - File(s): `tests/integration/test_settings_ui_reactivity.py` (NEW)
  - Expected: 통합 테스트 환경 미구축으로 실패
  - Details: 시뮬레이션 테스트 (Headless NiceGUI):
    ```python
    import pytest
    from unittest.mock import AsyncMock, MagicMock
    from arch_copilot.presentation.nicegui_app.pages.settings_page import settings_page

    @pytest.mark.asyncio
    async def test_settings_page_provider_change_should_reset_model_list():
        """Provider 변경 시 모델 목록 초기화 검증"""
        # NiceGUI 테스트 환경 설정 (실제 구현은 복잡할 수 있음, Mock 사용)
        # ...
        pass

    @pytest.mark.asyncio
    async def test_settings_page_refresh_models_should_populate_dropdown():
        """REFRESH MODELS 클릭 시 드롭다운 채우기 검증"""
        # ...
        pass
    ```

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 3.2**: Manual Test Checklist 작성
  - File(s): `tests/manual/MANUAL_TEST_CHECKLIST.md` (NEW)
  - Goal: 수동 테스트 가이드라인 문서화
  - Details:
    ```markdown
    # Manual Test Checklist - Settings UI Stability

    ## Test Environment
    - Python 3.11+
    - NiceGUI 9.0+
    - Ollama 또는 Gemini API Key

    ## Pre-Test Setup
    1. Ollama 서버 실행 (로컬 테스트 시): `ollama serve`
    2. 애플리케이션 실행: `python -m arch_copilot.main`
    3. Settings 페이지 접속

    ## Test Cases

    ### TC1: Provider 선택 시 조건부 입력창 표시
    **Steps**:
    1. Provider 드롭다운에서 "ollama" 선택
    2. Base URL 입력창이 표시되는지 확인
    3. API Key 입력창이 숨겨지는지 확인
    4. Provider 드롭다운에서 "gemini" 선택
    5. API Key 입력창이 표시되는지 확인
    6. Base URL 입력창이 즉시 사라지는지 확인

    **Expected**: 한 번에 하나의 입력창만 표시, 전환 즉시 반영

    ### TC2: 모델 목록 Refresh 동작
    **Steps**:
    1. Provider를 "ollama"로 선택
    2. Base URL에 `http://localhost:11434` 입력
    3. REFRESH MODELS 버튼 클릭
    4. "Fetching models..." 알림 확인
    5. "Found X models" 알림 확인
    6. Model 드롭다운 클릭
    7. 모델 목록이 드롭다운에 표시되는지 확인

    **Expected**: 드롭다운에 실제 모델 목록 표시, 선택 가능

    ### TC3: Provider 변경 시 모델 목록 초기화
    **Steps**:
    1. Ollama 선택 후 모델 목록 로드 (TC2 수행)
    2. Provider를 "gemini"로 변경
    3. Model 드롭다운 확인
    4. "Provider changed. Please refresh models." 알림 확인

    **Expected**: 드롭다운 비어있음, 이전 모델 목록 제거됨

    ### TC4: 설정 저장 및 적용
    **Steps**:
    1. Provider 선택, 모델 선택 완료
    2. SAVE CHANGES 버튼 클릭
    3. "Settings saved to .env" 알림 확인
    4. .env 파일 확인 (LLM_PROVIDER, LLM_MODEL 업데이트 확인)

    **Expected**: 설정이 .env 파일에 정확히 저장됨
    ```

**🔵 REFACTOR: Documentation & Cleanup**
- [ ] **Task 3.3**: Bug Fix 요약 문서 작성
  - Files: `docs/bugfixes/UI_REACTIVITY_FIX_2025-12-30.md` (NEW)
  - Goal: 수정 내용 및 재발 방지 가이드라인
  - Details:
    ```markdown
    # Bug Fix: Multi-Provider LLM UI Stability

    **Date**: 2025-12-30
    **Severity**: High
    **Affected Component**: Settings Page (NiceGUI)

    ## Root Cause
    1. NiceGUI `ui.select.options` 수동 변경 후 UI 갱신 누락
    2. `@ui.refreshable` 조건부 렌더링 시 이전 상태 미제거
    3. Provider 변경 시 모델 목록 초기화 로직 부재

    ## Solution
    1. NiceGUI Reactive Binding (`bind_value`, `bind_options`) 전면 도입
    2. `bind_visibility_from()` 사용으로 조건부 렌더링 개선
    3. Provider 변경 시 `reset_model_list()` 호출로 즉시 초기화

    ## Prevention Guidelines
    - **항상 Reactive Binding 사용**: 수동 UI 갱신 지양
    - **조건부 렌더링은 Visibility Binding 사용**: `@ui.refreshable` 최소화
    - **상태 변경 시 관련 상태 함께 초기화**: Provider 변경 → 모델 리스트 리셋
    ```

- [ ] **Task 3.4**: 코드 주석 정리
  - Files: `settings_page.py`
  - Goal: Reactive Binding 사용 이유 주석 추가
  - Checklist:
    - [ ] `bind_visibility_from()` 사용 이유 설명
    - [ ] `reset_model_list()` 호출 위치 명시
    - [ ] TODO 주석 제거 (완료된 작업)

#### Quality Gate ✋

**⚠️ STOP: Final validation before deployment**

**Manual Tests**:
- [ ] Manual Test Checklist 모든 항목 통과
- [ ] 회귀 테스트 통과 (기존 기능 정상 동작)

**Documentation**:
- [ ] Manual Test Checklist 작성 완료
- [ ] Bug Fix 요약 문서 작성 완료

**Code Quality**:
- [ ] 불필요한 주석 제거
- [ ] TODO 주석 정리
- [ ] 코드 포맷팅 일관성 유지

**Validation Commands**:
```bash
# 전체 테스트 실행
pytest tests/unit/ tests/integration/ -v

# 코드 품질 최종 검증
ruff check arch_copilot/
mypy arch_copilot/ --strict
```

**Final Manual Test**:
- [ ] Ollama 선택 → Base URL 표시 → REFRESH → 모델 선택 → SAVE
- [ ] Gemini 선택 → API Key 표시 → (모델 목록 초기화 확인)
- [ ] 설정 저장 후 .env 파일 확인
- [ ] 애플리케이션 재시작 후 설정 유지 확인

---

## ⚠️ Risk Assessment

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| **NiceGUI Reactive Binding 버그** | Low | High | NiceGUI 9.0+ 버전 사용 확인, 공식 문서 참조 |
| **Ollama 서버 미설치로 테스트 불가** | Medium | Medium | Manual Test Checklist에 Mock 서버 사용 가이드 추가 |
| **Gemini API 제한으로 모델 목록 조회 실패** | Low | Low | 기본 모델 목록 Fallback으로 UI 먹통 방지 |
| **기존 코드와 호환성 문제** | Low | Medium | Phase 1 Quality Gate에서 회귀 테스트 철저히 수행 |

---

## 🔄 Rollback Strategy

### If Phase 1 Fails
- `settings_page.py` 원복 (git checkout)
- Reactive Binding 제거, 기존 dict 기반 상태 관리 복구
- 영향: 없음 (UI만 영향)

### If Phase 2 Fails
- `ollama_client.py`, `gemini_client.py` 원복
- URL 정규화 및 예외 처리 개선 전 코드로 복구
- 영향: 기능 정상, 에러 처리 개선만 롤백

### If Phase 3 Fails
- 통합 테스트 및 문서만 영향
- 실제 기능 코드는 변경 없음
- 영향: 없음

---

## 📊 Progress Tracking

### Completion Status
- **Phase 1 (UI Reactive Binding)**: ⏳ 0%
- **Phase 2 (Client Error Handling)**: ⏳ 0%
- **Phase 3 (Integration & Docs)**: ⏳ 0%

**Overall Progress**: 0% complete

### Time Tracking
| Phase | Estimated | Actual | Variance |
|-------|-----------|--------|----------|
| Phase 1 | 1.5-2 hours | - | - |
| Phase 2 | 1-1.5 hours | - | - |
| Phase 3 | 0.5-1 hour | - | - |
| **Total** | 3-4.5 hours | - | - |

---

## 📝 Notes & Learnings

### Implementation Notes
- [Reactive Binding 적용 과정에서 발견한 인사이트]
- [NiceGUI 버전별 동작 차이 기록]

### Blockers Encountered
- **Blocker 1**: [설명] → [해결방법]

### Improvements for Future
- [NiceGUI Reactive Binding 패턴 표준화]
- [조건부 렌더링 Best Practices 문서화]

---

## ✅ Final Checklist

**Before marking plan as COMPLETE**:
- [ ] All 3 phases completed with quality gates passed
- [ ] Manual Test Checklist 모든 항목 통과
- [ ] Ollama 선택 시 Base URL만 표시
- [ ] Gemini 선택 시 API Key만 표시
- [ ] REFRESH MODELS 클릭 시 드롭다운에 모델 목록 표시
- [ ] Provider 변경 시 모델 목록 즉시 초기화
- [ ] 수동 UI 갱신 코드 모두 제거
- [ ] 코드 품질 검증 통과 (ruff, mypy)
- [ ] Bug Fix 요약 문서 작성 완료
- [ ] 회귀 테스트 통과 (기존 기능 정상 동작)

---

**Plan Status**: 🔄 Ready to Implement
**Next Action**: Phase 1 시작 - NiceGUI Reactive Binding 적용
**Blocked By**: None
**Last Updated**: 2025-12-30
