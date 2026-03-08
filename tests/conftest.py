import os
import pytest

# Ensure dummy keys are set before any tests are collected
os.environ["GROQ_API_KEY"] = "dummy_groq_key_for_testing"
os.environ["TAVILY_API_KEY"] = "dummy_tavily_key_for_testing"

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Ensure environment variables are set for all tests."""
    os.environ["GROQ_API_KEY"] = "dummy_groq_key_for_testing"
    os.environ["TAVILY_API_KEY"] = "dummy_tavily_key_for_testing"
