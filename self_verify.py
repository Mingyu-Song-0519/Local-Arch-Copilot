import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
sys.path.append(str(Path(__file__).parent))

from arch_copilot.infrastructure.di.bootstrap import bootstrap_container
from arch_copilot.infrastructure.di.container import get_container
from arch_copilot.application.use_cases.analyze_project import AnalyzeProjectUseCase
from arch_copilot.application.dtos.analysis_dtos import AnalysisRequest
from arch_copilot.infrastructure.ast_parser.project_scanner import ASTProjectScanner
from arch_copilot.infrastructure.graph_engine.graph_engine import GraphEngine

def self_verify():
    print("🚀 Starting Self-Analysis for 'Local Arch-Copilot'...")
    
    # 1. DI Bootstrap
    bootstrap_container()
    container = get_container()
    
    # 2. Resolve components
    scanner = container.resolve(ASTProjectScanner)
    graph_engine = container.resolve(GraphEngine)
    analyze_use_case = container.resolve(AnalyzeProjectUseCase)
    
    # 3. Execution
    root_path = Path(".").absolute()
    print(f"📂 Scanning directory: {root_path}")
    
    # Step 1: Scanner
    structure = scanner.scan(root_path)
    print(f"📊 Found {len(structure.files)} python files.")
    
    # Step 2: Graph Build
    graph_engine.build_graph(structure)
    print(f"🔗 Dependency graph built with {len(graph_engine.graph.nodes)} nodes.")
    
    # Step 3: Analysis
    request = AnalysisRequest(project_path=root_path)
    result = analyze_use_case.execute(request)
    
    # 4. Report
    print("\n" + "="*50)
    print("📋 ANALYSIS REPORT")
    print("="*50)
    print(f"✅ Total Files Analyzed: {result.total_files}")
    print(f"⚠️ Total Violations Found: {len(result.violations)}")
    
    if result.violations:
        print("\n❌ VIOLATIONS LIST:")
        for i, v in enumerate(result.violations, 1):
            try:
                rel_path = Path(v.source_file).relative_to(root_path)
            except ValueError:
                rel_path = v.source_file
            print(f"{i}. [{v.violation_type.value}] {rel_path}")
            print(f"   Message: {v.message}")
    else:
        print("\n🎉 PERFECT! No architecture violations found. The project strictly follows Clean Architecture.")
    print("="*50)

if __name__ == "__main__":
    self_verify()
