from typing import TypedDict


class AgentState(TypedDict):
    question: str
    history: list
    route: str
    answer: str
    session_id: str