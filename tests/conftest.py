import os
import pytest

# Ensure dummy keys are set before any tests are collected
os.environ["GROQ_API_KEY"] = "dummy_groq_key_for_testing"
os.environ["TAVILY_API_KEY"] = "dummy_tavily_key_for_testing"

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Ensure environment variables are set for all tests."""
    original_groq = os.environ.get("GROQ_API_KEY")
    original_tavily = os.environ.get("TAVILY_API_KEY")
    
    os.environ["GROQ_API_KEY"] = "dummy_groq_key_for_testing"
    os.environ["TAVILY_API_KEY"] = "dummy_tavily_key_for_testing"
    
    yield
    
    if original_groq is not None:
        os.environ["GROQ_API_KEY"] = original_groq
    elif "GROQ_API_KEY" in os.environ:
        del os.environ["GROQ_API_KEY"]
        
    if original_tavily is not None:
        os.environ["TAVILY_API_KEY"] = original_tavily
    elif "TAVILY_API_KEY" in os.environ:
        del os.environ["TAVILY_API_KEY"]
