from llama_index.llms.azure_openai import AzureOpenAI
from ..settings import settings
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import Settings

def get_azure_openai():
    llm = AzureOpenAI(
        engine=settings.OPENAI_DEPLOYMENT,
        model=settings.OPENAI_MODEL,
        temperature=0.0,
        azure_endpoint=settings.OPENAI_API_ENDPOINT,
        api_key=settings.OPENAI_API_KEY,
        api_version=settings.OPENAI_API_VERSION,
    )
    Settings.llm = llm
    return


def get_azure_embedding():
    embed_model = AzureOpenAIEmbedding(
        model=settings.EMBEDDING_MODEL,
        deployment_name=settings.EMBEDDING_DEPLOYMENT,
        azure_endpoint=settings.OPENAI_API_ENDPOINT,
        api_key=settings.OPENAI_API_KEY,
        api_version=settings.OPENAI_API_VERSION,
    )
    Settings.embed_model = embed_model
    return
