from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from app.core.db import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class CognitiveSession(Base):
    __tablename__ = "cognitive_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    anonymous_id: Mapped[str] = mapped_column(String(64), index=True)
    session_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    sleep_quality: Mapped[float] = mapped_column(Float)
    stress: Mapped[float] = mapped_column(Float)
    alertness: Mapped[float] = mapped_column(Float)
    digit_span: Mapped[int] = mapped_column(Integer)
    reaction_time_ms: Mapped[float] = mapped_column(Float)
    stroop_accuracy: Mapped[float] = mapped_column(Float)
    stroop_interference_ms: Mapped[float] = mapped_column(Float)
    notes: Mapped[str] = mapped_column(Text, default="")
    opt_in_sync: Mapped[bool] = mapped_column(Boolean, default=False)

class PaperChunk(Base):
    __tablename__ = "paper_chunks"
    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(500))
    chunk: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(Vector(384))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
