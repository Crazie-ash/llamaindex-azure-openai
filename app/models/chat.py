from pydantic import BaseModel
from typing import List, Optional, Dict, Union

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    status: bool
    message: str
    data: Optional[Dict[str, Union[str, None]]] 