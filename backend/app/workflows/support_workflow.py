from langgraph.graph import StateGraph, END

from app.agents.state import AgentState
from app.agents.router_agent import RouterAgent
from app.agents.support_agent import SupportAgent
from app.agents.billing_agent import BillingAgent
from app.agents.escalation_agent import EscalationAgent
from app.agents.ticket_agent import TicketAgent

from app.services.llm_service import LLMService
from app.rag.embeddings import EmbeddingService
from app.rag.vectorstores.chroma_store import ChromaStore
from app.rag.retriever import Retriever
from app.rag.rag_service import RAGService


# =====================================================
# Shared Services
# =====================================================

llm_service = LLMService()

embedding_service = EmbeddingService()

vectorstore = ChromaStore()

retriever = Retriever(
    vectorstore=vectorstore,
    embedding_service=embedding_service
)

rag_service = RAGService(
    retriever=retriever,
    llm_service=llm_service
)


# =====================================================
# Agents
# =====================================================

router_agent = RouterAgent(llm_service)

support_agent = SupportAgent(rag_service)

billing_agent = BillingAgent(rag_service)

escalation_agent = EscalationAgent(llm_service)

ticket_agent = TicketAgent()


# =====================================================
# Nodes
# =====================================================

def router_node(state: AgentState):
    route = router_agent.route(
        state["question"]
    )

    print(f"Route Selected: {route}")

    return {
        "route": route
    }


def support_node(state: AgentState):
    answer = support_agent.run(
        question=state["question"],
        history=state.get("history", [])
    )

    return {
        "answer": answer
    }


def billing_node(state: AgentState):
    answer = billing_agent.run(
        question=state["question"],
        history=state.get("history", [])
    )

    return {
        "answer": answer
    }


def escalation_node(state: AgentState):
    answer = escalation_agent.run(
        question=state["question"],
        history=state.get("history", [])
    )

    return {
        "answer": answer
    }


def ticket_node(state):

    answer = ticket_agent.run(
        question=state["question"],
        session_id=state["session_id"],
        user_id=state.get("user_id")
    )

    return {
        "answer": answer
    }


# =====================================================
# Routing Logic
# =====================================================

def route_decision(state: AgentState):
    route = state["route"]

    valid_routes = {
        "support",
        "billing",
        "escalation",
        "ticket"
    }

    if route not in valid_routes:
        return "support"

    return route


# =====================================================
# Build Graph
# =====================================================

workflow = StateGraph(AgentState)

workflow.add_node(
    "router",
    router_node
)

workflow.add_node(
    "support",
    support_node
)

workflow.add_node(
    "billing",
    billing_node
)

workflow.add_node(
    "escalation",
    escalation_node
)

workflow.add_node(
    "ticket",
    ticket_node
)

workflow.set_entry_point("router")

workflow.add_conditional_edges(
    "router",
    route_decision,
    {
        "support": "support",
        "billing": "billing",
        "escalation": "escalation",
        "ticket": "ticket",
    }
)

workflow.add_edge(
    "support",
    END
)

workflow.add_edge(
    "billing",
    END
)

workflow.add_edge(
    "escalation",
    END
)

workflow.add_edge(
    "ticket",
    END
)

graph = workflow.compile()