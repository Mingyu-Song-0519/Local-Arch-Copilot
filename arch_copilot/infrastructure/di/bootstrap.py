"""
Dependency Injection Bootstrap
"""

from pathlib import Path
from arch_copilot.domain.config.i_config import IConfig
from arch_copilot.infrastructure.config.config import Config
from arch_copilot.infrastructure.di.container import get_container
from arch_copilot.infrastructure.ast_parser.ast_parser import ASTParser
from arch_copilot.infrastructure.ast_parser.project_scanner import ASTProjectScanner
from arch_copilot.infrastructure.graph_engine.graph_engine import GraphEngine
from arch_copilot.infrastructure.ai_client.vllm_client import VLLMClient
from arch_copilot.domain.services.analysis_service import AnalysisService
from arch_copilot.application.use_cases.analyze_project import AnalyzeProjectUseCase


def bootstrap_container() -> None:
    """애플리케이션 시작 시 모든 의존성을 컨테이너에 등록"""
    container = get_container()

    # Configuration 등록 (싱글톤)
    # Config() 생성 시 환경 변수 로드됨
    config = Config()
    container.register_singleton(IConfig, config)

    # Infrastructure 등록
    ast_parser = ASTParser(project_root=Path(".").resolve()) # 기본 경로는 실행 위치 (절대 경로로 변환)
    container.register_singleton(ASTParser, ast_parser)
    
    scanner = ASTProjectScanner(ast_parser)
    container.register_singleton(ASTProjectScanner, scanner)
    
    graph_engine = GraphEngine()
    container.register_singleton(GraphEngine, graph_engine)
    
    ai_client = VLLMClient()
    container.register_singleton(VLLMClient, ai_client)

    # Domain Services 등록
    analysis_service = AnalysisService()
    container.register_singleton(AnalysisService, analysis_service)

    # Application Use Cases 등록
    analyze_use_case = AnalyzeProjectUseCase(analysis_service)
    container.register_singleton(AnalyzeProjectUseCase, analyze_use_case)
