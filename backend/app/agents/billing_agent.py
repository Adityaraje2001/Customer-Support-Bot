from app.rag.rag_service import RAGService


class BillingAgent:

    def __init__(
        self,
        rag_service: RAGService
    ):
        self.rag_service = rag_service

    def run(
        self,
        question: str,
        history=None
    ):
        return self.rag_service.answer_question(
            question=question,
            history=history
        )