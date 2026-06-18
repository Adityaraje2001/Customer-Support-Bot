import time
from app.rag.retriever import Retriever
from app.services.llm_service import LLMService

class RAGService:
    def __init__(
        self,
        retriever: Retriever,
        llm_service: LLMService
    ):
        self.retriever = retriever
        self.llm_service = llm_service

    def answer_question(self,question:str,history:list|None = None):
        conversation_context=""
        if history:
            conversation_context = "\n".join(
                [
                    f"{message['role']}: {message['content']}"
                    for message in history[-5:]
                ]
            )
        retrieval_query = f"""
            Conversation:
            {conversation_context}

            Current Question:
            {question}
            """
        
        start_time = time.perf_counter()
        retrieved_documents=self.retriever.retrieve(retrieval_query)
        retrieval_latency = time.perf_counter() - start_time
        retrieved_doc_count = len(retrieved_documents)
        
        context = "\n\n".join(doc["text"] for doc in retrieved_documents)
        
        prompt = f"""
            You are a customer support assistant.

            Conversation History:
            {conversation_context}

            Retrieved Context:
            {context}

            Current Question:
            {question}

            Instructions:
            - Answer only using the retrieved context.
            - Use conversation history to understand references.
            - If the answer is not found in the context, say:
            "I cannot answer that based on the available information."

            Answer:
            """ 
        
        start_time = time.perf_counter()
        answer = self.llm_service.get_response(prompt)
        llm_latency = time.perf_counter() - start_time
        
        metrics = {
            "retrieved_doc_count": retrieved_doc_count,
            "retrieval_latency": retrieval_latency,
            "llm_latency": llm_latency,
            "retrieved_context": context
        }
        
        return answer, metrics