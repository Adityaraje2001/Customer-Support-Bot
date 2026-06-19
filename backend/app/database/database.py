import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Resolve paths relative to the backend/ directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please configure it in .env.")

from typing import Any

# Connection pooling configurations
engine_kwargs: dict[str, Any] = {
    "pool_pre_ping": True,
    "pool_size": 5,
    "max_overflow": 10
}

# If the URL is SQLite (e.g. local testing before migration), adjust kwargs
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
    # SQLite does not support standard connection pooling sizes in the same way, but it accepts the kwargs safely or we can remove them
    engine_kwargs.pop("pool_size", None)
    engine_kwargs.pop("max_overflow", None)

engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()