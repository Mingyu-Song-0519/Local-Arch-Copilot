import asyncio
from typing import List, Dict, Any
from arch_copilot.domain.ai.i_llm_client import ILLMClient

class OpenAIClient(ILLMClient):
    """OpenAI API 클라이언트"""

    DEFAULT_MODELS = [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-3.5-turbo"
    ]

    def __init__(self, api_key: str, model_name: str = "gpt-4o") -> None:
        self.api_key = api_key
        self.model_name = model_name
        try:
            from openai import AsyncOpenAI
            self._client = AsyncOpenAI(api_key=api_key)
        except ImportError:
            self._client = None

    async def generate(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> str:
        if not self._client:
            raise ImportError("OpenAI SDK is not installed. Run 'pip install openai'.")
        
        response = await self._client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content

    async def chat_completion(self, messages: List[Dict[str, str]], max_tokens: int = 2048, temperature: float = 0.7) -> str:
        if not self._client:
            raise ImportError("OpenAI SDK is not installed. Run 'pip install openai'.")

        response = await self._client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content

    async def check_health(self) -> bool:
        return self._client is not None

    async def list_models(self) -> List[str]:
        """OpenAI 모델 목록 조회"""
        if not self._client:
            return self.DEFAULT_MODELS
        try:
            models = await self._client.models.list()
            # gpt 계열 모델만 필터링
            available = [m.id for m in models.data if "gpt" in m.id]
            return sorted(available) if available else self.DEFAULT_MODELS
        except Exception:
            return self.DEFAULT_MODELS
