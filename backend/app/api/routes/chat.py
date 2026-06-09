'''Chat API routes with SQLite-backed conversation memory.'''


from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.services.llm_service import LLMService
from app.schemas.chat import ChatRequest, ChatResponse
from app.memory.memory_manager import MemoryManager
import uuid

router = APIRouter()
llm_service = LLMService()
memory = MemoryManager()


# ──────────────────────────────────────────────
# Non-streaming endpoint — returns full response as JSON
# ──────────────────────────────────────────────
@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Use existing session_id or generate a new one
        session_id = request.session_id or str(uuid.uuid4())

        # Load past conversation from SQLite
        history = memory.get_history(session_id)

        # Get LLM response with full conversation context
        response_text = llm_service.get_response(request.message, history=history)

        # Persist both the user's message and the assistant's reply
        memory.add_message(session_id=session_id, role="user", content=request.message)
        memory.add_message(session_id=session_id, role="assistant", content=response_text)

        return ChatResponse(
            response=response_text,
            session_id=session_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# Streaming endpoint — returns tokens as SSE stream
# ──────────────────────────────────────────────
@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Stream the LLM response token-by-token using Server-Sent Events (SSE).

    The response is a text/event-stream where each event is:
      data: <token>

    The stream ends with:
      data: [DONE]
    """
    session_id = request.session_id or str(uuid.uuid4())
    history = memory.get_history(session_id)

    # Save the user message before streaming starts
    memory.add_message(session_id=session_id, role="user", content=request.message)

    async def _generate():
        """Wraps the LLM stream to collect the full response and save it afterwards."""
        collected_tokens: list[str] = []

        async for chunk in llm_service.stream_response(request.message, history=history):
            # Extract raw token text from the SSE envelope ("data: <token>\n\n")
            if chunk.startswith("data: ") and chunk.strip() not in (
                "data: [DONE]",
            ) and not chunk.strip().startswith("data: [ERROR]"):
                collected_tokens.append(chunk[6:].rstrip("\n"))
            yield chunk

        # Once streaming is done, persist the full assistant response
        full_response = "".join(collected_tokens)
        if full_response:
            memory.add_message(
                session_id=session_id, role="assistant", content=full_response
            )

    return StreamingResponse(
        _generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )