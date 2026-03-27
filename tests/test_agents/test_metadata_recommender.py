import pytest
from unittest.mock import patch, MagicMock
from src.graph.state import AgentState
from src.models.schemas import UserPreferences

@patch('src.agents.metadata_recommender.MetadataRecommender.invoke')
def test_metadata_recommender(mock_invoke):
    """Test the Metadata Recommender agent logic with mock data."""
    from src.agents.metadata_recommender import metadata_recommender, MetadataTags
    
    # Mock output
    mock_invoke.return_value = MetadataTags(
        trip_tags=["History", "Culture"],
        travel_style="Relaxing",
        recommended_transport="Walking",
        trip_complexity_score=4
    )
    
    prefs = UserPreferences(destination="Rome", duration=4, budget="luxury", style="culture")
    state: AgentState = {
        "user_prefs": prefs,
        "current_destination": "Rome",
        "destination_profile": "A historic city.",
        "metadata_tags": [],
        "fact_check_results": [],
        "critic_feedback": "",
        "critic_score": 0.0,
        "revision_count": 0,
        "draft_itinerary": None,
        "final_itinerary": None
    }
    
    result = metadata_recommender.run(state)
    
    assert "metadata_tags" in result
    assert "History" in result["metadata_tags"]
    mock_invoke.assert_called_once()
