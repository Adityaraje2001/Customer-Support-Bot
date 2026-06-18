from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):
    question: str
    history: list
    route: str
    answer: str
    session_id: str
    user_id: int
    retrieved_doc_count: int
    retrieval_latency: float
    llm_latency: float
    ticket_created: bool
    retrieved_context: str