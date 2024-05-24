from fastapi import APIRouter, Depends, HTTPException

from app.services.elasticsearch_service import get_elasticSearch
from ..models.chat import ChatRequest, ChatResponse
from ..controllers.chat_controller import handle_chat

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, es= Depends(get_elasticSearch)):
    try:
        return handle_chat(request, es)
    except HTTPException as e:
        raise e
