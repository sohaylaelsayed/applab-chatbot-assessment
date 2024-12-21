from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME: str = "applab-assessment"
    APP_VERSION: str = "0.1.0"

    FILE_ALLOWED_TYPES: list = ["application/pdf"]
    FILE_MAX_SIZE: int = 10
    FILE_DEFAULT_CHUNK_SIZE: int = 512000 # 512KB  

    EMBEDDING_BACKEND: str = "OPENAI"

    OPENAI_API_KEY: str = None

    EMBEDDING_MODEL_ID: str = "text-embedding-3-small"
    EMBEDDING_MODEL_SIZE: int = 1536
    INPUT_DAFAULT_MAX_CHARACTERS: int = 8191
    GENERATION_DAFAULT_MAX_TOKENS: int = 200
    GENERATION_DAFAULT_TEMPERATURE: float = 0.1 

    
    VECTOR_DB_BACKEND : str = "QDRANT"
    VECTOR_DB_PATH : str = "VECTOR_DB_PATH"
    VECTOR_DB_DISTANCE_METHOD: str = "cosine"



    class Config:
        env_file = ".env"

def get_settings():
    return Settings()