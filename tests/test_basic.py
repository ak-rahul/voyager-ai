import pytest
from src.utils.config import settings

def test_settings_load():
    """Verify that settings can be instantiated (even without .env)."""
    assert settings.PROJECT_NAME == "WanderAI Travel Planner"
    assert settings.VERSION == "1.0.0"

def test_pydantic_schemas():
    """Verify that pydantic models load without syntax errors."""
    from src.models.schemas import UserPreferences
    
    prefs = UserPreferences(
        destination="Tokyo",
        duration=5,
        budget="budget",
        style="culture"
    )
    
    assert prefs.destination == "Tokyo"
    assert prefs.budget == "budget"
