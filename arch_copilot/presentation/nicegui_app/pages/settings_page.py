"""
Settings Page (v3.1 - Stabilized Multi-Provider)

애플리케이션 환경 설정(LLM 공급자, 모델 선택 등)을 관리합니다.
NiceGUI의 @ui.refreshable을 사용하여 UI 반응성과 안정성 확보.
"""

from typing import List, Any
from nicegui import ui
from arch_copilot.presentation.nicegui_app.layouts.base_layout import base_layout
from arch_copilot.infrastructure.di.container import get_container
from arch_copilot.domain.config.i_config import IConfig
from arch_copilot.infrastructure.ai_client.llm_client_factory import LLMClientFactory
from pydantic import SecretStr

def settings_page():
    container = get_container()
    config = container.resolve(IConfig)
    
    # 1. 로컬 상태 초기화 (Config 객체에서 필요한 값만 복사)
    config_data = config.model_dump()
    state = {
        'provider': config_data.get('llm_provider', 'vllm'),
        'base_url': config_data.get('llm_base_url') or "http://localhost:11434",
        'api_key': config.llm_api_key.get_secret_value() if config.llm_api_key else "",
        'model': config_data.get('llm_model', 'mistral-24b:latest'),
        'available_models': [config_data.get('llm_model', 'mistral-24b:latest')]
    }

    # 2. 비즈니스 로직 함수 정의
    async def fetch_models():
        """공급자로부터 실제 사용 가능한 모델 목록 가져오기"""
        # 임시 설정 객체 생성 (팩토리 전달용 - 모든 필수 필드 포함)
        class TempConfig:
            llm_provider = state['provider']
            llm_base_url = state['base_url']
            llm_api_key = SecretStr(state['api_key']) if state['api_key'] else None
            llm_model = state['model']
            vllm_base_url = config_data.get('vllm_base_url', 'http://localhost:8000')
            vllm_model_name = config_data.get('vllm_model_name', 'default')

        try:
            client = LLMClientFactory.create(TempConfig())
            ui.notify(f"Fetching models from {state['provider']}...", type='info')
            models = await client.list_models()
            
            if models:
                state['available_models'] = models
                # 현재 선택된 모델이 목록에 없으면 첫 번째로 자동 변경
                if state['model'] not in models:
                    state['model'] = models[0]
                
                ui.notify(f"Found {len(models)} models!", type='positive')
                render_dynamic_section.refresh() # UI 갱신
            else:
                ui.notify("No models found. Check connection/URL.", type='warning')
        except Exception as e:
            ui.notify(f"Failed to load models: {str(e)}", type='negative')

    def save_all():
        """설정 영구 저장"""
        updates = {
            'llm_provider': state['provider'],
            'llm_base_url': state['base_url'],
            'llm_api_key': SecretStr(state['api_key']) if state['api_key'] else None,
            'llm_model': state['model']
        }
        config.update_settings(updates)
        ui.notify("Settings saved successfully!", type='positive', icon='cloud_done')

    def on_provider_change(e):
        """공급자 변경 시 상태 업데이트 및 UI 갱신"""
        state['provider'] = e.value
        state['available_models'] = [] # 목록 초기화
        state['model'] = ""
        ui.notify(f"Provider changed. Click 'Refresh' to load models.", type='info')
        render_dynamic_section.refresh()

    # 3. 브라우저 레이아웃 구성
    with base_layout("System Settings"):
        with ui.column().classes('w-full gap-4'):
            ui.label('Configuration').classes('text-3xl font-bold text-white')
            ui.label('AI 공급자 및 모델 파라미터를 관리합니다.').classes('text-gray-400')

        with ui.card().classes('w-full p-8 bg-zinc-900/50 border border-zinc-800 rounded-3xl mt-4'):
            with ui.row().classes('items-center gap-2 mb-6'):
                ui.icon('settings_input_component', color='primary', size='sm')
                ui.label('API Configuration').classes('text-xl font-bold text-white')

            with ui.column().classes('w-full gap-6'):
                # --- 고정된 상층부: API 공급자 선택 ---
                with ui.column().classes('w-full'):
                    ui.label('API Provider').classes('text-sm text-gray-500 mb-1')
                    ui.select(
                        options=['vllm', 'ollama', 'lmstudio', 'gemini', 'openai', 'anthropic'],
                        value=state['provider'],
                        on_change=on_provider_change
                    ).classes('w-full').props('dark outlined color=primary')

                # --- 유동적인 하층부: 입력창 및 모델 선택 ---
                @ui.refreshable
                def render_dynamic_section():
                    p = state['provider']
                    
                    with ui.column().classes('w-full gap-6'):
                        # 가시성 조건부 입력창
                        if p in ['vllm', 'ollama', 'lmstudio']:
                            ui.input(label='Base URL', placeholder='http://localhost:11434', 
                                     value=state['base_url'],
                                     on_change=lambda e: state.update({'base_url': e.value})) \
                                .classes('w-full').props('dark outlined color=primary')
                        
                        elif p in ['gemini', 'openai', 'anthropic']:
                            with ui.row().classes('w-full items-end gap-2'):
                                ui.input(label=f'{p.capitalize()} API Key', password=True, 
                                         value=state['api_key'],
                                         on_change=lambda e: state.update({'api_key': e.value})) \
                                    .classes('flex-grow').props('dark outlined color=primary')
                                
                                ui.button('VALIDATE', icon='api', on_click=fetch_models) \
                                    .props('unelevated color=primary') \
                                    .tooltip('입력한 API Key로 공급자와 연결하여 모델 목록을 가져옵니다.')

                        # 모델 선택 드롭다운
                        with ui.column().classes('w-full'):
                            ui.label('Model').classes('text-sm text-gray-500 mb-1')
                            with ui.row().classes('w-full gap-4 items-center'):
                                ui.select(
                                    options=state['available_models'] if state['available_models'] else ['Fetch models first...'],
                                    value=state['model'] if state['model'] in state['available_models'] else None,
                                    on_change=lambda e: state.update({'model': e.value})
                                ).classes('flex-grow').props('dark outlined color=primary')
                                
                                if p in ['vllm', 'ollama', 'lmstudio']:
                                    ui.button(icon='refresh', on_click=fetch_models) \
                                        .props('outline round color=primary') \
                                        .tooltip('설치된 모델 목록 새로고침')

                # 동적 섹션 렌더링 시작
                with ui.column().classes('w-full'):
                    render_dynamic_section()

        # --- Footer Actions ---
        with ui.row().classes('w-full justify-end mt-8'):
            ui.button('SAVE CHANGES', icon='check_circle', on_click=save_all) \
                .props('unelevated rounded-full size=lg') \
                .classes('px-10 py-3 bg-primary text-white font-black shadow-lg shadow-primary/20 hover:scale-105 transition-transform')
