# Implementation Plan: Local Arch-Copilot with GPT-OSS-20B

**Status**: 🔄 Ready to Start
**Started**: 2025-12-30
**Last Updated**: 2025-12-30
**Estimated Completion**: 2025-12-31

---

**⚠️ CRITICAL INSTRUCTIONS**: After completing each phase:
1. ✅ Check off completed task checkboxes
2. 🧪 Run all quality gate validation commands
3. ⚠️ Verify ALL quality gate items pass
4. 📅 Update "Last Updated" date above
5. 📝 Document learnings in Notes section
6. ➡️ Only then proceed to next phase

⛔ **DO NOT skip quality gates or proceed with failing checks**

---

## 📋 Overview

### Feature Description
RTX 5070 Ti (16GB VRAM) 환경에서 GPT-OSS-20B 모델을 최적 성능으로 실행하고, Python 프로젝트의 아키텍처를 분석하는 NiceGUI 기반 데스크탑 애플리케이션을 개발합니다.

**핵심 기능**:
- 🤖 GPT-OSS-20B 모델 최적화 (MXFP4, FP8 KV Cache)
- 🔍 Python AST 기반 초고속 프로젝트 구조 분석 (<0.1초)
- 📊 NetworkX 기반 의존성 그래프 시각화
- 🎯 Clean Architecture 위반 자동 탐지
- 🔄 순환 참조(Circular Dependency) 탐지
- 💬 AI 기반 아키텍처 심층 분석 및 리팩토링 제안

### Success Criteria
- [ ] GPT-OSS-20B가 16GB VRAM에서 40-50 TPS로 안정적 동작
- [ ] 1000개 파일 프로젝트를 0.1초 이내에 스캔
- [ ] Clean Architecture 4계층(Domain, Application, Infrastructure, Presentation) 구조 완성
- [ ] 모든 비즈니스 로직의 테스트 커버리지 ≥85%
- [ ] NiceGUI Native 모드로 데스크탑 앱처럼 실행
- [ ] Mermaid 그래프 시각화 및 인터랙티브 노드 클릭 기능
- [ ] AI 분석 결과의 스트리밍 응답 및 실시간 표시

### User Impact
개발자가 로컬 환경에서 클라우드 비용 없이:
- 프로젝트 아키텍처 품질을 즉시 검증
- Clean Architecture 원칙 준수 여부를 자동으로 체크
- AI 기반 리팩토링 제안을 통해 코드 품질 개선
- 의존성 그래프를 시각적으로 파악하여 복잡도 관리

---

## 🏗️ Architecture Decisions

| Decision | Rationale | Trade-offs |
|----------|-----------|------------|
| **Clean Architecture 4계층 구조** | 비즈니스 로직과 프레임워크의 완전한 분리. 테스트 용이성 극대화 | 초기 설정 복잡도 증가, 소규모 프로젝트에는 과도할 수 있음 |
| **vLLM + Ollama 조합** | vLLM은 최고 성능, Ollama는 사용자 친화적 API 제공 | vLLM 직접 사용보다 약간의 오버헤드, WSL2 필수 |
| **Python AST (not regex)** | 정확한 구문 분석, 0.1초 초고속 성능 | 문법 오류가 있는 파일은 스킵해야 함 |
| **NiceGUI (not Streamlit)** | 진정한 비동기 이벤트 처리, Native 앱 모드, 인터랙티브 요소 풍부 | Streamlit보다 커뮤니티가 작음, 러닝 커브 존재 |
| **NetworkX for Graph** | 순환 참조 탐지 알고리즘 내장, Mermaid 출력 변환 용이 | 10,000+ 노드 그래프에서는 시각화 성능 저하 가능 |
| **FP8 KV Cache** | 메모리 사용량 50% 감소, Blackwell 하드웨어 가속 지원 | 이론적으로 미세한 품질 저하(실측 무시 가능) |
| **JSON 캐싱 (not DB)** | 간단한 구조, 빠른 I/O, 버전 관리 용이 | 동시 접근 처리 불가, 대규모 데이터에는 부적합 |

---

## 📦 Dependencies

### Required Before Starting
- [ ] Windows 11 with WSL2 Ubuntu 24.04 LTS 설치
- [ ] NVIDIA Driver 570.xx 이상 설치 (Blackwell 아키텍처 지원)
- [ ] CUDA 12.8 설치 (WSL2 내부)
- [ ] Python 3.12 설치 (WSL2 내부)
- [ ] RTX 5070 Ti GPU 확인 (16GB VRAM)

### External Dependencies
**AI Infrastructure**:
- vllm==0.10.1+gptoss (GPT-OSS-20B 전용 빌드)
- ollama>=0.1.0 (Ollama API 클라이언트)

**Application Core**:
- python==3.12
- nicegui>=1.4.0 (UI 프레임워크)
- networkx>=3.0 (그래프 분석)
- pydantic>=2.0 (도메인 엔티티 검증)

**Development**:
- pytest>=7.0 (테스트 프레임워크)
- pytest-cov>=4.0 (커버리지 측정)
- pytest-asyncio>=0.21.0 (비동기 테스트)
- black>=23.0 (코드 포맷팅)
- mypy>=1.0 (타입 체킹)
- ruff>=0.1.0 (초고속 린터)

---

## 🧪 Test Strategy

### Testing Approach
**TDD Principle**: 모든 비즈니스 로직과 유스케이스는 테스트를 먼저 작성한 후 구현합니다.

### Test Pyramid for This Feature
| Test Type | Coverage Target | Purpose |
|-----------|-----------------|---------|
| **Unit Tests** | ≥85% | Domain entities, Services, Use cases |
| **Integration Tests** | Critical paths | AST parser, Graph engine, AI client 통합 |
| **E2E Tests** | Key user flows | UI 통한 전체 워크플로우 검증 |

### Test File Organization
```
tests/
├── unit/
│   ├── domain/
│   │   ├── test_entities.py
│   │   └── test_services.py
│   ├── application/
│   │   ├── test_scan_project.py
│   │   ├── test_analyze_architecture.py
│   │   └── test_generate_report.py
│   └── infrastructure/
│       ├── test_ast_parser.py
│       ├── test_graph_engine.py
│       └── test_storage.py
├── integration/
│   ├── test_ast_to_graph_pipeline.py
│   ├── test_ai_analysis_flow.py
│   └── test_ui_backend_integration.py
└── e2e/
    └── test_full_analysis_workflow.py
```

### Coverage Requirements by Phase
- **Phase 1 (AI Infrastructure)**: 통합 테스트로 검증 (성능/안정성 중심)
- **Phase 2 (Domain Layer)**: Unit tests ≥90% (핵심 비즈니스 로직)
- **Phase 3 (Application Layer)**: Unit tests ≥85% (유스케이스)
- **Phase 4 (Infrastructure - AST)**: Unit + Integration tests ≥80%
- **Phase 5 (Infrastructure - Graph)**: Integration tests ≥75%
- **Phase 6 (Infrastructure - AI Client)**: Integration tests ≥70%
- **Phase 7 (Presentation - UI)**: E2E tests (주요 사용자 시나리오)

### Test Naming Convention
```python
# tests/unit/domain/test_entities.py
class TestProjectStructure:
    def test_should_create_valid_project_structure(self):
        # Arrange → Act → Assert
        pass

    def test_should_raise_error_when_path_is_invalid(self):
        pass

# tests/integration/test_ast_to_graph_pipeline.py
class TestASTToGraphPipeline:
    async def test_should_scan_project_and_build_graph(self):
        # Given → When → Then
        pass
```

---

## 🚀 Implementation Phases

### Phase 1: AI Infrastructure Setup (vLLM + GPT-OSS-20B)
**Goal**: RTX 5070 Ti에서 GPT-OSS-20B를 40-50 TPS로 안정적으로 실행하는 환경 구축
**Estimated Time**: 3-4 hours
**Status**: ⏳ Pending

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 1.1**: AI 인프라 검증 테스트 작성
  - File(s): `tests/integration/test_vllm_infrastructure.py`
  - Expected: vLLM 서버가 없어서 연결 실패
  - Details: 테스트 케이스:
    - vLLM 서버 연결 성공 확인
    - GPT-OSS-20B 모델 로드 확인
    - 단순 프롬프트로 추론 속도 측정 (≥40 TPS 검증)
    - FP8 KV Cache 활성화 확인
    - 16k 컨텍스트 처리 가능 확인

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 1.2**: WSL2 Ubuntu 환경 설정
  - Actions:
    - Ubuntu 24.04 LTS 업데이트 (`sudo apt update && sudo apt upgrade`)
    - NVIDIA Container Toolkit 설치 (WSL2용)
    - CUDA 12.8 설치 확인 (`nvidia-smi`, `nvcc --version`)
  - Verification: `nvidia-smi` 명령어로 RTX 5070 Ti 인식 확인

- [ ] **Task 1.3**: Python 3.12 가상환경 생성
  - Actions:
    ```bash
    sudo apt install python3.12 python3.12-venv python3-pip
    python3.12 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    ```
  - File(s): `.venv/` (가상환경 디렉토리)

- [ ] **Task 1.4**: vLLM +gptoss 빌드 설치
  - Actions:
    ```bash
    pip install --pre vllm==0.10.1+gptoss \
      --extra-index-url https://wheels.vllm.ai/gpt-oss/ \
      --extra-index-url https://download.pytorch.org/whl/nightly/cu128 \
      --index-strategy unsafe-best-match
    ```
  - Goal: MXFP4 및 Blackwell 최적화 커널 포함된 vLLM 설치

- [ ] **Task 1.5**: GPT-OSS-20B 모델 다운로드 및 vLLM 서버 실행
  - Actions:
    ```bash
    # vLLM이 HuggingFace에서 자동 다운로드
    vllm serve openai/gpt-oss-20b \
      --kv-cache-dtype fp8 \
      --max-model-len 16384 \
      --gpu-memory-utilization 0.95 \
      --enforce-eager \
      --trust-remote-code \
      --port 8000
    ```
  - Goal: localhost:8000에서 OpenAI 호환 API 서버 실행

- [ ] **Task 1.6**: Ollama 설치 및 vLLM 연동 설정
  - Actions:
    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    # Ollama가 vLLM 서버를 백엔드로 사용하도록 설정
    # 또는 Python ollama 클라이언트로 직접 vLLM API 호출
    ```
  - Goal: Python에서 간편하게 AI 추론 호출 가능

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 1.7**: 시스템 환경 설정 문서화
  - File(s): `docs/setup/ai-infrastructure-setup.md`
  - Goal: 재현 가능한 설치 가이드 작성
  - Checklist:
    - [ ] 모든 설치 명령어 정리
    - [ ] 트러블슈팅 섹션 추가
    - [ ] 성능 벤치마크 결과 기록

- [ ] **Task 1.8**: vLLM 서버 시작 스크립트 작성
  - File(s): `scripts/start_vllm_server.sh`
  - Goal: 한 번의 명령으로 최적 설정으로 서버 시작
  - Content:
    ```bash
    #!/bin/bash
    source .venv/bin/activate
    vllm serve openai/gpt-oss-20b \
      --kv-cache-dtype fp8 \
      --max-model-len 16384 \
      --gpu-memory-utilization 0.95 \
      --enforce-eager \
      --trust-remote-code \
      --port 8000
    ```

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed to Phase 2 until ALL checks pass**

**Infrastructure Validation** (CRITICAL):
- [ ] **vLLM Server**: `curl http://localhost:8000/v1/models` 응답 확인
- [ ] **GPU Memory**: `nvidia-smi` 로 VRAM 사용량 ~12-14GB 확인
- [ ] **Inference Speed**: 간단한 프롬프트로 ≥40 TPS 달성 확인
- [ ] **FP8 KV Cache**: vLLM 로그에서 FP8 활성화 메시지 확인
- [ ] **Context Length**: 16k 토큰 처리 가능 확인 (샘플 긴 문서 입력)

**Integration Tests**:
- [ ] **All Tests Pass**: `pytest tests/integration/test_vllm_infrastructure.py -v`
- [ ] **No Warnings**: pytest 경고 메시지 없음
- [ ] **Test Performance**: 통합 테스트 실행 시간 <30초

**Documentation**:
- [ ] **Setup Guide**: AI 인프라 설정 문서 완성
- [ ] **Performance Baseline**: 초기 성능 지표 기록 (TPS, VRAM 사용량, 응답 시간)

**Validation Commands**:
```bash
# vLLM 서버 상태 확인
curl http://localhost:8000/v1/models

# GPU 메모리 사용량 확인
nvidia-smi --query-gpu=memory.used,memory.total --format=csv

# 간단한 추론 테스트
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-20b",
    "prompt": "Explain Clean Architecture in one sentence:",
    "max_tokens": 50,
    "temperature": 0.1
  }'

# 통합 테스트 실행
pytest tests/integration/test_vllm_infrastructure.py -v --tb=short
```

