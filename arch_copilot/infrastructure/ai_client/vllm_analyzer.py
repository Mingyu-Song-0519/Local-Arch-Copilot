from typing import List
from arch_copilot.domain.ai.i_ai_analyzer import IAIAnalyzer
from arch_copilot.domain.entities.violation import ArchitectureViolation
from arch_copilot.domain.ai.i_llm_client import ILLMClient

class VLLMAnalyzer(IAIAnalyzer):
    """LLM 클라이언트를 사용한 아키텍처 분석기 실체화"""

    def __init__(self, llm_client: ILLMClient) -> None:
        self._client = llm_client

    async def analyze_violations(self, violations: List[ArchitectureViolation], project_path: str) -> str:
        """위반 사항을 vLLM에 전달하여 리팩토링 리포트 생성"""
        
        # 1. 레이어 중요도 기반 정렬 (도메인이 가장 중요)
        def get_layer_priority(v: ArchitectureViolation) -> int:
            # 파일 경로에서 레이어 키워드 추출
            path_str = str(v.source_file).lower()
            if "domain" in path_str: return 4
            if "application" in path_str: return 3
            if "infrastructure" in path_str: return 2
            if "presentation" in path_str: return 1
            return 0

        # 중요도 내림차순 정렬 (domain 우선)
        sorted_violations = sorted(violations, key=get_layer_priority, reverse=True)
        
        # 2. 프롬프트 구성 (상위 30개 위반 사항 추출)
        violation_details = "\n".join([
            f"- [{v.violation_type.value}] {v.source_file}: {v.message}"
            for v in sorted_violations[:30]
        ])
        
        prompt = f"""
### Architecture Analysis Request for: {project_path}
Found {len(violations)} violations. Below are the top 30 prioritized issues (sorted by layer criticalness: Domain first):

{violation_details}

### Tasks:
1. **Critical Review**: Why do these violations happen in this specific project? Especially focus on Domain/Application layer leakage.
2. **Refactoring Guide**: Provide 3-Step action plan to fix these issues. 
3. **Impact**: What happens if we don't fix this 'Arch-Debt'?

---
### Constraint (IMPORTANT):
- **Language**: Respond in **CLEAN KOREAN (순수 한국어)**.
- **NO HANJA**: Do NOT use any Chinese characters (Hanja/级/等 etc.). 
- **Terminology**: Use standard Korean IT terms. For technical words, you can put English in parentheses if needed (e.g., '추상화(Abstraction)').
- **Tone**: Professional, Elite Architect style.
- **Format**: Markdown with clear headings.
"""

        messages = [
            {"role": "system", "content": "You are an Elite Clean Architecture Architect who provides professional advice in pure Korean without any Hanja characters."},
            {"role": "user", "content": prompt}
        ]

        # 3. vLLM 호출
        try:
            return await self._client.chat_completion(messages, max_tokens=4096)
        except Exception as e:
            return f"AI 분석 중 오류가 발생했습니다: {str(e)}"

    async def is_available(self) -> bool:
        """vLLM 서버 헬스 체크"""
        return await self._client.check_health()
