import asyncio
from typing import List, Dict, Any
import google.generativeai as genai
from arch_copilot.domain.ai.i_llm_client import ILLMClient

class GeminiClient(ILLMClient):
    """Google Gemini API 클라이언트"""

    # API 실패 시 사용할 기본 모델 목록
    DEFAULT_MODELS = [
        "gemini-2.0-flash-exp",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-pro",
        "gemini-pro-vision"
    ]

    def __init__(self, api_key: str, model_name: str = "gemini-1.5-pro") -> None:
        if api_key:
            genai.configure(api_key=api_key)
        self.model_name = model_name
        # 모델명 정규화 (사용자가 'gemini-1.5-flash'만 입력해도 'models/gemini-1.5-flash'로 처리)
        full_model_name = model_name if model_name.startswith("models/") else f"models/{model_name}"
        self.model = genai.GenerativeModel(full_model_name)

    async def generate(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> str:
        """Gemini는 동기 SDK이므로 thread pool에서 실행"""
        def _sync_generate():
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                )
            )
            return response.text

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _sync_generate)

    async def chat_completion(self, messages: List[Dict[str, str]], max_tokens: int = 2048, temperature: float = 0.7) -> str:
        """메시지 리스트를 Gemini 역사(history) 형식으로 변환하여 처리"""
        def _sync_chat():
            # 마지막 메시지를 제외한 나머지를 history로 변환 (역할 불일치 시 오류 가능성 있어 간단히 처리)
            # 여기서는 마지막 메시지만 질문으로 던지고 나머지는 컨텍스트로 무시하거나 간단히 history 생성
            history = []
            for msg in messages[:-1]:
                role = "user" if msg["role"] == "user" else "model"
                history.append({"role": role, "parts": [msg["content"]]})
            
            chat = self.model.start_chat(history=history)
            response = chat.send_message(
                messages[-1]["content"],
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                )
            )
            return response.text

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _sync_chat)

    async def check_health(self) -> bool:
        """모델 목록 조회를 통해 연결 상태 확인"""
        try:
            models = await self.list_models()
            return len(models) > 0
        except Exception:
            return False

    async def list_models(self) -> List[str]:
        """Gemini에서 지원하는 텍스트 생성 가능 모델 목록 조회"""
        def _sync_list():
            try:
                models = genai.list_models()
                # generateContent를 지원하는 모델만 추출
                available = [m.name.replace("models/", "") for m in models if "generateContent" in m.supported_generation_methods]
                # 빈 리스트이거나 API 호출 실패 시 기본 목록 반환
                return available if available else self.DEFAULT_MODELS
            except Exception as e:
                print(f"Failed to fetch Gemini models: {e}, returning default models")
                return self.DEFAULT_MODELS

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _sync_list)
