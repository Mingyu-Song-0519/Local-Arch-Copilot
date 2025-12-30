# Implementation Plan: Multi-Provider LLM & Dynamic Model Configuration

**Status**: 🔄 Ready to Implement
**Created**: 2025-12-30
**Last Updated**: 2025-12-30
**Estimated Completion**: 4-5 phases, 10-14 hours

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
사용자가 Settings 페이지에서 LLM 공급자(Ollama, LMStudio, Gemini, OpenAI, Anthropic)를 직접 선택하고, 로컬 환경의 경우 설치된 모델 목록을 실시간으로 가져와 선택할 수 있는 기능을 구현합니다. 이를 통해 단일 vLLM 클라이언트에 고정되지 않고 다양한 AI 공급자를 유연하게 사용할 수 있습니다.

### Success Criteria
- [ ] Settings 페이지에서 LLM 공급자 선택 드롭다운 표시
- [ ] 선택한 공급자에 따라 Base URL 또는 API Key 입력창 조건부 표시
- [ ] "REFRESH MODELS" 버튼 클릭 시 실제 사용 가능한 모델 목록 동적 로드
- [ ] 설정 변경 시 `.env` 파일에 자동 저장 및 애플리케이션 상태 갱신
- [ ] AI 분석 시 선택된 공급자의 클라이언트를 동적으로 사용
- [ ] vLLM/Ollama/LMStudio 서버 오프라인 시에도 정적 분석은 정상 동작

### User Impact
- **유연성 향상**: 단일 AI 공급자에 종속되지 않고 다양한 로컬/클라우드 LLM 사용 가능
- **비용 절감**: 로컬 Ollama/LMStudio 사용 시 API 비용 없이 무료로 사용
- **성능 최적화**: 프로젝트 규모에 따라 적절한 모델 선택 가능 (소형: 7B, 대형: 70B+)
- **개인정보 보호**: 민감한 코드는 로컬 모델 사용, 일반 코드는 클라우드 모델 사용

---

## 🏗️ Architecture Decisions

| Decision | Rationale | Trade-offs |
|----------|-----------|------------|
| **Domain에 ILLMClient 인터페이스 추가** | Application이 Infrastructure의 구체적인 클라이언트에 직접 의존하지 않도록 의존성 역전 원칙 적용 | 추가 추상화 레이어로 초기 개발 시간 증가 |
| **Factory Pattern으로 클라이언트 생성** | Provider에 따라 런타임에 적절한 클라이언트 객체 생성 (전략 패턴 + 팩토리 패턴) | 팩토리 코드 유지보수 필요 |
| **Pydantic Settings로 .env 읽기/쓰기** | 타입 안정성과 검증 로직을 자동으로 처리 | .env 파일 구조 변경 시 마이그레이션 필요 |
| **NiceGUI Reactive Binding으로 UI 동적 변경** | Provider 선택 시 UI 요소가 자동으로 반응하여 UX 향상 | 복잡한 상태 관리 필요 |
| **비동기 모델 로드** | 외부 API 호출 시 UI 블로킹 방지 | 에러 처리 및 타임아웃 로직 필요 |

---

## 📦 Dependencies

### Required Before Starting
- [ ] Python 3.11+ 설치
- [ ] Clean Architecture 4-Layer 구조 이해
- [ ] Pydantic v2 문법 숙지
- [ ] NiceGUI reactive binding 이해

### External Dependencies
- `httpx`: ^0.25.0 (비동기 HTTP 클라이언트, 이미 설치됨)
- `google-generativeai`: ^0.3.0 (Gemini 클라이언트, Phase 3에서 추가)
- `anthropic`: ^0.8.0 (Claude 클라이언트, Phase 3에서 추가)
- `openai`: ^1.0.0 (OpenAI 클라이언트, Phase 3에서 추가)

---

## 🧪 Test Strategy

### Testing Approach
**TDD Principle**: Write tests FIRST, then implement to make them pass

### Test Pyramid for This Feature
| Test Type | Coverage Target | Purpose |
|-----------|-----------------|---------|
| **Unit Tests** | ≥80% | Config 모델, Factory 로직, 클라이언트 인터페이스 검증 |
| **Integration Tests** | Critical paths | 실제 API 호출 (Mock 서버 사용), DI Container 통합 |
| **E2E Tests** | Key user flows | Settings → 공급자 선택 → 모델 로드 → 분석 실행 전체 흐름 |

### Test File Organization
```
tests/
├── unit/
│   ├── domain/
│   │   └── test_llm_client_interface.py
│   ├── infrastructure/
│   │   ├── test_config_persistence.py
│   │   ├── test_llm_client_factory.py
│   │   ├── test_ollama_client.py
│   │   └── test_gemini_client.py
├── integration/
│   └── test_multi_provider_integration.py
└── e2e/
    └── test_settings_ui_flow.py
```

### Coverage Requirements by Phase
- **Phase 1 (Domain - Config Interface)**: Config 인터페이스 및 Pydantic 모델 (≥90%)
- **Phase 2 (Infrastructure - Factory & Clients)**: Factory 로직 및 클라이언트 구현 (≥80%)
- **Phase 3 (Infrastructure - External Clients)**: Gemini/OpenAI 클라이언트 (≥75%, Mock 사용)
- **Phase 4 (Presentation - UI)**: Settings 페이지 E2E 테스트 (Critical paths)

### Test Naming Convention
```python
# pytest 스타일
def test_config_should_persist_llm_provider_to_env_file():
    """설정 변경 시 .env 파일에 LLM 공급자 저장 테스트"""
    pass

def test_factory_should_return_ollama_client_when_provider_is_ollama():
    """Factory가 provider='ollama'일 때 OllamaClient 반환 테스트"""
    pass
```

---

## 🚀 Implementation Phases

### Phase 1: Domain & Configuration Layer - LLM Config Interface
**Goal**: LLM 공급자 설정을 위한 Domain 인터페이스 및 Config 모델 확장
**Estimated Time**: 2-3 hours
**Status**: ⏳ Pending

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 1.1**: IConfig에 LLM 필드 추가 테스트
  - File(s): `tests/unit/infrastructure/test_config.py`
  - Expected: IConfig에 `llm_provider`, `llm_base_url`, `llm_api_key`, `llm_model` 속성 없어서 AttributeError
  - Details: 테스트 케이스:
    ```python
    def test_config_should_have_llm_provider_property():
        config = Config()
        assert hasattr(config, 'llm_provider')
        assert config.llm_provider in ['ollama', 'lmstudio', 'gemini', 'openai', 'anthropic']

    def test_config_should_have_llm_base_url_for_local_providers():
        config = Config(llm_provider='ollama', llm_base_url='http://localhost:11434')
        assert config.llm_base_url == 'http://localhost:11434'

    def test_config_should_have_llm_api_key_for_cloud_providers():
        config = Config(llm_provider='gemini', llm_api_key='test-key')
        assert config.llm_api_key == 'test-key'
    ```

- [ ] **Test 1.2**: Config Persistence 테스트
  - File(s): `tests/unit/infrastructure/test_config_persistence.py` (NEW)
  - Expected: `update_settings()` 메서드 없어서 실패
  - Details: 테스트 케이스:
    ```python
    def test_config_should_persist_changes_to_env_file(tmp_path):
        env_file = tmp_path / ".env"
        config = Config(_env_file=env_file)

        # Update settings
        config.update_settings({
            'llm_provider': 'ollama',
            'llm_base_url': 'http://localhost:11434',
            'llm_model': 'mistral-24b'
        })

        # Verify written to file
        content = env_file.read_text()
        assert 'LLM_PROVIDER=ollama' in content
        assert 'LLM_BASE_URL=http://localhost:11434' in content
        assert 'LLM_MODEL=mistral-24b' in content

    def test_config_should_mask_api_key_in_logs():
        config = Config(llm_api_key='sk-1234567890abcdef')
        assert 'sk-12****' in str(config)  # Masked
    ```

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 1.3**: IConfig 인터페이스 확장
  - File(s): `arch_copilot/domain/config/i_config.py`
  - Goal: LLM 공급자 관련 속성 추가
  - Details:
    ```python
    from typing import Protocol, Optional

    class IConfig(Protocol):
        """Configuration 인터페이스"""

        # 기존 속성들...
        @property
        def vllm_base_url(self) -> str: ...
        @property
        def vllm_model_name(self) -> str: ...

        # NEW: LLM Provider 설정
        @property
        def llm_provider(self) -> str:
            """LLM 공급자 (ollama, lmstudio, gemini, openai, anthropic)"""
            ...

        @property
        def llm_base_url(self) -> Optional[str]:
            """로컬 LLM 서버 URL (Ollama/LMStudio)"""
            ...

        @property
        def llm_api_key(self) -> Optional[str]:
            """클라우드 LLM API Key (Gemini/OpenAI/Anthropic)"""
            ...

        @property
        def llm_model(self) -> str:
            """사용할 모델 이름"""
            ...

        def update_settings(self, settings: dict[str, Any]) -> None:
            """설정 업데이트 및 영구 저장"""
            ...
    ```

