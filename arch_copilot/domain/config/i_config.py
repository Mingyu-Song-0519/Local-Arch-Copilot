from typing import Protocol


class IConfig(Protocol):
    """Configuration 인터페이스"""

    @property
    def vllm_base_url(self) -> str:
        """vLLM 서버 기본 URL"""
        ...

    @property
    def vllm_model_name(self) -> str:
        """사용할 모델 이름"""
        ...

    # --- 멀티 LLM 공급자 설정 ---
    @property
    def llm_provider(self) -> str:
        """LLM 공급자 (vllm, ollama, lmstudio, gemini, openai, anthropic)"""
        ...

    @property
    def llm_base_url(self) -> str | None:
        """로컬 LLM 서버 URL (Ollama/LMStudio용)"""
        ...

    @property
    def llm_api_key(self) -> str | None:
        """클라우드 LLM API Key (Gemini/OpenAI용)"""
        ...

    @property
    def llm_model(self) -> str:
        """선택된 모델 이름"""
        ...

    def update_settings(self, settings: dict[str, any]) -> None:
        """설정 업데이트 및 영구 저장"""
        ...

    @property
    def max_context_length(self) -> int:
        """최대 컨텍스트 길이"""
        ...

    @property
    def temperature(self) -> float:
        """생성 온도"""
        ...

    @property
    def ui_port(self) -> int:
        """UI 포트 번호"""
        ...

    @property
    def log_level(self) -> str:
        """로그 레벨"""
        ...
