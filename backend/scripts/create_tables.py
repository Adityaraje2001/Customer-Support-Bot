import sys
from pathlib import Path

# Add backend directory to sys.path so 'app' module can be found
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database.database import Base, engine
from app.models.ticket import Ticket  # noqa: F401
from app.models.chat_message import ChatMessage  # noqa: F401

Base.metadata.create_all(bind=engine)

print("Tables created successfully")