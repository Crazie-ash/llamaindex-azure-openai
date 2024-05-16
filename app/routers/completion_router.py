from fastapi import APIRouter
from ..models.completion import CompletionRequest, CompletionResponse
from ..controllers.completion_controller import handle_completion

router = APIRouter()

@router.post("/complete", response_model=CompletionResponse)
async def complete_text_endpoint(request: CompletionRequest):
    return handle_completion(request)
