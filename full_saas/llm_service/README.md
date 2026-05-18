# LLM Service

OpenAI-compatible local service. The bundled shim is CPU-light for reliable boot. Replace with vLLM for GPU Llama 3 8B inference as documented in `full_saas/README.md`.

## Run

```bash
docker compose up llm_service --build
```

## Environment

No required variables for the shim. vLLM deployments require model cache/Hugging Face credentials.
