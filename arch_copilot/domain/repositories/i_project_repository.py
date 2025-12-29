"""
Project Repository Interface
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

from arch_copilot.domain.entities.project import ProjectStructure


class IProjectRepository(ABC):
    """프로젝트 데이터를 관리하는 리포지토리 인터페이스"""

    @abstractmethod
    def save(self, project: ProjectStructure) -> None:
        """분석된 프로젝트 구조 저장"""
        pass

    @abstractmethod
    def load(self, root_path: Path) -> Optional[ProjectStructure]:
        """특정 경로의 프로젝트 구조 로드"""
        pass

    @abstractmethod
    def list_projects(self) -> List[Path]:
        """분석된 프로젝트 목록 조회"""
        pass

    @abstractmethod
    def delete(self, root_path: Path) -> None:
        """분석 데이터 삭제"""
        pass