- [ ] **Task 1.4**: Config Pydantic 모델 확장
  - File(s): `arch_copilot/infrastructure/config/config.py`
  - Goal: LLM 필드 추가 및 .env 저장 로직 구현
  - Details:
    ```python
    from pydantic import Field, SecretStr, field_validator
    from pydantic_settings import BaseSettings, SettingsConfigDict
    from pathlib import Path
    from typing import Optional, Literal, Any

    class Config(BaseSettings):
        """환경 변수 및 .env 파일 기반 설정 구현체"""

        # 기존 필드들...
        vllm_base_url: str = Field(default="http://localhost:8000")
        vllm_model_name: str = Field(default="openai/gpt-oss-20b")

        # NEW: LLM Provider 설정
        llm_provider: Literal['ollama', 'lmstudio', 'gemini', 'openai', 'anthropic', 'vllm'] = Field(
            default='vllm',
            description="LLM 공급자 선택"
        )
        llm_base_url: Optional[str] = Field(
            default=None,
            description="로컬 LLM 서버 URL (Ollama: http://localhost:11434/v1, LMStudio: http://localhost:1234/v1)"
        )
        llm_api_key: Optional[SecretStr] = Field(
            default=None,
            description="클라우드 LLM API Key (환경변수 또는 .env에 저장)"
        )
        llm_model: str = Field(
            default="mistral-24b:latest",
            description="사용할 모델 이름"
        )

        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            extra="ignore"
        )

        @field_validator("llm_provider")
        @classmethod
        def validate_provider(cls, v: str) -> str:
            allowed = {'ollama', 'lmstudio', 'gemini', 'openai', 'anthropic', 'vllm'}
            if v not in allowed:
                raise ValueError(f"Provider must be one of {allowed}")
            return v

        def update_settings(self, settings: dict[str, Any]) -> None:
            """설정 업데이트 및 .env 파일에 저장"""
            env_file = Path(".env")

            # 기존 .env 읽기
            if env_file.exists():
                lines = env_file.read_text(encoding="utf-8").splitlines()
            else:
                lines = []

            # 업데이트할 설정을 대문자 환경변수 이름으로 변환
            env_updates = {}
            for key, value in settings.items():
                env_key = key.upper()
                if value is not None:
                    env_updates[env_key] = str(value)

            # 기존 라인 업데이트 또는 추가
            updated_keys = set()
            new_lines = []
            for line in lines:
                if '=' in line and not line.strip().startswith('#'):
                    key = line.split('=', 1)[0].strip()
                    if key in env_updates:
                        new_lines.append(f"{key}={env_updates[key]}")
                        updated_keys.add(key)
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)

            # 새로운 키 추가
            for key, value in env_updates.items():
                if key not in updated_keys:
                    new_lines.append(f"{key}={value}")

            # .env 파일 쓰기
            env_file.write_text('\n'.join(new_lines) + '\n', encoding="utf-8")

            # 현재 인스턴스 업데이트 (runtime)
            for key, value in settings.items():
                if hasattr(self, key):
                    setattr(self, key, value)
    ```

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 1.5**: Config 검증 로직 강화
  - Files: `arch_copilot/infrastructure/config/config.py`
  - Goal: Provider별 필수 필드 검증
  - Checklist:
    - [ ] Ollama/LMStudio 선택 시 `llm_base_url` 필수 검증
    - [ ] Gemini/OpenAI/Anthropic 선택 시 `llm_api_key` 필수 검증
    - [ ] API Key는 SecretStr로 로그에 노출 방지
    - [ ] 환경변수 우선순위 (ENV > .env 파일) 명시

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed to Phase 2 until ALL checks pass**

**TDD Compliance** (CRITICAL):
- [ ] **Red Phase**: Tests were written FIRST and initially failed
- [ ] **Green Phase**: Production code written to make tests pass
- [ ] **Refactor Phase**: Code improved while tests still pass
- [ ] **Coverage Check**: Test coverage ≥90% for config module
  ```bash
  pytest tests/unit/infrastructure/test_config.py -v --cov=arch_copilot/infrastructure/config --cov-report=term-missing
  ```

**Build & Tests**:
- [ ] **Build**: Project builds without errors
- [ ] **All Tests Pass**: 100% of config tests passing
- [ ] **No Flaky Tests**: Tests pass consistently (run 3+ times)

**Code Quality**:
- [ ] **Linting**: `ruff check arch_copilot/infrastructure/config/`
- [ ] **Formatting**: `black --check arch_copilot/infrastructure/config/`
- [ ] **Type Safety**: `mypy arch_copilot/infrastructure/config/ --strict`

**Security**:
- [ ] **API Key 보안**: SecretStr 사용으로 로그에 평문 노출 방지
- [ ] **.env 파일**: .gitignore에 포함 확인

**Validation Commands**:
```bash
# Run config tests
pytest tests/unit/infrastructure/test_config.py -v --cov=arch_copilot/infrastructure/config --cov-report=html

# Type check
mypy arch_copilot/domain/config/ arch_copilot/infrastructure/config/ --strict

# Code quality
ruff check arch_copilot/infrastructure/config/
black --check arch_copilot/infrastructure/config/
```

**Manual Test Checklist**:
- [ ] .env 파일에 LLM_PROVIDER=ollama 설정 후 Config 로드 확인
- [ ] update_settings() 호출 후 .env 파일에 변경사항 반영 확인
- [ ] API Key 설정 시 로그에 마스킹된 값만 출력 확인

---

### Phase 2: Infrastructure Layer - LLM Client Factory & Base Client
**Goal**: Factory Pattern으로 Provider별 클라이언트 동적 생성, OpenAI-compatible 클라이언트 구현
**Estimated Time**: 3-4 hours
**Status**: ⏳ Pending
**Dependencies**: Phase 1 완료

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 2.1**: ILLMClient 인터페이스 테스트
  - File(s): `tests/unit/domain/test_llm_client_interface.py` (NEW)
  - Expected: ILLMClient 인터페이스 없어서 ImportError
  - Details: 테스트 케이스:
    ```python
    from arch_copilot.domain.ai.i_llm_client import ILLMClient

    def test_llm_client_interface_should_have_required_methods():
        """ILLMClient는 generate, chat_completion, check_health, list_models 메서드 필요"""
        assert hasattr(ILLMClient, 'generate')
        assert hasattr(ILLMClient, 'chat_completion')
        assert hasattr(ILLMClient, 'check_health')
        assert hasattr(ILLMClient, 'list_models')
    ```

- [ ] **Test 2.2**: LLMClientFactory 테스트
  - File(s): `tests/unit/infrastructure/test_llm_client_factory.py` (NEW)
  - Expected: LLMClientFactory 클래스 없어서 실패
  - Details: 테스트 케이스:
    ```python
    from arch_copilot.infrastructure.ai_client.llm_client_factory import LLMClientFactory
    from arch_copilot.infrastructure.ai_client.ollama_client import OllamaClient
    from arch_copilot.infrastructure.config.config import Config

    def test_factory_should_create_ollama_client_when_provider_is_ollama():
        config = Config(llm_provider='ollama', llm_base_url='http://localhost:11434/v1')
        client = LLMClientFactory.create(config)
        assert isinstance(client, OllamaClient)

    def test_factory_should_create_lmstudio_client_when_provider_is_lmstudio():
        config = Config(llm_provider='lmstudio', llm_base_url='http://localhost:1234/v1')
        client = LLMClientFactory.create(config)
        # LMStudio는 OpenAI-compatible이므로 OllamaClient 재사용
        assert isinstance(client, OllamaClient)

    def test_factory_should_raise_error_for_unsupported_provider():
        config = Config(llm_provider='unsupported')
        with pytest.raises(ValueError, match="Unsupported LLM provider"):
            LLMClientFactory.create(config)
    ```

