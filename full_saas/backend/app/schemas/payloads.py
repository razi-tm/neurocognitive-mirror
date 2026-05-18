from datetime import datetime
from pydantic import BaseModel, Field

class SessionPayload(BaseModel):
    anonymous_id: str = Field(min_length=8, max_length=64)
    session_date: datetime | None = None
    sleep_quality: float = Field(ge=1, le=10)
    stress: float = Field(ge=1, le=10)
    alertness: float = Field(ge=1, le=10)
    digit_span: int = Field(ge=1, le=30)
    reaction_time_ms: float = Field(ge=50, le=3000)
    stroop_accuracy: float = Field(ge=0, le=1)
    stroop_interference_ms: float = Field(ge=-500, le=2000)
    notes: str = ""
    opt_in_sync: bool = False

class AnalyzeRequest(BaseModel):
    sessions: list[SessionPayload] = Field(min_length=1)
    persist: bool = False

class NarrativeRequest(AnalyzeRequest):
    include_rag: bool = True

class ReportRequest(NarrativeRequest):
    format: str = Field(pattern="^(html|pdf)$")

class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=500)
    k: int = Field(default=5, ge=1, le=20)

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)
