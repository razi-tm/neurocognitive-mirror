from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://ncm:ncm@localhost:5432/ncm"
    redis_url: str = "redis://localhost:6379/0"
    elasticsearch_url: str = "http://localhost:9200"
    llm_base_url: str = "http://localhost:8001/v1"
    llm_api_key: str = "local-key"
    llm_model: str = "local-llama3-8b"
    jwt_secret: str = "change-me"
    cors_origins: str = "http://localhost:5173"
    sync_enabled: bool = False

settings = Settings()
