from app.database.database import SessionLocal
from app.models.ticket import Ticket


class TicketService:

    def create_ticket(
        self,
        session_id: str,
        question: str,
        user_id: int | None = None
    ):

        db = SessionLocal()

        try:

            ticket = Ticket(
                session_id=session_id,
                question=question,
                status="open",
                user_id=user_id
            )

            db.add(ticket)

            db.commit()

            db.refresh(ticket)

            return ticket

        finally:
            db.close()
    
    def get_ticket(
        self,
        ticket_id: int
):
        db = SessionLocal()

        try:
            return (
                db.query(Ticket)
                .filter(Ticket.id == ticket_id)
                .first()
            )

        finally:
            db.close()

    def update_ticket_status(
        self,
        ticket_id: int,
        status: str
    ):
        db = SessionLocal()

        try:
            ticket = (
                db.query(Ticket)
                .filter(Ticket.id == ticket_id)
            .first()
        )

            if not ticket:
                return None

            setattr(ticket, "status", status)

            db.commit()

            db.refresh(ticket)

            return ticket

        finally:
            db.close()

    def get_user_tickets(self, user_id: int):
        db = SessionLocal()

        try:
            return (
                db.query(Ticket)
                .filter(Ticket.user_id == user_id)
                .order_by(Ticket.created_at.desc())
                .all()
            )

        finally:
            db.close()

    def get_tickets_by_session(
        self,
        session_id: str
    ):
        db = SessionLocal()

        try:
            return (
                db.query(Ticket)
                .filter(Ticket.session_id == session_id)
                .order_by(Ticket.created_at.desc())
                .all()
            )

        finally:
            db.close()

    def list_open_tickets(self):
        db = SessionLocal()

        try:
            return (
                db.query(Ticket)
                .filter(Ticket.status == "open")
            .order_by(Ticket.created_at.desc())
            .all()
        )

        finally:
            db.close()
    def list_resolved_tickets(self):
        db = SessionLocal()

        try:
            return (
                db.query(Ticket)
                .filter(Ticket.status == "resolved")
                .order_by(Ticket.created_at.desc())
                .all()
            )

        finally:
            db.close()

    def get_all_tickets(self):
        db = SessionLocal()

        try:
            return db.query(Ticket).all()

        finally:
            db.close()
    