**Manual Test Checklist**:
- [ ] vLLM 서버를 재시작했을 때 모델이 정상 로드되는가?
- [ ] 동시에 3개의 요청을 보냈을 때 모두 응답하는가?
- [ ] 8k 토큰 이상의 긴 프롬프트를 처리할 수 있는가?

---

### Phase 2: Domain Layer (Entities & Business Logic)
**Goal**: Clean Architecture의 가장 안쪽 계층인 도메인 엔티티와 비즈니스 규칙 구현
**Estimated Time**: 2-3 hours
**Status**: ⏳ Pending
**Dependencies**: Phase 1 완료 (AI 인프라는 직접 의존하지 않지만, 전체 시스템 이해 필요)

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 2.1**: ProjectStructure 엔티티 테스트
  - File(s): `tests/unit/domain/test_project_structure.py`
  - Expected: 엔티티 클래스가 없어서 import 실패
  - Details: 테스트 케이스:
    - 유효한 경로로 ProjectStructure 생성
    - 빈 경로는 ValidationError 발생
    - 존재하지 않는 경로는 ValidationError 발생
    - 프로젝트 이름 추출 정확성 검증

- [ ] **Test 2.2**: FileNode 엔티티 테스트
  - File(s): `tests/unit/domain/test_file_node.py`
  - Expected: FileNode 클래스가 없어서 실패
  - Details: 테스트 케이스:
    - Python 파일 노드 생성
    - imports 리스트 검증
    - functions, classes 메타데이터 검증
    - relative_path 계산 정확성

- [ ] **Test 2.3**: DependencyGraph 엔티티 테스트
  - File(s): `tests/unit/domain/test_dependency_graph.py`
  - Expected: DependencyGraph 클래스가 없어서 실패
  - Details: 테스트 케이스:
    - 노드 추가/조회
    - 엣지(의존성) 추가
    - 순환 참조 존재 여부 확인 메서드
    - Mermaid 포맷 문자열 생성

- [ ] **Test 2.4**: ArchitectureViolation 값 객체 테스트
  - File(s): `tests/unit/domain/test_architecture_violation.py`
  - Expected: ArchitectureViolation 클래스가 없어서 실패
  - Details: 테스트 케이스:
    - Violation 생성 (위반 타입, 소스, 타겟)
    - severity 레벨 검증 (ERROR, WARNING, INFO)
    - 동일성 비교 (같은 violation은 중복 제거)

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 2.5**: 도메인 엔티티 구현
  - File(s):
    - `arch_copilot/domain/entities/project_structure.py`
    - `arch_copilot/domain/entities/file_node.py`
    - `arch_copilot/domain/entities/dependency_graph.py`
    - `arch_copilot/domain/entities/architecture_violation.py`
  - Goal: Pydantic BaseModel로 불변성과 검증 규칙 포함한 엔티티 작성
  - Details:
    ```python
    # project_structure.py 예시
    from pydantic import BaseModel, Field, validator
    from pathlib import Path

    class ProjectStructure(BaseModel):
        root_path: Path
        name: str
        total_files: int = 0

        @validator('root_path')
        def validate_path_exists(cls, v):
            if not v.exists():
                raise ValueError(f"Path does not exist: {v}")
            return v

        class Config:
            frozen = True  # 불변성
    ```

- [ ] **Task 2.6**: Repository 인터페이스 정의 (추상 클래스)
  - File(s): `arch_copilot/domain/repositories/project_repository.py`
  - Goal: 도메인이 인프라에 의존하지 않도록 추상 인터페이스 정의
  - Details:
    ```python
    from abc import ABC, abstractmethod
    from typing import List
    from ..entities import ProjectStructure, FileNode

    class IProjectRepository(ABC):
        @abstractmethod
        async def scan_project(self, path: Path) -> ProjectStructure:
            pass

        @abstractmethod
        async def get_file_nodes(self, project: ProjectStructure) -> List[FileNode]:
            pass
    ```

- [ ] **Task 2.7**: 도메인 서비스 구현
  - File(s): `arch_copilot/domain/services/architecture_validator.py`
  - Goal: Clean Architecture 규칙 검증 로직 (순수 비즈니스 로직)
  - Details:
    - Layer 규칙: Domain은 아무것도 참조 불가, Application은 Domain만 참조, Infrastructure는 모두 참조 가능
    - 순환 참조 탐지 로직
    - Violation severity 결정 로직

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 2.8**: 도메인 모델 정리 및 문서화
  - Files: 모든 domain/ 하위 파일
  - Goal: docstring 추가, 타입 힌트 완벽화
  - Checklist:
    - [ ] 모든 public 메서드에 docstring
    - [ ] 복잡한 비즈니스 규칙에 주석
    - [ ] `__init__.py`에 public API 명시
    - [ ] 타입 힌트 100% 적용

- [ ] **Task 2.9**: 도메인 다이어그램 생성
  - File(s): `docs/architecture/domain-model.md`
  - Goal: 엔티티 관계도 및 비즈니스 규칙 문서화

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed to Phase 3 until ALL checks pass**

**TDD Compliance** (CRITICAL):
- [ ] **Red Phase**: 모든 테스트가 먼저 작성되고 실패했음을 확인
- [ ] **Green Phase**: 최소한의 코드로 테스트 통과
- [ ] **Refactor Phase**: 리팩토링 후에도 테스트 모두 통과
- [ ] **Coverage Check**: Domain layer 커버리지 ≥90%
  ```bash
  pytest tests/unit/domain/ --cov=arch_copilot/domain --cov-report=html --cov-report=term
  # 목표: 90% 이상
  ```

**Build & Tests**:
- [ ] **All Tests Pass**: `pytest tests/unit/domain/ -v`
- [ ] **No Skipped Tests**: 모든 테스트 실행됨
- [ ] **Fast Execution**: 전체 도메인 테스트 <5초

**Code Quality**:
- [ ] **Type Checking**: `mypy arch_copilot/domain/ --strict`
- [ ] **Linting**: `ruff check arch_copilot/domain/`
- [ ] **Formatting**: `black --check arch_copilot/domain/`

**Architecture Compliance**:
- [ ] **No External Dependencies**: domain/은 외부 라이브러리(NiceGUI, NetworkX 등) 참조 금지 (Pydantic만 허용)
- [ ] **No Framework Coupling**: UI나 인프라 프레임워크 코드가 domain에 없음

**Documentation**:
- [ ] **Entity Docstrings**: 모든 엔티티 클래스에 목적 설명
- [ ] **Business Rules**: ArchitectureValidator 로직 주석 완비
- [ ] **Domain Model Diagram**: 엔티티 관계도 완성

**Validation Commands**:
```bash
# 테스트 실행 및 커버리지
pytest tests/unit/domain/ -v --cov=arch_copilot/domain --cov-report=term-missing

# 타입 체크
mypy arch_copilot/domain/ --strict

# 린팅
ruff check arch_copilot/domain/

# 포맷 검증
black --check arch_copilot/domain/

# 의존성 체크 (domain이 외부 모듈 import 안 하는지)
# 수동으로 각 파일의 import 문 검토
```

**Manual Test Checklist**:
- [ ] ProjectStructure를 잘못된 경로로 생성하면 ValidationError가 발생하는가?
- [ ] DependencyGraph에 A→B→C→A 순환 참조를 추가하면 탐지되는가?
- [ ] ArchitectureViolation의 severity가 올바르게 분류되는가?

---

### Phase 3: Application Layer (Use Cases)
**Goal**: 비즈니스 로직을 orchestrate하는 유스케이스 구현
**Estimated Time**: 3 hours
**Status**: ⏳ Pending
**Dependencies**: Phase 2 완료 (Domain entities)

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 3.1**: ScanProjectUseCase 테스트
  - File(s): `tests/unit/application/test_scan_project_use_case.py`
  - Expected: UseCase 클래스가 없어서 실패
  - Details: 테스트 케이스 (Mock Repository 사용):
    - 유효한 경로 입력 → ProjectStructure 반환
    - Repository 호출 검증 (Mock)
    - 잘못된 경로 → UseCaseException 발생

- [ ] **Test 3.2**: AnalyzeArchitectureUseCase 테스트
  - File(s): `tests/unit/application/test_analyze_architecture_use_case.py`
  - Expected: UseCase 클래스가 없어서 실패
  - Details: 테스트 케이스:
    - ProjectStructure + FileNodes → ArchitectureViolation 리스트
    - 순환 참조 탐지 확인
    - Layer 위반 탐지 확인
    - Domain service 호출 검증

- [ ] **Test 3.3**: GenerateReportUseCase 테스트
  - File(s): `tests/unit/application/test_generate_report_use_case.py`
  - Expected: UseCase 클래스가 없어서 실패
  - Details: 테스트 케이스:
    - AnalysisResult → 구조화된 리포트 (JSON)
    - Mermaid 그래프 문자열 포함
    - Violation 요약 통계 포함

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 3.4**: Use Case 기본 구조 구현
  - File(s):
    - `arch_copilot/application/use_cases/scan_project.py`
    - `arch_copilot/application/use_cases/analyze_architecture.py`
    - `arch_copilot/application/use_cases/generate_report.py`
  - Goal: 각 Use Case를 명확한 단일 책임을 가진 클래스로 구현
  - Details:
    ```python
    # scan_project.py 예시
    from dataclasses import dataclass
    from pathlib import Path
    from ...domain.entities import ProjectStructure
    from ...domain.repositories import IProjectRepository

    @dataclass
    class ScanProjectRequest:
        project_path: Path

    @dataclass
    class ScanProjectResponse:
        project: ProjectStructure
        file_count: int
        scan_duration_ms: float

    class ScanProjectUseCase:
        def __init__(self, repository: IProjectRepository):
            self._repository = repository

        async def execute(self, request: ScanProjectRequest) -> ScanProjectResponse:
            # 비즈니스 로직 orchestration
            project = await self._repository.scan_project(request.project_path)
            # ...
            return ScanProjectResponse(...)
    ```

- [ ] **Task 3.5**: DTO (Data Transfer Object) 정의
  - File(s): `arch_copilot/application/dtos/`
  - Goal: Use Case 간 데이터 전달을 위한 명확한 계약
  - Details:
    - Request/Response 쌍으로 구성
    - Pydantic으로 검증 규칙 포함

- [ ] **Task 3.6**: Application Service (Facade) 구현
  - File(s): `arch_copilot/application/services/analysis_service.py`
  - Goal: 여러 Use Case를 조합하는 고수준 서비스
  - Details:
    ```python
    class AnalysisService:
        def __init__(
            self,
            scan_use_case: ScanProjectUseCase,
            analyze_use_case: AnalyzeArchitectureUseCase,
            report_use_case: GenerateReportUseCase
        ):
            self._scan = scan_use_case
            self._analyze = analyze_use_case
            self._report = report_use_case

        async def full_analysis(self, path: Path) -> dict:
            # Use Case들을 순차 실행
            scan_result = await self._scan.execute(ScanProjectRequest(path))
            analyze_result = await self._analyze.execute(...)
            report = await self._report.execute(...)
            return report
    ```

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 3.7**: 에러 처리 및 로깅 추가
  - Files: 모든 application/ 파일
  - Goal: 명확한 예외 타입과 로깅
  - Checklist:
    - [ ] Custom Exception 클래스 정의 (UseCaseException, ValidationException)
    - [ ] 각 Use Case에 구조화된 로깅 추가
    - [ ] 에러 발생 시 명확한 메시지

- [ ] **Task 3.8**: Use Case 문서화
  - File(s): `docs/architecture/use-cases.md`
  - Goal: 각 Use Case의 목적, 입출력, 플로우 다이어그램

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed to Phase 4 until ALL checks pass**

**TDD Compliance** (CRITICAL):
- [ ] **Red Phase**: Use Case 테스트가 먼저 작성되고 실패 확인
- [ ] **Green Phase**: Use Case 구현으로 테스트 통과
- [ ] **Refactor Phase**: 리팩토링 후에도 모든 테스트 통과
- [ ] **Coverage Check**: Application layer 커버리지 ≥85%
  ```bash
  pytest tests/unit/application/ --cov=arch_copilot/application --cov-report=html --cov-report=term
  ```

**Build & Tests**:
- [ ] **All Tests Pass**: `pytest tests/unit/application/ -v`
- [ ] **Mock Isolation**: Repository를 Mock으로 대체한 순수 단위 테스트
- [ ] **Fast Execution**: Application 테스트 <10초

**Code Quality**:
- [ ] **Type Checking**: `mypy arch_copilot/application/ --strict`
- [ ] **Linting**: `ruff check arch_copilot/application/`
- [ ] **Formatting**: `black --check arch_copilot/application/`

