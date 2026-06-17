"""
Purpose:
Test the `MemoryManager` which handles message persistence and retrieval.

Mocks required:
- `app.memory.memory_manager.SessionLocal`: To prevent actual database connections.

Execution:
Run `pytest backend/tests/test_memory_manager.py -v`
"""

import pytest
from unittest.mock import MagicMock
from app.memory.memory_manager import MemoryManager
from app.models.chat_message import ChatMessage


@pytest.fixture
def mock_session(mocker):
    mock_session_cls = mocker.patch("app.memory.memory_manager.SessionLocal")
    mock_db = MagicMock()
    mock_session_cls.return_value = mock_db
    return mock_db


@pytest.fixture
def memory_manager():
    return MemoryManager()


def test_add_message(memory_manager, mock_session):
    # Act
    memory_manager.add_message(session_id="session-123", role="user", content="Hello")

    # Assert
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()
    
    # Verify the object added
    added_obj = mock_session.add.call_args[0][0]
    assert isinstance(added_obj, ChatMessage)
    assert added_obj.session_id == "session-123"
    assert added_obj.role == "user"
    assert added_obj.content == "Hello"


def test_get_history(memory_manager, mock_session):
    # Arrange
    mock_msg_1 = MagicMock(spec=ChatMessage)
    mock_msg_1.to_llm_dict.return_value = {"role": "user", "content": "Hi"}
    
    mock_msg_2 = MagicMock(spec=ChatMessage)
    mock_msg_2.to_llm_dict.return_value = {"role": "assistant", "content": "Hello"}
    
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_order = mock_filter.order_by.return_value
    mock_limit = mock_order.limit.return_value
    mock_limit.all.return_value = [mock_msg_1, mock_msg_2]

    # Act
    history = memory_manager.get_history("session-123", limit=10)

    # Assert
    assert len(history) == 2
    assert history[0] == {"role": "user", "content": "Hi"}
    assert history[1] == {"role": "assistant", "content": "Hello"}
    mock_session.query.assert_called_once_with(ChatMessage)
    mock_limit.all.assert_called_once()
    mock_session.close.assert_called_once()


def test_clear_session(memory_manager, mock_session):
    # Arrange
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter.return_value

    # Act
    memory_manager.clear_session("session-123")

    # Assert
    mock_session.query.assert_called_once_with(ChatMessage)
    mock_filter.delete.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()
