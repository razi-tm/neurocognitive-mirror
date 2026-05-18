# Datasets

Seed neuroscience context used by the RAG pipeline.

## Setup and Run

After Postgres is running, ingest files with:

```bash
cd full_saas/backend
python scripts/ingest_papers.py
```

## Environment

Uses `DATABASE_URL` from the backend environment.

## Deployment

Add curated Markdown or text files to `neuroscience/` and rerun ingestion. Content is embedded with `all-MiniLM-L6-v2` and stored in pgvector.