**Architecture Compliance**:
- [ ] **Domain Dependency Only**: application/은 domain/만 참조 (infrastructure 참조 금지)
- [ ] **No Framework Code**: NiceGUI, NetworkX 등 구체적 프레임워크 코드 없음

**Documentation**:
- [ ] **Use Case Docs**: 각 Use Case의 책임 명확히 문서화
- [ ] **Sequence Diagram**: 주요 Use Case의 시퀀스 다이어그램

**Validation Commands**:
```bash
# 테스트 및 커버리지
pytest tests/unit/application/ -v --cov=arch_copilot/application --cov-report=term-missing

# 타입 체크
mypy arch_copilot/application/ --strict

# 린팅 및 포맷
ruff check arch_copilot/application/
black --check arch_copilot/application/

# 의존성 역전 원칙 검증 (application이 infrastructure import 안 하는지 수동 확인)
grep -r "from.*infrastructure" arch_copilot/application/ || echo "OK: No infrastructure imports"
```

**Manual Test Checklist**:
- [ ] ScanProjectUseCase를 Mock Repository로 실행하면 정상 동작하는가?
- [ ] AnalyzeArchitectureUseCase가 순환 참조를 정확히 탐지하는가?
- [ ] GenerateReportUseCase의 출력이 예상한 JSON 구조인가?

---

### Phase 4: Infrastructure - AST Parser (Python Static Analysis)
**Goal**: Python AST를 사용하여 0.1초 이내에 프로젝트 구조를 스캔하는 구현체
**Estimated Time**: 3 hours
**Status**: ⏳ Pending
**Dependencies**: Phase 2 (Domain), Phase 3 (Application) 완료

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 4.1**: ASTFileParser 단위 테스트
  - File(s): `tests/unit/infrastructure/test_ast_file_parser.py`
  - Expected: ASTFileParser 클래스가 없어서 실패
  - Details: 테스트 케이스:
    - 간단한 Python 파일에서 imports 추출
    - 간단한 Python 파일에서 함수/클래스 시그니처 추출
    - 문법 오류 파일은 스킵하고 에러 로그
    - 비-Python 파일은 무시

- [ ] **Test 4.2**: ASTProjectScanner 통합 테스트
  - File(s): `tests/integration/test_ast_project_scanner.py`
  - Expected: Scanner 클래스가 없어서 실패
  - Details: 테스트 케이스:
    - 샘플 프로젝트 디렉토리 스캔 (10개 파일)
    - 모든 Python 파일 탐지 확인
    - 스캔 속도 <0.1초 검증
    - FileNode 리스트 정확성 검증

- [ ] **Test 4.3**: ProjectRepositoryImpl 테스트
  - File(s): `tests/integration/test_project_repository_impl.py`
  - Expected: Repository 구현체가 없어서 실패
  - Details: 테스트 케이스:
    - IProjectRepository 인터페이스 준수 확인
    - scan_project() 메서드 정확성
    - get_file_nodes() 메서드 정확성

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 4.4**: ASTFileParser 구현
  - File(s): `arch_copilot/infrastructure/ast_parser/file_parser.py`
  - Goal: 단일 Python 파일을 AST로 파싱하여 메타데이터 추출
  - Details:
    ```python
    import ast
    from pathlib import Path
    from typing import List, Dict

    class ASTFileParser:
        def parse_file(self, file_path: Path) -> Dict:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                tree = ast.parse(source, filename=str(file_path))

                imports = self._extract_imports(tree)
                functions = self._extract_functions(tree)
                classes = self._extract_classes(tree)

                return {
                    'imports': imports,
                    'functions': functions,
                    'classes': classes
                }
            except SyntaxError as e:
                # 문법 오류 파일은 로그하고 스킵
                logger.warning(f"Syntax error in {file_path}: {e}")
                return None

        def _extract_imports(self, tree: ast.AST) -> List[str]:
            # ast.Import, ast.ImportFrom 노드 추출
            pass
    ```

- [ ] **Task 4.5**: ASTProjectScanner 구현
  - File(s): `arch_copilot/infrastructure/ast_parser/project_scanner.py`
  - Goal: 디렉토리를 재귀적으로 스캔하여 모든 Python 파일 파싱
  - Details:
    - `Path.rglob("**/*.py")`로 파일 탐색
    - 병렬 처리로 속도 향상 (asyncio 또는 multiprocessing)
    - `.venv`, `__pycache__` 등 제외

- [ ] **Task 4.6**: ProjectRepositoryImpl 구현 (Dependency Inversion)
  - File(s): `arch_copilot/infrastructure/repositories/project_repository_impl.py`
  - Goal: Domain의 IProjectRepository 인터페이스 구현
  - Details:
    ```python
    from ...domain.repositories import IProjectRepository
    from ...domain.entities import ProjectStructure, FileNode
    from ..ast_parser import ASTProjectScanner

    class ProjectRepositoryImpl(IProjectRepository):
        def __init__(self, scanner: ASTProjectScanner):
            self._scanner = scanner

        async def scan_project(self, path: Path) -> ProjectStructure:
            # Scanner로 스캔 후 Domain 엔티티로 변환
            pass
    ```

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 4.7**: 성능 최적화
  - Files: `infrastructure/ast_parser/`
  - Goal: 1000개 파일 기준 0.1초 이내 스캔
  - Checklist:
    - [ ] 병렬 처리 (asyncio.gather 또는 ProcessPoolExecutor)
    - [ ] 불필요한 파일 I/O 최소화
    - [ ] AST 파싱 결과 캐싱 (파일 mtime 기반)

- [ ] **Task 4.8**: 에러 핸들링 강화
  - Files: 모든 ast_parser/ 파일
  - Goal: 어떤 프로젝트 구조에도 견고하게 동작
  - Checklist:
    - [ ] Permission denied 파일 스킵
    - [ ] 심볼릭 링크 무한 루프 방지
    - [ ] 대용량 파일 타임아웃 설정

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed to Phase 5 until ALL checks pass**

**TDD Compliance** (CRITICAL):
- [ ] **Red Phase**: AST 파서 테스트가 먼저 실패 확인
- [ ] **Green Phase**: 구현으로 테스트 통과
- [ ] **Refactor Phase**: 성능 최적화 후에도 테스트 통과
- [ ] **Coverage Check**: AST parser 커버리지 ≥80%
  ```bash
  pytest tests/unit/infrastructure/test_ast_*.py tests/integration/test_ast_*.py \
    --cov=arch_copilot/infrastructure/ast_parser \
    --cov-report=html --cov-report=term
  ```

**Build & Tests**:
- [ ] **All Tests Pass**: `pytest tests/unit/infrastructure/ tests/integration/test_ast*.py -v`
- [ ] **Performance Test**: 1000개 파일 샘플 프로젝트를 0.1초 이내 스캔

**Code Quality**:
- [ ] **Type Checking**: `mypy arch_copilot/infrastructure/ast_parser/ --strict`
- [ ] **Linting**: `ruff check arch_copilot/infrastructure/ast_parser/`
- [ ] **Formatting**: `black --check arch_copilot/infrastructure/ast_parser/`

**Performance**:
- [ ] **Scan Speed**: 벤치마크 테스트로 1000 파일 <0.1초 검증
- [ ] **Memory Usage**: 스캔 중 메모리 사용량 <500MB

**Documentation**:
- [ ] **AST Parser Docs**: 파싱 로직 및 제외 규칙 문서화
- [ ] **Performance Notes**: 최적화 기법 기록

**Validation Commands**:
```bash
# 단위 + 통합 테스트
pytest tests/unit/infrastructure/test_ast*.py tests/integration/test_ast*.py -v \
  --cov=arch_copilot/infrastructure/ast_parser --cov-report=term-missing

# 타입 체크
mypy arch_copilot/infrastructure/ast_parser/ --strict

# 린팅
ruff check arch_copilot/infrastructure/ast_parser/

# 성능 벤치마크 (별도 스크립트)
python scripts/benchmark_ast_scanner.py
# 예상 출력: "Scanned 1000 files in 0.08s"
```

**Manual Test Checklist**:
- [ ] 실제 대형 프로젝트 (예: Django)를 스캔했을 때 오류 없이 완료되는가?
- [ ] 문법 오류가 있는 파일을 포함한 프로젝트도 스캔되는가?
- [ ] 심볼릭 링크로 인한 무한 루프가 발생하지 않는가?

---

### Phase 5: Infrastructure - Graph Engine (NetworkX Integration)
**Goal**: 의존성 그래프 생성, 순환 참조 탐지, Mermaid 변환
**Estimated Time**: 2-3 hours
**Status**: ⏳ Pending
**Dependencies**: Phase 4 (AST Parser) 완료

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 5.1**: GraphBuilder 단위 테스트
  - File(s): `tests/unit/infrastructure/test_graph_builder.py`
  - Expected: GraphBuilder 클래스가 없어서 실패
  - Details: 테스트 케이스:
    - FileNode 리스트 → NetworkX DiGraph 생성
    - 노드 개수 확인
    - 엣지 개수 확인 (import 관계)

- [ ] **Test 5.2**: CycleDetector 테스트
  - File(s): `tests/unit/infrastructure/test_cycle_detector.py`
  - Expected: CycleDetector 클래스가 없어서 실패
  - Details: 테스트 케이스:
    - A→B→C 그래프에서 순환 없음
    - A→B→C→A 그래프에서 순환 탐지
    - 복잡한 그래프에서 모든 순환 찾기

- [ ] **Test 5.3**: MermaidConverter 테스트
  - File(s): `tests/unit/infrastructure/test_mermaid_converter.py`
  - Expected: MermaidConverter 클래스가 없어서 실패
  - Details: 테스트 케이스:
    - NetworkX 그래프 → Mermaid 문자열 변환
    - 노드 이름 이스케이프 (특수문자 처리)
    - 순환 참조 엣지는 빨간색으로 표시

- [ ] **Test 5.4**: DependencyGraphRepository 통합 테스트
  - File(s): `tests/integration/test_dependency_graph_repository.py`
  - Expected: Repository 구현체가 없어서 실패
  - Details: 전체 파이프라인 테스트 (FileNodes → Graph → Mermaid)

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 5.5**: GraphBuilder 구현
  - File(s): `arch_copilot/infrastructure/graph_engine/graph_builder.py`
  - Goal: FileNode 리스트를 NetworkX DiGraph로 변환
  - Details:
    ```python
    import networkx as nx
    from typing import List
    from ...domain.entities import FileNode

    class GraphBuilder:
        def build_graph(self, file_nodes: List[FileNode]) -> nx.DiGraph:
            G = nx.DiGraph()

            # 노드 추가
            for node in file_nodes:
                G.add_node(node.file_path, **node.dict())

            # 엣지 추가 (import 관계)
            for node in file_nodes:
                for imported in node.imports:
                    if imported in G.nodes:
                        G.add_edge(node.file_path, imported)

            return G
    ```

- [ ] **Task 5.6**: CycleDetector 구현
  - File(s): `arch_copilot/infrastructure/graph_engine/cycle_detector.py`
  - Goal: NetworkX 알고리즘으로 순환 참조 탐지
  - Details:
    ```python
    import networkx as nx
    from typing import List, Tuple

    class CycleDetector:
        def find_all_cycles(self, graph: nx.DiGraph) -> List[List[str]]:
            try:
                cycles = list(nx.simple_cycles(graph))
                return cycles
            except nx.NetworkXNoCycle:
                return []

        def has_cycle(self, graph: nx.DiGraph) -> bool:
            return len(self.find_all_cycles(graph)) > 0
    ```

- [ ] **Task 5.7**: MermaidConverter 구현
  - File(s): `arch_copilot/infrastructure/graph_engine/mermaid_converter.py`
  - Goal: NetworkX 그래프를 Mermaid 문법 문자열로 변환
  - Details:
    ```python
    import networkx as nx

    class MermaidConverter:
        def convert(self, graph: nx.DiGraph, cycles: List[List[str]] = None) -> str:
            mermaid = "graph TD;\n"

            for u, v in graph.edges():
                safe_u = self._sanitize_node_name(u)
                safe_v = self._sanitize_node_name(v)

                # 순환 참조 엣지는 빨간색
                if cycles and self._is_cycle_edge(u, v, cycles):
                    mermaid += f"    {safe_u} -->|cycle| {safe_v};\n"
                else:
                    mermaid += f"    {safe_u} --> {safe_v};\n"

            return mermaid

        def _sanitize_node_name(self, name: str) -> str:
            # 특수문자 제거 (Mermaid 호환)
            return name.replace('.', '_').replace('/', '_')
    ```

