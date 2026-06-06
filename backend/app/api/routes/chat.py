'''This is file for Chat API'''


from fastapi import APIRouter, HTTPException
from app.services.llm_service import LLMService
from app.schemas.chat import ChatRequest 
router = APIRouter()
llm_service = LLMService()


@router.post("/chat")
async def chat(messages: ChatRequest):
    try:
        response = llm_service.get_response(messages.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))