import asyncio
from typing import List, Dict, Any
from arch_copilot.domain.ai.i_llm_client import ILLMClient

class AnthropicClient(ILLMClient):
    """Anthropic Claude API 클라이언트"""

    DEFAULT_MODELS = [
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    ]

    def __init__(self, api_key: str, model_name: str = "claude-3-5-sonnet-20241022") -> None:
        self.api_key = api_key
        self.model_name = model_name
        try:
            import anthropic
            self._client = anthropic.AsyncAnthropic(api_key=api_key)
        except ImportError:
            self._client = None

    async def generate(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> str:
        if not self._client:
            raise ImportError("Anthropic SDK is not installed. Run 'pip install anthropic'.")
        
        response = await self._client.messages.create(
            model=self.model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    async def chat_completion(self, messages: List[Dict[str, str]], max_tokens: int = 2048, temperature: float = 0.7) -> str:
        if not self._client:
            raise ImportError("Anthropic SDK is not installed. Run 'pip install anthropic'.")

        # system message 분리 (Anthropic은 별도 파라미터로 받음)
        system_msg = ""
        filtered_messages = []
        for m in messages:
            if m["role"] == "system":
                system_msg += m["content"] + "\n"
            else:
                filtered_messages.append(m)

        response = await self._client.messages.create(
            model=self.model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_msg.strip() if system_msg else None,
            messages=filtered_messages
        )
        return response.content[0].text

    async def check_health(self) -> bool:
        return self._client is not None

    async def list_models(self) -> List[str]:
        """Anthropic은 현재 모델 목록 API가 제한적이므로 기본 목록 반환"""
        return self.DEFAULT_MODELS