- [ ] **Task 5.8**: DependencyGraphRepository 구현
  - File(s): `arch_copilot/infrastructure/repositories/dependency_graph_repository.py`
  - Goal: Graph 관련 작업을 Repository 패턴으로 캡슐화

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 5.9**: 그래프 최적화
  - Files: `infrastructure/graph_engine/`
  - Goal: 대규모 그래프 처리 성능 개선
  - Checklist:
    - [ ] 10,000+ 노드 그래프 처리 테스트
    - [ ] 메모리 효율성 검증
    - [ ] 알고리즘 복잡도 분석 문서화

- [ ] **Task 5.10**: 그래프 시각화 옵션 추가
  - Files: `mermaid_converter.py`
  - Goal: 레이어별 색상, 클러스터링 등
  - Checklist:
    - [ ] Domain 레이어는 파란색
    - [ ] Application 레이어는 초록색
    - [ ] Infrastructure 레이어는 회색
    - [ ] Presentation 레이어는 보라색

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed to Phase 6 until ALL checks pass**

**TDD Compliance** (CRITICAL):
- [ ] **Red Phase**: Graph 엔진 테스트가 먼저 실패 확인
- [ ] **Green Phase**: 구현으로 테스트 통과
- [ ] **Refactor Phase**: 최적화 후에도 테스트 통과
- [ ] **Coverage Check**: Graph engine 커버리지 ≥75%
  ```bash
  pytest tests/unit/infrastructure/test_graph*.py tests/integration/test_graph*.py \
    --cov=arch_copilot/infrastructure/graph_engine \
    --cov-report=html --cov-report=term
  ```

**Build & Tests**:
- [ ] **All Tests Pass**: `pytest tests/unit/infrastructure/test_graph*.py -v`
- [ ] **Integration Tests**: 전체 파이프라인 테스트 통과

**Code Quality**:
- [ ] **Type Checking**: `mypy arch_copilot/infrastructure/graph_engine/ --strict`
- [ ] **Linting**: `ruff check arch_copilot/infrastructure/graph_engine/`
- [ ] **Formatting**: `black --check arch_copilot/infrastructure/graph_engine/`

**Functionality**:
- [ ] **Cycle Detection**: 알려진 순환 참조가 정확히 탐지됨
- [ ] **Mermaid Output**: 생성된 Mermaid 코드가 렌더링 가능

**Performance**:
- [ ] **Large Graph**: 1000+ 노드 그래프 처리 <1초

**Documentation**:
- [ ] **Graph Algorithm Docs**: 순환 참조 탐지 알고리즘 설명
- [ ] **Mermaid Format**: Mermaid 출력 포맷 예시

**Validation Commands**:
```bash
# 테스트 및 커버리지
pytest tests/unit/infrastructure/test_graph*.py tests/integration/test_graph*.py -v \
  --cov=arch_copilot/infrastructure/graph_engine --cov-report=term-missing

# 타입 체크
mypy arch_copilot/infrastructure/graph_engine/ --strict

# 린팅
ruff check arch_copilot/infrastructure/graph_engine/

# Mermaid 출력 검증 (수동)
python -c "
from arch_copilot.infrastructure.graph_engine import MermaidConverter
# ... 테스트 그래프 생성
print(converter.convert(test_graph))
" | pbcopy  # 클립보드에 복사 후 https://mermaid.live 에서 렌더링 확인
```

**Manual Test Checklist**:
- [ ] 생성된 Mermaid 코드를 Mermaid Live Editor에 붙여넣었을 때 정상 렌더링되는가?
- [ ] 순환 참조가 빨간색으로 표시되는가?
- [ ] 대형 프로젝트(1000+ 파일)의 그래프가 생성되는가?

---

### Phase 6: Infrastructure - AI Client (Ollama/vLLM Integration)
**Goal**: GPT-OSS-20B를 활용한 AI 분석 기능 구현
**Estimated Time**: 2-3 hours
**Status**: ⏳ Pending
**Dependencies**: Phase 1 (AI Infrastructure), Phase 5 (Graph Engine) 완료

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 6.1**: OllamaClient 통합 테스트
  - File(s): `tests/integration/test_ollama_client.py`
  - Expected: OllamaClient 클래스가 없어서 실패
  - Details: 테스트 케이스 (실제 vLLM 서버 필요):
    - 간단한 프롬프트 전송 및 응답 수신
    - Streaming 응답 처리
    - 타임아웃 처리
    - 에러 응답 처리

- [ ] **Test 6.2**: PromptBuilder 단위 테스트
  - File(s): `tests/unit/infrastructure/test_prompt_builder.py`
  - Expected: PromptBuilder 클래스가 없어서 실패
  - Details: 테스트 케이스:
    - ProjectStructure + Violations → 구조화된 프롬프트 생성
    - Harmony 포맷 준수 확인
    - JSON 형식으로 압축된 데이터 포함
    - reasoning_effort=medium 설정 확인

- [ ] **Test 6.3**: AIAnalysisService 통합 테스트
  - File(s): `tests/integration/test_ai_analysis_service.py`
  - Expected: AIAnalysisService 클래스가 없어서 실패
  - Details: 테스트 케이스:
    - 프로젝트 구조 → AI 분석 결과
    - 응답 파싱 (마크다운/JSON)
    - 스트리밍 모드 동작 확인

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 6.4**: OllamaClient 구현
  - File(s): `arch_copilot/infrastructure/ai_client/ollama_client.py`
  - Goal: vLLM 서버와 통신하는 비동기 클라이언트
  - Details:
    ```python
    import httpx
    from typing import AsyncIterator

    class OllamaClient:
        def __init__(self, base_url: str = "http://localhost:8000"):
            self._base_url = base_url
            self._client = httpx.AsyncClient(timeout=60.0)

        async def generate(
            self,
            prompt: str,
            stream: bool = False,
            temperature: float = 0.1
        ) -> AsyncIterator[str]:
            # vLLM OpenAI-compatible API 호출
            url = f"{self._base_url}/v1/completions"
            payload = {
                "model": "openai/gpt-oss-20b",
                "prompt": prompt,
                "max_tokens": 2048,
                "temperature": temperature,
                "stream": stream
            }

            if stream:
                async with self._client.stream("POST", url, json=payload) as response:
                    async for line in response.aiter_lines():
                        # SSE 파싱
                        yield line
            else:
                response = await self._client.post(url, json=payload)
                return response.json()
    ```

- [ ] **Task 6.5**: PromptBuilder 구현
  - File(s): `arch_copilot/infrastructure/ai_client/prompt_builder.py`
  - Goal: GPT-OSS-20B 최적화 프롬프트 생성
  - Details:
    ```python
    class PromptBuilder:
        def build_analysis_prompt(
            self,
            project_structure: dict,
            violations: List[dict]
        ) -> str:
            # Harmony 포맷 사용
            prompt = "<|start|>system<|message|>\n"
            prompt += "You are a Clean Architecture expert. Analyze the provided Python project structure.\n"
            prompt += "<|reasoning_effort|>medium\n"
            prompt += "<|end|>\n\n"

            prompt += "<|start|>user<|message|>\n"
            prompt += "Project Structure (JSON compressed):\n"
            prompt += json.dumps(project_structure, indent=2)
            prompt += "\n\nDetected Violations:\n"
            prompt += json.dumps(violations, indent=2)
            prompt += "\n\nProvide analysis and refactoring suggestions.\n"
            prompt += "<|end|>\n"

            return prompt
    ```

- [ ] **Task 6.6**: AIAnalysisService 구현
  - File(s): `arch_copilot/infrastructure/ai_client/ai_analysis_service.py`
  - Goal: AI 분석 로직을 캡슐화한 서비스
  - Details:
    - PromptBuilder로 프롬프트 생성
    - OllamaClient로 추론 실행
    - 응답 파싱 및 구조화

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 6.7**: AI 응답 캐싱
  - Files: `ai_analysis_service.py`
  - Goal: 동일 프로젝트 재분석 시 AI 호출 스킵
  - Checklist:
    - [ ] 프로젝트 해시 기반 캐시 키 생성
    - [ ] 캐시 만료 시간 설정 (1시간)
    - [ ] 캐시 히트율 로깅

- [ ] **Task 6.8**: 에러 처리 및 재시도 로직
  - Files: `ollama_client.py`
  - Goal: 네트워크 오류, 모델 오류 등 견고하게 처리
  - Checklist:
    - [ ] Connection error → 3회 재시도
    - [ ] Timeout → 사용자에게 명확한 에러 메시지
    - [ ] GPU OOM → 컨텍스트 길이 줄이기 제안

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed to Phase 7 until ALL checks pass**

**TDD Compliance** (CRITICAL):
- [ ] **Red Phase**: AI 클라이언트 테스트가 먼저 실패 확인
- [ ] **Green Phase**: 구현으로 테스트 통과
- [ ] **Refactor Phase**: 캐싱 및 에러 처리 추가 후에도 테스트 통과
- [ ] **Coverage Check**: AI client 커버리지 ≥70%
  ```bash
  pytest tests/integration/test_ai*.py tests/unit/infrastructure/test_prompt*.py \
    --cov=arch_copilot/infrastructure/ai_client \
    --cov-report=html --cov-report=term
  ```

**Build & Tests**:
- [ ] **Integration Tests Pass**: vLLM 서버 실행 상태에서 통합 테스트 통과
- [ ] **Streaming Test**: 스트리밍 응답이 정상 처리됨

**Code Quality**:
- [ ] **Type Checking**: `mypy arch_copilot/infrastructure/ai_client/ --strict`
- [ ] **Linting**: `ruff check arch_copilot/infrastructure/ai_client/`
- [ ] **Formatting**: `black --check arch_copilot/infrastructure/ai_client/`

**Functionality**:
- [ ] **AI Response Quality**: 샘플 프로젝트 분석 결과가 의미 있음
- [ ] **Prompt Format**: Harmony 포맷이 올바르게 생성됨
- [ ] **Error Handling**: vLLM 서버 중단 시 명확한 에러 메시지

**Performance**:
- [ ] **Response Time**: 일반적인 프로젝트 분석 <10초 (AI 추론 시간 제외)
- [ ] **Streaming Latency**: 첫 토큰 응답까지 <1초

**Documentation**:
- [ ] **AI Integration Docs**: Ollama/vLLM 연동 방법 문서화
- [ ] **Prompt Engineering**: 프롬프트 설계 원칙 기록

**Validation Commands**:
```bash
# vLLM 서버 실행 확인
curl http://localhost:8000/v1/models

# 통합 테스트 (vLLM 서버 필요)
pytest tests/integration/test_ai*.py -v -s

# 단위 테스트
pytest tests/unit/infrastructure/test_prompt*.py -v \
  --cov=arch_copilot/infrastructure/ai_client --cov-report=term-missing

# 타입 체크
mypy arch_copilot/infrastructure/ai_client/ --strict

# 린팅
ruff check arch_copilot/infrastructure/ai_client/
```

**Manual Test Checklist**:
- [ ] 샘플 프로젝트를 AI에 분석시켰을 때 의미 있는 제안이 나오는가?
- [ ] vLLM 서버가 중단된 상태에서 명확한 에러 메시지가 표시되는가?
- [ ] 스트리밍 모드에서 응답이 실시간으로 출력되는가?

---

### Phase 7: Presentation Layer (NiceGUI Desktop App)
**Goal**: Native 데스크탑 앱처럼 동작하는 NiceGUI UI 구현
**Estimated Time**: 4-5 hours
**Status**: ⏳ Pending
**Dependencies**: Phase 2-6 모두 완료

#### Tasks

**🔴 RED: Write Failing E2E Tests First**
- [ ] **Test 7.1**: Full Workflow E2E 테스트
  - File(s): `tests/e2e/test_full_analysis_workflow.py`
  - Expected: UI 컴포넌트가 없어서 실패
  - Details: 테스트 시나리오 (Selenium 또는 Playwright):
    - 앱 실행
    - 프로젝트 경로 입력
    - "Analyze Structure" 버튼 클릭
    - 그래프 탭에서 Mermaid 시각화 확인
    - AI Analysis 탭으로 전환
    - AI 응답 스트리밍 확인
    - 리포트 다운로드

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 7.2**: 기본 레이아웃 구현
  - File(s): `arch_copilot/presentation/nicegui_app/layouts/main_layout.py`
  - Goal: Header, Sidebar, Main Content 영역 구성
  - Details:
    ```python
    from nicegui import ui

    def create_main_layout():
        with ui.header().classes('bg-slate-900 text-white'):
            ui.label('Local Arch-Copilot').classes('text-xl font-bold')
            ui.label('GPT-OSS-20B Powered').classes('text-sm text-gray-400')

        with ui.left_drawer(value=True).classes('bg-slate-800 text-white'):
            # 사이드바 컨텐츠
            pass

        # 메인 컨텐츠 영역
        return ui.column().classes('w-full h-full')
    ```

