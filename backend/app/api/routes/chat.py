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

        # Generate a unique message ID for this assistant response
        message_id = str(uuid.uuid4())

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
            user_id=current_user.id,
            message_id=message_id
        )

        return ChatResponse(
            response=response_text,
            session_id=session_id,
            agent_used=result.get("route"),
            message_id=message_id,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =====================================================
# Conversation History Endpoints
# =====================================================

@router.get("/conversations")
async def get_conversations(
    current_user: User = Depends(require_customer)
):
    """
    Retrieves all conversations for the current user.
    """
    try:
        conversations = memory.get_conversations_for_user(current_user.id)
        # We only want to return metadata, not all messages for the list view
        for conv in conversations:
            if "messages" in conv:
                del conv["messages"]
        return conversations
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/conversations/{session_id}/messages")
async def get_conversation_messages(
    session_id: str,
    current_user: User = Depends(require_customer)
):
    """
    Retrieves messages for a specific conversation session.
    """
    try:
        conversations = memory.get_conversations_for_user(current_user.id)
        for conv in conversations:
            if conv["id"] == session_id:
                return conv.get("messages", [])
                
        raise HTTPException(status_code=404, detail="Conversation not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.delete("/conversations/{session_id}")
async def delete_conversation(
    session_id: str,
    current_user: User = Depends(require_customer)
):
    """
    Deletes a specific conversation session and all its messages.
    """
    try:
        # First verify the conversation belongs to the user
        conversations = memory.get_conversations_for_user(current_user.id)
        owns_conversation = any(conv["id"] == session_id for conv in conversations)
        
        if not owns_conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
            
        memory.clear_session(session_id)
        return {"status": "success", "message": "Conversation deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )