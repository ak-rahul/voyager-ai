import pytest
from unittest.mock import patch, MagicMock
from src.graph.state import AgentState
from src.models.schemas import UserPreferences, ItineraryResponse, BudgetBreakdown

@patch('src.agents.content_improver.ContentImprover.invoke')
def test_content_improver_run(mock_invoke):
    """Test Content Improver creates a draft itinerary."""
    from src.agents.content_improver import content_improver
    
    mock_invoke.return_value = ItineraryResponse(
        destination="Bali",
        summary="A tropical escape.",
        days=[],
        budget=BudgetBreakdown(flightsTransit=1000, accommodation=500, foodDining=300, activities=200, total=2000)
    )
    
    prefs = UserPreferences(destination="Bali", duration=7, budget="moderate", style="relaxation")
    state: AgentState = {
        "user_prefs": prefs,
        "current_destination": "Bali",
        "destination_profile": "Nice beaches.",
        "metadata_tags": ["Tropical"],
        "fact_check_results": [],
        "critic_feedback": "Initial prompt",
        "critic_score": 0.0,
        "revision_count": 0,
        "draft_itinerary": None,
        "final_itinerary": None
    }
    
    result = content_improver.run(state)
    
    assert "draft_itinerary" in result
    assert result["draft_itinerary"].summary == "A tropical escape."
    mock_invoke.assert_called_once()
