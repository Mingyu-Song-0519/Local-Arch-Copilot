"""
Graph Engine 단위 테스트
"""

from pathlib import Path
import pytest

from arch_copilot.domain.entities.project import FileNode, ProjectStructure
from arch_copilot.domain.entities.violation import ViolationType
from arch_copilot.infrastructure.graph_engine.graph_engine import GraphEngine


class TestGraphEngine:
    """그래프 엔진 테스트"""

    @pytest.fixture
    def engine(self) -> GraphEngine:
        return GraphEngine()

    @pytest.fixture
    def circular_project(self) -> ProjectStructure:
        project = ProjectStructure(root_path=Path("/test"))
        # A -> B -> C -> A
        project.add_file(FileNode(path=Path("a.py"), imports={"b"}))
        project.add_file(FileNode(path=Path("b.py"), imports={"c"}))
        project.add_file(FileNode(path=Path("c.py"), imports={"a"}))
        return project

    def test_should_build_graph_and_detect_cycles(self, engine: GraphEngine, circular_project: ProjectStructure) -> None:
        """순환 참조 탐지 검증"""
        engine.build_graph(circular_project)
        print(f"\nDEBUG: Graph Edges: {list(engine.graph.edges)}")
        violations = engine.detect_cycles()
        
        assert len(violations) > 0
        assert any(v.violation_type == ViolationType.CIRCULAR_DEPENDENCY for v in violations)
        assert "Circular dependency detected" in violations[0].message
        assert "a.py" in violations[0].message
        assert "b.py" in violations[0].message
        assert "c.py" in violations[0].message

    def test_should_get_all_dependencies(self, engine: GraphEngine) -> None:
        """하위 의존성 추출 검증"""
        project = ProjectStructure(root_path=Path("/test"))
        project.add_file(FileNode(path=Path("top.py"), imports={"mid"}))
        project.add_file(FileNode(path=Path("mid.py"), imports={"bot"}))
        project.add_file(FileNode(path=Path("bot.py"), imports=set()))
        
        engine.build_graph(project)
        deps = engine.get_all_dependencies("top.py")
        
        assert "mid.py" in deps
        assert "bot.py" in deps
        assert len(deps) == 2
