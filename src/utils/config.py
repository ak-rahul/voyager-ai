import os
import logging
from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv() # Force load environment variables

class Settings(BaseSettings):
    """
    Enterprise-level configuration management using pydantic_settings.
    Automatically loads from .env or environment variables.
    """
    
    # Project Info
    PROJECT_NAME: str = "WanderAI Travel Planner"
    VERSION: str = "1.0.0"
    
    # API Keys
    GROQ_API_KEY: str = ""
    TAVILY_API_KEY: Optional[str] = None  # Example for real-time web search
    OPENWEATHER_API_KEY: Optional[str] = None

    # App Settings
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    TIMEOUT_SECONDS: int = 30
    MAX_RETRIES: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global dependency
settings = Settings()

def setup_logger(name: str) -> logging.Logger:
    """Configures and returns a standard logger for the given module."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(settings.LOG_LEVEL)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(settings.LOG_LEVEL)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
    return logger
