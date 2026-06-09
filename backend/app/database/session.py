from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

# Create the data directory if it doesn't already exist to prevent Path errors
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Define the connection string
DATABASE_URL = f"sqlite:///{DATA_DIR / 'app.db'}"

# 2. Create the SQLAlchemy Engine
# connect_args={"check_same_thread": False} is required for SQLite to play nicely with FastAPI's async thread pooling
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# 3. Create the Session Factory
# autocommit and autoflush are turned off as standard best practice for safe database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the Declarative Base
# All of your ORM models will inherit from this class so SQLAlchemy recognizes them as tables
Base = declarative_base()