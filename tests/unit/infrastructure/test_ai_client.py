"""
AI Client Unit Test (Mocked)
"""

import pytest
import respx
from httpx import Response
from arch_copilot.infrastructure.ai_client.vllm_client import VLLMClient


@pytest.mark.asyncio
async def test_vllm_client_generate_success() -> None:
    client = VLLMClient()
    
    with respx.mock:
        respx.post("http://localhost:8000/v1/completions").mock(
            return_value=Response(200, json={
                "choices": [{"text": "Hello Architecture"}]
            })
        )
        
        result = await client.generate("Hi")
        assert result == "Hello Architecture"

@pytest.mark.asyncio
async def test_vllm_client_health_check() -> None:
    client = VLLMClient()
    
    with respx.mock:
        respx.get("http://localhost:8000/v1/models").mock(return_value=Response(200))
        assert await client.check_health() is True
        
        respx.get("http://localhost:8000/v1/models").mock(return_value=Response(500))
        assert await client.check_health() is False
