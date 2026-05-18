from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Local OpenAI Compatible LLM Shim")
class Message(BaseModel):
    role: str
    content: str
class ChatRequest(BaseModel):
    model: str
    messages: list[Message]
    temperature: float = 0.3

@app.get("/health")
def health(): return {"status":"ok"}

@app.post("/v1/chat/completions")
def completions(req: ChatRequest):
    user = " ".join(m.content for m in req.messages if m.role == "user")
    content = "Local LLM narrative: Your longitudinal profile should be interpreted as patterns in working memory, processing speed, and executive control shaped by sleep, stress, and alertness. " + user[:500]
    return {"id":"chatcmpl-local","object":"chat.completion","choices":[{"index":0,"message":{"role":"assistant","content":content},"finish_reason":"stop"}],"model":req.model}
