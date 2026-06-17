history = [
    {
        "role": "user",
        "content": "What payment methods are accepted?"
    },
    {
        "role": "assistant",
        "content": "We accept credit cards, debit cards, and PayPal."
    }
]

question = "Can I use it internationally?"

import os
import sys

# Add backend to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.llm_service import LLMService
from app.services.question_rewriter import QuestionRewriter

llm_service = LLMService()
question_rewriter = QuestionRewriter(llm_service)

rewritten_question = question_rewriter.rewrite_query(question, history)
print(rewritten_question)