from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.core.db import Base, SessionLocal, engine
from sqlalchemy import text
from app.models.entities import PaperChunk
from app.rag.embeddings import embed

DATA = Path(__file__).resolve().parents[2] / "datasets" / "neuroscience"

def chunks(text: str, size: int = 900):
    words = text.split()
    for i in range(0, len(words), size):
        yield " ".join(words[i:i+size])

if __name__ == "__main__":
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for path in DATA.glob("*.md"):
            title = path.stem.replace("_", " ").title()
            existing = db.query(PaperChunk).filter(PaperChunk.source == str(path.name)).first()
            if existing:
                continue
            parts = list(chunks(path.read_text()))
            vectors = embed(parts)
            for part, vec in zip(parts, vectors):
                db.add(PaperChunk(source=path.name, title=title, chunk=part, embedding=vec))
        db.commit()
    finally:
        db.close()
