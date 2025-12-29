"""
AST Parser 단위 테스트
"""

from pathlib import Path
import tempfile
import pytest

from arch_copilot.infrastructure.ast_parser.ast_parser import ASTParser
from arch_copilot.infrastructure.ast_parser.project_scanner import ASTProjectScanner


class TestASTParser:
    """AST 파서 테스트"""

    def test_should_extract_imports_and_definitions(self) -> None:
        """import 및 클래스/함수 추출 검증"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            file_path = root / "domain" / "user.py"
            file_path.parent.mkdir()
            
            code = """
import os
from pathlib import Path
from dataclasses import dataclass

@dataclass
class User:
    name: str

def create_user(name: str) -> User:
    return User(name=name)
"""
            file_path.write_text(code)
            
            parser = ASTParser(project_root=root)
            node = parser.parse_file(file_path)
            
            assert node.layer == "domain"
            assert "os" in node.imports
            assert "pathlib" in node.imports
            assert "dataclasses" in node.imports
            assert "User" in node.classes
            assert "create_user" in node.functions
            assert node.path == Path("domain/user.py")

    def test_should_handle_invalid_syntax(self) -> None:
        """문법 오류 파일 처리 검증"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            file_path = root / "invalid.py"
            file_path.write_text("invalid code !!!")
            
            parser = ASTParser(project_root=root)
            node = parser.parse_file(file_path)
            
            assert node.path == Path("invalid.py")
            assert len(node.imports) == 0
            assert node.layer is None

    def test_should_scan_directory(self) -> None:
        """디렉토리 전체 스캔 검증"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "domain").mkdir()
            (root / "infrastructure").mkdir()
            
            (root / "domain" / "a.py").write_text("class A: pass")
            (root / "infrastructure" / "b.py").write_text("import domain.a")
            
            parser = ASTParser(project_root=root)
            scanner = ASTProjectScanner(parser=parser)
            
            project = scanner.scan(root)
            
            assert project.total_files == 2
            assert project.files[Path("domain/a.py")].layer == "domain"
            assert project.files[Path("infrastructure/b.py")].layer == "infrastructure"
            assert project.root_path == root # ProjectStructure 에는 root_path 가 있음
            # ProjectStructure.files 는 Dict[Path, FileNode] 이고 
            # FileNode.path 는 relative path 임.
            assert Path("domain/a.py") in project.files
