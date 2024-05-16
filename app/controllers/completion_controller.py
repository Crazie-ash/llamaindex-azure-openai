from fastapi import HTTPException
from ..models.completion import CompletionRequest, CompletionResponse
from ..services.completion_service import complete_text
import logging

logger = logging.getLogger(__name__)

def handle_completion(request: CompletionRequest) -> CompletionResponse:
    try:
        response_text = complete_text(request.prompt)
        return CompletionResponse(
            status=True,
            message="Text completion successful",
            data={"response": response_text}
        )
    except RuntimeError as e:
        logger.error(f"Error in handle_completion: {e}")
        return CompletionResponse(
            status=False,
            message="Failed to complete text",
            data=None
        )
    except Exception as e:
        logger.error(f"Unexpected error in handle_completion: {e}")
        return CompletionResponse(
            status=False,
            message="Unexpected server error",
            data=None
        )
