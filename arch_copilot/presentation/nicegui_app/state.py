"""
Global State for NiceGUI Application

페이지 전환 간에 데이터를 유지하기 위한 전역 상태 객체입니다.
"""

from typing import Any, Optional

class AppState:
    def __init__(self):
        self.analyzing: bool = False
        self.result: Optional[Any] = None
        self.graph_data: Optional[Any] = None
        self.last_path: str = ""

# 싱글톤 인스턴스
app_state = AppState()
