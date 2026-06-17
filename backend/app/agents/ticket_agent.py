import re

from app.services.ticket_service import TicketService


class TicketAgent:

    def __init__(self):
        self.ticket_service = TicketService()

    def run(
        self,
        question: str,
        session_id: str
    ):
        question_lower = question.lower()

        # =====================================================
        # Ticket Listing
        # =====================================================

        if self._is_my_tickets_request(question_lower):
            return self.get_my_tickets(session_id)

        if self._is_open_tickets_request(question_lower):
            return self.get_open_tickets()

        if self._is_resolved_tickets_request(question_lower):
            return self.get_resolved_tickets()

        # =====================================================
        # Ticket Lifecycle Actions
        # =====================================================

        ticket_id = self._extract_ticket_id(question)

        if ticket_id:

            if self._is_start_ticket_request(question_lower):
                return self.start_progress(ticket_id)

            if self._is_resolve_ticket_request(question_lower):
                return self.resolve_ticket(ticket_id)

            if self._is_close_ticket_request(question_lower):
                return self.close_ticket(ticket_id)

            return self.get_ticket_status(ticket_id)

        # =====================================================
        # Create Ticket
        # =====================================================

        return self.create_ticket(
            question=question,
            session_id=session_id
        )

    # =====================================================
    # Helpers
    # =====================================================

    def _extract_ticket_id(
        self,
        question: str
    ) -> int | None:
        match = re.search(
            r"ticket\s*#?(\d+)",
            question.lower()
        )

        return int(match.group(1)) if match else None

    def _is_my_tickets_request(
        self,
        question: str
    ) -> bool:
        return any(
            phrase in question
            for phrase in [
                "my tickets",
                "show my tickets",
                "list my tickets"
            ]
        )

    def _is_open_tickets_request(
        self,
        question: str
    ) -> bool:
        return "open tickets" in question

    def _is_resolved_tickets_request(
        self,
        question: str
    ) -> bool:
        return "resolved tickets" in question

    def _is_start_ticket_request(
        self,
        question: str
    ) -> bool:
        return (
            "start ticket" in question
            or "in progress" in question
        )

    def _is_resolve_ticket_request(
        self,
        question: str
    ) -> bool:
        return "resolve ticket" in question

    def _is_close_ticket_request(
        self,
        question: str
    ) -> bool:
        return "close ticket" in question

    # =====================================================
    # Create Ticket
    # =====================================================

    def create_ticket(
        self,
        question: str,
        session_id: str
    ):
        ticket = self.ticket_service.create_ticket(
            session_id=session_id,
            question=question
        )

        return (
            f"Support ticket #{ticket.id} has been created successfully.\n"
            f"Status: {ticket.status}\n"
            f"Created At: {ticket.created_at}"
        )

    # =====================================================
    # Ticket Status
    # =====================================================

    def get_ticket_status(
        self,
        ticket_id: int
    ):
        ticket = self.ticket_service.get_ticket(ticket_id)

        if not ticket:
            return f"Ticket #{ticket_id} was not found."

        return (
            f"Ticket #{ticket.id}\n"
            f"Status: {ticket.status}\n"
            f"Created At: {ticket.created_at}"
        )

    # =====================================================
    # Ticket Listing
    # =====================================================

    def get_my_tickets(
        self,
        session_id: str
    ):
        tickets = self.ticket_service.get_tickets_by_session(
            session_id
        )

        return self.format_ticket_list(tickets)

    def get_open_tickets(self):
        tickets = self.ticket_service.list_open_tickets()

        return self.format_ticket_list(tickets)

    def get_resolved_tickets(self):
        tickets = self.ticket_service.list_resolved_tickets()

        return self.format_ticket_list(tickets)

    # =====================================================
    # Ticket Lifecycle
    # =====================================================

    def start_progress(
        self,
        ticket_id: int
    ):
        ticket = self.ticket_service.update_ticket_status(
            ticket_id,
            "in_progress"
        )

        if not ticket:
            return f"Ticket #{ticket_id} was not found."

        return f"Ticket #{ticket.id} marked as in progress."

    def resolve_ticket(
        self,
        ticket_id: int
    ):
        ticket = self.ticket_service.update_ticket_status(
            ticket_id,
            "resolved"
        )

        if not ticket:
            return f"Ticket #{ticket_id} was not found."

        return f"Ticket #{ticket.id} marked as resolved."

    def close_ticket(
        self,
        ticket_id: int
    ):
        ticket = self.ticket_service.update_ticket_status(
            ticket_id,
            "closed"
        )

        if not ticket:
            return f"Ticket #{ticket_id} was not found."

        return f"Ticket #{ticket.id} marked as closed."

    # =====================================================
    # Formatting
    # =====================================================

    def format_ticket_list(
        self,
        tickets
    ):
        if not tickets:
            return "No tickets found."

        return "\n".join(
            [
                f"Ticket #{ticket.id} - {ticket.status}"
                for ticket in tickets
            ]
        )