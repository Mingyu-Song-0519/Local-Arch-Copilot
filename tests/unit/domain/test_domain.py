"""
Domain Layer 단위 테스트

엔티티와 서비스의 비즈니스 로직을 검증합니다.
"""

from pathlib import Path

import pytest

from arch_copilot.domain.entities.project import FileNode, ProjectStructure
from arch_copilot.domain.entities.violation import ViolationType
from arch_copilot.domain.services.analysis_service import AnalysisService


class TestDomainLayer:
    """도메인 레이어 테스트 클래스"""

    @pytest.fixture
    def analysis_service(self) -> AnalysisService:
        return AnalysisService()

    @pytest.fixture
    def sample_project(self) -> ProjectStructure:
        project = ProjectStructure(root_path=Path("/test_project"))
        
        # 정상적인 의존성: Presentation -> Application -> Domain
        project.add_file(FileNode(path=Path("domain/user.py"), layer="domain"))
        project.add_file(FileNode(
            path=Path("application/service.py"), 
            layer="application",
            imports={"test_project.domain.user"}
        ))
        project.add_file(FileNode(
            path=Path("presentation/ui.py"), 
            layer="presentation",
            imports={"test_project.application.service"}
        ))
        
        # 위반 사항: Domain -> Application (상위 레이어가 하위 레이어 참조)
        project.add_file(FileNode(
            path=Path("domain/bad_entity.py"), 
            layer="domain",
            imports={"test_project.application.service"}
        ))
        
        # 위반 사항: 알 수 없는 레이어
        project.add_file(FileNode(path=Path("unknown/file.py"), layer="external"))
        
        return project

    def test_should_detect_layer_misuse(self, analysis_service: AnalysisService, sample_project: ProjectStructure) -> None:
        """계층 간 의존성 규칙 위반 탐지 확인"""
        violations = analysis_service.detect_static_violations(sample_project)
        
        # 위반 사항 1: domain/bad_entity.py -> application/service.py (LAYER_MISMATCH)
        # 위반 사항 2: unknown/file.py (UNDEFINED_LAYER)
        
        violation_types = [v.violation_type for v in violations]
        assert ViolationType.LAYER_MISMATCH in violation_types
        assert ViolationType.UNDEFINED_LAYER in violation_types
        
        # 상세 메시지 확인
        mismatch = next(v for v in violations if v.violation_type == ViolationType.LAYER_MISMATCH)
        assert mismatch.source_file == Path("domain/bad_entity.py")
        assert "domain" in mismatch.message
        assert "application" in mismatch.message

    def test_file_node_helper_methods(self) -> None:
        """FileNode의 헬퍼 메서드 확인"""
        node = FileNode(path=Path("test.py"), layer="domain")
        assert node.is_in_layer("domain") is True
        assert node.is_in_layer("application") is False

    def test_project_structure_aggregation(self, sample_project: ProjectStructure) -> None:
        """ProjectStructure의 집계 기능 확인"""
        assert sample_project.total_files == 5
        domain_files = sample_project.get_layer_files("domain")
        assert len(domain_files) == 2
        assert all(f.layer == "domain" for f in domain_files)
