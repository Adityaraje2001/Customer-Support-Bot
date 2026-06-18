"""
Purpose:
Test the `SupportAgent` logic which handles general support inquiries using RAG.

Mocks required:
- `app.rag.rag_service.RAGService`: To prevent actual embedding generation, DB queries, and LLM calls.

Execution:
Run `pytest backend/tests/test_support_agent.py -v`
"""

import pytest
from unittest.mock import MagicMock
from app.agents.support_agent import SupportAgent


@pytest.fixture
def mock_rag_service():
    return MagicMock()


@pytest.fixture
def support_agent(mock_rag_service):
    return SupportAgent(rag_service=mock_rag_service)


def test_run(support_agent, mock_rag_service):
    # Arrange
    mock_rag_service.answer_question.return_value = ("This is a support answer.", {"eval_score": 0.9})

    # Act
    answer, metrics = support_agent.run(question="How do I use the app?", history=[])

    # Assert
    assert answer == "This is a support answer."
    assert metrics == {"eval_score": 0.9}
    mock_rag_service.answer_question.assert_called_once_with(
        question="How do I use the app?",
        history=[]
    )
