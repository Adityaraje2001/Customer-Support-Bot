"""
Service layer for feedback CRUD and analytics.

Follows the SessionLocal / try-finally pattern used by TicketService.
"""

import logging
from collections import defaultdict

from sqlalchemy.exc import IntegrityError

from app.database.database import SessionLocal
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate

logger = logging.getLogger(__name__)


class FeedbackService:

    def create_feedback(
        self,
        data: FeedbackCreate,
        user_id: int | None = None,
    ) -> Feedback | None:
        """
        Insert a feedback row.

        Returns the created Feedback or None if a duplicate exists
        (same message_id + user_id).
        """
        db = SessionLocal()

        try:
            feedback = Feedback(
                user_id=user_id,
                session_id=data.session_id,
                message_id=data.message_id,
                question=data.question,
                answer=data.answer,
                route_selected=data.route_selected,
                feedback_type=data.feedback_type,
                feedback_comment=data.feedback_comment,
            )

            db.add(feedback)
            db.commit()
            db.refresh(feedback)

            return feedback

        except IntegrityError:
            db.rollback()
            logger.warning(
                "Duplicate feedback for message_id=%s, user_id=%s",
                data.message_id,
                user_id,
            )
            return None

        finally:
            db.close()

    def list_feedback(self) -> list[Feedback]:
        """Return all feedback rows, newest first."""
        db = SessionLocal()

        try:
            return (
                db.query(Feedback)
                .order_by(Feedback.created_at.desc())
                .all()
            )

        finally:
            db.close()

    def get_feedback_stats(self) -> dict:
        """
        Compute aggregated feedback statistics.

        Returns a dict with:
          total, helpful, not_helpful, helpful_pct, not_helpful_pct,
          by_agent: { agent_name: { helpful: N, not_helpful: N } }
        """
        db = SessionLocal()

        try:
            rows = db.query(Feedback).all()

            total = len(rows)
            helpful = sum(1 for r in rows if r.feedback_type == "helpful")
            not_helpful = sum(1 for r in rows if r.feedback_type == "not_helpful")

            by_agent: dict[str, dict[str, int]] = defaultdict(
                lambda: {"helpful": 0, "not_helpful": 0}
            )

            for row in rows:
                agent = str(row.route_selected or "unknown")
                if row.feedback_type == "helpful":
                    by_agent[agent]["helpful"] += 1
                elif row.feedback_type == "not_helpful":
                    by_agent[agent]["not_helpful"] += 1

            return {
                "total": total,
                "helpful": helpful,
                "not_helpful": not_helpful,
                "helpful_pct": round((helpful / total * 100) if total else 0, 1),
                "not_helpful_pct": round((not_helpful / total * 100) if total else 0, 1),
                "by_agent": dict(by_agent),
            }

        finally:
            db.close()
