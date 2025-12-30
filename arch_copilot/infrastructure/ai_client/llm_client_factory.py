from arch_copilot.domain.config.i_config import IConfig
from arch_copilot.domain.ai.i_llm_client import ILLMClient
from arch_copilot.infrastructure.ai_client.ollama_client import OllamaClient

class LLMClientFactory:
    """LLM 클라이언트 팩토리 (Strategy Pattern)"""

    @staticmethod
    def create(config: IConfig) -> ILLMClient:
        """설정에 따라 적절한 LLM 클라이언트 생성"""
        provider = config.llm_provider

        if provider in ["ollama", "lmstudio", "vllm"]:
            # OpenAI 호환 로컬 서버들 (vLLM 포함)
            base_url = config.llm_base_url or (config.vllm_base_url if hasattr(config, 'vllm_base_url') else "http://localhost:8000")
            model_name = config.llm_model
            return OllamaClient(base_url=base_url, model_name=model_name)

        elif provider == "gemini":
            from arch_copilot.infrastructure.ai_client.gemini_client import GeminiClient
            api_key = config.llm_api_key.get_secret_value() if hasattr(config.llm_api_key, 'get_secret_value') else str(config.llm_api_key)
            return GeminiClient(api_key=api_key, model_name=config.llm_model)

        elif provider == "openai":
            from arch_copilot.infrastructure.ai_client.openai_client import OpenAIClient
            api_key = config.llm_api_key.get_secret_value() if hasattr(config.llm_api_key, 'get_secret_value') else str(config.llm_api_key)
            return OpenAIClient(api_key=api_key, model_name=config.llm_model)

        elif provider == "anthropic":
            from arch_copilot.infrastructure.ai_client.anthropic_client import AnthropicClient
            api_key = config.llm_api_key.get_secret_value() if hasattr(config.llm_api_key, 'get_secret_value') else str(config.llm_api_key)
            return AnthropicClient(api_key=api_key, model_name=config.llm_model)

        else:
            # 기본적으로 OllamaClient(OpenAI 호환)를 시도
            base_url = config.llm_base_url or (config.vllm_base_url if hasattr(config, 'vllm_base_url') else "http://localhost:8000")
            return OllamaClient(base_url=base_url, model_name=config.llm_model)
