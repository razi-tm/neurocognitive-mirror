from datetime import datetime
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.db import get_db
from app.models.entities import CognitiveSession, User
from app.rag.retriever import build_prompt, retrieve
from app.schemas.payloads import AnalyzeRequest, AuthRequest, NarrativeRequest, ReportRequest, SearchRequest, TokenPair
from app.services.analytics import analyze_sessions
from app.services.llm import chat
from app.services.reporting import html_report, pdf_report
from app.core.security import create_token, hash_password, verify_password

router = APIRouter(prefix="/api")


@router.post("/auth/register", response_model=TokenPair)
def register(req: AuthRequest, db: Session = Depends(get_db)) -> TokenPair:
    existing = db.query(User).filter(User.email == req.email.lower()).first()
    if existing:
        from fastapi import HTTPException
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(email=req.email.lower(), password_hash=hash_password(req.password))
    db.add(user); db.commit()
    return TokenPair(access_token=create_token(user.email, 30), refresh_token=create_token(user.email, 60 * 24 * 14))

@router.post("/auth/login", response_model=TokenPair)
def login(req: AuthRequest, db: Session = Depends(get_db)) -> TokenPair:
    user = db.query(User).filter(User.email == req.email.lower()).first()
    if not user or not verify_password(req.password, user.password_hash):
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenPair(access_token=create_token(user.email, 30), refresh_token=create_token(user.email, 60 * 24 * 14))

@router.get("/demo-data")
def demo_data() -> dict:
    import math, random
    rng = random.Random(42); rows=[]
    for i in range(52):
        sleep=max(1,min(10,7+math.sin(i/8)+rng.uniform(-.6,.6))); stress=max(1,min(10,4+rng.uniform(-1,1)-.3*(sleep-7)))
        alert=max(1,min(10,6+.5*(sleep-7)-.2*stress+rng.uniform(-.7,.7)))
        rows.append({"anonymous_id":"demo-user","session_date":datetime.utcnow().isoformat(),"sleep_quality":sleep,"stress":stress,"alertness":alert,"digit_span":round(7+.4*(sleep-7)+.15*alert-.1*stress+rng.uniform(-1,1)),"reaction_time_ms":280+9*stress-5*alert+rng.uniform(-25,25),"stroop_accuracy":max(.4,min(.99,.82+.015*alert-.012*stress+rng.uniform(-.05,.05))),"stroop_interference_ms":120+9*stress-6*alert+rng.uniform(-25,25),"notes":"demo","opt_in_sync":False})
    return {"sessions": rows}

@router.post("/analyze")
def analyze(req: AnalyzeRequest, db: Session = Depends(get_db)) -> dict:
    analysis = analyze_sessions(req.sessions)
    if req.persist and settings.sync_enabled:
        for s in req.sessions:
            if s.opt_in_sync:
                db.add(CognitiveSession(**s.model_dump(exclude={"session_date"}), session_date=s.session_date or datetime.utcnow()))
        db.commit()
    return analysis

@router.post("/narrative")
async def narrative(req: NarrativeRequest, db: Session = Depends(get_db)) -> dict:
    analysis = analyze_sessions(req.sessions)
    contexts = retrieve(db, str(analysis), 4) if req.include_rag else []
    prompt = build_prompt(str(analysis), contexts) if contexts else str(analysis)
    return {"narrative": await chat(prompt), "contexts": contexts, "analysis": analysis}

@router.post("/report")
async def report(req: ReportRequest, db: Session = Depends(get_db)) -> Response:
    analysis = analyze_sessions(req.sessions)
    contexts = retrieve(db, str(analysis), 4) if req.include_rag else []
    narrative = await chat(build_prompt(str(analysis), contexts) if contexts else str(analysis))
    if req.format == "pdf":
        return Response(pdf_report(narrative, analysis), media_type="application/pdf")
    return Response(html_report(narrative, analysis), media_type="text/html")

@router.post("/search")
def search(req: SearchRequest, db: Session = Depends(get_db)) -> dict:
    return {"results": retrieve(db, req.query, req.k)}
