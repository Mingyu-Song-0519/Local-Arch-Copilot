"""
Main Analysis Page

프로젝트 경로 선택, 스캔 시작 및 결과 요약을 보여줍니다.
"""

from pathlib import Path
from datetime import datetime
import json
import asyncio
from nicegui import ui
from arch_copilot.presentation.nicegui_app.layouts.base_layout import base_layout
from arch_copilot.infrastructure.di.container import get_container
from arch_copilot.application.use_cases.analyze_project import AnalyzeProjectUseCase
from arch_copilot.application.dtos.analysis_dtos import AnalysisRequest
from arch_copilot.infrastructure.ast_parser.project_scanner import ASTProjectScanner
from arch_copilot.infrastructure.graph_engine.graph_engine import GraphEngine
from arch_copilot.presentation.nicegui_app.components.graph_view import GraphView
from arch_copilot.domain.config.i_config import IConfig
from arch_copilot.domain.ai.i_llm_client import ILLMClient
from arch_copilot.presentation.nicegui_app.state import app_state

async def analysis_page():
    # Vis.js 라이브러리 로딩 (페이지 진입 시 1회 수행, 버전 호환성 고려)
    try:
        ui.add_head_html('<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>')
    except TypeError:
        # 일부 NiceGUI 버전 대응
        ui.add_head_html('<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>', sanitize=False)
    
    container = get_container()
    analyze_use_case = container.resolve(AnalyzeProjectUseCase)
    scanner = container.resolve(ASTProjectScanner)
    graph_engine = container.resolve(GraphEngine)
    graph_view = GraphView()

    @ui.refreshable
    async def stats_section():
        config = container.resolve(IConfig)
        llm_client = container.resolve(ILLMClient)
        
        # 실제 엔진 가동 여부 확인
        is_healthy = await llm_client.check_health()
        engine_name = config.llm_provider.upper() if config.llm_provider else "AI ENGINE"
        status_text = "Running" if is_healthy else "Not Reachable"
        status_color = "green-400" if is_healthy else "red-400"
        status_icon = "check_circle" if is_healthy else "error"

        with ui.row().classes('w-full gap-8'):
            # Statistics Card
            with ui.card().classes('flex-1 p-6 bg-zinc-900/30 border border-zinc-800 rounded-2xl'):
                ui.label('Project Statistics').classes('text-gray-500 text-sm italic')
                if app_state.result:
                    ui.label(f"Files: {app_state.result.total_files}").classes('text-2xl font-bold')
                    ui.label(f"Violations: {len(app_state.result.violations)}").classes('text-xl text-red-400')
                else:
                    ui.label('No analysis performed yet.').classes('text-gray-400')

            # System Status Card
            with ui.card().classes('flex-1 p-6 bg-zinc-900/30 border border-zinc-800 rounded-2xl'):
                ui.label('System Health').classes('text-gray-500 text-sm italic')
                with ui.row().classes('items-center gap-2'):
                    ui.icon(status_icon, color=status_color.split('-')[0])
                    ui.label(f'AI Engine: {engine_name} ({status_text})').classes(f'text-{status_color} font-medium')
                if app_state.analyzing:
                    ui.spinner(size='sm').classes('mt-2')
                    ui.label('Analyzing project structure...').classes('text-xs text-primary animate-pulse')

    @ui.refreshable
    def graph_section():
        if app_state.graph_data:
            graph_view.render(app_state.graph_data)
        else:
            ui.label('Graph visualization will appear here...').classes('text-gray-500 text-center py-20 border-2 border-dashed border-zinc-800 rounded-3xl w-full')

    @ui.refreshable
    def violations_section():
        if app_state.result and app_state.result.violations:
            with ui.column().classes('w-full gap-4'):
                for v in app_state.result.violations:
                    with ui.card().classes('w-full p-4 bg-red-900/10 border border-red-900/30 rounded-xl'):
                        with ui.row().classes('items-center justify-between w-full'):
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('warning', color='red-500')
                                ui.label(v.violation_type.value).classes('font-bold text-red-400')
                            ui.label(str(v.source_file)).classes('text-xs text-gray-500')
                        ui.label(v.message).classes('mt-2 text-gray-300')
        elif app_state.result:
            ui.label('No violations found! Great job.').classes('text-green-400 text-center py-10 w-full')
        else:
            ui.label('Violation details will appear here after analysis.').classes('text-gray-500 text-center py-10 w-full')

    def save_report():
        result = app_state.result
        if not result or not result.ai_recommendations:
            ui.notify('No report available to save.', type='warning')
            return
        
        # 텍스트 내용 구성
        content = f"# Architecture Analysis Report: {result.project_path}\n\n"
        content += f"- **Analyzed on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"- **Summary:** {result.summary}\n"
        content += f"- **Violations:** {len(result.violations)}\n\n"
        content += "## AI Recommendations\n\n"
        content += result.ai_recommendations
        
        filename = f"report_{result.project_path.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        safe_content = json.dumps(content)
        safe_filename = json.dumps(filename)
        
        js_code = f"""
        (async () => {{
            const content = {safe_content};
            const filename = {safe_filename};
            try {{
                if (window.showSaveFilePicker) {{
                    const handle = await window.showSaveFilePicker({{
                        suggestedName: filename,
                        types: [{{
                            description: 'Markdown File',
                            accept: {{ 'text/markdown': ['.md'] }}
                        }}]
                    }});
                    const writable = await handle.createWritable();
                    await writable.write(content);
                    await writable.close();
                }} else {{
                    const blob = new Blob([content], {{ type: 'text/markdown' }});
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = filename;
                    a.click();
                    window.URL.revokeObjectURL(url);
                }}
            }} catch (err) {{
                if (err.name !== 'AbortError') {{
                    console.error('Save failed:', err);
                }}
            }}
        }})();
        """
        
        try:
            ui.run_javascript(js_code)
            ui.notify(f"Opening save dialog for: {filename}", type='info', icon='folder_open')
        except Exception as e:
            ui.download(content.encode('utf-8'), filename=filename)
            ui.notify(f"Download triggered: {filename}", type='positive')

    @ui.refreshable
    def ai_analysis_section():
        if app_state.result and app_state.result.ai_recommendations:
            with ui.column().classes('w-full gap-4 p-8 bg-black/20 rounded-3xl border border-zinc-800/50'):
                with ui.row().classes('items-center gap-3 border-b border-zinc-800 pb-4 mb-2 w-full'):
                    ui.icon('psychology', color='primary', size='md').classes('animate-pulse')
                    ui.label('AI Architectural Refactoring Guide').classes('text-2xl font-black text-white tracking-tight')
                    ui.space()
                    ui.button('SAVE AS MD', icon='download', on_click=save_report) \
                        .props('flat text-color=primary rounded-full').classes('font-bold')
                
                ui.markdown(app_state.result.ai_recommendations).classes('text-gray-300 leading-relaxed prose prose-invert max-w-none')
        elif app_state.result:
            config = container.resolve(IConfig)
            provider = config.llm_provider.capitalize() if config.llm_provider else "Unknown"
            model = config.llm_model or config.vllm_model_name
            base_url = config.llm_base_url or config.vllm_base_url

            with ui.column().classes('w-full py-20 items-center justify-center bg-zinc-900/30 rounded-3xl border border-dashed border-zinc-800'):
                ui.icon('report_problem', size='4rem', color='amber')
                ui.label('AI Analysis Unreachable').classes('mt-4 text-xl font-bold text-amber-500')
                with ui.column().classes('items-center gap-1 mt-2 text-gray-400 text-center'):
                    ui.label(f'AI 모델: {model} ({provider})')
                    ui.label(f'연결 상태: 연결 실패 ({base_url})')
                    ui.markdown("""
> [!TIP]
> **해결 방법:**
> 1. 해당 AI 공급자(Ollama, Gemini 등)가 활성화되어 있고 네트워크 접근이 가능한지 확인하세요.
> 2. API Key가 필요한 경우 Settings에서 올바른 Key가 입력되었는지 확인하십시오.
> 3. 로컬 서버의 경우 서비스가 실행 중인지, 포트가 열려 있는지 체크하십시오.
                    """).classes('mt-4 text-sm')
        else:
            ui.label('Run analysis to see AI insights.').classes('text-gray-500 text-center py-20 w-full')

    async def start_analysis():
        path_str = path_input.value.strip()
        if not path_str:
            ui.notify('Please enter a project path.', type='warning')
            return
        
        # 전역 상태에 최근 경로 저장
        app_state.last_path = path_str
        
        root_path = Path(path_str).resolve()
        if not root_path.exists():
            ui.notify(f'Path does not exist: {root_path}', type='negative')
            return

        app_state.analyzing = True
        stats_section.refresh()
        
        try:
            # 1. Scan Project (IO Bound)
            from nicegui import run
            project_structure = await run.io_bound(scanner.scan, root_path)
            
            # 2. Analyze Violations & AI Insights (Native Async Use Case)
            request = AnalysisRequest(project_path=root_path)
            app_state.result = await analyze_use_case.execute(request, project=project_structure)
            
            # 3. Build Graph with Violations (CPU Bound - 엣지 강조 포함)
            app_state.graph_data = await run.cpu_bound(graph_engine.build_graph, project_structure, app_state.result.violations)
            
            ui.notify('Analysis & AI Reasoning completed!', type='positive', icon='auto_awesome')
        except Exception as e:
            import traceback
            traceback.print_exc()
            ui.notify(f'Error during analysis: {str(e)}', type='negative')
        finally:
            app_state.analyzing = False
            stats_section.refresh()
            graph_section.refresh()
            violations_section.refresh()
            ai_analysis_section.refresh()

    with base_layout("Architecture Dashboard"):
        # Hero Section
        with ui.column().classes('w-full gap-4'):
            ui.label('AI-Powered Architecture Analysis').classes('text-4xl font-extrabold text-white')
            ui.label('Clean Architecture 규칙 준수 여부와 순환 참조를 즉시 진단합니다.').classes('text-xl text-gray-400')

        # Control Panel
        with ui.card().classes('w-full p-8 bg-zinc-900/50 border border-zinc-800 backdrop-blur-xl rounded-3xl'):
            ui.label('Project Scan Configuration').classes('text-lg font-semibold text-primary mb-4')
            with ui.row().classes('w-full items-center gap-4'):
                path_input = ui.input(label='Target Project Path', placeholder='E:/MyProjects/AwesomeApp', value=app_state.last_path) \
                    .classes('flex-grow text-white font-medium') \
                    .props('dark label-color=primary outlined')
                ui.button('START ANALYSIS', icon='rocket_launch', on_click=start_analysis).props('unelevated rounded-full').classes('px-8 py-2')

        await stats_section()

        # Tabs
        with ui.tabs().classes('w-full text-white mt-4') as tabs:
            ui.tab('DEPENDENCY GRAPH')
            ui.tab('VIOLATION LIST')
            ui.tab('AI ANALYSIS (BETA)')
        
        with ui.tab_panels(tabs, value='DEPENDENCY GRAPH').classes('w-full bg-transparent h-[750px] mt-4'):
            with ui.tab_panel('DEPENDENCY GRAPH').classes('p-0'):
                graph_section()
            with ui.tab_panel('VIOLATION LIST'):
                violations_section()
            with ui.tab_panel('AI ANALYSIS (BETA)'):
                ai_analysis_section()
