from pydantic import BaseModel

class CompletionRequest(BaseModel):
    prompt: str

class CompletionResponse(BaseModel):
    status: bool
    message: str
    data: dict = None
