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

    def build_graph(self, project: ProjectStructure, violations: List[ArchitectureViolation] = None) -> nx.DiGraph:
        """ProjectStructure로부터 의존성 그래프를 빌드하며, 위반 사항 정보도 주입합니다."""
        graph = nx.DiGraph()
        
        # 1. 노드 추가
        for file_path in project.files:
            node_name = str(file_path).replace("\\", "/")
            graph.add_node(node_name, layer=project.files[file_path].layer)
            
        # 2. 에지 추가 (의존성)
        for file_path, node in project.files.items():
            source_name = str(file_path).replace("\\", "/")
            for imp in node.imports:
                target = self._find_target_file(imp, project)
                if target:
                    target_name = str(target).replace("\\", "/")
                    graph.add_edge(source_name, target_name, has_violation=False)
        
        # 3. 위반 사항 주입 (엣지 강조용)
        if violations:
            for v in violations:
                # source_file에서 target_file로의 의존성이 위반된 경우
                # v.message에 타겟 정보가 포함되어 있거나, source_file 기준으로 매칭 시도
                u = str(v.source_file).replace("\\", "/")
                # DiGraph의 모든 엣지를 돌며 source가 u인 것 중 위반과 관련된 엣지 탐색
                if u in graph:
                    for _, v_target, data in graph.edges(u, data=True):
                        # 간단한 정책: 위반 리스트에 있는 파일에서 나가는 모든 의존성 선에 마킹 (추후 정밀 매칭 가능)
                        data['has_violation'] = True
                        data['violation_message'] = v.message
        
        self.graph = graph
        print(f"DEBUG: Graph built. Nodes: {len(graph.nodes)}, Edges: {len(graph.edges)}, Violations Marked: {len(violations) if violations else 0}")
        return graph

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
