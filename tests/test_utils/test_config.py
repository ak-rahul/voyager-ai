import pytest
import os
from unittest.mock import patch

def test_config_loads_defaults():
    from src.utils.config import Settings
    settings = Settings(GROQ_API_KEY="test_key", TAVILY_API_KEY="test_tavily_key")
    
    assert settings.PROJECT_NAME == "WanderAI Travel Planner"
    assert settings.GROQ_API_KEY == "test_key"
    assert settings.TAVILY_API_KEY == "test_tavily_key"