- [ ] **Test 2.3**: OllamaClient 구현 테스트
  - File(s): `tests/unit/infrastructure/test_ollama_client.py` (NEW)
  - Expected: OllamaClient 클래스 없어서 실패
  - Details: Mock httpx를 사용한 테스트 케이스:
    ```python
    import pytest
    from unittest.mock import AsyncMock, patch
    from arch_copilot.infrastructure.ai_client.ollama_client import OllamaClient

    @pytest.mark.asyncio
    async def test_ollama_client_should_generate_text():
        client = OllamaClient(base_url='http://localhost:11434/v1', model_name='mistral-24b')

        with patch('httpx.AsyncClient.post') as mock_post:
            mock_post.return_value.json.return_value = {
                'choices': [{'text': 'Generated text'}]
            }

            result = await client.generate('Test prompt')
            assert result == 'Generated text'

    @pytest.mark.asyncio
    async def test_ollama_client_should_list_models():
        client = OllamaClient(base_url='http://localhost:11434/v1')

        with patch('httpx.AsyncClient.get') as mock_get:
            mock_get.return_value.json.return_value = {
                'data': [
                    {'id': 'mistral-24b:latest'},
                    {'id': 'llama3:70b'}
                ]
            }

            models = await client.list_models()
            assert 'mistral-24b:latest' in models
            assert 'llama3:70b' in models

    @pytest.mark.asyncio
    async def test_ollama_client_should_return_false_when_server_offline():
        client = OllamaClient(base_url='http://localhost:11434/v1')

        with patch('httpx.AsyncClient.get', side_effect=httpx.ConnectError):
            health = await client.check_health()
            assert health is False
    ```

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 2.4**: Domain - ILLMClient 인터페이스 정의
  - File(s): `arch_copilot/domain/ai/i_llm_client.py` (NEW)
  - Goal: 모든 LLM 클라이언트가 따라야 할 인터페이스
  - Details:
    ```python
    from abc import ABC, abstractmethod
    from typing import List, Dict, Optional

    class ILLMClient(ABC):
        """LLM 클라이언트 인터페이스 (모든 공급자가 구현)"""

        @abstractmethod
        async def generate(
            self,
            prompt: str,
            max_tokens: int = 2048,
            temperature: float = 0.7
        ) -> str:
            """텍스트 생성 (Completion API)"""
            pass

        @abstractmethod
        async def chat_completion(
            self,
            messages: List[Dict[str, str]],
            max_tokens: int = 2048,
            temperature: float = 0.7
        ) -> str:
            """채팅 형식 생성 (Chat API)"""
            pass

        @abstractmethod
        async def check_health(self) -> bool:
            """서버 또는 API 상태 확인"""
            pass

        @abstractmethod
        async def list_models(self) -> List[str]:
            """사용 가능한 모델 목록 조회"""
            pass
    ```

- [ ] **Task 2.5**: Infrastructure - OllamaClient 구현 (OpenAI-compatible)
  - File(s): `arch_copilot/infrastructure/ai_client/ollama_client.py` (NEW)
  - Goal: Ollama/LMStudio/vLLM 등 OpenAI-compatible 서버용 클라이언트
  - Details:
    ```python
    import httpx
    from typing import List, Dict
    from arch_copilot.domain.ai.i_llm_client import ILLMClient

    class OllamaClient(ILLMClient):
        """OpenAI 호환 API를 사용하는 클라이언트 (Ollama, LMStudio, vLLM)"""

        def __init__(self, base_url: str, model_name: str = "mistral-24b:latest") -> None:
            self.base_url = base_url.rstrip('/')
            self.model_name = model_name
            self.timeout = httpx.Timeout(180.0, connect=10.0)

        async def generate(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> str:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "model": self.model_name,
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                }
                response = await client.post(f"{self.base_url}/completions", json=payload)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["text"].strip()

        async def chat_completion(self, messages: List[Dict[str, str]], max_tokens: int = 2048, temperature: float = 0.7) -> str:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "model": self.model_name,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                }
                response = await client.post(f"{self.base_url}/chat/completions", json=payload)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()

        async def check_health(self) -> bool:
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get(f"{self.base_url}/models")
                    return response.status_code == 200
            except Exception:
                return False

        async def list_models(self) -> List[str]:
            """사용 가능한 모델 목록 조회 (OpenAI /v1/models API)"""
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(f"{self.base_url}/models")
                    response.raise_for_status()
                    data = response.json()
                    # OpenAI API 형식: {'data': [{'id': 'model-name'}, ...]}
                    return [model['id'] for model in data.get('data', [])]
            except Exception as e:
                print(f"Failed to fetch models: {e}")
                return []
    ```

- [ ] **Task 2.6**: Infrastructure - LLMClientFactory 구현
  - File(s): `arch_copilot/infrastructure/ai_client/llm_client_factory.py` (NEW)
  - Goal: Config에 따라 적절한 클라이언트 생성
  - Details:
    ```python
    from arch_copilot.domain.config.i_config import IConfig
    from arch_copilot.domain.ai.i_llm_client import ILLMClient
    from arch_copilot.infrastructure.ai_client.ollama_client import OllamaClient

    class LLMClientFactory:
        """LLM 클라이언트 팩토리 (Strategy Pattern)"""

        @staticmethod
        def create(config: IConfig) -> ILLMClient:
            """설정에 따라 적절한 LLM 클라이언트 생성"""
            provider = config.llm_provider

            if provider in ['ollama', 'lmstudio', 'vllm']:
                # OpenAI-compatible 로컬 서버
                base_url = config.llm_base_url or config.vllm_base_url
                model_name = config.llm_model
                return OllamaClient(base_url=base_url, model_name=model_name)

            elif provider == 'gemini':
                # Phase 3에서 구현
                raise NotImplementedError("Gemini client not yet implemented")

            elif provider == 'openai':
                # Phase 3에서 구현
                raise NotImplementedError("OpenAI client not yet implemented")

            elif provider == 'anthropic':
                # Phase 3에서 구현
                raise NotImplementedError("Anthropic client not yet implemented")

            else:
                raise ValueError(f"Unsupported LLM provider: {provider}")
    ```

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 2.7**: VLLMClient를 OllamaClient로 리팩토링
  - Files: `arch_copilot/infrastructure/ai_client/vllm_client.py`
  - Goal: 기존 VLLMClient를 OllamaClient로 대체 (동일한 OpenAI-compatible API)
  - Checklist:
    - [ ] VLLMClient 사용처를 OllamaClient로 변경
    - [ ] VLLMAnalyzer는 ILLMClient를 주입받도록 수정
    - [ ] 하위 호환성 유지 (VLLMClient를 OllamaClient의 alias로 유지)

- [ ] **Task 2.8**: Domain __init__.py 업데이트
  - Files: `arch_copilot/domain/ai/__init__.py`
  - Goal: Public API 노출
  - Checklist:
    - [ ] ILLMClient export

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed to Phase 3 until ALL checks pass**

**TDD Compliance** (CRITICAL):
- [ ] Tests written FIRST and initially failed
- [ ] Implementation makes tests pass
- [ ] Coverage: Factory & Clients ≥80%

**Architecture Compliance**:
- [ ] ILLMClient in `domain/ai/` (no external dependencies)
- [ ] OllamaClient implements ILLMClient
- [ ] Factory doesn't depend on Application layer

**Functionality**:
- [ ] Factory creates correct client based on provider
- [ ] OllamaClient successfully lists models (with mock)
- [ ] Health check returns False when server offline