- [ ] **Task 7.3**: 프로젝트 스캔 UI 구현
  - File(s): `arch_copilot/presentation/nicegui_app/components/project_scanner.py`
  - Goal: 경로 입력 + 스캔 버튼 + 진행 상태
  - Details:
    - Path input field (검증 포함)
    - "Analyze Structure" 버튼
    - 비동기 스캔 로직 (UI 블로킹 방지)
    - 진행 표시 (Spinner + 진행률)

- [ ] **Task 7.4**: 그래프 시각화 탭 구현
  - File(s): `arch_copilot/presentation/nicegui_app/pages/graph_visualizer.py`
  - Goal: Mermaid 그래프 + 인터랙티브 노드 클릭
  - Details:
    ```python
    async def create_graph_tab(analysis_result: dict):
        mermaid_code = analysis_result['mermaid_graph']

        graph_container = ui.column().classes('w-full h-full')

        with graph_container:
            ui.mermaid(mermaid_code).classes('w-full bg-slate-800 p-4 rounded')

            # 통계 정보
            with ui.row().classes('mt-4 gap-4'):
                ui.card().with_slots([
                    ui.label('Total Files'),
                    ui.label(str(analysis_result['total_files'])).classes('text-2xl font-bold')
                ])
                ui.card().with_slots([
                    ui.label('Violations'),
                    ui.label(str(analysis_result['violation_count'])).classes('text-2xl font-bold text-red-500')
                ])
    ```

- [ ] **Task 7.5**: AI 분석 채팅 탭 구현
  - File(s): `arch_copilot/presentation/nicegui_app/pages/ai_chat.py`
  - Goal: AI 응답 스트리밍 + 인터랙티브 채팅
  - Details:
    ```python
    async def create_ai_tab(ai_service: AIAnalysisService):
        chat_container = ui.column().classes('w-full h-full')

        with chat_container:
            # 채팅 메시지 영역
            messages = ui.column().classes('flex-1 overflow-y-auto')

            # AI 분석 트리거 버튼
            async def run_analysis():
                # 스트리밍 응답 처리
                async for chunk in ai_service.analyze_streaming(...):
                    # 실시간으로 메시지 업데이트
                    messages.append(ui.chat_message(chunk))

            ui.button('Run AI Analysis', on_click=run_analysis)
    ```

- [ ] **Task 7.6**: 메인 진입점 구현
  - File(s): `arch_copilot/main.py`
  - Goal: 모든 레이어를 연결하고 앱 실행
  - Details:
    ```python
    from nicegui import ui
    from .presentation.nicegui_app.layouts import create_main_layout
    from .application.services import AnalysisService
    from .infrastructure import (
        ProjectRepositoryImpl,
        ASTProjectScanner,
        GraphBuilder,
        OllamaClient
    )

    # Dependency Injection 설정
    ast_scanner = ASTProjectScanner()
    project_repo = ProjectRepositoryImpl(ast_scanner)
    graph_builder = GraphBuilder()
    ai_client = OllamaClient()

    # Use Cases 초기화
    # ...

    # UI 생성
    @ui.page('/')
    def main_page():
        create_main_layout()
        # ...

    # Native 모드로 실행
    ui.run(
        title='Local Arch-Copilot',
        dark=True,
        native=True,
        window_size=(1400, 900),
        reload=False
    )
    ```

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 7.7**: UI 컴포넌트 모듈화
  - Files: `presentation/nicegui_app/components/`
  - Goal: 재사용 가능한 UI 컴포넌트 추출
  - Checklist:
    - [ ] StatisticsCard 컴포넌트
    - [ ] ViolationListItem 컴포넌트
    - [ ] LoadingSpinner 컴포넌트
    - [ ] ErrorMessage 컴포넌트

- [ ] **Task 7.8**: 사용자 경험 개선
  - Files: 모든 UI 파일
  - Goal: 반응성, 애니메이션, 피드백
  - Checklist:
    - [ ] 로딩 중 스피너 표시
    - [ ] 에러 발생 시 Toast 알림
    - [ ] 성공 시 체크마크 애니메이션
    - [ ] 키보드 단축키 (Ctrl+Enter로 분석 실행 등)

- [ ] **Task 7.9**: 최종 통합 테스트
  - Files: `tests/e2e/test_full_analysis_workflow.py`
  - Goal: 실제 사용자 워크플로우 자동화 테스트
  - Checklist:
    - [ ] 샘플 프로젝트로 전체 플로우 검증
    - [ ] 각 단계별 스크린샷 캡처
    - [ ] 성능 지표 수집 (스캔 시간, AI 응답 시간)

#### Quality Gate ✋

**⚠️ STOP: Final checks before declaring MVP COMPLETE**

**E2E Tests** (CRITICAL):
- [ ] **Full Workflow**: E2E 테스트 모두 통과
- [ ] **User Scenarios**: 주요 사용자 시나리오 3개 이상 검증
- [ ] **Cross-Platform**: Windows에서 Native 모드 정상 실행

**Integration**:
- [ ] **All Layers Connected**: Domain → Application → Infrastructure → Presentation 연결 확인
- [ ] **Dependency Injection**: 모든 의존성이 올바르게 주입됨
- [ ] **Clean Architecture**: 의존성 방향 규칙 준수 (내부 → 외부)

**Code Quality**:
- [ ] **Type Checking**: `mypy arch_copilot/ --strict` 통과
- [ ] **Linting**: `ruff check arch_copilot/` 통과
- [ ] **Formatting**: `black --check arch_copilot/` 통과

**Performance**:
- [ ] **Scan Speed**: 1000 파일 프로젝트 <0.1초
- [ ] **Graph Rendering**: 1000 노드 그래프 <2초
- [ ] **AI Response**: 첫 토큰까지 <1초, 전체 분석 <10초
- [ ] **UI Responsiveness**: 모든 클릭 이벤트 즉시 반응

**User Experience**:
- [ ] **Native Look**: 브라우저처럼 보이지 않고 데스크탑 앱처럼 보임
- [ ] **Error Messages**: 모든 에러에 명확한 메시지
- [ ] **Loading States**: 모든 비동기 작업에 로딩 표시
- [ ] **Accessibility**: 기본적인 키보드 탐색 가능

**Documentation**:
- [ ] **README**: 설치, 실행, 사용법 완비
- [ ] **Architecture Diagram**: Clean Architecture 레이어 다이어그램
- [ ] **API Docs**: 주요 Use Case 및 Repository 문서화
- [ ] **User Guide**: 스크린샷 포함 사용 가이드

**Validation Commands**:
```bash
# 전체 테스트 스위트 실행
pytest tests/ -v --cov=arch_copilot --cov-report=html --cov-report=term

# 전체 커버리지 확인 (목표: ≥85%)
pytest tests/ --cov=arch_copilot --cov-report=term
# 예상: Coverage: 85%+

# 타입 체크
mypy arch_copilot/ --strict

# 린팅
ruff check arch_copilot/

# 포맷 검증
black --check arch_copilot/

# E2E 테스트
pytest tests/e2e/ -v -s

# 앱 실행 (수동 테스트)
python -m arch_copilot.main
```

**Manual Test Checklist**:
- [ ] 앱을 실행했을 때 Native 창으로 열리는가?
- [ ] 샘플 프로젝트를 스캔했을 때 그래프가 정상 표시되는가?
- [ ] 순환 참조가 감지되고 빨간색으로 표시되는가?
- [ ] AI 분석이 스트리밍으로 실시간 표시되는가?
- [ ] 에러 발생 시 명확한 메시지가 표시되는가?
- [ ] 앱을 종료하고 재실행했을 때 이전 분석 결과가 캐싱되어 빠르게 로드되는가?

**Final Acceptance Criteria**:
- [ ] 모든 Success Criteria (페이지 상단) 달성
- [ ] 전체 테스트 커버리지 ≥85%
- [ ] vLLM 서버에서 GPT-OSS-20B가 40-50 TPS로 동작
- [ ] 1000개 파일 프로젝트를 0.1초 이내에 스캔
- [ ] Clean Architecture 4계층 구조 완성 및 준수
- [ ] NiceGUI Native 모드로 데스크탑 앱처럼 실행
- [ ] 모든 문서 완성 (README, Architecture Docs, User Guide)

---

## ⚠️ Risk Assessment

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| **vLLM 설치 실패 (WSL2 환경)** | Medium | High | 상세한 설치 가이드 문서화, Docker 컨테이너 대안 준비 |
| **16GB VRAM 부족 (모델 로딩 실패)** | Low | High | FP8 KV Cache 필수 활성화, 컨텍스트 길이 16k로 제한, 대안으로 llama.cpp 사용 |
| **AST 파싱 성능 목표 미달 (>0.1초)** | Low | Medium | 병렬 처리(multiprocessing), 캐싱 전략, 불필요한 파일 제외 최적화 |
| **NetworkX 그래프 시각화 느림 (대규모 프로젝트)** | Medium | Low | 노드 개수 제한(상위 100개), 레이어별 필터링 옵션, 대안으로 Cytoscape.js 고려 |
| **AI 응답 품질 낮음 (무의미한 제안)** | Medium | Medium | 프롬프트 엔지니어링 반복 개선, temperature=0.1로 일관성 확보, Few-shot examples 추가 |
| **NiceGUI Native 모드 버그** | Low | Medium | Native 모드 실패 시 웹 모드로 fallback, 최신 NiceGUI 버전 사용 |
| **테스트 커버리지 목표 미달 (<85%)** | Low | Medium | TDD 원칙 철저히 준수, 각 Phase별 커버리지 게이트 통과 강제 |
| **Clean Architecture 의존성 역전 위반** | Low | High | 각 Phase별 아키텍처 검증, `grep` 명령어로 불법 import 자동 체크 |

---

## 🔄 Rollback Strategy

### If Phase 1 Fails (AI Infrastructure)
**Steps to revert**:
- WSL2 환경 초기화: `wsl --unregister Ubuntu` 후 재설치
- vLLM 제거: `pip uninstall vllm`
- 대안: llama.cpp + GGUF 포맷으로 전환 (성능은 다소 낮지만 설치 간단)

### If Phase 2 Fails (Domain Layer)
**Steps to revert**:
- `arch_copilot/domain/` 디렉토리 삭제
- `tests/unit/domain/` 디렉토리 삭제
- 영향: 없음 (다른 레이어 미구현 상태)

### If Phase 3 Fails (Application Layer)
**Steps to revert**:
- `arch_copilot/application/` 디렉토리 삭제
- `tests/unit/application/` 디렉토리 삭제
- Domain Layer는 독립적이므로 영향 없음

### If Phase 4-6 Fails (Infrastructure)
**Steps to revert**:
- 해당 Infrastructure 모듈만 삭제
- Domain과 Application은 인터페이스에만 의존하므로 영향 최소
- 다른 Infrastructure 구현체로 교체 가능 (예: AST 대신 regex 파서)

### If Phase 7 Fails (Presentation)
**Steps to revert**:
- `arch_copilot/presentation/` 디렉토리 삭제
- CLI 인터페이스로 대체하여 기능 검증
- 비즈니스 로직은 모두 Use Case에 있으므로 재사용 가능

---

## 📊 Progress Tracking

### Completion Status
- **Phase 1 (AI Infrastructure)**: ⏳ 0%
- **Phase 2 (Domain Layer)**: ⏳ 0%
- **Phase 3 (Application Layer)**: ⏳ 0%
- **Phase 4 (Infrastructure - AST)**: ⏳ 0%
- **Phase 5 (Infrastructure - Graph)**: ⏳ 0%
- **Phase 6 (Infrastructure - AI Client)**: ⏳ 0%
- **Phase 7 (Presentation - UI)**: ⏳ 0%

**Overall Progress**: 0% complete

### Time Tracking
| Phase | Estimated | Actual | Variance |
|-------|-----------|--------|----------|
| Phase 1 | 3-4 hours | - | - |
| Phase 2 | 2-3 hours | - | - |
| Phase 3 | 3 hours | - | - |
| Phase 4 | 3 hours | - | - |
| Phase 5 | 2-3 hours | - | - |
| Phase 6 | 2-3 hours | - | - |
| Phase 7 | 4-5 hours | - | - |
| **Total** | 19-25 hours | - | - |

---

## 📝 Notes & Learnings

### Implementation Notes
(구현 중 발견한 인사이트를 여기에 기록)

### Blockers Encountered
(구현 중 막힌 부분과 해결 방법을 기록)

### Improvements for Future Plans
(다음 프로젝트에서 개선할 점)

---

## 📚 References

### Documentation
- **GPT-OSS-20B Optimization Guide**: `gpt oss 20b.txt`
- **Work Plan**: `work plan.txt`
- **vLLM Official Docs**: https://docs.vllm.ai/
- **NiceGUI Docs**: https://nicegui.io/
- **NetworkX Docs**: https://networkx.org/documentation/stable/
- **Clean Architecture (Uncle Bob)**: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html

