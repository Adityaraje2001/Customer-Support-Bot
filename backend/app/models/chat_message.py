import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, Integer
from app.database.database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    # Unique identifier for each message
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Groups messages into conversations; indexed for fast queries
    session_id = Column(String, index=True, nullable=False)
    
    # Ownership (nullable for backwards compat)
    user_id = Column(Integer, index=True, nullable=True)
    
    # "user", "assistant", or "system"
    role = Column(String, nullable=False)
    
    # The actual message body
    content = Column(Text, nullable=False)
    
    # For ordering messages chronologically
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_llm_dict(self) -> dict:
        """Return {"role": ..., "content": ...} for the LLM API."""
        return {
            "role": self.role,
            "content": self.content
        }