**Validation Commands**:
```bash
pytest tests/unit/domain/test_llm_client_interface.py -v
pytest tests/unit/infrastructure/test_llm_client_factory.py -v
pytest tests/unit/infrastructure/test_ollama_client.py -v --cov=arch_copilot/infrastructure/ai_client
mypy arch_copilot/domain/ai/ arch_copilot/infrastructure/ai_client/ --strict
```

---

### Phase 3: Infrastructure Layer - Cloud Provider Clients
**Goal**: Gemini, OpenAI, Anthropic 클라이언트 구현
**Estimated Time**: 2-3 hours
**Status**: ⏳ Pending
**Dependencies**: Phase 2 완료

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 3.1**: GeminiClient 테스트
  - File(s): `tests/unit/infrastructure/test_gemini_client.py` (NEW)
  - Expected: GeminiClient 클래스 없어서 실패
  - Details: Mock google.generativeai 사용:
    ```python
    import pytest
    from unittest.mock import AsyncMock, patch, MagicMock
    from arch_copilot.infrastructure.ai_client.gemini_client import GeminiClient

    @pytest.mark.asyncio
    async def test_gemini_client_should_generate_text():
        client = GeminiClient(api_key='test-key', model_name='gemini-pro')

        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_response = MagicMock()
            mock_response.text = 'Gemini generated text'
            mock_model.return_value.generate_content.return_value = mock_response

            result = await client.generate('Test prompt')
            assert result == 'Gemini generated text'

    @pytest.mark.asyncio
    async def test_gemini_client_should_list_models():
        client = GeminiClient(api_key='test-key')

        with patch('google.generativeai.list_models') as mock_list:
            mock_list.return_value = [
                MagicMock(name='models/gemini-pro'),
                MagicMock(name='models/gemini-pro-vision')
            ]

            models = await client.list_models()
            assert 'gemini-pro' in models
            assert 'gemini-pro-vision' in models
    ```

- [ ] **Test 3.2**: OpenAIClient 테스트
  - File(s): `tests/unit/infrastructure/test_openai_client.py` (NEW)
  - Expected: OpenAIClient 클래스 없어서 실패
  - Details: Mock openai 라이브러리 사용

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 3.3**: GeminiClient 구현
  - File(s): `arch_copilot/infrastructure/ai_client/gemini_client.py` (NEW)
  - Goal: Google Gemini API 클라이언트
  - Details:
    ```python
    import google.generativeai as genai
    from typing import List, Dict
    from arch_copilot.domain.ai.i_llm_client import ILLMClient

    class GeminiClient(ILLMClient):
        """Google Gemini API 클라이언트"""

        def __init__(self, api_key: str, model_name: str = "gemini-pro") -> None:
            genai.configure(api_key=api_key)
            self.model_name = model_name
            self.model = genai.GenerativeModel(model_name)

        async def generate(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> str:
            """Gemini는 비동기를 직접 지원하지 않으므로 run_in_executor 사용"""
            import asyncio
            loop = asyncio.get_event_loop()

            def _generate():
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=max_tokens,
                        temperature=temperature
                    )
                )
                return response.text

            return await loop.run_in_executor(None, _generate)

        async def chat_completion(self, messages: List[Dict[str, str]], max_tokens: int = 2048, temperature: float = 0.7) -> str:
            # Gemini Chat API 사용
            chat = self.model.start_chat(history=[])
            last_message = messages[-1]['content']

            import asyncio
            loop = asyncio.get_event_loop()

            def _chat():
                response = chat.send_message(
                    last_message,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=max_tokens,
                        temperature=temperature
                    )
                )
                return response.text

            return await loop.run_in_executor(None, _chat)

        async def check_health(self) -> bool:
            try:
                models = await self.list_models()
                return len(models) > 0
            except Exception:
                return False

        async def list_models(self) -> List[str]:
            import asyncio
            loop = asyncio.get_event_loop()

            def _list():
                models = genai.list_models()
                return [m.name.replace('models/', '') for m in models if 'generateContent' in m.supported_generation_methods]

            return await loop.run_in_executor(None, _list)
    ```

- [ ] **Task 3.4**: OpenAIClient 구현 (선택사항)
  - File(s): `arch_copilot/infrastructure/ai_client/openai_client.py` (NEW)
  - Goal: OpenAI API 클라이언트 (OllamaClient와 유사하지만 공식 SDK 사용)
  - Details: openai Python SDK 사용

- [ ] **Task 3.5**: Factory에 클라우드 클라이언트 추가
  - File(s): `arch_copilot/infrastructure/ai_client/llm_client_factory.py`
  - Goal: Gemini, OpenAI 클라이언트 생성 로직 추가
  - Details:
    ```python
    from arch_copilot.infrastructure.ai_client.gemini_client import GeminiClient
    # from arch_copilot.infrastructure.ai_client.openai_client import OpenAIClient

    class LLMClientFactory:
        @staticmethod
        def create(config: IConfig) -> ILLMClient:
            provider = config.llm_provider

            # ... 기존 로컬 클라이언트 ...

            elif provider == 'gemini':
                if not config.llm_api_key:
                    raise ValueError("Gemini requires llm_api_key in config")
                api_key = config.llm_api_key.get_secret_value()
                return GeminiClient(api_key=api_key, model_name=config.llm_model)

            elif provider == 'openai':
                if not config.llm_api_key:
                    raise ValueError("OpenAI requires llm_api_key in config")
                # OpenAIClient 구현 후 활성화
                raise NotImplementedError("OpenAI client not yet implemented")

            # ...
    ```

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 3.6**: 에러 처리 개선
  - Files: All client files
  - Goal: 일관된 예외 처리 및 재시도 로직
  - Checklist:
    - [ ] API 타임아웃 처리
    - [ ] Rate Limiting 처리 (429 에러)
    - [ ] 네트워크 에러 재시도 (3회)

#### Quality Gate ✋

**TDD Compliance**:
- [ ] All cloud client tests pass
- [ ] Coverage: Cloud clients ≥75% (Mock 사용)

**Functionality**:
- [ ] GeminiClient가 모델 목록 조회 성공 (Mock)
- [ ] API Key 없을 시 명확한 에러 메시지

**Validation Commands**:
```bash
pytest tests/unit/infrastructure/test_gemini_client.py -v
pytest tests/unit/infrastructure/test_llm_client_factory.py -v
```

---

### Phase 4: Presentation Layer - Dynamic Settings UI
**Goal**: Settings 페이지에 Provider 선택, 조건부 입력, 모델 동적 로드 기능 구현
**Estimated Time**: 3-4 hours
**Status**: ⏳ Pending
**Dependencies**: Phase 1-3 완료

#### Tasks

