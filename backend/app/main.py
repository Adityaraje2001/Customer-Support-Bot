"""AI Customer Support Agent — FastAPI application entry point."""
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


# ---------------------------------------------------------------------------
# Lifespan — replaces deprecated @app.on_event("startup")
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run one-time startup tasks (DB table creation)."""
    from app.database.database import Base, engine
    from app.models.ticket import Ticket         # noqa: F401 — registers model
    from app.models.chat_message import ChatMessage  # noqa: F401
    from app.models.user import User             # noqa: F401
    Base.metadata.create_all(bind=engine)
    yield


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
app = FastAPI(
    title="AI Customer Support Agent API",
    description="Backend API for AI Customer Support Agent",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to AI Customer Support Agent API"}


app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

