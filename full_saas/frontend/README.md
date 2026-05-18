# Frontend

React + Vite + TypeScript local-first client.

## Setup

```bash
npm install
```

## Run

```bash
npm run dev
```

## Environment Variables

| Variable | Purpose |
|---|---|
| `VITE_API_URL` | Backend URL, defaults to `http://localhost:8000`. |

## Deployment

The Docker Compose service runs Vite for local-first use. For production, run `npm run build` and serve `dist/` behind TLS.

## Architecture

IndexedDB via Dexie stores sessions locally. Axios calls are opt-in for analysis, narrative, report, search, and sync.
