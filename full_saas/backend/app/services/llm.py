import httpx
from app.core.config import settings

async def chat(prompt: str) -> str:
    payload = {"model": settings.llm_model, "messages": [{"role":"system","content":"You produce concise neuroscience-informed, privacy-preserving cognitive analytics."},{"role":"user","content":prompt}], "temperature": 0.35}
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f"{settings.llm_base_url.rstrip('/')}/chat/completions", json=payload, headers={"Authorization": f"Bearer {settings.llm_api_key}"})
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
    except Exception:
        return "Local narrative fallback: recent cognitive efficiency reflects the interaction of sleep, stress, alertness, working memory, response speed, and executive inhibition. This educational summary is not a diagnosis."
