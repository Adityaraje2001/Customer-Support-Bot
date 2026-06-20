"""
SQLAlchemy model for user feedback on AI responses.

Stores thumbs-up / thumbs-down ratings and optional comments
for analytics and future model improvements.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint

from app.database.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    # Enforce one feedback per message per user
    __table_args__ = (
        UniqueConstraint("message_id", "user_id", name="uq_feedback_message_user"),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        index=True,
        nullable=True,
    )

    session_id = Column(
        String,
        nullable=False,
    )

    message_id = Column(
        String,
        index=True,
        nullable=False,
    )

    question = Column(
        Text,
        nullable=False,
    )

    answer = Column(
        Text,
        nullable=False,
    )

    route_selected = Column(
        String,
        nullable=True,
    )

    feedback_type = Column(
        String,
        nullable=False,
    )

    feedback_comment = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"<Feedback(id={self.id}, user_id={self.user_id}, "
            f"feedback_type='{self.feedback_type}')>"
        )
