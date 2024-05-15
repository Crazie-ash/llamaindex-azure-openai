import os
from llama_index.llms.azure_openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# Retrieve environment variables
api_key = os.getenv("OPENAI_API_KEY")
api_version = os.getenv("OPENAI_API_VERSION")
api_endpoint = os.getenv("OPENAI_API_ENDPOINT")
model_used = os.getenv("OPENAI_MODEL")
deployment_used = os.getenv("OPENAI_DEPLOYMENT")

llm = AzureOpenAI(
    engine=deployment_used,
    model=model_used,
    temperature=0.0,
    azure_endpoint=api_endpoint,
    api_key=api_key,
    api_version=api_version,
)

response = llm.complete("The sky is a beautiful blue and")
print(response)