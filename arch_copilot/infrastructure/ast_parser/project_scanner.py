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
        
        exclude_patterns = exclude_patterns or [
            ".venv", "venv", "venv_tf", "env", ".env",
            "__pycache__", ".git", ".pytest_cache", ".claude",
            "node_modules", "dist", "build", ".idea", ".vscode",
            "playwright-report", "test-results", "htmlcov"
        ]
        
        print(f"DEBUG: Scanning root_path (resolved): {root_path}")
        if not root_path.is_dir():
            print(f"DEBUG: root_path is not a directory!")
            return project

        for dirpath, dirnames, filenames in os.walk(str(root_path)):
            current_dir = Path(dirpath).resolve()
            
            # 제외 패턴 필터링
            original_dirnames = list(dirnames)
            dirnames[:] = [d for d in dirnames if d not in exclude_patterns]
            excluded = set(original_dirnames) - set(dirnames)
            
            if filenames:
                print(f"DEBUG: Visiting {current_dir} (Files found: {len(filenames)})")
            
            for filename in filenames:
                if filename.endswith(".py"):
                    full_path = current_dir / filename
                    print(f"DEBUG: Found python file: {full_path}")
                    try:
                        # parse_file 내부에서도 resolve된 경로 사용 유도
                        file_node = self.parser.parse_file(full_path, root_path=root_path)
                        project.add_file(file_node)
                    except Exception as e:
                        print(f"ERROR: Failed to parse {full_path}: {e}")
                    
        print(f"DEBUG: Scan finished. Total files collected: {len(project.files)}")
        return project
