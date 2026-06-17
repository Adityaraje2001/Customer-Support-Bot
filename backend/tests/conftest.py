"""
Purpose:
Shared fixtures for the test suite, such as the FastAPI TestClient, and global mocks
to prevent external model downloads and API calls during import.

Key problem solved:
  support_workflow.py instantiates LLMService(), EmbeddingService(), ChromaStore()
  at MODULE LEVEL. This means they execute the moment `app.main` is imported,
  before pytest-mock's `mocker.patch` can intercept them.

  Solution: mock the entire classes in sys.modules BEFORE importing app.main,
  so the module-level calls get a MagicMock, not the real objects.
"""

import sys
from unittest.mock import MagicMock, patch

# ── 1. Block heavy/external imports before anything else ─────────────────────
# Prevents sentence-transformers from trying to download models
sys.modules['sentence_transformers'] = MagicMock()

# ── 2. Patch module-level service instantiation BEFORE importing app ──────────
# support_workflow.py calls LLMService(), EmbeddingService(), ChromaStore()
# at the top level. We intercept those constructors here.
_llm_patcher = patch('app.services.llm_service.LLMService', new_callable=MagicMock)
_embed_patcher = patch('app.rag.embeddings.EmbeddingService', new_callable=MagicMock)
_chroma_patcher = patch('app.rag.vectorstores.chroma_store.ChromaStore', new_callable=MagicMock)

_llm_patcher.start()
_embed_patcher.start()
_chroma_patcher.start()

# ── 3. Now it's safe to import app ───────────────────────────────────────────
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth.dependencies import get_current_user
from app.models.user import User

def override_get_current_user():
    return User(id=1, email="test@test.com", username="testuser", role="customer")

app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.fixture(autouse=True)
def mock_core_services(mocker):
    """Automatically mock core service *methods* to prevent real calls in every test."""
    mocker.patch('app.services.llm_service.LLMService.get_response', return_value='Mocked LLM Response')
    mocker.patch('app.rag.embeddings.EmbeddingService.embed_text', return_value=[0.1] * 384)
    mocker.patch('app.rag.retriever.Retriever.retrieve', return_value=[])


@pytest.fixture
def client():
    """Returns a FastAPI TestClient instance."""
    with TestClient(app) as test_client:
        yield test_client
