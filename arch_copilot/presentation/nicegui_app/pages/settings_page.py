"""
Settings Page

애플리케이션 환경 설정(vLLM URL, 모델 이름 등)을 관리합니다.
"""

from nicegui import ui
from arch_copilot.presentation.nicegui_app.layouts.base_layout import base_layout
from arch_copilot.infrastructure.di.container import get_container
from arch_copilot.domain.config.i_config import IConfig


import traceback

def settings_page():
    container = get_container()
    config = container.resolve(IConfig)
    try:
        with base_layout("System Settings"):
            with ui.column().classes('w-full gap-4'):
                ui.label('Configuration').classes('text-3xl font-bold text-white')
                ui.label('AI 모델 및 분석 엔진 설정을 관리합니다.').classes('text-gray-400')

            with ui.card().classes('w-full p-8 bg-zinc-900/50 border border-zinc-800 rounded-3xl'):
                ui.label('AI Engine (vLLM)').classes('text-lg font-semibold text-primary mb-4')
                
                with ui.column().classes('w-full gap-4'):
                    ui.input(label='VLLM Server URL', value=config.vllm_base_url).classes('w-full').props('readonly')
                    ui.input(label='Model Name', value=config.vllm_model_name).classes('w-full').props('readonly')
                    ui.label('현재 설정은 .env 파일에서 로드되었습니다. (Read-only)').classes('text-xs text-gray-600')

            with ui.card().classes('w-full p-8 bg-zinc-900/50 border border-zinc-800 rounded-3xl'):
                ui.label('Analysis Rules').classes('text-lg font-semibold text-secondary mb-4')
                
                with ui.row().classes('w-full gap-8'):
                    ui.checkbox('Strict Layer Enforcement', value=True).classes('text-gray-300')
                    ui.checkbox('Allow Shared layer from all', value=True).classes('text-gray-300')

            ui.button('SAVE CHANGES', icon='save').props('unelevated rounded-full').classes('px-10 py-3 bg-primary text-white font-bold ml-auto')
    except Exception as e:
        print(f"CRITICAL ERROR in settings_page: {e}")
        traceback.print_exc()
        ui.label(f"Error loading settings: {e}").classes('text-red-500')
