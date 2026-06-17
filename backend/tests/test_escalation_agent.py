"""
Purpose:
Test the `EscalationAgent` logic which handles escalating to human support.

Mocks required:
- `app.services.llm_service.LLMService`: Passed to agent but currently unused for static response.

Execution:
Run `pytest backend/tests/test_escalation_agent.py -v`
"""

import pytest
from unittest.mock import MagicMock
from app.agents.escalation_agent import EscalationAgent


@pytest.fixture
def mock_llm_service():
    return MagicMock()


@pytest.fixture
def escalation_agent(mock_llm_service):
    return EscalationAgent(llm_service=mock_llm_service)


def test_run(escalation_agent):
    # Act
    response = escalation_agent.run(question="I want to speak to a manager", history=[])

    # Assert
    assert "escalated" in response
    assert "human support" in response
