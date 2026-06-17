"""Chat API routes with SQLite-backed conversation memory."""

import uuid

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest, ChatResponse
from app.memory.memory_manager import MemoryManager
from app.services.llm_service import LLMService
from app.services.question_rewriter import QuestionRewriter
from app.workflows.support_workflow import graph
from app.auth.dependencies import get_current_user
from app.auth.rbac import require_customer
from app.models.user import User


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
async def chat(
    request: ChatRequest,
    current_user: User = Depends(require_customer)
):
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
                "session_id": session_id,
                "user_id": current_user.id
            }
        )

        response_text = result["answer"]

        # Save original user message
        memory.add_message(
            session_id=session_id,
            role="user",
            content=request.message,
            user_id=current_user.id
        )

        # Save assistant response
        memory.add_message(
            session_id=session_id,
            role="assistant",
            content=response_text,
            user_id=current_user.id
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
async def chat_stream(
    request: ChatRequest,
    current_user: User = Depends(require_customer)
):
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
        content=request.message,
        user_id=current_user.id
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
                content=full_response,
                user_id=current_user.id
            )

    return StreamingResponse(
        _generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )