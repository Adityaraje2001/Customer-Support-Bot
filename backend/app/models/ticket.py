from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from app.database.database import Base

from datetime import datetime


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id = Column(
        String,
        nullable=False
    )

    user_id = Column(
        Integer,
        index=True,
        nullable=True
    )

    question = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        default="open"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )