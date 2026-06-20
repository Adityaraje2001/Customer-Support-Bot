"""
Purpose:
Test the `FeedbackService` which handles database operations for feedback.

Mocks required:
- `app.services.feedback_service.SessionLocal`: To prevent actual database connections.

Execution:
Run `pytest backend/tests/test_feedback_service.py -v`
"""

import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import IntegrityError

from app.services.feedback_service import FeedbackService
from app.schemas.feedback import FeedbackCreate
from app.models.feedback import Feedback


@pytest.fixture
def mock_session():
    """Mocks the SQLAlchemy SessionLocal to return a MagicMock session."""
    with patch("app.services.feedback_service.SessionLocal") as mock_session_cls:
        mock_db = MagicMock()
        mock_session_cls.return_value = mock_db
        yield mock_db


@pytest.fixture
def feedback_service():
    return FeedbackService()


@pytest.fixture
def sample_feedback_data():
    return FeedbackCreate(
        session_id="session-abc",
        message_id="msg-123",
        question="How do I reset my password?",
        answer="Click on the forgot password link.",
        route_selected="support",
        feedback_type="helpful",
        feedback_comment=None,
    )


# ── Create feedback ──────────────────────────────────────────────────────

def test_create_feedback(feedback_service, mock_session, sample_feedback_data):
    """Verify feedback is created, committed, and refreshed."""
    result = feedback_service.create_feedback(
        data=sample_feedback_data,
        user_id=1,
    )

    assert result is not None
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    mock_session.close.assert_called_once()


def test_create_feedback_sets_fields(feedback_service, mock_session, sample_feedback_data):
    """Verify the created Feedback object has the correct field values."""
    result = feedback_service.create_feedback(
        data=sample_feedback_data,
        user_id=42,
    )

    assert result.session_id == "session-abc"
    assert result.message_id == "msg-123"
    assert result.question == "How do I reset my password?"
    assert result.answer == "Click on the forgot password link."
    assert result.route_selected == "support"
    assert result.feedback_type == "helpful"
    assert result.user_id == 42


def test_create_feedback_duplicate_returns_none(feedback_service, mock_session, sample_feedback_data):
    """Verify that a duplicate (IntegrityError) returns None."""
    mock_session.commit.side_effect = IntegrityError(
        statement="INSERT", params={}, orig=Exception("UNIQUE constraint")
    )

    result = feedback_service.create_feedback(
        data=sample_feedback_data,
        user_id=1,
    )

    assert result is None
    mock_session.rollback.assert_called_once()
    mock_session.close.assert_called_once()


# ── List feedback ────────────────────────────────────────────────────────

def test_list_feedback(feedback_service, mock_session):
    """Verify listing returns all feedback ordered by created_at desc."""
    mock_feedback_1 = MagicMock(spec=Feedback)
    mock_feedback_2 = MagicMock(spec=Feedback)

    mock_query = mock_session.query.return_value
    mock_order = mock_query.order_by.return_value
    mock_order.all.return_value = [mock_feedback_1, mock_feedback_2]

    results = feedback_service.list_feedback()

    assert len(results) == 2
    assert results == [mock_feedback_1, mock_feedback_2]
    mock_session.query.assert_called_once_with(Feedback)
    mock_session.close.assert_called_once()


# ── Get feedback stats ───────────────────────────────────────────────────

def test_get_feedback_stats_empty(feedback_service, mock_session):
    """Verify stats with no feedback returns zeroes."""
    mock_session.query.return_value.all.return_value = []

    stats = feedback_service.get_feedback_stats()

    assert stats["total"] == 0
    assert stats["helpful"] == 0
    assert stats["not_helpful"] == 0
    assert stats["helpful_pct"] == 0
    assert stats["not_helpful_pct"] == 0
    assert stats["by_agent"] == {}


def test_get_feedback_stats_with_data(feedback_service, mock_session):
    """Verify stats aggregation with mixed feedback data."""
    fb1 = MagicMock(feedback_type="helpful", route_selected="support")
    fb2 = MagicMock(feedback_type="helpful", route_selected="support")
    fb3 = MagicMock(feedback_type="not_helpful", route_selected="billing")
    fb4 = MagicMock(feedback_type="helpful", route_selected="billing")

    mock_session.query.return_value.all.return_value = [fb1, fb2, fb3, fb4]

    stats = feedback_service.get_feedback_stats()

    assert stats["total"] == 4
    assert stats["helpful"] == 3
    assert stats["not_helpful"] == 1
    assert stats["helpful_pct"] == 75.0
    assert stats["not_helpful_pct"] == 25.0
    assert stats["by_agent"]["support"]["helpful"] == 2
    assert stats["by_agent"]["support"]["not_helpful"] == 0
    assert stats["by_agent"]["billing"]["helpful"] == 1
    assert stats["by_agent"]["billing"]["not_helpful"] == 1
