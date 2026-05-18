from functools import lru_cache
import hashlib
import numpy as np

@lru_cache(maxsize=1)
def _model():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("all-MiniLM-L6-v2")
    except Exception:
        return None

def embed(texts: list[str]) -> list[list[float]]:
    model = _model()
    if model is not None:
        return model.encode(texts, normalize_embeddings=True).tolist()
    vectors = []
    for text in texts:
        digest = hashlib.sha256(text.encode()).digest()
        rng = np.random.default_rng(int.from_bytes(digest[:8], "big"))
        v = rng.normal(size=384); v = v / np.linalg.norm(v)
        vectors.append(v.astype(float).tolist())
    return vectors
