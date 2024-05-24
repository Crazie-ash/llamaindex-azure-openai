import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_API_VERSION: str = os.getenv("OPENAI_API_VERSION")
    OPENAI_API_ENDPOINT: str = os.getenv("OPENAI_API_ENDPOINT")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL")
    OPENAI_DEPLOYMENT: str = os.getenv("OPENAI_DEPLOYMENT")
    ELASTICSEARCH_HOST: str = os.getenv("ELASTICSEARCH_HOST")
    ELASTICSEARCH_USER: str = os.getenv("ELASTICSEARCH_USER")
    ELASTICSEARCH_PASSWORD: str = os.getenv("ELASTICSEARCH_PASSWORD")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL")
    EMBEDDING_DEPLOYMENT: str = os.getenv("EMBEDDING_DEPLOYMENT")


settings = Settings()
