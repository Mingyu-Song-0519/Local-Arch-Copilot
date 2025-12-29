#!/bin/bash

# vLLM Server Start Script for GPT-OSS-20B
# Optimized for RTX 5070 Ti (16GB VRAM)

MODEL_NAME="openai/gpt-oss-20b"
PORT=8000

echo "🚀 Starting vLLM Server with $MODEL_NAME on port $PORT..."

# Optimized parameters:
# - gpu_memory_utilization: 0.9 (Leave some space for OS/UI)
# - max_model_len: 16384 (Support long context)
# - kv_cache_dtype: fp8 (Reduce memory usage, optimized for Ada Lovelace)
# - device: cuda

~/arch_copilot_venv/bin/python3 -m vllm.entrypoints.openai.api_server \
    --model $MODEL_NAME \
    --port $PORT \
    --gpu-memory-utilization 0.90 \
    --max-model-len 16384 \
    --kv-cache-dtype fp8 \
    --trust-remote-code \
    --dtype bfloat16 \
    --enforce-eager
