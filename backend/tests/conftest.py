"""
Purpose:
Shared fixtures for the test suite, such as the FastAPI TestClient, and global mocks to prevent external model downloads and API calls.
"""

import sys
from unittest.mock import MagicMock

# Prevent actual model downloads during module imports by mocking sentence_transformers
sys.modules['sentence_transformers'] = MagicMock()

import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(autouse=True)
def mock_core_services(mocker):
    """Automatically mock core services to prevent external calls in all tests."""
    mocker.patch("app.rag.embeddings.EmbeddingService.embed_text", return_value=[0.1] * 384)
    mocker.patch("app.services.llm_service.LLMService.get_response", return_value="Mocked LLM Response")
    mocker.patch("app.rag.retriever.Retriever.retrieve", return_value=[])

@pytest.fixture
def client():
    """Returns a FastAPI TestClient instance."""
    with TestClient(app) as test_client:
        yield test_client
