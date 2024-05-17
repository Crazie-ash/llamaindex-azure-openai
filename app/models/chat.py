from pydantic import BaseModel
from typing import List, Optional, Dict, Union

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

class ChatResponse(BaseModel):
    status: bool
    message: str
    data: Optional[Dict[str, Union[str, None]]] 