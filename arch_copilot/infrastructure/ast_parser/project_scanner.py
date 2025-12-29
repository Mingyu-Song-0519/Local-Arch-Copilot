"""
AST Project Scanner

ASTParser를 사용하여 전체 프로젝트 디렉토리를 스캔하고 ProjectStructure 엔티티를 생성합니다.
"""

import os
from pathlib import Path
from typing import List

from arch_copilot.domain.entities.project import ProjectStructure
from arch_copilot.infrastructure.ast_parser.ast_parser import ASTParser


class ASTProjectScanner:
    """디렉토리 구조를 탐색하며 AST 기반 분석을 수행하는 스캐너"""

    def __init__(self, parser: ASTParser) -> None:
        self.parser = parser

    def scan(self, root_path: Path, exclude_patterns: List[str] = None) -> ProjectStructure:
        """지정된 루트 경로 이하의 모든 Python 파일을 스캔합니다."""
        project = ProjectStructure(root_path=root_path)
        
        exclude_patterns = exclude_patterns or [".venv", "venv", "__pycache__", ".git", ".pytest_cache"]
        
        for dirpath, dirnames, filenames in os.walk(root_path):
            # 제외 패턴 필터링
            dirnames[:] = [d for d in dirnames if d not in exclude_patterns]
            
            for filename in filenames:
                if filename.endswith(".py"):
                    full_path = Path(dirpath) / filename
                    file_node = self.parser.parse_file(full_path)
                    project.add_file(file_node)
                    
        return project