### Related Tools
- **Mermaid Live Editor**: https://mermaid.live/
- **Ollama Docs**: https://ollama.com/docs
- **Blackwell GPU Specs**: NVIDIA RTX 5070 Ti Whitepaper

---

## ✅ Final Checklist

**Before marking plan as COMPLETE**:
- [ ] All 7 phases completed with quality gates passed
- [ ] Full integration testing performed (E2E tests)
- [ ] All documentation updated (README, Architecture Docs, User Guide)
- [ ] Performance benchmarks meet targets (0.1s scan, 40-50 TPS AI)
- [ ] Test coverage ≥85% overall
- [ ] Security review completed (no hardcoded secrets, input validation)
- [ ] Clean Architecture compliance verified (dependency rule check)
- [ ] User acceptance testing with real projects
- [ ] Plan document finalized and archived

---

## 🔍 Plan Review & Amendments

**Review Date**: 2025-12-30
**Reviewer**: Architecture Analysis

### 식별된 개선 영역

#### 1. ⚠️ Critical Missing Components

**1.1 Dependency Injection Container 부재**
- **현재 상태**: Phase 7에서 수동으로 의존성 연결
- **문제점**:
  - 테스트 시 의존성 교체 어려움
  - 결합도 증가로 확장성 저하
  - 각 레이어 간 의존성 관리 복잡
- **해결 방안**: Phase 0.5 추가 - DI Container 설정
- **우선순위**: 🔴 HIGH

**1.2 Configuration Management 누락**
- **현재 상태**: 설정값이 코드에 하드코딩 (vLLM URL, 포트 등)
- **문제점**:
  - 환경별 배포 불가 (Dev/Staging/Prod)
  - 민감 정보 코드 내 노출 위험
  - 설정 변경 시 코드 수정 필요
- **해결 방안**: Phase 0.5에 환경 변수 + 설정 파일 관리 추가
- **우선순위**: 🔴 HIGH

**1.3 Logging & Monitoring Strategy 미흡**
- **현재 상태**: 로깅 언급만 있고 구체적 전략 없음
- **문제점**:
  - 프로덕션 디버깅 어려움
  - 성능 병목 지점 파악 불가
  - AI 추론 성능 추적 불가
- **해결 방안**: Phase 8 추가 - 구조화된 로깅 시스템
- **우선순위**: 🟡 MEDIUM

#### 2. 🏗️ Clean Architecture 강화 필요

**2.1 Storage Layer 추상화 부족**
- **현재 상태**: JSON 캐싱이 Infrastructure에 직접 구현
- **Clean Architecture 위반**:
  - Domain이 스토리지 방식에 대해 알아야 함
  - 스토리지 변경 시 Infrastructure 전체 수정
- **해결 방안**:
  - Domain에 `IStorageRepository` 인터페이스 추가
  - Infrastructure에 `JsonStorageRepository` 구현
- **영향 Phase**: Phase 2, Phase 4

**2.2 Error Handling 계층 구조 부재**
- **현재 상태**: 예외 타입이 각 레이어에 흩어짐
- **문제점**:
  - 일관성 없는 에러 처리
  - 상위 레이어가 하위 레이어 예외에 직접 의존
- **해결 방안**:
  - Domain에 예외 계층 정의
  - Application/Infrastructure는 Domain 예외로 변환
- **영향 Phase**: Phase 2, Phase 3

**2.3 Use Case Input/Output Ports 명확화**
- **현재 상태**: Request/Response DTO 사용
- **개선점**: Port 인터페이스로 재정의하여 Clean Architecture 원칙 강화
- **영향 Phase**: Phase 3

#### 3. 🧪 Testing & Quality Assurance

**3.1 Performance Benchmarking 도구 부재**
- **현재 상태**: 성능 목표만 있고 측정 방법 미정의
- **필요 항목**:
  - AST 스캔 속도 벤치마크 스크립트
  - AI 추론 TPS 측정 도구
  - 메모리 프로파일링 도구
- **해결 방안**: Phase 9 추가
- **우선순위**: 🟡 MEDIUM

**3.2 Documentation Generation 자동화 부재**
- **현재 상태**: 수동 문서 작성
- **문제점**: 문서-코드 불일치 가능성
- **해결 방안**: Sphinx + autodoc 통합
- **영향 Phase**: Phase 9

#### 4. 🚀 Production Readiness

**4.1 Docker 컨테이너화 미계획**
- **현재 상태**: WSL2 환경에만 의존
- **문제점**: 배포 복잡도, 재현성 부족
- **해결 방안**: Phase 9에 Dockerfile + docker-compose 추가
- **우선순위**: 🟡 MEDIUM

**4.2 CI/CD 파이프라인 부재**
- **현재 상태**: 수동 테스트 및 빌드
- **해결 방안**: Phase 0에 GitHub Actions 기본 설정
- **우선순위**: 🟢 LOW (but recommended)

---

## 🆕 Additional Phases

### Phase 0: Project Scaffolding & Foundation Setup
**Goal**: 프로젝트 기본 구조 및 개발 환경 설정
**Estimated Time**: 1-2 hours
**Status**: ⏳ New Phase
**Execute Before**: Phase 1

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 0.1**: 프로젝트 구조 검증 테스트
  - File(s): `tests/test_project_structure.py`
  - Expected: 필수 디렉토리가 없어서 실패
  - Details: 테스트 케이스:
    - `arch_copilot/domain/` 존재 확인
    - `arch_copilot/application/` 존재 확인
    - `arch_copilot/infrastructure/` 존재 확인
    - `arch_copilot/presentation/` 존재 확인
    - `tests/unit/`, `tests/integration/`, `tests/e2e/` 존재 확인

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 0.2**: Clean Architecture 디렉토리 구조 생성
  - Actions:
    ```bash
    mkdir -p arch_copilot/{domain/{entities,repositories,services},application/{use_cases,dtos,services},infrastructure/{ast_parser,graph_engine,ai_client,repositories,storage},presentation/nicegui_app/{layouts,components,pages}}
    mkdir -p tests/{unit/{domain,application,infrastructure},integration,e2e}
    mkdir -p docs/{architecture,setup,guides}
    mkdir -p scripts
    ```
  - Goal: 모든 필수 디렉토리 생성

- [ ] **Task 0.3**: pyproject.toml 및 패키지 메타데이터 설정
  - File(s): `pyproject.toml`
  - Goal: Python 프로젝트 설정 및 의존성 관리
  - Details:
    ```toml
    [build-system]
    requires = ["setuptools>=68.0.0", "wheel"]
    build-backend = "setuptools.build_meta"

    [project]
    name = "arch-copilot"
    version = "0.1.0"
    description = "Local Architecture Copilot powered by GPT-OSS-20B"
    requires-python = ">=3.12"
    dependencies = [
        "nicegui>=1.4.0",
        "networkx>=3.0",
        "pydantic>=2.0",
        "httpx>=0.24.0",
    ]

    [project.optional-dependencies]
    dev = [
        "pytest>=7.0",
        "pytest-cov>=4.0",
        "pytest-asyncio>=0.21.0",
        "black>=23.0",
        "mypy>=1.0",
        "ruff>=0.1.0",
    ]
    ai = [
        "ollama>=0.1.0",
    ]

    [tool.pytest.ini_options]
    testpaths = ["tests"]
    python_files = ["test_*.py"]
    python_classes = ["Test*"]
    python_functions = ["test_*"]
    asyncio_mode = "auto"

    [tool.black]
    line-length = 100
    target-version = ['py312']

    [tool.ruff]
    line-length = 100
    target-version = "py312"

    [tool.mypy]
    python_version = "3.12"
    strict = true
    warn_return_any = true
    warn_unused_configs = true

    [tool.coverage.run]
    source = ["arch_copilot"]
    omit = ["tests/*", "**/__pycache__/*"]

    [tool.coverage.report]
    exclude_lines = [
        "pragma: no cover",
        "def __repr__",
        "raise AssertionError",
        "raise NotImplementedError",
        "if __name__ == .__main__.:",
        "if TYPE_CHECKING:",
    ]
    ```

- [ ] **Task 0.4**: Pre-commit hooks 설정
  - File(s): `.pre-commit-config.yaml`
  - Goal: 코드 품질 자동 검증
  - Details:
    ```yaml
    repos:
      - repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v4.5.0
        hooks:
          - id: trailing-whitespace
          - id: end-of-file-fixer
          - id: check-yaml
          - id: check-added-large-files

      - repo: https://github.com/psf/black
        rev: 23.12.1
        hooks:
          - id: black

      - repo: https://github.com/astral-sh/ruff-pre-commit
        rev: v0.1.9
        hooks:
          - id: ruff
            args: [--fix]

      - repo: https://github.com/pre-commit/mirrors-mypy
        rev: v1.8.0
        hooks:
          - id: mypy
            additional_dependencies: [pydantic>=2.0]
    ```

- [ ] **Task 0.5**: 각 레이어에 __init__.py 생성
  - Files: 모든 디렉토리에 `__init__.py`
  - Goal: Python 패키지로 인식
  - Details: Clean Architecture 레이어별로 public API 명시

- [ ] **Task 0.6**: README.md 초안 작성
  - File(s): `README.md`
  - Goal: 프로젝트 개요 및 Quick Start
  - Details:
    ```markdown
    # Local Arch-Copilot

    Python 프로젝트의 Clean Architecture 준수 여부를 분석하는 로컬 AI 기반 도구

    ## Features
    - 🤖 GPT-OSS-20B 기반 아키텍처 분석
    - 🔍 0.1초 이내 초고속 프로젝트 스캔
    - 📊 의존성 그래프 시각화
    - 🎯 Clean Architecture 위반 자동 탐지

    ## Requirements
    - Python 3.12+
    - NVIDIA RTX 5070 Ti (16GB VRAM)
    - WSL2 Ubuntu 24.04 LTS

    ## Quick Start
    (Phase 1 완료 후 작성)

    ## Architecture
    Clean Architecture 4계층 구조:
    - Domain: 비즈니스 로직 (외부 의존성 0)
    - Application: Use Cases
    - Infrastructure: 구체적 구현
    - Presentation: UI (NiceGUI)
    ```

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 0.7**: .gitignore 설정
  - File(s): `.gitignore`
  - Goal: 불필요한 파일 커밋 방지
  - Details:
    ```
    # Python
    __pycache__/
    *.py[cod]
    *$py.class
    .venv/
    venv/
    ENV/

    # Testing
    .pytest_cache/
    .coverage
    htmlcov/
    .mypy_cache/

    # IDE
    .vscode/
    .idea/

    # Project specific
    *.log
    .cache/
    storage/*.json

    # AI Models (large files)
    models/
    *.bin
    *.gguf
    ```

- [ ] **Task 0.8**: 기본 GitHub Actions 워크플로우 설정 (선택)
  - File(s): `.github/workflows/tests.yml`
  - Goal: CI/CD 기본 파이프라인
  - Details:
    ```yaml
    name: Tests

    on: [push, pull_request]

    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with:
              python-version: '3.12'
          - run: pip install -e ".[dev]"
          - run: pytest tests/ --cov=arch_copilot --cov-report=xml
          - run: mypy arch_copilot/ --strict
          - run: ruff check arch_copilot/
    ```

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed to Phase 1 until ALL checks pass**

**Project Structure**:
- [ ] **Directory Structure**: 모든 필수 디렉토리 존재
- [ ] **Test Discovery**: pytest가 테스트 디렉토리 인식
- [ ] **Package Import**: `import arch_copilot` 성공

**Configuration**:
- [ ] **pyproject.toml**: 올바른 형식, 의존성 정의
- [ ] **Pre-commit**: `pre-commit install` 성공
- [ ] **Git**: `.gitignore` 적용 확인

**Code Quality**:
- [ ] **Black**: 모든 파일 포맷 통과
- [ ] **Ruff**: 린팅 오류 없음
- [ ] **Mypy**: 타입 체크 설정 완료

**Documentation**:
- [ ] **README**: 프로젝트 개요 작성
- [ ] **Architecture Docs**: 디렉토리 구조 문서화

**Validation Commands**:
```bash
# 프로젝트 구조 검증
pytest tests/test_project_structure.py -v

# 패키지 import 테스트
python -c "import arch_copilot; print('OK')"

# Pre-commit 실행
pre-commit run --all-files

# 코드 품질
black --check arch_copilot/
ruff check arch_copilot/
mypy arch_copilot/ --strict || echo "OK: No code yet"
```

**Manual Test Checklist**:
- [ ] 모든 디렉토리가 올바른 위치에 생성되었는가?
- [ ] pyproject.toml의 의존성이 올바른가?
- [ ] Git이 불필요한 파일을 무시하는가?

---

