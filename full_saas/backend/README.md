# Backend

FastAPI analytics, RAG, reporting, search, and optional sync service.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

## Environment Variables

`DATABASE_URL`, `REDIS_URL`, `ELASTICSEARCH_URL`, `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`, `JWT_SECRET`, `CORS_ORIGINS`, `SYNC_ENABLED`.

## Deployment

Use the repository Docker Compose file. Run `python scripts/ingest_papers.py` after database startup to seed RAG chunks.

## Architecture

Routers live in `app/api`, schemas in `app/schemas`, persistence models in `app/models`, and RAG/LLM/reporting services in `app/services` and `app/rag`.
