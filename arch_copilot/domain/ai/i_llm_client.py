from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ILLMClient(ABC):
    """LLM 클라이언트 인터페이스 (모든 공급자가 구현)"""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> str:
        """텍스트 생성 (Completion API)"""
        pass

    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> str:
        """채팅 형식 생성 (Chat API)"""
        pass

    @abstractmethod
    async def check_health(self) -> bool:
        """서버 또는 API 상태 확인"""
        pass

    @abstractmethod
    async def list_models(self) -> List[str]:
        """사용 가능한 모델 목록 조회"""
        pass
