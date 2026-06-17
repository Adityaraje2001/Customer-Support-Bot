from app.services.llm_service import LLMService


class QuestionRewriter:

    def __init__(
        self,
        llm_service: LLMService
    ):
        self.llm_service = llm_service

    def rewrite_query(self,question:str,history:list|None = None):
        if not history:
            return question
        conversation_context=""
        if history:
            conversation_context = "\n".join(
                [
                    f"{message['role']}: {message['content']}"
                    for message in history[-5:]
                ]
            )
        history_text = conversation_context or "No previous conversation."
        prompt = f"""
            You are a query rewriting assistant.
            Your task is to rewrite the user's latest question
            into a standalone question.
            Use the conversation history to resolve references.

            Conversation History:
            {history_text}

            Latest Question:
            {question}

            Rules:
            - Preserve meaning.
            - Do not answer.
            - Only return the rewritten question.
            - If the question is already standalone,
            return it unchanged.


            Rewritten Question:
            """ 
        rewritten_question = self.llm_service.get_response(prompt)
        return rewritten_question.strip()