from fastapi import APIRouter, HTTPException
from app.data.schemas import ChatRequest, ChatResponse
from app.services.ai_service import ai_agent_service
from app.utils.logger import logger

router = APIRouter(tags=["AI Agent Chat"])

@router.post("/api/chat", response_model=ChatResponse)
def handle_chat_query(req: ChatRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Message prompt cannot be empty.")
        
    try:
        response = ai_agent_service.process_chat_query(req)
        return response
    except Exception as e:
        logger.error(f"Error handling chat request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process chat query: {str(e)}")
