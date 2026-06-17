"""
Purpose:
Test the LangGraph workflow routing and execution.

Mocks required:
- The global agent instances in `app.workflows.support_workflow` (e.g. `router_agent`, `support_agent`) 
to isolate the graph structure and routing logic from actual LLM or DB calls.

Execution:
Run `pytest backend/tests/test_workflow.py -v`
"""

import pytest
from app.workflows.support_workflow import graph, route_decision


def test_route_decision():
    # Test valid routes
    assert route_decision({"route": "support", "question": "", "session_id": ""}) == "support"
    assert route_decision({"route": "billing", "question": "", "session_id": ""}) == "billing"
    assert route_decision({"route": "escalation", "question": "", "session_id": ""}) == "escalation"
    assert route_decision({"route": "ticket", "question": "", "session_id": ""}) == "ticket"

    # Test invalid route fallbacks to support
    assert route_decision({"route": "unknown", "question": "", "session_id": ""}) == "support"
    assert route_decision({"route": "", "question": "", "session_id": ""}) == "support"


def test_graph_invoke_support(mocker):
    # Arrange
    mocker.patch("app.workflows.support_workflow.router_agent.route", return_value="support")
    mocker.patch("app.workflows.support_workflow.support_agent.run", return_value="Support response")

    # Act
    result = graph.invoke({
        "question": "How to use?",
        "history": [],
        "session_id": "123"
    })

    # Assert
    assert result["route"] == "support"
    assert result["answer"] == "Support response"


def test_graph_invoke_billing(mocker):
    # Arrange
    mocker.patch("app.workflows.support_workflow.router_agent.route", return_value="billing")
    mocker.patch("app.workflows.support_workflow.billing_agent.run", return_value="Billing response")

    # Act
    result = graph.invoke({
        "question": "My bill?",
        "history": [],
        "session_id": "123"
    })

    # Assert
    assert result["route"] == "billing"
    assert result["answer"] == "Billing response"


def test_graph_invoke_ticket(mocker):
    # Arrange
    mocker.patch("app.workflows.support_workflow.router_agent.route", return_value="ticket")
    mocker.patch("app.workflows.support_workflow.ticket_agent.run", return_value="Ticket response")

    # Act
    result = graph.invoke({
        "question": "Open a ticket",
        "history": [],
        "session_id": "123"
    })

    # Assert
    assert result["route"] == "ticket"
    assert result["answer"] == "Ticket response"


def test_graph_invoke_escalation(mocker):
    # Arrange
    mocker.patch("app.workflows.support_workflow.router_agent.route", return_value="escalation")
    mocker.patch("app.workflows.support_workflow.escalation_agent.run", return_value="Escalation response")

    # Act
    result = graph.invoke({
        "question": "Manager",
        "history": [],
        "session_id": "123"
    })

    # Assert
    assert result["route"] == "escalation"
    assert result["answer"] == "Escalation response"
