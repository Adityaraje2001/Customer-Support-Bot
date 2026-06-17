"""Chat API routes with SQLite-backed conversation memory."""

import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest, ChatResponse
from app.memory.memory_manager import MemoryManager
from app.services.llm_service import LLMService
from app.services.question_rewriter import QuestionRewriter
from app.workflows.support_workflow import graph


router = APIRouter()

# =====================================================
# Shared Services
# =====================================================

llm_service = LLMService()

question_rewriter = QuestionRewriter(
    llm_service=llm_service
)

memory = MemoryManager()


# =====================================================
# Chat Endpoint
# =====================================================

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Create or reuse session
        session_id = request.session_id or str(uuid.uuid4())

        # Load conversation history
        history = memory.get_history(session_id)

        # Rewrite follow-up questions into standalone queries
        rewritten_question = question_rewriter.rewrite_query(
            request.message,
            history
        )

        # Run LangGraph workflow
        result = graph.invoke(
            {
                "question": rewritten_question,
                "history": history,
                "session_id": session_id
            }
        )

        response_text = result["answer"]

        # Save original user message
        memory.add_message(
            session_id=session_id,
            role="user",
            content=request.message
        )

        # Save assistant response
        memory.add_message(
            session_id=session_id,
            role="assistant",
            content=response_text
        )

        return ChatResponse(
            response=response_text,
            session_id=session_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================================
# Streaming Endpoint (Legacy)
# =====================================================

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Legacy streaming endpoint.

    Frontend currently uses /chat.
    This endpoint is retained for future LangGraph streaming support.
    """

    session_id = request.session_id or str(uuid.uuid4())

    history = memory.get_history(session_id)

    memory.add_message(
        session_id=session_id,
        role="user",
        content=request.message
    )

    async def _generate():

        collected_tokens = []

        async for chunk in llm_service.stream_response(
            request.message,
            history=history
        ):

            if (
                chunk.startswith("data: ")
                and chunk.strip() != "data: [DONE]"
                and not chunk.strip().startswith("data: [ERROR]")
            ):
                collected_tokens.append(
                    chunk[6:].rstrip("\n")
                )

            yield chunk

        full_response = "".join(collected_tokens)

        if full_response:
            memory.add_message(
                session_id=session_id,
                role="assistant",
                content=full_response
            )

    return StreamingResponse(
        _generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )