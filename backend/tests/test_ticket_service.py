"""
Purpose:
Test the `TicketService` which handles database operations for tickets.

Mocks required:
- `app.services.ticket_service.SessionLocal`: To prevent actual database connections and operations.
- `app.models.ticket.Ticket`: For mocking returned database records.

Execution:
Run `pytest backend/tests/test_ticket_service.py -v`
"""

import pytest
from unittest.mock import MagicMock
from app.services.ticket_service import TicketService
from app.models.ticket import Ticket


@pytest.fixture
def mock_session(mocker):
    """Mocks the SQLAlchemy SessionLocal to return a MagicMock session."""
    mock_session_cls = mocker.patch("app.services.ticket_service.SessionLocal")
    mock_db = MagicMock()
    mock_session_cls.return_value = mock_db
    return mock_db


@pytest.fixture
def ticket_service():
    return TicketService()


def test_create_ticket(ticket_service, mock_session):
    # Act
    ticket = ticket_service.create_ticket(
        session_id="session-123",
        question="How do I reset my password?"
    )

    # Assert
    assert ticket.session_id == "session-123"
    assert ticket.question == "How do I reset my password?"
    assert ticket.status == "open"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    mock_session.close.assert_called_once()


def test_get_ticket(ticket_service, mock_session):
    # Arrange
    mock_ticket = MagicMock(spec=Ticket)
    mock_ticket.id = 1
    
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = mock_ticket

    # Act
    result = ticket_service.get_ticket(ticket_id=1)

    # Assert
    assert result == mock_ticket
    mock_session.query.assert_called_once_with(Ticket)
    mock_session.close.assert_called_once()


def test_update_ticket_status_exists(ticket_service, mock_session):
    # Arrange
    mock_ticket = MagicMock(spec=Ticket)
    mock_ticket.status = "open"
    
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = mock_ticket

    # Act
    result = ticket_service.update_ticket_status(ticket_id=1, status="resolved")

    # Assert
    assert result.status == "resolved"
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    mock_session.close.assert_called_once()


def test_update_ticket_status_not_exists(ticket_service, mock_session):
    # Arrange
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    # Act
    result = ticket_service.update_ticket_status(ticket_id=999, status="resolved")

    # Assert
    assert result is None
    mock_session.commit.assert_not_called()
    mock_session.close.assert_called_once()


def test_get_tickets_by_session(ticket_service, mock_session):
    # Arrange
    mock_ticket_1 = MagicMock(spec=Ticket)
    mock_ticket_2 = MagicMock(spec=Ticket)
    
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_order = mock_filter.order_by.return_value
    mock_order.all.return_value = [mock_ticket_1, mock_ticket_2]

    # Act
    results = ticket_service.get_tickets_by_session(session_id="session-123")

    # Assert
    assert len(results) == 2
    assert results == [mock_ticket_1, mock_ticket_2]
    mock_session.query.assert_called_once_with(Ticket)
    mock_session.close.assert_called_once()


def test_list_open_tickets(ticket_service, mock_session):
    # Arrange
    mock_ticket = MagicMock(spec=Ticket)
    mock_ticket.status = "open"
    
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_order = mock_filter.order_by.return_value
    mock_order.all.return_value = [mock_ticket]

    # Act
    results = ticket_service.list_open_tickets()

    # Assert
    assert len(results) == 1
    assert results[0] == mock_ticket
    mock_session.close.assert_called_once()


def test_list_resolved_tickets(ticket_service, mock_session):
    # Arrange
    mock_ticket = MagicMock(spec=Ticket)
    mock_ticket.status = "resolved"
    
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_order = mock_filter.order_by.return_value
    mock_order.all.return_value = [mock_ticket]

    # Act
    results = ticket_service.list_resolved_tickets()

    # Assert
    assert len(results) == 1
    assert results[0] == mock_ticket
    mock_session.close.assert_called_once()