### Phase 0.5: Configuration & Dependency Injection Setup
**Goal**: 환경 설정 관리 및 DI Container 구현
**Estimated Time**: 2 hours
**Status**: ⏳ New Phase
**Execute Before**: Phase 2

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 0.5.1**: Configuration 로드 테스트
  - File(s): `tests/unit/infrastructure/test_config.py`
  - Expected: Config 클래스가 없어서 실패
  - Details: 테스트 케이스:
    - 환경 변수에서 설정 로드
    - .env 파일에서 설정 로드
    - 기본값 fallback 동작
    - 필수 설정 누락 시 에러

- [ ] **Test 0.5.2**: DI Container 테스트
  - File(s): `tests/unit/infrastructure/test_container.py`
  - Expected: Container 클래스가 없어서 실패
  - Details: 테스트 케이스:
    - 싱글톤 인스턴스 등록 및 해결
    - 팩토리 함수 등록 및 해결
    - 의존성 자동 주입
    - 순환 의존성 탐지

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 0.5.3**: Domain 레이어 - Configuration 인터페이스 정의
  - File(s): `arch_copilot/domain/config/i_config.py`
  - Goal: Configuration 추상 인터페이스
  - Details:
    ```python
    from abc import ABC, abstractmethod

    class IConfig(ABC):
        @property
        @abstractmethod
        def vllm_base_url(self) -> str:
            pass

        @property
        @abstractmethod
        def vllm_model_name(self) -> str:
            pass

        @property
        @abstractmethod
        def max_context_length(self) -> int:
            pass

        @property
        @abstractmethod
        def cache_dir(self) -> str:
            pass
    ```

- [ ] **Task 0.5.4**: Infrastructure - Config 구현
  - File(s): `arch_copilot/infrastructure/config/config.py`
  - Goal: 환경 변수 + .env 파일 기반 설정
  - Details:
    ```python
    from pydantic_settings import BaseSettings
    from pathlib import Path

    class Config(BaseSettings, IConfig):
        # AI Infrastructure
        vllm_base_url: str = "http://localhost:8000"
        vllm_model_name: str = "openai/gpt-oss-20b"
        max_context_length: int = 16384
        temperature: float = 0.1

        # Application
        cache_dir: Path = Path("./storage/cache")
        log_level: str = "INFO"

        # UI
        ui_port: int = 8080
        ui_title: str = "Local Arch-Copilot"

        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"
    ```

- [ ] **Task 0.5.5**: .env.example 파일 생성
  - File(s): `.env.example`
  - Goal: 환경 변수 템플릿
  - Details:
    ```bash
    # AI Infrastructure
    VLLM_BASE_URL=http://localhost:8000
    VLLM_MODEL_NAME=openai/gpt-oss-20b
    MAX_CONTEXT_LENGTH=16384
    TEMPERATURE=0.1

    # Application
    CACHE_DIR=./storage/cache
    LOG_LEVEL=INFO

    # UI
    UI_PORT=8080
    UI_TITLE=Local Arch-Copilot
    ```

- [ ] **Task 0.5.6**: DI Container 구현
  - File(s): `arch_copilot/infrastructure/di/container.py`
  - Goal: 의존성 주입 컨테이너
  - Details:
    ```python
    from typing import TypeVar, Callable, Any, Dict
    from functools import lru_cache

    T = TypeVar('T')

    class Container:
        def __init__(self):
            self._singletons: Dict[type, Any] = {}
            self._factories: Dict[type, Callable] = {}

        def register_singleton(self, interface: type[T], instance: T) -> None:
            self._singletons[interface] = instance

        def register_factory(self, interface: type[T], factory: Callable[[], T]) -> None:
            self._factories[interface] = factory

        def resolve(self, interface: type[T]) -> T:
            if interface in self._singletons:
                return self._singletons[interface]

            if interface in self._factories:
                instance = self._factories[interface]()
                self._singletons[interface] = instance
                return instance

            raise ValueError(f"No binding found for {interface}")

    # Global container instance
    _container = Container()

    def get_container() -> Container:
        return _container
    ```

- [ ] **Task 0.5.7**: Container 초기화 함수 구현
  - File(s): `arch_copilot/infrastructure/di/bootstrap.py`
  - Goal: 모든 의존성 등록
  - Details:
    ```python
    from .container import get_container
    from ..config import Config
    from ...domain.config import IConfig

    def bootstrap_container() -> None:
        container = get_container()

        # Configuration
        config = Config()
        container.register_singleton(IConfig, config)

        # Repositories (Phase 4-6에서 추가)
        # Use Cases (Phase 3에서 추가)
        # Services (Phase 3에서 추가)
    ```

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 0.5.8**: 설정 검증 로직 추가
  - Files: `infrastructure/config/config.py`
  - Goal: 잘못된 설정값 조기 탐지
  - Checklist:
    - [ ] vLLM URL 형식 검증
    - [ ] 포트 번호 범위 검증
    - [ ] 필수 디렉토리 자동 생성

- [ ] **Task 0.5.9**: Configuration 문서화
  - File(s): `docs/setup/configuration.md`
  - Goal: 모든 환경 변수 설명
  - Details: 각 설정의 목적, 기본값, 유효 범위 문서화

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed to Phase 1 until ALL checks pass**

**TDD Compliance** (CRITICAL):
- [ ] **Red Phase**: 설정 및 DI 테스트가 먼저 실패 확인
- [ ] **Green Phase**: 구현으로 테스트 통과
- [ ] **Refactor Phase**: 검증 로직 추가 후에도 테스트 통과
- [ ] **Coverage Check**: Config/DI 커버리지 ≥85%

**Functionality**:
- [ ] **Environment Variables**: .env 파일에서 설정 로드 성공
- [ ] **Default Values**: 환경 변수 미설정 시 기본값 사용
- [ ] **DI Resolution**: Container가 의존성 올바르게 해결

**Architecture Compliance**:
- [ ] **Interface in Domain**: IConfig가 domain/에 위치
- [ ] **Implementation in Infrastructure**: Config가 infrastructure/에 위치
- [ ] **Dependency Direction**: Infrastructure → Domain (올바름)

**Documentation**:
- [ ] **Configuration Guide**: 모든 환경 변수 문서화
- [ ] **DI Usage**: Container 사용법 문서화

**Validation Commands**:
```bash
# 테스트
pytest tests/unit/infrastructure/test_config.py tests/unit/infrastructure/test_container.py -v \
  --cov=arch_copilot/infrastructure/config \
  --cov=arch_copilot/infrastructure/di

# 설정 로드 검증
python -c "
from arch_copilot.infrastructure.config import Config
config = Config()
print(f'vLLM URL: {config.vllm_base_url}')
print(f'Model: {config.vllm_model_name}')
"

# DI Container 검증
python -c "
from arch_copilot.infrastructure.di import bootstrap_container, get_container
from arch_copilot.domain.config import IConfig
bootstrap_container()
config = get_container().resolve(IConfig)
print(f'Config resolved: {config.vllm_base_url}')
"
```

**Manual Test Checklist**:
- [ ] .env 파일을 생성하고 값을 변경했을 때 설정이 반영되는가?
- [ ] 필수 설정이 누락되었을 때 명확한 에러가 발생하는가?
- [ ] DI Container가 동일한 인터페이스에 대해 같은 인스턴스를 반환하는가?

---

### Phase 8: Cross-Cutting Concerns & Production Readiness
**Goal**: 로깅, 모니터링, 에러 처리 표준화
**Estimated Time**: 3-4 hours
**Status**: ⏳ New Phase
**Execute After**: Phase 7

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 8.1**: 구조화된 로깅 테스트
  - File(s): `tests/unit/infrastructure/test_logger.py`
  - Expected: Logger 클래스가 없어서 실패
  - Details: 테스트 케이스:
    - JSON 형식 로그 출력
    - 로그 레벨 필터링
    - 컨텍스트 정보 포함 (request_id 등)
    - 파일 및 콘솔 동시 출력

- [ ] **Test 8.2**: 메트릭 수집 테스트
  - File(s): `tests/unit/infrastructure/test_metrics.py`
  - Expected: MetricsCollector 클래스가 없어서 실패
  - Details: 테스트 케이스:
    - AST 스캔 시간 측정
    - AI 추론 TPS 계산
    - 메모리 사용량 기록
    - 메트릭 리포트 생성

- [ ] **Test 8.3**: 전역 에러 핸들러 테스트
  - File(s): `tests/unit/presentation/test_error_handler.py`
  - Expected: ErrorHandler가 없어서 실패
  - Details: 테스트 케이스:
    - Domain 예외 → UI 에러 메시지 변환
    - 예상치 못한 예외 → 일반 에러 메시지
    - 에러 로깅 및 추적

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 8.4**: Domain - Exception 계층 구조 정의
  - File(s): `arch_copilot/domain/exceptions.py`
  - Goal: 모든 비즈니스 예외의 기반 클래스
  - Details:
    ```python
    class DomainException(Exception):
        """Base exception for all domain errors"""
        def __init__(self, message: str, code: str = None):
            self.message = message
            self.code = code
            super().__init__(self.message)

    class ValidationException(DomainException):
        """Invalid input or state"""
        pass

    class NotFoundException(DomainException):
        """Resource not found"""
        pass

    class CircularDependencyException(DomainException):
        """Circular dependency detected"""
        pass

    class ArchitectureViolationException(DomainException):
        """Clean Architecture rule violation"""
        pass
    ```

- [ ] **Task 8.5**: Infrastructure - 구조화된 로깅 시스템
  - File(s): `arch_copilot/infrastructure/logging/structured_logger.py`
  - Goal: JSON 형식 구조화 로그
  - Details:
    ```python
    import structlog
    from typing import Any, Dict

    def configure_logging(log_level: str = "INFO") -> None:
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            wrapper_class=structlog.stdlib.BoundLogger,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

    def get_logger(name: str) -> Any:
        return structlog.get_logger(name)
    ```

- [ ] **Task 8.6**: Infrastructure - 메트릭 수집 시스템
  - File(s): `arch_copilot/infrastructure/monitoring/metrics_collector.py`
  - Goal: 성능 지표 수집 및 리포트
  - Details:
    ```python
    from dataclasses import dataclass, field
    from typing import List, Dict
    from time import time
    from contextlib import contextmanager

    @dataclass
    class Metric:
        name: str
        value: float
        unit: str
        timestamp: float = field(default_factory=time)

    class MetricsCollector:
        def __init__(self):
            self._metrics: List[Metric] = []

        @contextmanager
        def measure_time(self, name: str):
            start = time()
            try:
                yield
            finally:
                duration = time() - start
                self.record(name, duration * 1000, "ms")

        def record(self, name: str, value: float, unit: str) -> None:
            self._metrics.append(Metric(name, value, unit))

        def get_report(self) -> Dict[str, Any]:
            report = {}
            for metric in self._metrics:
                if metric.name not in report:
                    report[metric.name] = []
                report[metric.name].append({
                    "value": metric.value,
                    "unit": metric.unit,
                    "timestamp": metric.timestamp
                })
            return report

        def clear(self) -> None:
            self._metrics.clear()
    ```

- [ ] **Task 8.7**: Presentation - 전역 에러 핸들러
  - File(s): `arch_copilot/presentation/error_handler.py`
  - Goal: 모든 예외를 사용자 친화적 메시지로 변환
  - Details:
    ```python
    from nicegui import ui
    from ..domain.exceptions import (
        DomainException,
        ValidationException,
        NotFoundException
    )
    from ..infrastructure.logging import get_logger

    logger = get_logger(__name__)

    def handle_error(error: Exception) -> None:
        if isinstance(error, ValidationException):
            ui.notify(f"입력 오류: {error.message}", type="warning")
            logger.warning("validation_error", error=str(error))

        elif isinstance(error, NotFoundException):
            ui.notify(f"찾을 수 없음: {error.message}", type="warning")
            logger.warning("not_found", error=str(error))

        elif isinstance(error, DomainException):
            ui.notify(f"오류: {error.message}", type="negative")
            logger.error("domain_error", error=str(error), code=error.code)

        else:
            ui.notify("예상치 못한 오류가 발생했습니다.", type="negative")
            logger.exception("unexpected_error", error=str(error))
    ```

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 8.8**: 모든 Use Case에 메트릭 추가
  - Files: `application/use_cases/*.py`
  - Goal: 성능 모니터링 가능
  - Checklist:
    - [ ] ScanProjectUseCase: 스캔 시간 측정
    - [ ] AnalyzeArchitectureUseCase: 분석 시간 측정
    - [ ] AI 관련 Use Case: TPS 계산

- [ ] **Task 8.9**: 로깅 표준화
  - Files: 모든 레이어
  - Goal: 일관된 로깅 규칙
  - Checklist:
    - [ ] 모든 Public 메서드 진입/종료 로그
    - [ ] 에러 발생 시 스택 트레이스 포함
    - [ ] 민감 정보 (경로, 코드 내용) 마스킹

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed to Phase 9 until ALL checks pass**

