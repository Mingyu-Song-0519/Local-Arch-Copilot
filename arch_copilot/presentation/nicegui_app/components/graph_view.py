"""
Graph View Component (using NetworkX & Cytoscape-like library or SVG)

NiceGUI에서 의존성 그래프를 시각적으로 표현합니다.
"""

from nicegui import ui
import networkx as nx


class GraphView:
    """의존성 그래프 시각화 컴포넌트"""

    def __init__(self, container_classes: str = 'w-full h-[500px] border border-zinc-800 rounded-3xl overflow-hidden') -> None:
        self.container_classes = container_classes

    def render(self, graph: nx.DiGraph):
        """NetworkX 그래프를 기반으로 시각화 레이아웃을 생성합니다."""
        with ui.column().classes(self.container_classes):
            if not graph or len(graph.nodes) == 0:
                ui.label('No graph data available.').classes('m-auto text-gray-500')
                return

            ui.label(f'Project Dependency Graph ({len(graph.nodes)} nodes)').classes('p-4 text-xs text-gray-400')
            
            # Simple list-based or Mermaid based visualization for now
            # (In a real app, use a dedicated cytoscape or d3 wrapper)
            mermaid_code = self._to_mermaid(graph)
            ui.mermaid(mermaid_code).classes('w-full flex-grow')

    def _to_mermaid(self, graph: nx.DiGraph) -> str:
        """NetworkX 그래프를 Mermaid syntax로 변환합니다."""
        lines = ["graph TD"]
        for u, v in graph.edges:
            # 특수 문자 제거 및 간단한 ID 생성
            u_clean = u.replace(".", "_").replace("/", "_").replace("-", "_").replace(" ", "_")
            v_clean = v.replace(".", "_").replace("/", "_").replace("-", "_").replace(" ", "_")
            lines.append(f"  {u_clean}[\"{u}\"] --> {v_clean}[\"{v}\"]")
        
        # 레이어별 스타일링 (Subgraphs)
        # TODO: 계층별로 묶어주는 로직 추가 가능
        
        return "\n".join(lines)
