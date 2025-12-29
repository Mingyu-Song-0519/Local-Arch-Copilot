"""
Graph Page

의존성 그래프를 전체 화면으로 상세히 보여주는 페이지입니다.
"""

from nicegui import ui
from arch_copilot.presentation.nicegui_app.layouts.base_layout import base_layout
from arch_copilot.infrastructure.di.container import get_container
from arch_copilot.infrastructure.graph_engine.graph_engine import GraphEngine
from arch_copilot.presentation.nicegui_app.components.graph_view import GraphView


def graph_page():
    container = get_container()
    graph_engine = container.resolve(GraphEngine)
    graph_view = GraphView(container_classes='w-full h-[80vh] bg-zinc-900/10 border border-zinc-800 rounded-3xl')

    with base_layout("Dependency Graph View"):
        with ui.column().classes('w-full gap-4'):
            ui.label('Full Dependency Visualization').classes('text-3xl font-bold text-white')
            ui.label('프로젝트 내 모든 파일 간의 의존성 관계를 네트워크 그래프로 확인합니다.').classes('text-gray-400')
        
        if graph_engine.graph and len(graph_engine.graph.nodes) > 0:
            graph_view.render(graph_engine.graph)
        else:
            with ui.card().classes('w-full p-20 items-center justify-center bg-zinc-900/30 border border-zinc-800 border-dashed rounded-3xl'):
                ui.icon('hub', size='64px').classes('text-gray-700')
                ui.label('No graph data available. Please run an analysis first on the Dashboard.').classes('text-gray-500 mt-4')
                ui.button('Go to Dashboard', on_click=lambda: ui.navigate.to('/')).props('flat')
