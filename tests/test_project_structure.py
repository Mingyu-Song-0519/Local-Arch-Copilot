"""
프로젝트 구조 검증 테스트

Clean Architecture 디렉토리 구조가 올바르게 생성되었는지 확인합니다.
"""

from pathlib import Path

import pytest


class TestProjectStructure:
    """프로젝트 구조 검증"""

    @pytest.fixture
    def project_root(self) -> Path:
        """프로젝트 루트 경로"""
        return Path(__file__).parent.parent

    def test_should_have_arch_copilot_package(self, project_root: Path) -> None:
        """arch_copilot 패키지가 존재해야 함"""
        assert (project_root / "arch_copilot").is_dir()
        assert (project_root / "arch_copilot" / "__init__.py").is_file()

    def test_should_have_domain_layer(self, project_root: Path) -> None:
        """Domain 레이어가 존재해야 함"""
        domain_path = project_root / "arch_copilot" / "domain"
        assert domain_path.is_dir()
        assert (domain_path / "__init__.py").is_file()
        assert (domain_path / "entities").is_dir()
        assert (domain_path / "repositories").is_dir()
        assert (domain_path / "services").is_dir()

    def test_should_have_application_layer(self, project_root: Path) -> None:
        """Application 레이어가 존재해야 함"""
        app_path = project_root / "arch_copilot" / "application"
        assert app_path.is_dir()
        assert (app_path / "__init__.py").is_file()
        assert (app_path / "use_cases").is_dir()
        assert (app_path / "dtos").is_dir()
        assert (app_path / "services").is_dir()

    def test_should_have_infrastructure_layer(self, project_root: Path) -> None:
        """Infrastructure 레이어가 존재해야 함"""
        infra_path = project_root / "arch_copilot" / "infrastructure"
        assert infra_path.is_dir()
        assert (infra_path / "__init__.py").is_file()
        assert (infra_path / "ast_parser").is_dir()
        assert (infra_path / "graph_engine").is_dir()
        assert (infra_path / "ai_client").is_dir()
        assert (infra_path / "repositories").is_dir()

    def test_should_have_presentation_layer(self, project_root: Path) -> None:
        """Presentation 레이어가 존재해야 함"""
        pres_path = project_root / "arch_copilot" / "presentation"
        assert pres_path.is_dir()
        assert (pres_path / "__init__.py").is_file()
        assert (pres_path / "nicegui_app").is_dir()

    def test_should_have_test_directories(self, project_root: Path) -> None:
        """테스트 디렉토리 구조가 존재해야 함"""
        tests_path = project_root / "tests"
        assert (tests_path / "unit").is_dir()
        assert (tests_path / "integration").is_dir()
        assert (tests_path / "e2e").is_dir()

    def test_should_have_pyproject_toml(self, project_root: Path) -> None:
        """pyproject.toml이 존재해야 함"""
        assert (project_root / "pyproject.toml").is_file()

    def test_should_be_importable(self) -> None:
        """arch_copilot 패키지가 import 가능해야 함"""
        import arch_copilot

        assert arch_copilot.__version__ == "0.1.0"
