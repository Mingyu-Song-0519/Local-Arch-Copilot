"""
Domain Service - Analysis Service

프로젝트 구조 분석 및 아키텍처 규칙 검증 로직을 담당합니다.
"""

from typing import List

from arch_copilot.domain.entities.project import FileNode, ProjectStructure
from arch_copilot.domain.entities.violation import ArchitectureViolation, ViolationType


class AnalysisService:
    """도메인 레벨의 아키텍처 분석 서비스"""

    def __init__(self) -> None:
        # 규칙 정의 (추후 설정이나 도메인 정책 파일로 분리 가능)
        self.layer_order = ["domain", "application", "infrastructure", "presentation"]

    def detect_static_violations(self, project: ProjectStructure) -> List[ArchitectureViolation]:
        """정적 분석(의존성 규칙) 기반 위반 사항 탐지"""
        violations = []
        
        for file_path, file_node in project.files.items():
            # 1. 정의되지 않은 레이어 확인
            if file_node.layer not in self.layer_order:
                violations.append(
                    ArchitectureViolation(
                        violation_type=ViolationType.UNDEFINED_LAYER,
                        source_file=file_path,
                        message=f"File '{file_path.name}' is in unknown layer: {file_node.layer}"
                    )
                )
                continue

            # 2. 계층 간 의존성 규칙 확인 (상위 -> 하위 금지)
            # Clean Architecture: Presentation -> Application -> Domain <- Infrastructure
            # 여기서는 단순화하여 내부(Domain)에서 외부(Infra)를 참조하는지 확인합니다.
            violations.extend(self._check_layer_dependency(file_node, project))
            
        return violations

    def _check_layer_dependency(self, source: FileNode, project: ProjectStructure) -> List[ArchitectureViolation]:
        violations = []
        source_idx = self.layer_order.index(source.layer)
        
        for imp in source.imports:
            # import 경로에서 레이어 추정 (단순화된 로직)
            target_layer = self._guess_layer_from_import(imp)
            if not target_layer or target_layer not in self.layer_order:
                continue
                
            target_idx = self.layer_order.index(target_layer)
            
            # Domain(0)은 아무것도 참조하면 안 됨 (Application(1) 이상 참조 시 위반)
            # Application(1)은 Domain(0)만 참조 가능 (Infra(2) 참조 시 위반)
            # 실무적으로는 Presentation/Infra가 Application/Domain을 참조함.
            # 규칙: 고수준(상위) 레이어는 저수준(하위) 레이어를 참조하면 안 됨.
            # 여기의 layer_order는 [domain(0), application(1), infrastructure(2), presentation(3)] 순서이므로
            # 낮은 인덱스가 더 고수준(핵심)입니다.
            # 위반 제약: source_idx < target_idx 이면 위반 (예: domain -> application)
            if source_idx < target_idx:
                violations.append(
                    ArchitectureViolation(
                        violation_type=ViolationType.LAYER_MISMATCH,
                        source_file=source.path,
                        message=f"Dependency violation: '{source.layer}' layer should not depend on '{target_layer}' layer."
                    )
                )
        return violations

    def _guess_layer_from_import(self, import_str: str) -> str | None:
        """import 문자열에서 레이어 이름을 추론합니다."""
        for layer in self.layer_order:
            if f".{layer}" in import_str or f"{layer}." in import_str:
                return layer
        return None
