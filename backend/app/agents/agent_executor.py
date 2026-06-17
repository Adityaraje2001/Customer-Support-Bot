'''route = router.route(question)

if route == "support":
    return support_agent.run(...)

elif route == "billing":
    return billing_agent.run(...)

elif route == "escalation":
    return escalation_agent.run(...)

elif route == "ticket":
    return ticket_agent.run(...)'''

from app.api.routes.chat import question_rewriter
from app.agents.router_agent import RouterAgent
from app.agents.billing_agent import BillingAgent
from app.agents.escalation_agent import EscalationAgent
from app.agents.ticket_agent import TicketAgent
from app.services.llm_service import LLMService
from app.agents.support_agent import SupportAgent
from app.rag.rag_service import RAGService
from app.rag.retriever import Retriever
from app.rag.vectorstores.chroma_store import ChromaStore
from app.rag.embeddings import EmbeddingService


class AgentExecutor:
    def __init__(self):
        pass
    def run(self, question: str, history=None):
        llm_service = LLMService()
        retriever = Retriever(vectorstore=ChromaStore(),embedding_service=EmbeddingService())
        rag_service = RAGService(retriever,llm_service)

        support_agent = SupportAgent(rag_service)
        billing_agent = BillingAgent(rag_service)
        escalation_agent = EscalationAgent(llm_service)
        ticket_agent = TicketAgent()
        
        router = RouterAgent(llm_service)
        
        route = router.route(question)
        print("****"+route+"****")
        if route == "support":
            return support_agent.run(question,history)
        elif route == "billing":
            return billing_agent.run(question,history)
        elif route == "escalation":
            return escalation_agent.run(question,history)
        elif route == "ticket":
            return ticket_agent.run(question,history)
        else:
            return "Invalid route"

agent_executor = AgentExecutor()
print(agent_executor.run("I want a refund"))
