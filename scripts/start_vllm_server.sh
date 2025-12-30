#!/bin/bash

# vLLM Server Start Script for GPT-OSS-20B
# Balanced Config for RTX 5070 Ti (16GB VRAM)

MODEL_NAME="openai/gpt-oss-20b"
PORT=8000

echo "🚀 Starting vLLM Server in BALANCED mode..."
echo "💡 Aiming for 13.6GB (0.85) usage to balance model and system."

~/arch_copilot_venv/bin/python3 -m vllm.entrypoints.openai.api_server \
    --model $MODEL_NAME \
    --port $PORT \
    --kv-cache-dtype auto \
    --max-model-len 16384 \
    --gpu-memory-utilization 0.85 \
    --enforce-eager \
    --trust-remote-code \
    --disable-log-stats \
    --uvicorn-log-level info
