"""AI Customer Support Agent — FastAPI application entry point."""
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router

logger = logging.getLogger(__name__)

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
    """Run one-time startup tasks (DB table creation, MLflow validation)."""
    # --- Database ----------------------------------------------------------
    from app.database.database import Base, engine
    from app.models.ticket import Ticket         # noqa: F401 — registers model
    from app.models.chat_message import ChatMessage  # noqa: F401
    from app.models.user import User             # noqa: F401
    from app.models.document import Document     # noqa: F401
    from app.models.feedback import Feedback     # noqa: F401
    
    # Startup Database Health Check
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection verified successfully.")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise e

    Base.metadata.create_all(bind=engine)

    # --- MLflow / Databricks -----------------------------------------------
    from app.monitoring.mlflow_tracker import mlflow_tracker

    status = mlflow_tracker.validate_connection()

    if status["connection_verified"]:
        logger.info(
            "✅ Databricks MLflow tracking is ACTIVE — "
            "experiment_id=%s, host=%s",
            status["experiment_id"],
            status["databricks_host"],
        )
    elif status["tracking_enabled"]:
        logger.warning(
            "⚠️  MLflow tracking enabled but connectivity unverified — %s",
            status.get("reason", "unknown"),
        )
    else:
        logger.warning(
            "⚠️  MLflow tracking is DISABLED — %s",
            status.get("reason", "Databricks not configured or unreachable"),
        )

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

