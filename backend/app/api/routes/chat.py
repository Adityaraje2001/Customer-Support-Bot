"""Chat API routes with SQLite-backed conversation memory."""

import uuid
import time

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
from app.monitoring.mlflow_tracker import mlflow_tracker
from app.evaluation.evaluator import ResponseEvaluator


router = APIRouter()

# =====================================================
# Shared Services
# =====================================================

llm_service = LLMService()

question_rewriter = QuestionRewriter(
    llm_service=llm_service
)

evaluator = ResponseEvaluator(llm_service)

memory = MemoryManager()


# =====================================================
# Chat Endpoint
# =====================================================

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(require_customer)
):
    start_time = time.perf_counter()
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
        retrieved_context = result.get("retrieved_context", "")
        route_selected = result.get("route", "unknown")

        # Evaluate response
        eval_start = time.perf_counter()
        try:
            evaluation_scores = evaluator.evaluate(
                question=rewritten_question,
                answer=response_text,
                retrieved_context=retrieved_context,
                route_selected=route_selected
            )
        except Exception:
            evaluation_scores = None
        evaluation_latency = time.perf_counter() - eval_start

        # Calculate latency
        total_response_latency = time.perf_counter() - start_time

        # Track with MLflow
        mlflow_tracker.track_chat_interaction(
            question=rewritten_question,
            route_selected=route_selected,
            session_id=session_id,
            user_id=current_user.id,  # type: ignore
            retrieved_document_count=result.get("retrieved_doc_count", 0),
            retrieval_latency_ms=result.get("retrieval_latency", 0.0) * 1000,
            llm_latency_ms=result.get("llm_latency", 0.0) * 1000,
            total_response_latency_ms=total_response_latency * 1000,
            evaluation_latency_ms=evaluation_latency * 1000,
            response_length=len(response_text),
            ticket_created=result.get("ticket_created", False),
            evaluation_scores=evaluation_scores
        )

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
            session_id=session_id,
            agent_used=result.get("route")
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