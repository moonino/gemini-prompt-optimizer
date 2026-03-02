import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Prompt Optimizer Proxy"
    GEMINI_API_KEY: str = ""
    # Gemini API Native Endpoint
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta"
    
    # LLMLingua Settings
    COMPRESSION_ENABLED: bool = True
    COMPRESSION_RATE: float = 0.5
    
    DATABASE_URL: str = "sqlite:///./db/usage.db"

    # Gemini Pricing (USD per 1M Input Tokens) - 2025/2026 Updated
    # Pricing varies by context length, here we use the base rate (under 128k/200k)
    GEMINI_MODEL_PRICING: dict = {
        "gemini-2.0-flash": 0.10,        # Expected Lite/Flash pricing
        "gemini-2.0-flash-lite": 0.075,  # Estimate
        "gemini-1.5-flash": 0.075,       # Current
        "gemini-1.5-flash-8b": 0.0375,   # Half of flash
        "gemini-1.5-pro": 1.25,          # Under 128k
        "gemini-1.0-pro": 0.50,          # Legacy
        "default": 0.10                  # Default to Flash-like pricing
    }

    class Config:
        env_file = ".env"

settings = Settings()
