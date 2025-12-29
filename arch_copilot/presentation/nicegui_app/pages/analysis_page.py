"""
Main Analysis Page

프로젝트 경로 선택, 스캔 시작 및 결과 요약을 보여줍니다.
"""

from pathlib import Path
from nicegui import ui
from arch_copilot.presentation.nicegui_app.layouts.base_layout import base_layout
from arch_copilot.infrastructure.di.container import get_container
from arch_copilot.application.use_cases.analyze_project import AnalyzeProjectUseCase
from arch_copilot.application.dtos.analysis_dtos import AnalysisRequest
from arch_copilot.infrastructure.ast_parser.project_scanner import ASTProjectScanner
from arch_copilot.infrastructure.graph_engine.graph_engine import GraphEngine
from arch_copilot.presentation.nicegui_app.components.graph_view import GraphView

def analysis_page():
    container = get_container()
    analyze_use_case = container.resolve(AnalyzeProjectUseCase)
    scanner = container.resolve(ASTProjectScanner)
    graph_engine = container.resolve(GraphEngine)
    graph_view = GraphView()

    state = {
        'analyzing': False,
        'result': None,
        'graph_data': None
    }

    @ui.refreshable
    def stats_section():
        with ui.row().classes('w-full gap-8'):
            # Statistics Card
            with ui.card().classes('flex-1 p-6 bg-zinc-900/30 border border-zinc-800 rounded-2xl'):
                ui.label('Project Statistics').classes('text-gray-500 text-sm italic')
                if state['result']:
                    ui.label(f"Files: {state['result'].total_files}").classes('text-2xl font-bold')
                    ui.label(f"Violations: {len(state['result'].violations)}").classes('text-xl text-red-400')
                else:
                    ui.label('No analysis performed yet.').classes('text-gray-400')

            # System Status Card
            with ui.card().classes('flex-1 p-6 bg-zinc-900/30 border border-zinc-800 rounded-2xl'):
                ui.label('System Health').classes('text-gray-500 text-sm italic')
                with ui.row().classes('items-center gap-2'):
                    ui.icon('check_circle', color='green')
                    ui.label('AI Engine: vLLM (Running)').classes('text-green-400 font-medium')
                if state['analyzing']:
                    ui.spinner(size='sm').classes('mt-2')
                    ui.label('Analyzing project structure...').classes('text-xs text-primary animate-pulse')

    @ui.refreshable
    def graph_section():
        if state['graph_data']:
            graph_view.render(state['graph_data'])
        else:
            ui.label('Graph visualization will appear here...').classes('text-gray-500 text-center py-20 border-2 border-dashed border-zinc-800 rounded-3xl w-full')

    @ui.refreshable
    def violations_section():
        if state['result'] and state['result'].violations:
            with ui.column().classes('w-full gap-4'):
                for v in state['result'].violations:
                    with ui.card().classes('w-full p-4 bg-red-900/10 border border-red-900/30 rounded-xl'):
                        with ui.row().classes('items-center justify-between w-full'):
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('warning', color='red-500')
                                ui.label(v.violation_type.value).classes('font-bold text-red-400')
                            ui.label(str(v.source_file)).classes('text-xs text-gray-500')
                        ui.label(v.message).classes('mt-2 text-gray-300')
        elif state['result']:
            ui.label('No violations found! Great job.').classes('text-green-400 text-center py-10 w-full')
        else:
            ui.label('Violation details will appear here after analysis.').classes('text-gray-500 text-center py-10 w-full')

    async def start_analysis():
        path_str = path_input.value
        if not path_str:
            ui.notify('Please enter a project path.', type='warning')
            return
        
        root_path = Path(path_str)
        if not root_path.exists():
            ui.notify('Path does not exist.', type='negative')
            return

        state['analyzing'] = True
        stats_section.refresh()
        
        try:
            # 1. Scan Project
            project_structure = scanner.scan(root_path)
            
            # 2. Build Graph
            graph_engine.build_graph(project_structure)
            state['graph_data'] = graph_engine.graph
            
            # 3. Analyze Violations
            request = AnalysisRequest(project_path=root_path)
            state['result'] = analyze_use_case.execute(request)
            
            ui.notify('Analysis completed!', type='positive')
        except Exception as e:
            ui.notify(f'Error: {str(e)}', type='negative')
        finally:
            state['analyzing'] = False
            stats_section.refresh()
            graph_section.refresh()
            violations_section.refresh()

    with base_layout("Architecture Dashboard"):
        # Hero Section
        with ui.column().classes('w-full gap-4'):
            ui.label('AI-Powered Architecture Analysis').classes('text-4xl font-extrabold text-white')
            ui.label('Clean Architecture 규칙 준수 여부와 순환 참조를 즉시 진단합니다.').classes('text-xl text-gray-400')

        # Control Panel
        with ui.card().classes('w-full p-8 bg-zinc-900/50 border border-zinc-800 backdrop-blur-xl rounded-3xl'):
            ui.label('Project Scan Configuration').classes('text-lg font-semibold text-primary mb-4')
            with ui.row().classes('w-full items-center gap-4'):
                path_input = ui.input(label='Target Project Path', placeholder='E:/MyProjects/AwesomeApp').classes('flex-grow')
                ui.button('START ANALYSIS', icon='rocket_launch', on_click=start_analysis).props('unelevated rounded-full').classes('px-8 py-2')

        stats_section()

        # Tabs
        with ui.tabs().classes('w-full text-white mt-4') as tabs:
            ui.tab('DEPENDENCY GRAPH')
            ui.tab('VIOLATION LIST')
            ui.tab('AI ANALYSIS (BETA)')
        
        with ui.tab_panels(tabs, value='DEPENDENCY GRAPH').classes('w-full bg-transparent'):
            with ui.tab_panel('DEPENDENCY GRAPH'):
                graph_section()
            with ui.tab_panel('VIOLATION LIST'):
                violations_section()
            with ui.tab_panel('AI ANALYSIS (BETA)'):
                ui.label('Advanced AI reasoning on architectural debt.').classes('text-gray-500')
