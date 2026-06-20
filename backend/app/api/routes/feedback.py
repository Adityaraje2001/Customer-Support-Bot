"""Feedback API routes for submitting and viewing user feedback."""

from fastapi import APIRouter, HTTPException, Depends

from app.auth.rbac import require_customer, require_admin
from app.models.user import User
from app.schemas.feedback import FeedbackCreate, FeedbackResponse, FeedbackStats
from app.services.feedback_service import FeedbackService
from app.monitoring.mlflow_tracker import mlflow_tracker


router = APIRouter(
    prefix="/feedback",
    tags=["feedback"],
)

# =====================================================
# Shared Services
# =====================================================

feedback_service = FeedbackService()


# =====================================================
# Feedback Endpoints
# =====================================================

@router.post("/", response_model=FeedbackResponse, status_code=201)
async def submit_feedback(
    data: FeedbackCreate,
    current_user: User = Depends(require_customer),
):
    """Submit feedback for an AI response. Customers and above."""
    feedback = feedback_service.create_feedback(
        data=data,
        user_id=current_user.id,  # type: ignore
    )

    if feedback is None:
        raise HTTPException(
            status_code=409,
            detail="Feedback already submitted for this message.",
        )

    # Log to MLflow
    mlflow_tracker.track_feedback(
        feedback_type=data.feedback_type,
        route_selected=data.route_selected or "unknown",
        session_id=data.session_id,
        user_id=current_user.id,  # type: ignore
    )

    return feedback


@router.get("/", response_model=list[FeedbackResponse])
async def list_feedback(
    current_user: User = Depends(require_admin),
):
    """List all feedback (admin only)."""
    return feedback_service.list_feedback()


@router.get("/stats", response_model=FeedbackStats)
async def get_feedback_stats(
    current_user: User = Depends(require_admin),
):
    """Get aggregated feedback statistics (admin only)."""
    return feedback_service.get_feedback_stats()
