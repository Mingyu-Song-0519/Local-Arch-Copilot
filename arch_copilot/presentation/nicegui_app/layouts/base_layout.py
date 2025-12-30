"""
Base Layout for NiceGUI App

Vibrant & Premium Design (Glassmorphism, Dark mode focus)
"""

from contextlib import contextmanager
from nicegui import ui


@contextmanager
def base_layout(title: str = "Local Arch-Copilot"):
    """
    공통 레이아웃을 제공하는 컨텍스트 매니저
    """
    # 글로벌 스타일 설정
    ui.colors(primary='#6E00FF', secondary='#00D1FF', accent='#FF00E5')
    
    # 테두리가 부드러운 다크 모드 배경
    ui.query('body').style('background-color: #0F111A; color: #E0E0E0; font-family: "Inter", sans-serif;')
    
    # 헤더
    with ui.header().classes('items-center justify-between px-8 py-4 bg-opacity-80 backdrop-blur-md border-b border-gray-800'):
        with ui.row().classes('items-center gap-4'):
            ui.icon('architecture', size='32px').classes('text-primary')
            ui.label(title).classes('text-2xl font-bold tracking-tight')
        
        with ui.row().classes('gap-6 items-center'):
            ui.link('Dashboard', '/').classes('text-gray-300 hover:text-white transition-colors')
            ui.link('Settings', '/settings').classes('text-gray-300 hover:text-white transition-colors')
            ui.button(icon='dark_mode', on_click=ui.dark_mode().toggle).props('flat round color=white')

    # 메인 컨텐츠 영역
    with ui.column().classes('w-full max-w-7xl mx-auto p-8 gap-8'):
        yield

    # 푸터
    with ui.footer().classes('bg-transparent text-gray-500 py-8 justify-center border-t border-gray-900'):
        ui.label('Powered by GPT-OSS-20B & Clean Architecture')