**🔴 RED: Write Failing E2E Tests First**
- [ ] **Test 4.1**: Settings UI E2E 테스트
  - File(s): `tests/e2e/test_settings_ui_flow.py` (NEW)
  - Expected: UI 요소 없어서 실패
  - Details: Playwright 또는 Selenium 사용 (NiceGUI 테스트 가능 시):
    ```python
    def test_settings_page_should_show_provider_dropdown():
        # Settings 페이지 접속
        # Provider 드롭다운 존재 확인
        # 선택지: ollama, lmstudio, gemini, openai 확인
        pass

    def test_settings_page_should_show_base_url_when_ollama_selected():
        # Provider를 'ollama' 선택
        # Base URL 입력창 표시 확인
        # API Key 입력창 숨김 확인
        pass

    def test_settings_page_should_refresh_models_on_button_click():
        # Provider를 'ollama' 선택
        # Base URL 입력
        # REFRESH MODELS 버튼 클릭
        # Model 드롭다운에 모델 목록 표시 확인
        pass
    ```

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 4.2**: Settings Page UI 구현
  - File(s): `arch_copilot/presentation/nicegui_app/pages/settings_page.py`
  - Goal: Dynamic LLM Configuration UI
  - Details:
    ```python
    from nicegui import ui, run
    from arch_copilot.presentation.nicegui_app.layouts.base_layout import base_layout
    from arch_copilot.infrastructure.di.container import get_container
    from arch_copilot.domain.config.i_config import IConfig
    from arch_copilot.infrastructure.ai_client.llm_client_factory import LLMClientFactory

    def settings_page():
        container = get_container()
        config = container.resolve(IConfig)

        # Reactive state
        state = {
            'provider': config.llm_provider,
            'base_url': config.llm_base_url or 'http://localhost:11434/v1',
            'api_key': '',
            'model': config.llm_model,
            'available_models': []
        }

        with base_layout("System Settings"):
            with ui.column().classes('w-full gap-4'):
                ui.label('LLM Configuration').classes('text-3xl font-bold text-white')
                ui.label('AI 공급자 및 모델을 선택합니다.').classes('text-gray-400')

            with ui.card().classes('w-full p-8 bg-zinc-900/50 border border-zinc-800 rounded-3xl'):
                ui.label('AI Provider').classes('text-lg font-semibold text-primary mb-4')

                with ui.column().classes('w-full gap-4'):
                    # Provider 선택 드롭다운
                    provider_select = ui.select(
                        label='API Provider',
                        options=['ollama', 'lmstudio', 'gemini', 'openai', 'anthropic', 'vllm'],
                        value=state['provider'],
                        on_change=lambda e: on_provider_change(e.value)
                    ).classes('w-full text-white').props('dark outlined')

                    # 조건부 입력창 (Reactive)
                    @ui.refreshable
                    def conditional_inputs():
                        if state['provider'] in ['ollama', 'lmstudio', 'vllm']:
                            # Base URL 입력
                            ui.input(
                                label='Base URL',
                                value=state['base_url'],
                                on_change=lambda e: state.update({'base_url': e.value})
                            ).classes('w-full text-white').props('dark outlined')

                        elif state['provider'] in ['gemini', 'openai', 'anthropic']:
                            # API Key 입력
                            ui.input(
                                label='API Key',
                                value=state['api_key'],
                                password=True,
                                password_toggle_button=True,
                                on_change=lambda e: state.update({'api_key': e.value})
                            ).classes('w-full text-white').props('dark outlined')
                            ui.label('⚠️ API Key는 .env 파일에 평문으로 저장됩니다.').classes('text-xs text-yellow-600')

                    conditional_inputs()

                    # Model 선택
                    with ui.row().classes('w-full gap-4 items-end'):
                        model_select = ui.select(
                            label='Model',
                            options=state['available_models'] or [state['model']],
                            value=state['model'],
                            on_change=lambda e: state.update({'model': e.value})
                        ).classes('flex-grow text-white').props('dark outlined')

                        ui.button(
                            'REFRESH MODELS',
                            icon='refresh',
                            on_click=lambda: refresh_models()
                        ).props('unelevated rounded').classes('bg-secondary text-white')

                    ui.label('로컬 서버 (Ollama/LMStudio) 또는 API (Gemini)에서 모델 목록을 가져옵니다.').classes('text-xs text-gray-600')

            # 저장 버튼
            ui.button(
                'SAVE CHANGES',
                icon='save',
                on_click=lambda: save_settings()
            ).props('unelevated rounded-full').classes('px-10 py-3 bg-primary text-white font-bold ml-auto')

        # Event Handlers
        def on_provider_change(new_provider: str):
            state['provider'] = new_provider

            # Provider에 따라 기본값 설정
            if new_provider == 'ollama':
                state['base_url'] = 'http://localhost:11434/v1'
                state['model'] = 'mistral-24b:latest'
            elif new_provider == 'lmstudio':
                state['base_url'] = 'http://localhost:1234/v1'
            elif new_provider == 'gemini':
                state['model'] = 'gemini-pro'

            # UI 새로고침
            conditional_inputs.refresh()

        async def refresh_models():
            """선택된 Provider에서 모델 목록 가져오기"""
            ui.notify('모델 목록을 가져오는 중...', type='info')

            try:
                # 임시 Config로 클라이언트 생성
                from arch_copilot.infrastructure.config.config import Config
                temp_config = Config(
                    llm_provider=state['provider'],
                    llm_base_url=state['base_url'],
                    llm_api_key=state['api_key'] if state['api_key'] else None,
                    llm_model=state['model']
                )

                client = LLMClientFactory.create(temp_config)
                models = await client.list_models()

                if models:
                    state['available_models'] = models
                    model_select.options = models
                    model_select.update()
                    ui.notify(f'{len(models)}개의 모델을 찾았습니다.', type='positive')
                else:
                    ui.notify('모델을 찾을 수 없습니다. 서버 연결을 확인하세요.', type='warning')

            except Exception as e:
                ui.notify(f'모델 목록 가져오기 실패: {str(e)}', type='negative')

        def save_settings():
            """설정을 .env 파일에 저장"""
            try:
                config.update_settings({
                    'llm_provider': state['provider'],
                    'llm_base_url': state['base_url'] if state['provider'] in ['ollama', 'lmstudio', 'vllm'] else None,
                    'llm_api_key': state['api_key'] if state['provider'] in ['gemini', 'openai', 'anthropic'] else None,
                    'llm_model': state['model']
                })

                ui.notify('설정이 저장되었습니다. 애플리케이션을 재시작하여 적용하세요.', type='positive')

            except Exception as e:
                ui.notify(f'설정 저장 실패: {str(e)}', type='negative')
    ```

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 4.3**: UI 반응성 개선
  - Files: `settings_page.py`
  - Goal: 사용자 경험 향상
  - Checklist:
    - [ ] 모델 로드 중 스피너 표시
    - [ ] 입력 검증 (URL 형식, API Key 길이)
    - [ ] 설정 변경 전 확인 다이얼로그

- [ ] **Task 4.4**: DI Container에 Factory 적용
  - Files: `arch_copilot/infrastructure/di/bootstrap.py`
  - Goal: VLLMClient 대신 Factory로 클라이언트 생성
  - Checklist:
    - [ ] VLLMClient 직접 생성 제거
    - [ ] LLMClientFactory.create(config) 사용
    - [ ] VLLMAnalyzer에 ILLMClient 주입

#### Quality Gate ✋

**E2E Tests**:
- [ ] Settings 페이지에서 Provider 선택 가능
- [ ] Base URL/API Key 조건부 표시 확인
- [ ] 모델 목록 동적 로드 성공 (Mock 서버)

**User Experience**:
- [ ] Provider 변경 시 UI 즉시 반응
- [ ] 모델 로드 중 로딩 인디케이터 표시
- [ ] 저장 성공/실패 메시지 명확히 표시

**Validation Commands**:
```bash
# E2E 테스트 (수동)
python -m arch_copilot.main
# 1. Settings 페이지 접속
# 2. Provider를 'ollama'로 변경 → Base URL 입력창 확인
# 3. REFRESH MODELS 클릭 → 모델 목록 확인
# 4. SAVE CHANGES → .env 파일 확인
```

---

## ⚠️ Risk Assessment

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| **로컬 서버 (Ollama/LMStudio) 미설치** | Medium | Medium | UI에서 서버 오프라인 감지 시 명확한 가이드 메시지 표시 |
| **API Key 보안 이슈** | Low | High | .env 파일 .gitignore 추가, SecretStr 사용으로 로그 마스킹 |
| **Gemini/OpenAI API 요금 폭탄** | Medium | High | Settings에 월별 사용량 제한 설정 기능 추가 (향후 고도화) |
| **모델 목록 API 형식 차이** | Medium | Medium | Provider별 응답 형식 파싱 로직 분리, 실패 시 빈 배열 반환 |
| **의존성 라이브러리 충돌** | Low | Medium | pyproject.toml에 정확한 버전 명시, 가상환경 사용 권장 |

---

## 🔄 Rollback Strategy

### If Phase 1 Fails
- `domain/config/i_config.py` 원복
- `infrastructure/config/config.py` 원복
- `.env` 파일 백업본 복구
- 영향: 없음 (다른 레이어 미변경)

### If Phase 2 Fails
- `domain/ai/i_llm_client.py` 삭제
- `infrastructure/ai_client/ollama_client.py` 삭제
- `infrastructure/ai_client/llm_client_factory.py` 삭제
- 기존 VLLMClient 계속 사용

### If Phase 3 Fails
- `infrastructure/ai_client/gemini_client.py` 삭제
- Factory에서 Gemini 관련 코드 제거
- 로컬 Provider만 지원 (Ollama/LMStudio/vLLM)

