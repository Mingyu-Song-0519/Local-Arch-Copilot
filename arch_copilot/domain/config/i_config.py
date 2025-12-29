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
