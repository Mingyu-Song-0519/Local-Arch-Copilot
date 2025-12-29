"""
Application Layer 단위 테스트

도메인 서비스를 모킹하여 유스케이스의 제어 흐름을 검증합니다.
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from arch_copilot.application.dtos.analysis_dtos import AnalysisRequest
from arch_copilot.application.use_cases.analyze_project import AnalyzeProjectUseCase
from arch_copilot.domain.entities.project import ProjectStructure
from arch_copilot.domain.services.analysis_service import AnalysisService


class TestApplicationLayer:
    """애플리케이션 레이어 테스트 클래스"""

    @pytest.fixture
    def mock_analysis_service(self) -> MagicMock:
        return MagicMock(spec=AnalysisService)

    @pytest.fixture
    def analyze_use_case(self, mock_analysis_service: MagicMock) -> AnalyzeProjectUseCase:
        return AnalyzeProjectUseCase(analysis_service=mock_analysis_service)

    def test_analyze_project_use_case_success(
        self, analyze_use_case: AnalyzeProjectUseCase, mock_analysis_service: MagicMock
    ) -> None:
        """분석 유스케이스 성공 시나리오 테스트"""
        # Given
        request = AnalysisRequest(project_path=Path("/test/project"))
        mock_analysis_service.detect_static_violations.return_value = []

        # When
        result = analyze_use_case.execute(request)

        # Then
        assert result.project_path == Path("/test/project")
        assert result.error_message is None
        assert "Analyzed 0 files" in result.summary
        mock_analysis_service.detect_static_violations.assert_called_once()
        assert isinstance(mock_analysis_service.detect_static_violations.call_args[0][0], ProjectStructure)

    def test_analyze_project_use_case_failure(
        self, analyze_use_case: AnalyzeProjectUseCase, mock_analysis_service: MagicMock
    ) -> None:
        """분석 유스케이스 에러 발생 시 시나리오 테스트"""
        # Given
        request = AnalysisRequest(project_path=Path("/test/project"))
        mock_analysis_service.detect_static_violations.side_effect = Exception("Domain Error")

        # When
        result = analyze_use_case.execute(request)

        # Then
        assert result.error_message is not None
        assert "Domain Error" in result.error_message
        assert result.summary == "Analysis failed."
