from pydantic import BaseModel

# FastAPI request/response validation schemas for chat
# TODO: Add specific fields for memory context, agent state.

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    response: str
    session_id: str | None = None
    agent_used: str | None = None
