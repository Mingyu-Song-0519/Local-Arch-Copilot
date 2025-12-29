"""
AST Parser Implementation

Python AST 모듈을 사용하여 개별 파일의 구조와 의존성을 분석합니다.
"""

import ast
from pathlib import Path
from typing import List, Set

from arch_copilot.domain.entities.project import FileNode


class ASTParser:
    """Python AST를 이용한 소스 코드 분석기"""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root

    def parse_file(self, file_path: Path) -> FileNode:
        """단일 파일을 분석하여 FileNode를 반환합니다."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            
            imports = self._extract_imports(tree)
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            
            # 레이어 추정 (디렉토리 구조 기반)
            layer = self._detect_layer(file_path)

            return FileNode(
                path=file_path.relative_to(self.project_root),
                imports=imports,
                layer=layer,
                classes=classes,
                functions=functions
            )
        except Exception:
            # 파싱 실패 시 최소 정보만 가진 노드 반환
            return FileNode(path=file_path.relative_to(self.project_root))

    def _extract_imports(self, tree: ast.AST) -> Set[str]:
        """추출된 import 목록을 반환합니다."""
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.add(name.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)
        return imports

    def _detect_layer(self, file_path: Path) -> str | None:
        """파일 경로에서 아키텍처 레이어를 추정합니다."""
        parts = file_path.relative_to(self.project_root).parts
        # 예: arch_copilot/domain/entities/user.py -> domain
        #     application/use_cases/login.py -> application
        
        layers = ["domain", "application", "infrastructure", "presentation"]
        for part in parts:
            if part in layers:
                return part
        return None
