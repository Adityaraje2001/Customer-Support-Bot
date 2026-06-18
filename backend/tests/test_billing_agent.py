"""
Purpose:
Test the `BillingAgent` logic which handles billing inquiries using RAG.

Mocks required:
- `app.rag.rag_service.RAGService`: To prevent actual embedding generation, DB queries, and LLM calls.

Execution:
Run `pytest backend/tests/test_billing_agent.py -v`
"""

import pytest
from unittest.mock import MagicMock
from app.agents.billing_agent import BillingAgent


@pytest.fixture
def mock_rag_service():
    return MagicMock()


@pytest.fixture
def billing_agent(mock_rag_service):
    return BillingAgent(rag_service=mock_rag_service)


def test_run(billing_agent, mock_rag_service):
    # Arrange
    mock_rag_service.answer_question.return_value = ("This is a billing answer.", {"eval_score": 0.9})

    # Act
    answer, metrics = billing_agent.run(question="Where is my invoice?", history=[])

    # Assert
    assert answer == "This is a billing answer."
    assert metrics == {"eval_score": 0.9}
    mock_rag_service.answer_question.assert_called_once_with(
        question="Where is my invoice?",
        history=[]
    )
