from typing import TypedDict, Annotated, Sequence
import operator

# Define the state graph schema for LangGraph
# TODO: Add required state attributes like user_id, history, current_agent

class AgentState(TypedDict):
    messages: Annotated[Sequence[str], operator.add]
    next_node: str
