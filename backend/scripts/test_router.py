import os
import sys

# Add backend to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.llm_service import LLMService
from app.agents.router_agent import RouterAgent


llm_service = LLMService()
router = RouterAgent(llm_service)
test_questions = [
    "What is the status of ticket #1?"
]
for question in test_questions:
    route = router.route(question)
    print(f"{question} -> {route}")