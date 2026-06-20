"""
Pydantic schemas for feedback request/response validation.
"""

from datetime import datetime

from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    """Schema for submitting new feedback."""
    session_id: str
    message_id: str
    question: str
    answer: str
    route_selected: str | None = None
    feedback_type: str  # "helpful" or "not_helpful"
    feedback_comment: str | None = None


class FeedbackResponse(BaseModel):
    """Schema for returning feedback records."""
    id: int
    user_id: int | None
    session_id: str
    message_id: str
    question: str
    answer: str
    route_selected: str | None
    feedback_type: str
    feedback_comment: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class FeedbackStats(BaseModel):
    """Aggregated feedback statistics for the admin analytics page."""
    total: int
    helpful: int
    not_helpful: int
    helpful_pct: float
    not_helpful_pct: float
    by_agent: dict[str, dict[str, int]]
