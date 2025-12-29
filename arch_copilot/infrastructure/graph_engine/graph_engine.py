"""
Graph Engine Implementation using NetworkX

프로젝트 파일 간의 의존성을 그래프로 시각화하고 분석합니다.
"""

from pathlib import Path
from typing import List, Set, Tuple

import networkx as nx

from arch_copilot.domain.entities.project import ProjectStructure
from arch_copilot.domain.entities.violation import ArchitectureViolation, ViolationType


class GraphEngine:
    """NetworkX를 이용한 의존성 그래프 엔진"""

    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def build_graph(self, project: ProjectStructure) -> None:
        """ProjectStructure로부터 의존성 그래프를 빌드합니다."""
        self.graph.clear()
        
        # 노드 추가
        for file_path in project.files:
            node_name = str(file_path).replace("\\", "/")
            self.graph.add_node(node_name, layer=project.files[file_path].layer)
            
        # 에지 추가 (의존성)
        for file_path, node in project.files.items():
            source_name = str(file_path).replace("\\", "/")
            for imp in node.imports:
                target = self._find_target_file(imp, project)
                if target:
                    target_name = str(target).replace("\\", "/")
                    self.graph.add_edge(source_name, target_name)
                    # print(f"DEBUG: Edge added {source_name} -> {target_name}")

    def detect_cycles(self) -> List[ArchitectureViolation]:
        """순환 참조(Circular Dependency)를 탐지합니다."""
        violations = []
        cycles = list(nx.simple_cycles(self.graph))
        for cycle in cycles:
            # 순환 참조의 첫 번째 파일을 source로 간주
            violations.append(
                ArchitectureViolation(
                    violation_type=ViolationType.CIRCULAR_DEPENDENCY,
                    source_file=Path(cycle[0]),
                    message=f"Circular dependency detected: {' -> '.join(cycle)} -> {cycle[0]}"
                )
            )
        return violations

    def _find_target_file(self, import_str: str, project: ProjectStructure) -> str | None:
        """import 문자열에 해당하는 프로젝트 내 파일을 찾습니다."""
        potential_path = import_str.replace(".", "/")
        for file_path in project.files:
            file_str = str(file_path).replace("\\", "/")
            # 하위 모듈 또는 파일명만 매칭되어도 에지 생성 (테스트 대응 및 유연성)
            if (file_str == potential_path or 
                file_str == f"{potential_path}.py" or 
                file_str.endswith(f"/{potential_path}.py") or
                file_str.endswith(f"/{potential_path}") or
                file_str == f"{potential_path}/__init__.py" or
                potential_path == file_path.stem): # stem 기반 매칭 추가 (파일명만 있을 때)
                return str(file_path)
        return None

    def get_all_dependencies(self, file_path_str: str) -> Set[str]:
        """특정 파일의 모든 하위 의존성을 반환합니다."""
        if file_path_str not in self.graph:
            return set()
        return set(nx.descendants(self.graph, file_path_str))