### If Phase 4 Fails
- `presentation/nicegui_app/pages/settings_page.py` 원복 (git checkout)
- UI는 기존 Read-only 상태 유지
- 백엔드 Factory는 정상 동작

---

## 📊 Progress Tracking

### Completion Status
- **Phase 1 (Domain & Config)**: ⏳ 0%
- **Phase 2 (Factory & Base Client)**: ⏳ 0%
- **Phase 3 (Cloud Clients)**: ⏳ 0%
- **Phase 4 (Settings UI)**: ⏳ 0%

**Overall Progress**: 0% complete

### Time Tracking
| Phase | Estimated | Actual | Variance |
|-------|-----------|--------|----------|
| Phase 1 | 2-3 hours | - | - |
| Phase 2 | 3-4 hours | - | - |
| Phase 3 | 2-3 hours | - | - |
| Phase 4 | 3-4 hours | - | - |
| **Total** | 10-14 hours | - | - |

---

## 📝 Notes & Learnings

### Implementation Notes
- [구현 중 발견한 인사이트 기록]
- [계획과 다르게 진행한 의사결정 기록]

### Blockers Encountered
- **Blocker 1**: [설명] → [해결방법]

### Improvements for Future Plans
- [다음번에 다르게 할 점]
- [특히 잘 작동한 부분]

---

## 📚 References

