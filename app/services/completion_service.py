from llama_index.llms.azure_openai import AzureOpenAI
from ..settings import settings
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

def complete_text(prompt: str) -> str:
    try:
        llm = get_azure_openai()
        response = llm.complete(prompt)
        if hasattr(response, 'text'):
            response_text = response.text.strip()
        else:
            response_text = response.raw['choices'][0].message.content.strip()
        
        return response_text
    except Exception as e:
        logger.error(f"Error completing text: {e}")
        raise RuntimeError("Failed to complete text") from e
