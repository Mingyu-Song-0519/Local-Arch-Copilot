from abc import ABC, abstractmethod
from typing import List
from ..entities.violation import ArchitectureViolation

class IAIAnalyzer(ABC):
    """AI 기반 아키텍처 분석기 인터페이스 (의존성 역전용)"""

    @abstractmethod
    async def analyze_violations(
        self,
        violations: List[ArchitectureViolation],
        project_path: str
    ) -> str:
        """
        위반 사항을 분석하여 마크다운 리포트 생성
        
        Args:
            violations: 탐지된 아키텍처 위반 목록
            project_path: 분석 대상 프로젝트 경로
            
        Returns:
            마크다운 형식의 상세 분석 리포트
        """
        pass

    @abstractmethod
    async def is_available(self) -> bool:
        """AI 서비스 가용성 확인 (vLLM 서버 상태 등)"""
        pass
