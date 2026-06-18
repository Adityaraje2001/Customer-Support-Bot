import pytest
from unittest.mock import MagicMock
from app.evaluation.evaluator import ResponseEvaluator

def test_evaluator_valid_json():
    mock_llm = MagicMock()
    mock_llm.get_response.return_value = '```json\n{"answer_relevance": 5, "context_relevance": 4, "groundedness": 5, "hallucination_risk": 5, "route_accuracy": 5}\n```'
    
    evaluator = ResponseEvaluator(mock_llm)
    scores = evaluator.evaluate(
        question="How do I reset my password?",
        answer="Click the reset button.",
        retrieved_context="To reset your password, click the reset button on the login page.",
        route_selected="support"
    )
    
    assert scores == {
        "answer_relevance": 5,
        "context_relevance": 4,
        "groundedness": 5,
        "hallucination_risk": 5,
        "route_accuracy": 5
    }

def test_evaluator_fallback_on_invalid_json():
    mock_llm = MagicMock()
    mock_llm.get_response.return_value = 'This is not json.'
    
    evaluator = ResponseEvaluator(mock_llm)
    scores = evaluator.evaluate(
        question="Q",
        answer="A",
        retrieved_context="C",
        route_selected="R"
    )
    
    assert scores == {
        "answer_relevance": 3,
        "context_relevance": 3,
        "groundedness": 3,
        "hallucination_risk": 3,
        "route_accuracy": 3
    }

def test_evaluator_clamps_values():
    mock_llm = MagicMock()
    mock_llm.get_response.return_value = '{"answer_relevance": 10, "context_relevance": 0, "groundedness": 3, "hallucination_risk": 3, "route_accuracy": 3}'
    
    evaluator = ResponseEvaluator(mock_llm)
    scores = evaluator.evaluate(
        question="Q",
        answer="A",
        retrieved_context="C",
        route_selected="R"
    )
    
    assert scores["answer_relevance"] == 5
    assert scores["context_relevance"] == 1
