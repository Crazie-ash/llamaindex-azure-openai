from fastapi import HTTPException
from ..models.chat import ChatRequest, ChatResponse
from ..services.chat_service import handle_chat_service
import logging

logger = logging.getLogger(__name__)

def handle_chat(request: ChatRequest) -> ChatResponse:
    try:
        response = handle_chat_service(request.messages)
        return ChatResponse(
            status=True,
            message="Chat successful",
            data={"response": response}
        )
    except RuntimeError as e:
        logger.error(f"Error in handle_chat: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to chat",
            headers={"X-Error": "RuntimeError"}
        )
    except Exception as e:
        logger.error(f"Unexpected error in handle_chat: {e}")
        raise HTTPException(
            status_code=500,
            detail="Unexpected server error",
            headers={"X-Error": "ServerError"}
        )