### Documentation
- [Ollama API Docs](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [LMStudio API Docs](https://lmstudio.ai/docs/api)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [OpenAI API Docs](https://platform.openai.com/docs/api-reference)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [NiceGUI Binding](https://nicegui.io/documentation/binding)

### Related Issues
- 기존 Issue: AI 분석 기능 구현 (#1 가정)
- PR: VLLMClient 초기 구현 (#2 가정)

---

## ✅ Final Checklist

**Before marking plan as COMPLETE**:
- [ ] All 4 phases completed with quality gates passed
- [ ] Settings 페이지에서 모든 Provider 선택 가능
- [ ] 로컬 Provider (Ollama) 모델 목록 동적 로드 확인
- [ ] 클라우드 Provider (Gemini) 모델 목록 동적 로드 확인
- [ ] .env 파일에 설정 정상 저장 확인
- [ ] AI 분석 시 선택된 클라이언트로 동작 확인
- [ ] Test coverage ≥80% overall
- [ ] Clean Architecture 의존성 규칙 준수 확인
- [ ] API Key 보안 검증 (로그에 평문 노출 없음)
- [ ] 성능 저하 없음 (UI 반응성 유지)

---

**Plan Status**: 🔄 Ready to Implement
**Next Action**: Phase 1 시작 - Domain에 LLM Config 인터페이스 정의
**Blocked By**: None
**Last Updated**: 2025-12-30

---

## 🔧 Plan Review & Additional Enhancements

### Identified Gaps & Improvements

#### 1. **Phase 0: Pre-Implementation Setup** (추가 권장)
**Goal**: 개발 환경 설정 및 의존성 설치
**Estimated Time**: 0.5-1 hour
**Status**: ⏳ Pending

**Tasks**:
- [ ] **Task 0.1**: 개발 환경 검증
  - Python 3.11+ 설치 확인
  - 가상환경 활성화 확인 (`venv` 또는 `conda`)
  - pyproject.toml 의존성 검토

- [ ] **Task 0.2**: 외부 의존성 설치 (Phase 3용 준비)
  - `google-generativeai` 라이브러리 사전 설치 (선택사항)
  - `anthropic` 라이브러리 사전 설치 (선택사항)
  - `openai` 라이브러리 사전 설치 (선택사항)
  - 설치 명령어:
    ```bash
    # Phase 3 구현 전까지는 선택사항
    pip install google-generativeai anthropic openai

    # 또는 pyproject.toml에 optional dependencies 추가
    # [project.optional-dependencies]
    # cloud-providers = ["google-generativeai>=0.3.0", "anthropic>=0.8.0", "openai>=1.0.0"]
    ```

- [ ] **Task 0.3**: 테스트 환경 설정
  - pytest-asyncio 플러그인 설치 확인 (비동기 테스트용)
  - pytest-cov 플러그인 설치 확인 (커버리지 측정용)
  - pytest-mock 플러그인 설치 확인 (모킹용)
  - 설치 명령어:
    ```bash
    pip install pytest-asyncio pytest-cov pytest-mock
    ```

- [ ] **Task 0.4**: .env 파일 백업
  - 기존 `.env` 파일을 `.env.backup`으로 복사
  - Phase 1 실패 시 복구용

**Quality Gate**:
- [ ] 모든 필수 의존성 설치 완료
- [ ] pytest 실행 가능 확인
- [ ] .env 백업 완료

---

#### 2. **Phase 1 개선사항: Config 검증 로직 강화**

**추가할 Validator**:

```python
from pydantic import model_validator
from typing import Self

class Config(BaseSettings):
    # ... 기존 필드들 ...

    @model_validator(mode='after')
    def validate_provider_requirements(self) -> Self:
        """Provider별 필수 필드 검증"""
        provider = self.llm_provider

        # 로컬 Provider는 base_url 필수
        if provider in ['ollama', 'lmstudio'] and not self.llm_base_url:
            raise ValueError(f"{provider} requires llm_base_url to be set")

        # 클라우드 Provider는 api_key 필수
        if provider in ['gemini', 'openai', 'anthropic'] and not self.llm_api_key:
            raise ValueError(f"{provider} requires llm_api_key to be set")

        # vLLM은 기존 vllm_base_url 사용 가능
        if provider == 'vllm' and not self.llm_base_url and not self.vllm_base_url:
            raise ValueError("vLLM requires either llm_base_url or vllm_base_url")

        return self

    def __repr__(self) -> str:
        """API Key 마스킹하여 로그 출력"""
        safe_dict = self.model_dump()
        if self.llm_api_key:
            # SecretStr의 실제 값을 마스킹
            key = self.llm_api_key.get_secret_value()
            safe_dict['llm_api_key'] = f"{key[:6]}****{key[-4:]}" if len(key) > 10 else "****"
        return f"Config({safe_dict})"
```

**추가 테스트 케이스** (Phase 1):

```python
def test_config_should_raise_error_when_ollama_without_base_url():
    """Ollama 선택 시 base_url 없으면 ValidationError"""
    with pytest.raises(ValueError, match="ollama requires llm_base_url"):
        Config(llm_provider='ollama', llm_base_url=None)

def test_config_should_raise_error_when_gemini_without_api_key():
    """Gemini 선택 시 api_key 없으면 ValidationError"""
    with pytest.raises(ValueError, match="gemini requires llm_api_key"):
        Config(llm_provider='gemini', llm_api_key=None)

def test_config_should_fallback_to_vllm_base_url_when_provider_is_vllm():
    """vLLM Provider는 llm_base_url 또는 vllm_base_url 둘 중 하나 사용 가능"""
    config = Config(llm_provider='vllm', vllm_base_url='http://localhost:8000')
    assert config.llm_base_url is None or config.vllm_base_url is not None
```

---

#### 3. **Phase 2 개선사항: 에러 처리 및 재시도 로직**

**추가할 Base Exception 클래스** (Domain Layer):

```python
# arch_copilot/domain/exceptions.py

class LLMClientError(Exception):
    """LLM 클라이언트 기본 예외"""
    pass

class LLMConnectionError(LLMClientError):
    """LLM 서버 연결 실패"""
    pass

class LLMAuthenticationError(LLMClientError):
    """LLM API 인증 실패 (잘못된 API Key)"""
    pass

class LLMRateLimitError(LLMClientError):
    """LLM API Rate Limit 초과"""
    pass

class LLMTimeoutError(LLMClientError):
    """LLM API 타임아웃"""
    pass
```

**OllamaClient에 재시도 로직 추가**:

```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class OllamaClient(ILLMClient):
    # ... 기존 코드 ...

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.ConnectError, httpx.TimeoutException))
    )
    async def list_models(self) -> List[str]:
        """사용 가능한 모델 목록 조회 (재시도 3회)"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/models")
                response.raise_for_status()
                data = response.json()
                return [model['id'] for model in data.get('data', [])]
        except httpx.ConnectError as e:
            raise LLMConnectionError(f"Cannot connect to {self.base_url}: {e}")
        except httpx.TimeoutException as e:
            raise LLMTimeoutError(f"Request timeout to {self.base_url}: {e}")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise LLMAuthenticationError("Invalid API credentials")
            elif e.response.status_code == 429:
                raise LLMRateLimitError("Rate limit exceeded")
            else:
                raise LLMClientError(f"HTTP error {e.response.status_code}: {e}")
        except Exception as e:
            raise LLMClientError(f"Unexpected error: {e}")
```

**추가 의존성**:
```toml
# pyproject.toml
[project.dependencies]
tenacity = "^8.2.0"  # 재시도 로직
```

---

#### 4. **Phase 3 개선사항: Anthropic (Claude) Client 추가**

**AnthropicClient 구현** (GeminiClient와 동등한 우선순위로 격상):

```python
# arch_copilot/infrastructure/ai_client/anthropic_client.py

import anthropic
from typing import List, Dict
from arch_copilot.domain.ai.i_llm_client import ILLMClient

class AnthropicClient(ILLMClient):
    """Anthropic Claude API 클라이언트"""

    def __init__(self, api_key: str, model_name: str = "claude-3-5-sonnet-20241022") -> None:
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model_name = model_name

    async def generate(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> str:
        """Claude는 비동기를 직접 지원하지 않으므로 run_in_executor 사용"""
        import asyncio
        loop = asyncio.get_event_loop()

        def _generate():
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text

        return await loop.run_in_executor(None, _generate)

    async def chat_completion(self, messages: List[Dict[str, str]], max_tokens: int = 2048, temperature: float = 0.7) -> str:
        import asyncio
        loop = asyncio.get_event_loop()

        def _chat():
            # OpenAI 형식을 Anthropic 형식으로 변환
            anthropic_messages = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in messages
            ]

            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=anthropic_messages
            )
            return message.content[0].text

        return await loop.run_in_executor(None, _chat)

    async def check_health(self) -> bool:
        try:
            models = await self.list_models()
            return len(models) > 0
        except Exception:
            return False

    async def list_models(self) -> List[str]:
        """Anthropic은 공식 모델 목록 API가 없으므로 하드코딩"""
        import asyncio
        loop = asyncio.get_event_loop()

        def _list():
            # 2025년 기준 Claude 모델 목록
            return [
                "claude-3-5-sonnet-20241022",
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307",
                "claude-2.1",
                "claude-2.0"
            ]

        return await loop.run_in_executor(None, _list)
```

**Factory 업데이트**:

```python
# llm_client_factory.py

from arch_copilot.infrastructure.ai_client.anthropic_client import AnthropicClient

class LLMClientFactory:
    @staticmethod
    def create(config: IConfig) -> ILLMClient:
        # ... 기존 코드 ...

        elif provider == 'anthropic':
            if not config.llm_api_key:
                raise ValueError("Anthropic requires llm_api_key in config")
            api_key = config.llm_api_key.get_secret_value()
            return AnthropicClient(api_key=api_key, model_name=config.llm_model)
```

---

#### 5. **Phase 4 개선사항: 설정 유효성 검사 UI**

**Settings 페이지에 실시간 검증 추가**:

```python
# settings_page.py

async def validate_settings():
    """설정 저장 전 유효성 검사"""
    errors = []

    # Provider별 필수 필드 검증
    if state['provider'] in ['ollama', 'lmstudio', 'vllm']:
        if not state['base_url']:
            errors.append("Base URL is required for local providers")
        elif not state['base_url'].startswith(('http://', 'https://')):
            errors.append("Base URL must start with http:// or https://")

    if state['provider'] in ['gemini', 'openai', 'anthropic']:
        if not state['api_key']:
            errors.append("API Key is required for cloud providers")
        elif len(state['api_key']) < 10:
            errors.append("API Key seems too short (minimum 10 characters)")

    # 모델 이름 검증
    if not state['model']:
        errors.append("Model name is required")

    if errors:
        for error in errors:
            ui.notify(error, type='negative')
        return False

    return True

async def test_connection():
    """설정 저장 전 연결 테스트"""
    ui.notify('연결 테스트 중...', type='info')

    try:
        from arch_copilot.infrastructure.config.config import Config
        temp_config = Config(
            llm_provider=state['provider'],
            llm_base_url=state['base_url'],
            llm_api_key=state['api_key'] if state['api_key'] else None,
            llm_model=state['model']
        )

        client = LLMClientFactory.create(temp_config)
        is_healthy = await client.check_health()

        if is_healthy:
            ui.notify('✅ 연결 성공! 서버가 정상 응답합니다.', type='positive')
            return True
        else:
            ui.notify('⚠️ 서버에 연결할 수 없습니다.', type='warning')
            return False

    except Exception as e:
        ui.notify(f'❌ 연결 테스트 실패: {str(e)}', type='negative')
        return False

def save_settings():
    """설정을 .env 파일에 저장 (검증 추가)"""
    # 유효성 검사 먼저 실행
    if not await validate_settings():
        return

    try:
        config.update_settings({
            'llm_provider': state['provider'],
            'llm_base_url': state['base_url'] if state['provider'] in ['ollama', 'lmstudio', 'vllm'] else None,
            'llm_api_key': state['api_key'] if state['provider'] in ['gemini', 'openai', 'anthropic'] else None,
            'llm_model': state['model']
        })

        ui.notify('✅ 설정이 저장되었습니다. 애플리케이션을 재시작하여 적용하세요.', type='positive')

    except Exception as e:
        ui.notify(f'❌ 설정 저장 실패: {str(e)}', type='negative')
```

**UI에 "TEST CONNECTION" 버튼 추가**:

```python
# settings_page.py - 저장 버튼 섹션

with ui.row().classes('w-full gap-4 justify-end'):
    ui.button(
        'TEST CONNECTION',
        icon='cable',
        on_click=lambda: test_connection()
    ).props('outlined rounded-full').classes('px-8 py-3 text-primary border-primary')

    ui.button(
        'SAVE CHANGES',
        icon='save',
        on_click=lambda: save_settings()
    ).props('unelevated rounded-full').classes('px-10 py-3 bg-primary text-white font-bold')
```

---

#### 6. **통합 테스트 Phase 추가 (Phase 5 권장)**

**Goal**: 전체 워크플로우 End-to-End 테스트
**Estimated Time**: 1-2 hours
**Status**: ⏳ Pending
**Dependencies**: Phase 1-4 완료

**Tasks**:

**🔴 RED: Write Failing Integration Tests First**
- [ ] **Test 5.1**: 전체 워크플로우 통합 테스트
  - File(s): `tests/integration/test_multi_provider_e2e.py` (NEW)
  - Expected: 통합 테스트 환경 미구축으로 실패
  - Details: 테스트 시나리오:
    ```python
    import pytest
    from arch_copilot.infrastructure.config.config import Config
    from arch_copilot.infrastructure.ai_client.llm_client_factory import LLMClientFactory
    from arch_copilot.infrastructure.di.bootstrap import bootstrap_container
    from arch_copilot.infrastructure.di.container import get_container
    from arch_copilot.application.use_cases.analyze_project import AnalyzeProjectUseCase

    @pytest.mark.asyncio
    async def test_e2e_ollama_provider_analysis():
        """E2E: Ollama Provider 선택 → 분석 실행"""
        # 1. Config 설정
        config = Config(
            llm_provider='ollama',
            llm_base_url='http://localhost:11434/v1',
            llm_model='mistral-24b:latest'
        )

        # 2. Factory로 클라이언트 생성
        client = LLMClientFactory.create(config)

        # 3. Health Check
        assert await client.check_health() is True

        # 4. 모델 목록 조회
        models = await client.list_models()
        assert 'mistral-24b:latest' in models

        # 5. DI Container 통합 (실제 분석 UseCase 실행)
        bootstrap_container()
        container = get_container()
        use_case = container.resolve(AnalyzeProjectUseCase)

        # 6. 프로젝트 분석 실행 (간단한 테스트 프로젝트)
        from arch_copilot.application.dtos.analysis_dtos import AnalysisRequest
        request = AnalysisRequest(project_path=Path("./tests/fixtures/sample_project"))
        result = use_case.execute(request)

        # 7. AI 분석 결과 포함 확인
        assert result.ai_recommendations is not None
        assert len(result.ai_recommendations) > 0
    ```

**🟢 GREEN: Implement Integration Test Infrastructure**
- [ ] **Task 5.2**: 테스트 픽스처 준비
  - File(s): `tests/fixtures/sample_project/` (NEW)
  - Goal: 간단한 Python 프로젝트 구조 생성 (의도적인 Clean Architecture 위반 포함)

- [ ] **Task 5.3**: Mock Ollama 서버 구축 (선택사항)
  - File(s): `tests/mocks/mock_ollama_server.py` (NEW)
  - Goal: 실제 Ollama 서버 없이도 테스트 가능하도록 Mock HTTP 서버 구축

**Quality Gate**:
- [ ] 전체 워크플로우 E2E 테스트 통과
- [ ] 모든 Provider (Ollama, Gemini, Anthropic) 통합 테스트 성공 (Mock 사용)
- [ ] DI Container와 Factory 통합 검증

---

#### 7. **문서화 개선사항**

**추가할 문서**:

1. **`docs/guides/MULTI_PROVIDER_SETUP.md`** (사용자 가이드)
   - Ollama 설치 방법
   - LMStudio 설치 방법
   - Gemini API Key 발급 방법
   - Anthropic API Key 발급 방법
   - Settings 페이지 사용법 (스크린샷 포함)

2. **`docs/api/LLM_CLIENT_INTERFACE.md`** (개발자 문서)
   - ILLMClient 인터페이스 사양
   - 새로운 Provider 추가 방법
   - Factory 확장 가이드

3. **README.md 업데이트**:
   ```markdown
   ## Supported LLM Providers

   Local Arch-Copilot supports multiple LLM providers:

   | Provider | Type | Setup |
   |----------|------|-------|
   | Ollama | Local | [Install Ollama](https://ollama.ai) |
   | LMStudio | Local | [Install LMStudio](https://lmstudio.ai) |
   | Google Gemini | Cloud | [Get API Key](https://ai.google.dev) |
   | Anthropic Claude | Cloud | [Get API Key](https://console.anthropic.com) |
   | OpenAI GPT | Cloud | [Get API Key](https://platform.openai.com) |

   Configure your preferred provider in the Settings page.
   ```

---

#### 8. **성능 최적화 고려사항**

**추가 개선사항**:

1. **클라이언트 인스턴스 캐싱**:
   ```python
   # bootstrap.py

   def bootstrap_container() -> None:
       container = get_container()
       config = container.resolve(IConfig)

       # Factory로 클라이언트 생성 (싱글톤으로 캐싱)
       llm_client = LLMClientFactory.create(config)
       container.register_singleton(ILLMClient, llm_client)

       # VLLMAnalyzer에 ILLMClient 주입
       vllm_analyzer = VLLMAnalyzer(llm_client)
       container.register_singleton(IAIAnalyzer, vllm_analyzer)
   ```

2. **모델 목록 캐싱** (1시간 TTL):
   ```python
   from functools import lru_cache
   import time

   class OllamaClient(ILLMClient):
       _model_cache: List[str] = []
       _cache_time: float = 0
       _cache_ttl: int = 3600  # 1시간

       async def list_models(self) -> List[str]:
           """모델 목록 조회 (1시간 캐싱)"""
           current_time = time.time()

           if self._model_cache and (current_time - self._cache_time) < self._cache_ttl:
               return self._model_cache

           # 캐시 미스: 실제 API 호출
           models = await self._fetch_models_from_api()
           self._model_cache = models
           self._cache_time = current_time

           return models
   ```

---

#### 9. **보안 강화사항**

**추가 보안 조치**:

1. **.env 파일 암호화** (선택사항, 향후 고도화):
   ```python
   # 간단한 암호화 예시 (실제로는 cryptography 라이브러리 사용 권장)
   from cryptography.fernet import Fernet

   def encrypt_api_key(api_key: str, encryption_key: bytes) -> str:
       f = Fernet(encryption_key)
       return f.encrypt(api_key.encode()).decode()

   def decrypt_api_key(encrypted_key: str, encryption_key: bytes) -> str:
       f = Fernet(encryption_key)
       return f.decrypt(encrypted_key.encode()).decode()
   ```

2. **API Key 길이 검증**:
   ```python
   @field_validator("llm_api_key")
   @classmethod
   def validate_api_key_format(cls, v: SecretStr | None) -> SecretStr | None:
       if v is None:
           return v

       key = v.get_secret_value()

       # Provider별 API Key 형식 검증
       if key.startswith('sk-'):  # OpenAI
           if len(key) < 40:
               raise ValueError("OpenAI API key seems invalid (too short)")
       elif key.startswith('AIza'):  # Gemini
           if len(key) < 39:
               raise ValueError("Gemini API key seems invalid (too short)")
       elif key.startswith('sk-ant-'):  # Anthropic
           if len(key) < 50:
               raise ValueError("Anthropic API key seems invalid (too short)")

       return v
   ```

---

#### 10. **CI/CD 파이프라인 통합**

**추가할 GitHub Actions Workflow**:

```yaml
# .github/workflows/multi-provider-tests.yml

name: Multi-Provider LLM Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -e .[dev,test]
        pip install google-generativeai anthropic openai

    - name: Run unit tests
      run: |
        pytest tests/unit/ -v --cov=arch_copilot --cov-report=xml

    - name: Run integration tests (Mock mode)
      env:
        LLM_PROVIDER: ollama
        LLM_BASE_URL: http://mock-server:11434/v1
      run: |
        pytest tests/integration/ -v -m "not real_api"

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

## 📊 Updated Time Estimates

| Phase | Original Estimate | With Enhancements | Total |
|-------|-------------------|-------------------|-------|
| **Phase 0** | - | 0.5-1 hour | 0.5-1 hour |
| **Phase 1** | 2-3 hours | +0.5 hour (validation) | 2.5-3.5 hours |
| **Phase 2** | 3-4 hours | +1 hour (error handling) | 4-5 hours |
| **Phase 3** | 2-3 hours | +1 hour (Anthropic) | 3-4 hours |
| **Phase 4** | 3-4 hours | +1 hour (validation UI) | 4-5 hours |
| **Phase 5** | - | 1-2 hours | 1-2 hours |
| **Documentation** | - | 1 hour | 1 hour |
| **Total** | 10-14 hours | +5-6 hours | **15-20 hours** |

---

## ✅ Enhanced Final Checklist

**Before marking plan as COMPLETE**:
- [ ] All 5 phases completed (including Phase 0 and Phase 5)
- [ ] Settings 페이지에서 모든 Provider 선택 가능
- [ ] 로컬 Provider (Ollama) 모델 목록 동적 로드 확인
- [ ] 클라우드 Provider (Gemini, Anthropic) 모델 목록 동적 로드 확인
- [ ] .env 파일에 설정 정상 저장 확인
- [ ] AI 분석 시 선택된 클라이언트로 동작 확인
- [ ] Test coverage ≥80% overall
- [ ] Clean Architecture 의존성 규칙 준수 확인
- [ ] API Key 보안 검증 (로그에 평문 노출 없음)
- [ ] 성능 저하 없음 (UI 반응성 유지)
- [ ] **NEW**: 연결 테스트 기능 동작 확인
- [ ] **NEW**: Provider별 필수 필드 검증 동작 확인
- [ ] **NEW**: 에러 재시도 로직 동작 확인 (3회 재시도)
- [ ] **NEW**: E2E 통합 테스트 통과
- [ ] **NEW**: 사용자 가이드 문서 작성 완료
- [ ] **NEW**: CI/CD 파이프라인 통과

---

**Plan Status**: 🔄 Enhanced & Ready to Implement
**Next Action**: Phase 0 시작 - 개발 환경 설정 및 의존성 설치
**Blocked By**: None
**Last Updated**: 2025-12-30 (Enhanced)
