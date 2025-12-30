"""
Analyze Project Use Case

프로젝트 구조를 스캔하고 아키텍처 위반 사항을 분석하는 유스케이스입니다.
"""

import time
from traceback import format_exc

from arch_copilot.application.dtos.analysis_dtos import AnalysisRequest, AnalysisResult
from arch_copilot.domain.entities.project import ProjectStructure
from arch_copilot.domain.services.analysis_service import AnalysisService


from arch_copilot.domain.ai.i_ai_analyzer import IAIAnalyzer
from arch_copilot.domain.exceptions import AIAnalysisError
from arch_copilot.infrastructure.ast_parser.project_scanner import ASTProjectScanner


class AnalyzeProjectUseCase:
    """프로젝트 분석 실행 유스케이스"""

    def __init__(self, analysis_service: AnalysisService, scanner: ASTProjectScanner, ai_analyzer: IAIAnalyzer = None) -> None:
        self._analysis_service = analysis_service
        self._scanner = scanner
        self._ai_analyzer = ai_analyzer

    async def execute(self, request: AnalysisRequest, project: ProjectStructure | None = None) -> AnalysisResult:
        """분석 유스케이스 실행 (비동기 처리 지원)"""
        start_time = time.time()
        
        try:
            # 1. 프로젝트 스캔
            if project is None:
                project = self._scanner.scan(request.project_path, request.exclude_patterns)
            
            # 2. 정적 분석
            violations = self._analysis_service.detect_static_violations(project)
            
            # 3. AI 기반 심층 분석 (vLLM)
            ai_recommendations = None
            if self._ai_analyzer and violations:
                try:
                    # AI 분석은 시간이 걸릴 수 있으므로 105개 위반 사항 중심 분석
                    ai_recommendations = await self._ai_analyzer.analyze_violations(
                        violations, 
                        str(request.project_path)
                    )
                except Exception as e:
                    print(f"DEBUG: AI Analysis skipped/failed: {str(e)}")
            
            # 4. 결과 생성
            duration = time.time() - start_time
            summary = f"Analyzed {project.total_files} files. Found {len(violations)} violations."
            
            return AnalysisResult(
                project_path=request.project_path,
                total_files=project.total_files,
                violations=violations,
                summary=summary,
                duration_seconds=duration,
                ai_recommendations=ai_recommendations
            )
            
        except Exception as e:
            return AnalysisResult(
                project_path=request.project_path,
                total_files=0,
                violations=[],
                summary="Analysis failed.",
                duration_seconds=time.time() - start_time,
                error_message=f"{str(e)}\n{format_exc()}"
            )
