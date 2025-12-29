"""
Domain Entities - Project

분석 대상 프로젝트의 핵심 데이터를 표현합니다.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set


@dataclass(frozen=True)
class FileNode:
    """프로젝트 내 개별 파일 정보"""
    path: Path
    imports: Set[str] = field(default_factory=set)
    layer: str | None = None  # domain, application, infrastructure, presentation
    classes: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)

    def is_in_layer(self, layer_name: str) -> bool:
        return self.layer == layer_name


@dataclass
class ProjectStructure:
    """프로젝트 전체 구조 및 의존성 맵"""
    root_path: Path
    files: Dict[Path, FileNode] = field(default_factory=dict)
    
    def add_file(self, file_node: FileNode) -> None:
        self.files[file_node.path] = file_node

    def get_layer_files(self, layer_name: str) -> List[FileNode]:
        return [f for f in self.files.values() if f.layer == layer_name]

    @property
    def total_files(self) -> int:
        return len(self.files)
