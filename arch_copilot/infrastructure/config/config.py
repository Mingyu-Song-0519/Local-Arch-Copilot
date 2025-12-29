"""
Configuration Implementation
"""

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from arch_copilot.domain.config.i_config import IConfig


class Config(BaseSettings):
    """
    환경 변수 및 .env 파일 기반 설정 구현체
    """

    # AI Infrastructure
    vllm_base_url: str = Field(default="http://localhost:8000")
    vllm_model_name: str = Field(default="openai/gpt-oss-20b")
    max_context_length: int = Field(default=16384)
    temperature: float = Field(default=0.1)

    # Application
    cache_dir: Path = Field(default=Path("./storage/cache"))
    log_level: str = Field(default="INFO")

    # UI
    ui_port: int = Field(default=8080)
    ui_title: str = Field(default="Local Arch-Copilot")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @field_validator("vllm_base_url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return v

    @field_validator("ui_port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        if not (1024 <= v <= 65535):
            raise ValueError("Port must be between 1024 and 65535")
        return v
