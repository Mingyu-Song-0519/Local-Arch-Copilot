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
from arch_copilot.domain.services.analysis_service import AnalysisService
from arch_copilot.domain.ai.i_ai_analyzer import IAIAnalyzer
from arch_copilot.domain.ai.i_llm_client import ILLMClient
from arch_copilot.infrastructure.ai_client.llm_client_factory import LLMClientFactory
from arch_copilot.infrastructure.ai_client.vllm_analyzer import VLLMAnalyzer
from arch_copilot.application.use_cases.analyze_project import AnalyzeProjectUseCase


def bootstrap_container() -> None:
    """애플리케이션 시작 시 모든 의존성을 컨테이너에 등록"""
    container = get_container()

    # Configuration 등록 (싱글톤)
    # Config() 생성 시 환경 변수 로드됨
    config = Config()
    container.register_singleton(IConfig, config)

    # Infrastructure 등록
    ast_parser = ASTParser() # 동적 경로 처리를 위해 인자 제거
    container.register_singleton(ASTParser, ast_parser)
    
    scanner = ASTProjectScanner(ast_parser)
    container.register_singleton(ASTProjectScanner, scanner)
    
    graph_engine = GraphEngine()
    container.register_singleton(GraphEngine, graph_engine)
    # 4. Infrastructure - AI Client & Analyzer (동적 생성을 위해 팩토리로 등록)
    container.register_factory(
        ILLMClient,
        lambda: LLMClientFactory.create(container.resolve(IConfig))
    )
    
    container.register_factory(
        IAIAnalyzer,
        lambda: VLLMAnalyzer(container.resolve(ILLMClient))
    )

    # Domain Services 등록
    analysis_service = AnalysisService()
    container.register_singleton(AnalysisService, analysis_service)

    # 5. Application - Use Cases
    container.register_factory(
        AnalyzeProjectUseCase,
        lambda: AnalyzeProjectUseCase(
            analysis_service=container.resolve(AnalysisService),
            scanner=container.resolve(ASTProjectScanner),
            ai_analyzer=container.resolve(IAIAnalyzer)
        )
    )
