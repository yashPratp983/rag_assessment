from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    qdrant_url: str
    embedding_model_name: str
    llm_model_name: str
    qdrant_api_key: str
    qdrant_collection_name: str
    groq_api_key: str
    top_k: int

    class Config:
        env_file = ".env"
        case_sensitive = False

    @classmethod
    def get_settings(cls):
        return cls()

# Use this to get the settings
settings = Settings.get_settings()