"""
Purpose:
Test the `RouterAgent` logic which classifies the user question into different intents/routes.

Mocks required:
- `app.services.llm_service.LLMService`: Mock the LLM to return predefined routes ("support", "billing", "escalation", "ticket").

Execution:
Run `pytest backend/tests/test_router_agent.py -v`
"""

import pytest
from unittest.mock import MagicMock
from app.agents.router_agent import RouterAgent


@pytest.fixture
def mock_llm_service():
    return MagicMock()


@pytest.fixture
def router_agent(mock_llm_service):
    return RouterAgent(llm_service=mock_llm_service)


@pytest.mark.parametrize(
    "llm_response, expected_route",
    [
        ("support", "support"),
        ("billing", "billing"),
        ("escalation", "escalation"),
        ("ticket", "ticket"),
        ("Support", "support"),
        ("  Billing  ", "billing")
    ]
)
def test_route(router_agent, mock_llm_service, llm_response, expected_route):
    # Arrange
    mock_llm_service.get_response.return_value = llm_response

    # Act
    route = router_agent.route("dummy question")

    # Assert
    assert route == expected_route
    mock_llm_service.get_response.assert_called_once()
