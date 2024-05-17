from typing import Optional
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core.llms import ChatMessage
from ..settings import settings
from ..models.chat import Message
import logging

logger = logging.getLogger(__name__)

def get_azure_openai():
    return AzureOpenAI(
        engine=settings.OPENAI_DEPLOYMENT,
        model=settings.OPENAI_MODEL,
        temperature=0.0,
        azure_endpoint=settings.OPENAI_API_ENDPOINT,
        api_key=settings.OPENAI_API_KEY,
        api_version=settings.OPENAI_API_VERSION,
    )

def handle_chat_service(messages: list[Message]) -> Optional[str]:
    try:
        llm = get_azure_openai()
        chat_messages = [ChatMessage(role=msg.role, content=msg.content) for msg in messages]
        response = llm.chat(chat_messages)
        
        if hasattr(response, 'text'):
            response_text = response.text.strip()
        else:
            response_text = response.raw['choices'][0].message.content.strip()
        
        return response_text
    except Exception as e:
        logger.error(f"Error completing text: {e}")
        raise RuntimeError("Failed to complete text") from e
