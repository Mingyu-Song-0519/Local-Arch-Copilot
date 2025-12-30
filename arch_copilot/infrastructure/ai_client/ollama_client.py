import httpx
from typing import List, Dict, Any
from arch_copilot.domain.ai.i_llm_client import ILLMClient

class OllamaClient(ILLMClient):
    """OpenAI 호환 API를 사용하는 클라이언트 (Ollama, LMStudio, vLLM)"""

    def __init__(self, base_url: str, model_name: str = "mistral-24b:latest") -> None:
        # /v1 경로가 있으면 제거하고 내부에서 상황에 맞게 붙임
        self.base_url = base_url.rstrip('/')
        if self.base_url.endswith('/v1'):
            self.base_url = self.base_url[:-3].rstrip('/')
            
        self.model_name = model_name
        self.timeout = httpx.Timeout(300.0, connect=10.0)

    async def generate(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> str:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
            # OpenAI 호환 completions 엔드포인트
            response = await client.post(f"{self.base_url}/v1/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["text"].strip()

    async def chat_completion(self, messages: List[Dict[str, str]], max_tokens: int = 2048, temperature: float = 0.7) -> str:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            payload = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
            # OpenAI 호환 chat/completions 엔드포인트
            response = await client.post(f"{self.base_url}/v1/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

    async def check_health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # /v1/models 엔드포인트로 헬스체크 대용
                response = await client.get(f"{self.base_url}/v1/models")
                return response.status_code == 200
        except Exception:
            return False

    async def list_models(self) -> List[str]:
        """사용 가능한 모델 목록 조회 (OpenAI /v1/models API 기반)"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/v1/models")
                response.raise_for_status()
                data = response.json()
                # OpenAI 형식: {"data": [{"id": "model-id"}, ...]}
                return [model['id'] for model in data.get('data', [])]
        except Exception as e:
            print(f"Failed to fetch models from {self.base_url}: {e}")
            return []
