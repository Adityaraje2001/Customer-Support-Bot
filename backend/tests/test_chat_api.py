"""
Purpose:
Test the `/chat` endpoint.

Mocks required:
- `app.api.routes.chat.memory`: Mock `MemoryManager` methods to prevent DB calls.
- `app.api.routes.chat.question_rewriter`: Mock `rewrite_query` to avoid LLM rewriting.
- `app.api.routes.chat.graph`: Mock `invoke` to avoid running the full LangGraph workflow.

Execution:
Run `pytest backend/tests/test_chat_api.py -v`
"""

import pytest
from app.schemas.chat import ChatRequest


def test_chat_success(client, mocker):
    # Arrange
    mock_memory = mocker.patch("app.api.routes.chat.memory")
    mock_memory.get_history.return_value = []
    
    mock_rewriter = mocker.patch("app.api.routes.chat.question_rewriter")
    mock_rewriter.rewrite_query.return_value = "Rewritten question"
    
    mock_graph = mocker.patch("app.api.routes.chat.graph")
    mock_graph.invoke.return_value = {"answer": "Mocked workflow answer", "route": "support"}

    # Act
    response = client.post("/api/chat", json={
        "message": "Original question",
        "session_id": "session-123"
    })

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "Mocked workflow answer"
    assert data["session_id"] == "session-123"
    
    mock_memory.get_history.assert_called_once_with("session-123")
    mock_rewriter.rewrite_query.assert_called_once_with("Original question", [])
    mock_graph.invoke.assert_called_once_with({
        "question": "Rewritten question",
        "history": [],
        "session_id": "session-123",
        "user_id": 1
    })
    assert mock_memory.add_message.call_count == 2


def test_chat_error(client, mocker):
    # Arrange
    mock_memory = mocker.patch("app.api.routes.chat.memory")
    mock_memory.get_history.side_effect = Exception("Database error")

    # Act
    response = client.post("/api/chat", json={
        "message": "Original question",
        "session_id": "session-123"
    })

    # Assert
    assert response.status_code == 500
    assert "Database error" in response.json()["detail"]
