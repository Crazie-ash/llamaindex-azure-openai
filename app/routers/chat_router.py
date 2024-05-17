from fastapi import APIRouter, HTTPException
from ..models.chat import ChatRequest, ChatResponse
from ..controllers.chat_controller import handle_chat

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        return handle_chat(request)
    except HTTPException as e:
        raise e
