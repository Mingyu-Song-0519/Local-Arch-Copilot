"""
Application DTOs

유스케이스의 입력과 출력을 정의합니다.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from arch_copilot.domain.entities.violation import ArchitectureViolation


@dataclass(frozen=True)
class AnalysisRequest:
    """분석 요청 DTO"""
    project_path: Path
    recursive: bool = True
    exclude_patterns: List[str] = None


@dataclass(frozen=True)
class AnalysisResult:
    """분석 결과 DTO"""
    project_path: Path
    total_files: int
    violations: List[ArchitectureViolation]
    summary: str
    duration_seconds: float
    ai_recommendations: Optional[str] = None # NEW: AI 기반 리팩토링 제안
    error_message: Optional[str] = None
