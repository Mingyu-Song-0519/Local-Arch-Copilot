"""
Domain Value Objects - Violation

아키텍처 위반 사항을 정의합니다.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class ViolationType(Enum):
    LAYER_MISMATCH = "LAYER_MISMATCH"  # 계층 위반 (상위 -> 하위 참조 등)
    CIRCULAR_DEPENDENCY = "CIRCULAR_DEPENDENCY"  # 순환 참조
    UNDEFINED_LAYER = "UNDEFINED_LAYER"  # 정의되지 않은 레이어에 위치
    CLEAN_ARCHITECTURE_VIOLATION = "CLEAN_ARCHITECTURE_VIOLATION" # AI가 판단한 CA 위반


@dataclass(frozen=True)
class ArchitectureViolation:
    """아키텍처 위반 상세 정보"""
    violation_type: ViolationType
    source_file: Path
    target_file: Path | None = None
    message: str = ""
    suggested_fix: str | None = None

    def __str__(self) -> str:
        return f"[{self.violation_type.value}] {self.source_file}: {self.message}"
