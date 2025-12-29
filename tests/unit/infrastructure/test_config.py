"""
Configuration 테스트

환경 변수 로드, 기본값 설정, 검증 로직을 테스트합니다.
"""

import os
from pathlib import Path
from unittest import mock

import pytest
from pydantic import ValidationError

from arch_copilot.infrastructure.config.config import Config


class TestConfig:
    """Config 클래스 테스트"""

    @pytest.fixture
    def mock_env(self):
        """환경 변수 Mock"""
        with mock.patch.dict(os.environ, {}, clear=True):
            yield

    def test_should_load_defaults(self, mock_env) -> None:
        """기본값으로 설정 로드"""
        config = Config()

        assert config.vllm_base_url == "http://localhost:8000"
        assert config.vllm_model_name == "openai/gpt-oss-20b"
        assert config.max_context_length == 16384
        assert config.temperature == 0.1
        assert config.log_level == "INFO"
        assert config.ui_port == 8080

    def test_should_load_from_env_vars(self, mock_env) -> None:
        """환경 변수에서 설정 로드"""
        with mock.patch.dict(
            os.environ,
            {
                "VLLM_BASE_URL": "http://remote-server:8000",
                "UI_PORT": "9090",
                "TEMPERATURE": "0.7",
            },
        ):
            config = Config()
            assert config.vllm_base_url == "http://remote-server:8000"
            assert config.ui_port == 9090
            assert config.temperature == 0.7

    def test_should_validate_ui_port(self, mock_env) -> None:
        """포트 번호 범위 검증"""
        # 잘못된 포트 번호
        with mock.patch.dict(os.environ, {"UI_PORT": "70000"}):
            with pytest.raises(ValidationError):
                Config()

    def test_should_validate_vllm_url(self, mock_env) -> None:
        """URL 형식 검증"""
        # 잘못된 URL
        with mock.patch.dict(os.environ, {"VLLM_BASE_URL": "not-a-url"}):
            with pytest.raises(ValidationError):
                Config()
