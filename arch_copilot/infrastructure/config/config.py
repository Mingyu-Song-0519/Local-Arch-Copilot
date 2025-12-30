"""
Configuration Implementation
"""

from pathlib import Path

from typing import Any, Literal
from pydantic import Field, SecretStr, field_validator
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

    # Multi-Provider LLM
    llm_provider: Literal["vllm", "ollama", "lmstudio", "gemini", "openai", "anthropic"] = Field(
        default="vllm"
    )
    llm_base_url: str | None = Field(default=None)
    llm_api_key: SecretStr | None = Field(default=None)
    llm_model: str = Field(default="mistral-24b:latest")

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
                # SecretStr 처리
                str_val = value.get_secret_value() if isinstance(value, SecretStr) else str(value)
                env_updates[env_key] = str_val
            else:
                env_updates[env_key] = ""

        # 기존 라인 업데이트 또는 추가
        updated_keys = set()
        new_lines = []
        for line in lines:
            if "=" in line and not line.strip().startswith("#"):
                key = line.split("=", 1)[0].strip()
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
        env_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

        # 현재 인스턴스 업데이트 (runtime)
        for key, value in settings.items():
            if hasattr(self, key):
                # 타입 변환 처리 (필요 시)
                setattr(self, key, value)
