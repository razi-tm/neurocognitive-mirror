from sqlalchemy import text
from sqlalchemy.orm import Session
from app.rag.embeddings import embed

def retrieve(db: Session, query: str, k: int = 5) -> list[dict]:
    vector = embed([query])[0]
    rows = db.execute(text("""
        SELECT title, source, chunk, 1 - (embedding <=> CAST(:embedding AS vector)) AS score
        FROM paper_chunks
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :k
    """), {"embedding": str(vector), "k": k}).mappings().all()
    return [dict(r) for r in rows]

def build_prompt(question: str, contexts: list[dict], max_chars: int = 6000) -> str:
    used, blocks = 0, []
    for c in contexts:
        block = f"Source: {c['title']} ({c['source']}) score={c.get('score',0):.3f}\n{c['chunk']}"
        if used + len(block) > max_chars:
            break
        blocks.append(block); used += len(block)
    return "Use the neuroscience context for educational interpretation; do not diagnose.\n\n" + "\n\n".join(blocks) + f"\n\nUser data/question:\n{question}"
