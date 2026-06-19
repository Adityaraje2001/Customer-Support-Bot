# AI Customer Support Agent

A production-grade AI Customer Support Agent built with FastAPI, LangGraph, Groq, ChromaDB, and Next.js.
Designed with future integrations for Databricks, Delta Lake, and MLflow.

## Architecture

- **Backend**: Python, FastAPI, LangGraph
- **LLM**: Groq (openai/gpt-oss-120b)
- **Vector DB**: ChromaDB with sentence-transformers
- **Frontend**: Next.js
- **Database**: PostgreSQL (Neon)

## Getting Started

1. Clone the repository
2. Set up `.env` files in `backend/` and `frontend/`
3. Run with Docker Compose:

```bash
docker-compose up --build
```

### Database Migration (SQLite to PostgreSQL)

To migrate your existing SQLite data to PostgreSQL:

1. Configure your `DATABASE_URL` in `backend/.env` with your PostgreSQL connection string.
2. Run the migration script:

```bash
python backend/scripts/migrate_sqlite_to_postgres.py
```
