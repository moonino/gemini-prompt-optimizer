import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Prompt Optimizer Proxy"
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    
    # LLMLingua Settings
    COMPRESSION_ENABLED: bool = True
    COMPRESSION_RATE: float = 0.5
    
    DATABASE_URL: str = "sqlite:///./db/usage.db"

    class Config:
        env_file = ".env"

settings = Settings()
