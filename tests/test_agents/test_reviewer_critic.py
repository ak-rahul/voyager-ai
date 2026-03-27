import pytest
from unittest.mock import patch
from src.graph.state import AgentState
from src.models.schemas import UserPreferences, ItineraryResponse, BudgetBreakdown

@patch('src.agents.reviewer_critic.ReviewerCritic.invoke')
def test_reviewer_critic_valid(mock_invoke):
    from src.agents.reviewer_critic import reviewer_critic, ReviewScore
    
    mock_invoke.return_value = ReviewScore(score=8.5, critic_feedback="Great itinerary.")
    
    draft = ItineraryResponse(
        destination="Kyoto",
        summary="Temples.",
        days=[],
        budget=BudgetBreakdown(flightsTransit=0, accommodation=0, foodDining=0, activities=0, total=0)
    )
    prefs = UserPreferences(destination="Kyoto", duration=1, budget="budget", style="culture")
    
    state: AgentState = {
        "user_prefs": prefs,
        "current_destination": "Kyoto",
        "destination_profile": "",
        "metadata_tags": [],
        "fact_check_results": [],
        "critic_feedback": "",
        "critic_score": 0.0,
        "revision_count": 0,
        "draft_itinerary": draft,
        "final_itinerary": None
    }
    
    result = reviewer_critic.run(state)
    
    assert result["critic_score"] == 8.5
    assert "Great itinerary" in result["critic_feedback"]

def test_reviewer_critic_missing_draft():
    from src.agents.reviewer_critic import reviewer_critic
    state: AgentState = {
        "user_prefs": UserPreferences(destination="Null", duration=1, budget="budget", style="culture"),
        "current_destination": "Null",
        "destination_profile": "",
        "metadata_tags": [],
        "fact_check_results": [],
        "critic_feedback": "",
        "critic_score": 0.0,
        "revision_count": 0,
        "draft_itinerary": None,
        "final_itinerary": None
    }
    
    result = reviewer_critic.run(state)
    assert result["critic_score"] == 0.0
    assert "Missing draft." in result["critic_feedback"]
