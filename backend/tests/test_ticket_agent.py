"""
Purpose:
Test the `TicketAgent` logic, including intent detection and calls to `TicketService`.

Mocks required:
- `app.services.ticket_service.TicketService`: To prevent database interactions when the agent runs its logic.

Execution:
Run `pytest backend/tests/test_ticket_agent.py -v`
"""

import pytest
from unittest.mock import MagicMock
from app.agents.ticket_agent import TicketAgent
from app.models.ticket import Ticket


@pytest.fixture
def mock_ticket_service(mocker):
    mock_service = mocker.patch("app.agents.ticket_agent.TicketService")
    return mock_service.return_value


@pytest.fixture
def ticket_agent(mock_ticket_service):
    # The agent instantiates TicketService internally, which is patched
    return TicketAgent()


def test_create_ticket(ticket_agent, mock_ticket_service):
    # Arrange
    mock_ticket = MagicMock(spec=Ticket)
    mock_ticket.id = 1
    mock_ticket.status = "open"
    mock_ticket.created_at = "2026-01-01"
    mock_ticket_service.create_ticket.return_value = mock_ticket

    # Act
    response = ticket_agent.run("I need help with my account", "session-123")

    # Assert
    assert "ticket #1" in response.lower()
    assert "created successfully" in response
    mock_ticket_service.create_ticket.assert_called_once_with(
        session_id="session-123",
        question="I need help with my account"
    )


def test_get_my_tickets(ticket_agent, mock_ticket_service):
    # Arrange
    mock_ticket = MagicMock(spec=Ticket)
    mock_ticket.id = 1
    mock_ticket.status = "open"
    mock_ticket_service.get_tickets_by_session.return_value = [mock_ticket]

    # Act
    response = ticket_agent.run("show my tickets", "session-123")

    # Assert
    assert "Ticket #1 - open" in response
    mock_ticket_service.get_tickets_by_session.assert_called_once_with("session-123")


def test_get_open_tickets(ticket_agent, mock_ticket_service):
    # Arrange
    mock_ticket_service.list_open_tickets.return_value = []

    # Act
    response = ticket_agent.run("show open tickets", "session-123")

    # Assert
    assert "No tickets found" in response
    mock_ticket_service.list_open_tickets.assert_called_once()


def test_get_resolved_tickets(ticket_agent, mock_ticket_service):
    # Arrange
    mock_ticket_service.list_resolved_tickets.return_value = []

    # Act
    response = ticket_agent.run("list resolved tickets", "session-123")

    # Assert
    assert "No tickets found" in response
    mock_ticket_service.list_resolved_tickets.assert_called_once()


def test_start_ticket_progress(ticket_agent, mock_ticket_service):
    # Arrange
    mock_ticket = MagicMock(spec=Ticket)
    mock_ticket.id = 1
    mock_ticket_service.update_ticket_status.return_value = mock_ticket

    # Act
    response = ticket_agent.run("start ticket 1", "session-123")

    # Assert
    assert "Ticket #1 marked as in progress" in response
    mock_ticket_service.update_ticket_status.assert_called_once_with(1, "in_progress")


def test_resolve_ticket(ticket_agent, mock_ticket_service):
    # Arrange
    mock_ticket = MagicMock(spec=Ticket)
    mock_ticket.id = 2
    mock_ticket_service.update_ticket_status.return_value = mock_ticket

    # Act
    response = ticket_agent.run("resolve ticket #2", "session-123")

    # Assert
    assert "Ticket #2 marked as resolved" in response
    mock_ticket_service.update_ticket_status.assert_called_once_with(2, "resolved")


def test_get_ticket_status(ticket_agent, mock_ticket_service):
    # Arrange
    mock_ticket = MagicMock(spec=Ticket)
    mock_ticket.id = 5
    mock_ticket.status = "open"
    mock_ticket.created_at = "2026-01-01"
    mock_ticket_service.get_ticket.return_value = mock_ticket

    # Act
    response = ticket_agent.run("status of ticket 5", "session-123")

    # Assert
    assert "Ticket #5" in response
    assert "Status: open" in response
    mock_ticket_service.get_ticket.assert_called_once_with(5)
