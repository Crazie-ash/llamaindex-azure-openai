from typing import Optional
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core.llms import ChatMessage
from ..models.chat import Message
import logging
from llama_index.core import Settings


logger = logging.getLogger(__name__)

def handle_chat_service(messages: list[Message]) -> Optional[str]:
    try:
        chat_messages = [ChatMessage(role=msg.role, content=msg.content) for msg in messages]
        response = Settings.llm.chat(chat_messages)
        
        if hasattr(response, 'text'):
            response_text = response.text.strip()
        else:
            response_text = response.raw['choices'][0].message.content.strip()
        
        return response_text
    except Exception as e:
        logger.error(f"Error chat text: {e}")
        raise RuntimeError("Failed to chat text") from e
