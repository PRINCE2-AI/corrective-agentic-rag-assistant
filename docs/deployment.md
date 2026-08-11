# Deployment Guide

Corrective Agentic RAG Assistant can run locally through Python or through Docker.

## Local API

```bash
uvicorn app.api:api --host 0.0.0.0 --port 8000
```

## Local Dashboard

```bash
streamlit run app/ui.py
```

## Docker API

```bash
docker build -t corrective-agentic-rag-assistant .
docker run --env-file .env -p 8000:8000 corrective-agentic-rag-assistant
```

## Docker Compose

```bash
docker compose up --build
```

Services:

| Service | URL |
| --- | --- |
| API | http://localhost:8000 |
| Dashboard | http://localhost:8501 |

## Notes

- Start from `.env.example` and create `.env` before running Docker Compose.
- Ollama and Tavily are optional; the project should degrade gracefully when they are not configured.
- The `data/` directory is mounted as a local volume for sample documents and generated stores.
