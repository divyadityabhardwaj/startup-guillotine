import os
from typing import Optional
from pydantic_settings import BaseSettings

# from dotenv import load_dotenv
# load_dotenv()

class Settings(BaseSettings):
    # API Keys
    GEMINI_API_KEY: Optional[str] = None
    TAVILY_API_KEY: Optional[str] = None
    REDDIT_CLIENT_ID: Optional[str] = None
    REDDIT_SECRET: Optional[str] = None
    REDDIT_USER_AGENT: Optional[str] = None
    
    # Redis (for Vercel, we'll use Upstash or similar)
    REDIS_URL: Optional[str] = None
    
    # API Limits and Settings
    MAX_TAVILY_RESULTS: int = 10
    REDDIT_LIMIT: int = 50
    REDDIT_DAYS: int = 180
    MAX_RETRIES: int = 3
    BASE_DELAY: float = 1.5
    
    # Gemini Models (Flash only for reliability)
    GEMINI_FLASH_MODEL: str = "gemini-1.5-flash"
    
    # Serverless Settings
    FUNCTION_TIMEOUT: int = 60  # Vercel function timeout in seconds
    MAX_CONCURRENT_REQUESTS: int = 5
    

settings = Settings()

if not settings.GEMINI_API_KEY:
    raise ValueError("Missing required environment variable: GEMINI_API_KEY")

if not settings.TAVILY_API_KEY:
    raise ValueError("Missing required environment variable: TAVILY_API_KEY")