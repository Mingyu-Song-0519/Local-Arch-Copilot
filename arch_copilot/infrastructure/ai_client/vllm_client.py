"""
AI Client Implementation (vLLM / OpenAI Compatible)

httpx를 사용하여 vLLM 서버와 통신합니다.
"""

import httpx
from typing import Any, Dict, List, Optional


class VLLMClient:
    """vLLM 서버 전용 OpenAI 호환 클라이언트"""

    def __init__(self, base_url: str = "http://localhost:8000/v1", model_name: str = "openai/gpt-oss-20b") -> None:
        self.base_url = base_url
        self.model_name = model_name
        self.timeout = httpx.Timeout(120.0, connect=10.0) # 긴 추론 대기 시간 고려

    async def generate(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> str:
        """텍스트 생성을 요청합니다."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
            response = await client.post(f"{self.base_url}/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["text"].strip()

    async def chat_completion(self, messages: List[Dict[str, str]], max_tokens: int = 2048) -> str:
        """채팅 형식의 추론을 요청합니다."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            payload = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": max_tokens,
            }
            response = await client.post(f"{self.base_url}/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

    async def check_health(self) -> bool:
        """서버 상태를 확인합니다."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/models")
                return response.status_code == 200
        except Exception:
            return False