**TDD Compliance** (CRITICAL):
- [ ] **Red Phase**: 로깅/메트릭 테스트가 먼저 실패
- [ ] **Green Phase**: 구현으로 테스트 통과
- [ ] **Refactor Phase**: 통합 후에도 테스트 통과
- [ ] **Coverage Check**: Cross-cutting concerns 커버리지 ≥70%

**Functionality**:
- [ ] **Structured Logging**: JSON 형식 로그 출력 확인
- [ ] **Metrics Collection**: 성능 지표 정확히 수집
- [ ] **Error Handling**: 모든 예외 타입 올바르게 처리

**Integration**:
- [ ] **All Use Cases**: 메트릭 수집 통합
- [ ] **All Layers**: 구조화된 로깅 사용
- [ ] **UI**: 전역 에러 핸들러 적용

**Documentation**:
- [ ] **Logging Guide**: 로깅 규칙 및 예시
- [ ] **Metrics Reference**: 수집되는 모든 메트릭 설명
- [ ] **Error Codes**: 모든 Domain 예외 코드 문서화

**Validation Commands**:
```bash
# 테스트
pytest tests/unit/infrastructure/test_logger.py tests/unit/infrastructure/test_metrics.py -v

# 로그 출력 확인
python -c "
from arch_copilot.infrastructure.logging import configure_logging, get_logger
configure_logging('INFO')
logger = get_logger('test')
logger.info('test_message', user='test_user', action='test_action')
"

# 메트릭 수집 확인
python -c "
from arch_copilot.infrastructure.monitoring import MetricsCollector
collector = MetricsCollector()
with collector.measure_time('test_operation'):
    import time; time.sleep(0.1)
print(collector.get_report())
"
```

**Manual Test Checklist**:
- [ ] 애플리케이션 실행 시 로그가 JSON 형식으로 출력되는가?
- [ ] 에러 발생 시 UI에 사용자 친화적 메시지가 표시되는가?
- [ ] 성능 메트릭이 정확히 수집되는가?

---

### Phase 9: Performance Optimization & Documentation
**Goal**: 성능 벤치마크, Docker 컨테이너화, 문서 자동화
**Estimated Time**: 3-4 hours
**Status**: ⏳ New Phase
**Execute After**: Phase 8

#### Tasks

**🔴 RED: Write Failing Tests First**
- [ ] **Test 9.1**: 성능 벤치마크 테스트
  - File(s): `tests/performance/test_benchmarks.py`
  - Expected: 벤치마크 스크립트가 없어서 실패
  - Details: 성능 목표:
    - 1000개 파일 스캔 <0.1초
    - 그래프 생성 <1초
    - AI 추론 ≥40 TPS

**🟢 GREEN: Implement to Make Tests Pass**
- [ ] **Task 9.2**: AST 스캔 벤치마크 스크립트
  - File(s): `scripts/benchmark_ast_scanner.py`
  - Goal: 다양한 프로젝트 크기로 성능 측정
  - Details:
    ```python
    import asyncio
    from pathlib import Path
    from time import time
    from arch_copilot.infrastructure.ast_parser import ASTProjectScanner

    async def benchmark_scan(project_path: Path, file_count: int):
        scanner = ASTProjectScanner()

        start = time()
        result = await scanner.scan(project_path)
        duration = time() - start

        print(f"Files: {file_count}")
        print(f"Duration: {duration:.3f}s")
        print(f"Files/sec: {file_count / duration:.1f}")

        assert duration < 0.1, f"Too slow: {duration}s (target: <0.1s)"

    # 다양한 크기의 샘플 프로젝트 벤치마크
    ```

- [ ] **Task 9.3**: AI 추론 속도 벤치마크
  - File(s): `scripts/benchmark_ai_inference.py`
  - Goal: TPS 및 응답 시간 측정
  - Details: vLLM 서버 성능 테스트 스크립트

- [ ] **Task 9.4**: Dockerfile 작성
  - File(s): `Dockerfile`
  - Goal: 애플리케이션 컨테이너화
  - Details:
    ```dockerfile
    FROM python:3.12-slim

    # NVIDIA GPU 지원을 위한 베이스 이미지로 변경할 수도 있음
    # FROM nvidia/cuda:12.8-runtime-ubuntu24.04

    WORKDIR /app

    COPY pyproject.toml ./
    RUN pip install --no-cache-dir -e .

    COPY arch_copilot ./arch_copilot
    COPY .env.example ./.env

    EXPOSE 8080

    CMD ["python", "-m", "arch_copilot.main"]
    ```

- [ ] **Task 9.5**: docker-compose.yml 작성
  - File(s): `docker-compose.yml`
  - Goal: vLLM + 애플리케이션 통합 실행
  - Details:
    ```yaml
    version: '3.8'

    services:
      vllm:
        image: vllm/vllm-openai:latest
        command: >
          --model openai/gpt-oss-20b
          --kv-cache-dtype fp8
          --max-model-len 16384
          --gpu-memory-utilization 0.95
        ports:
          - "8000:8000"
        deploy:
          resources:
            reservations:
              devices:
                - driver: nvidia
                  count: 1
                  capabilities: [gpu]

      app:
        build: .
        ports:
          - "8080:8080"
        environment:
          - VLLM_BASE_URL=http://vllm:8000
        depends_on:
          - vllm
        volumes:
          - ./storage:/app/storage
    ```

- [ ] **Task 9.6**: Sphinx 문서 자동화 설정
  - File(s): `docs/conf.py`
  - Goal: 코드에서 자동으로 API 문서 생성
  - Details:
    ```python
    # Sphinx configuration
    project = 'Local Arch-Copilot'
    extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.napoleon',
        'sphinx.ext.viewcode',
        'sphinx_rtd_theme',
    ]
    html_theme = 'sphinx_rtd_theme'
    ```

**🔵 REFACTOR: Clean Up Code**
- [ ] **Task 9.7**: 성능 프로파일링
  - Files: 전체 애플리케이션
  - Goal: 병목 지점 식별 및 최적화
  - Checklist:
    - [ ] cProfile로 CPU 병목 분석
    - [ ] memory_profiler로 메모리 사용 분석
    - [ ] 불필요한 I/O 제거

- [ ] **Task 9.8**: 배포 가이드 작성
  - File(s): `docs/guides/deployment.md`
  - Goal: 프로덕션 배포 절차
  - Details:
    - Docker 배포 방법
    - WSL2 네이티브 배포 방법
    - 트러블슈팅 가이드

#### Quality Gate ✋

**⚠️ STOP: Final validation before production release**

**Performance**:
- [ ] **AST Scan**: 1000 파일 <0.1초 달성
- [ ] **Graph Generation**: 1000 노드 <1초 달성
- [ ] **AI Inference**: ≥40 TPS 확인
- [ ] **Memory**: 전체 메모리 사용 <1GB (모델 제외)

**Containerization**:
- [ ] **Docker Build**: 이미지 빌드 성공
- [ ] **Docker Run**: 컨테이너 정상 실행
- [ ] **Docker Compose**: 전체 스택 정상 동작

**Documentation**:
- [ ] **API Docs**: Sphinx 문서 생성 성공
- [ ] **README**: 최신 정보 반영
- [ ] **Deployment Guide**: 배포 절차 완비

**Validation Commands**:
```bash
# 성능 벤치마크
python scripts/benchmark_ast_scanner.py
python scripts/benchmark_ai_inference.py

# Docker 빌드 및 실행
docker build -t arch-copilot .
docker run -p 8080:8080 arch-copilot

# Docker Compose 전체 스택
docker-compose up

# 문서 생성
cd docs
make html
```

**Manual Test Checklist**:
- [ ] Docker 컨테이너로 실행했을 때 모든 기능이 정상 동작하는가?
- [ ] 성능 벤치마크가 모든 목표를 달성하는가?
- [ ] API 문서가 정확하게 생성되는가?

---

## 📋 Updated Architecture Decisions

### Additional Architectural Patterns

| Decision | Rationale | Trade-offs |
|----------|-----------|------------|
| **Dependency Injection Container** | 테스트 용이성, 결합도 감소, 확장성 향상 | 초기 설정 복잡도 증가, 러닝 커브 |
| **Pydantic Settings** | 환경 변수 검증, 타입 안전성, 기본값 관리 | Pydantic 의존성 추가 |
| **Structured Logging (structlog)** | JSON 로그, 검색 용이, 모니터링 통합 | 일반 로그보다 오버헤드 약간 증가 |
| **Metrics Collection** | 성능 모니터링, 병목 지점 파악, 최적화 근거 | 메모리 사용량 약간 증가 |
| **Domain Exception Hierarchy** | 일관된 에러 처리, 레이어 간 명확한 계약 | 예외 클래스 관리 필요 |
| **Docker Containerization** | 배포 일관성, 환경 독립성, 확장성 | 컨테이너 오버헤드, 디버깅 복잡도 |

---

## 🔄 Updated Phase Execution Order

**권장 실행 순서**:
1. **Phase 0**: Project Scaffolding (1-2h)
2. **Phase 0.5**: Configuration & DI Setup (2h)
3. **Phase 1**: AI Infrastructure Setup (3-4h)
4. **Phase 2**: Domain Layer (2-3h)
5. **Phase 3**: Application Layer (3h)
6. **Phase 4**: Infrastructure - AST Parser (3h)
7. **Phase 5**: Infrastructure - Graph Engine (2-3h)
8. **Phase 6**: Infrastructure - AI Client (2-3h)
9. **Phase 7**: Presentation Layer (4-5h)
10. **Phase 8**: Cross-Cutting Concerns (3-4h)
11. **Phase 9**: Performance & Documentation (3-4h)

**총 예상 시간**: 28-37 hours (vs 기존 19-25 hours)

---

## 📊 Updated Progress Tracking

### Completion Status
- **Phase 0 (Scaffolding)**: ⏳ 0% - NEW
- **Phase 0.5 (Config & DI)**: ⏳ 0% - NEW
- **Phase 1 (AI Infrastructure)**: ⏳ 0%
- **Phase 2 (Domain Layer)**: ⏳ 0%
- **Phase 3 (Application Layer)**: ⏳ 0%
- **Phase 4 (Infrastructure - AST)**: ⏳ 0%
- **Phase 5 (Infrastructure - Graph)**: ⏳ 0%
- **Phase 6 (Infrastructure - AI Client)**: ⏳ 0%
- **Phase 7 (Presentation - UI)**: ⏳ 0%
- **Phase 8 (Cross-Cutting)**: ⏳ 0% - NEW
- **Phase 9 (Production)**: ⏳ 0% - NEW

**Overall Progress**: 0% complete

### Updated Time Tracking
| Phase | Estimated | Actual | Variance | Priority |
|-------|-----------|--------|----------|----------|
| Phase 0 | 1-2 hours | - | - | 🔴 CRITICAL |
| Phase 0.5 | 2 hours | - | - | 🔴 CRITICAL |
| Phase 1 | 3-4 hours | - | - | 🔴 HIGH |
| Phase 2 | 2-3 hours | - | - | 🔴 HIGH |
| Phase 3 | 3 hours | - | - | 🔴 HIGH |
| Phase 4 | 3 hours | - | - | 🔴 HIGH |
| Phase 5 | 2-3 hours | - | - | 🔴 HIGH |
| Phase 6 | 2-3 hours | - | - | 🔴 HIGH |
| Phase 7 | 4-5 hours | - | - | 🔴 HIGH |
| Phase 8 | 3-4 hours | - | - | 🟡 MEDIUM |
| Phase 9 | 3-4 hours | - | - | 🟢 LOW |
| **Total** | 28-37 hours | - | - | - |

---

## ✅ Updated Final Checklist

**Before marking plan as COMPLETE**:
- [ ] All 11 phases completed with quality gates passed (기존 7개 + 신규 4개)
- [ ] Full integration testing performed (E2E tests)
- [ ] All documentation updated (README, Architecture Docs, User Guide, API Docs)
- [ ] Performance benchmarks meet targets (0.1s scan, 40-50 TPS AI)
- [ ] Test coverage ≥85% overall
- [ ] Security review completed (no hardcoded secrets, input validation)
- [ ] Clean Architecture compliance verified (dependency rule check)
- [ ] User acceptance testing with real projects
- [ ] **DI Container functioning correctly** - NEW
- [ ] **Configuration management working** - NEW
- [ ] **Structured logging implemented** - NEW
- [ ] **Metrics collection operational** - NEW
- [ ] **Docker deployment tested** - NEW
- [ ] **API documentation generated** - NEW
- [ ] Plan document finalized and archived

---

**Plan Status**: 🔄 Ready to Start (Updated)
**Next Action**: Phase 0 프로젝트 스캐폴딩 시작 - 디렉토리 구조 생성 및 pyproject.toml 설정
**Blocked By**: None
**Last Review**: 2025-12-30
