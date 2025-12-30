"""
Local Arch-Copilot - 메인 진입점

NiceGUI Native 모드로 데스크탑 앱 실행
"""


from nicegui import ui
from arch_copilot.presentation.nicegui_app.pages.analysis_page import analysis_page
from arch_copilot.presentation.nicegui_app.pages.settings_page import settings_page
from arch_copilot.infrastructure.di.bootstrap import bootstrap_container

def main() -> None:
    # 1. Dependency Injection Bootstrap
    bootstrap_container()
    
    # 2. Page Routing
    @ui.page('/')
    async def dashboard():
        await analysis_page()

    @ui.page('/settings')
    def s_page():
        settings_page()

    # 3. Start NiceGUI
    import os
    port = int(os.environ.get('PORT', 7070))
    ui.run(
        title="Local Arch-Copilot",
        port=port,
        dark=True,
        show=False, 
        reload=False
    )

if __name__ in {"__main__", "__mp_main__"}:
    main()
