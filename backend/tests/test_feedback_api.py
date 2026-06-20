"""
Purpose:
Test the feedback API endpoints (RBAC, creation, stats).

Execution:
Run `pytest backend/tests/test_feedback_api.py -v`
"""

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from app.main import app
from app.auth.dependencies import get_current_user
from app.models.user import User


# ── Fixtures ──────────────────────────────────────────────────────────────

def _make_customer():
    return User(id=1, email="customer@test.com", username="customer", role="customer")

def _make_admin():
    return User(id=99, email="admin@test.com", username="admin", role="admin")


@pytest.fixture
def feedback_payload():
    return {
        "session_id": "sess-001",
        "message_id": "msg-001",
        "question": "How do I reset my password?",
        "answer": "Click forgot password.",
        "route_selected": "support",
        "feedback_type": "helpful",
    }


# ── POST /api/feedback ───────────────────────────────────────────────────

def test_submit_feedback_success(feedback_payload):
    """Customer can submit feedback and receives 201."""
    app.dependency_overrides[get_current_user] = _make_customer

    mock_feedback = MagicMock()
    mock_feedback.id = 1
    mock_feedback.user_id = 1
    mock_feedback.session_id = "sess-001"
    mock_feedback.message_id = "msg-001"
    mock_feedback.question = "How do I reset my password?"
    mock_feedback.answer = "Click forgot password."
    mock_feedback.route_selected = "support"
    mock_feedback.feedback_type = "helpful"
    mock_feedback.feedback_comment = None
    mock_feedback.created_at = "2026-06-20T12:00:00"

    with patch("app.api.routes.feedback.feedback_service") as mock_service, \
         patch("app.api.routes.feedback.mlflow_tracker") as mock_mlflow:
        mock_service.create_feedback.return_value = mock_feedback

        with TestClient(app) as client:
            response = client.post("/api/feedback/", json=feedback_payload)

        assert response.status_code == 201
        data = response.json()
        assert data["feedback_type"] == "helpful"
        assert data["message_id"] == "msg-001"
        mock_mlflow.track_feedback.assert_called_once()

    app.dependency_overrides.pop(get_current_user, None)


def test_submit_feedback_duplicate(feedback_payload):
    """Duplicate feedback returns 409."""
    app.dependency_overrides[get_current_user] = _make_customer

    with patch("app.api.routes.feedback.feedback_service") as mock_service, \
         patch("app.api.routes.feedback.mlflow_tracker"):
        mock_service.create_feedback.return_value = None

        with TestClient(app) as client:
            response = client.post("/api/feedback/", json=feedback_payload)

        assert response.status_code == 409
        assert "already submitted" in response.json()["detail"]

    app.dependency_overrides.pop(get_current_user, None)


# ── GET /api/feedback ────────────────────────────────────────────────────

def test_list_feedback_admin_only():
    """Customer cannot list all feedback (403)."""
    app.dependency_overrides[get_current_user] = _make_customer

    with TestClient(app) as client:
        response = client.get("/api/feedback/")

    assert response.status_code == 403
    app.dependency_overrides.pop(get_current_user, None)


def test_list_feedback_as_admin():
    """Admin can list all feedback."""
    app.dependency_overrides[get_current_user] = _make_admin

    with patch("app.api.routes.feedback.feedback_service") as mock_service:
        mock_service.list_feedback.return_value = []

        with TestClient(app) as client:
            response = client.get("/api/feedback/")

        assert response.status_code == 200
        assert response.json() == []

    app.dependency_overrides.pop(get_current_user, None)


# ── GET /api/feedback/stats ──────────────────────────────────────────────

def test_get_feedback_stats_admin_only():
    """Customer cannot access feedback stats (403)."""
    app.dependency_overrides[get_current_user] = _make_customer

    with TestClient(app) as client:
        response = client.get("/api/feedback/stats")

    assert response.status_code == 403
    app.dependency_overrides.pop(get_current_user, None)


def test_get_feedback_stats_as_admin():
    """Admin can view feedback stats."""
    app.dependency_overrides[get_current_user] = _make_admin

    with patch("app.api.routes.feedback.feedback_service") as mock_service:
        mock_service.get_feedback_stats.return_value = {
            "total": 10,
            "helpful": 7,
            "not_helpful": 3,
            "helpful_pct": 70.0,
            "not_helpful_pct": 30.0,
            "by_agent": {"support": {"helpful": 5, "not_helpful": 2}},
        }

        with TestClient(app) as client:
            response = client.get("/api/feedback/stats")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 10
        assert data["helpful_pct"] == 70.0

    app.dependency_overrides.pop(get_current_user, None)
