import pytest
from unittest.mock import patch
from src.graph.state import AgentState
from src.models.schemas import UserPreferences, ItineraryResponse, BudgetBreakdown

@patch('src.agents.fact_checker.FactChecker.invoke')
@patch('src.agents.fact_checker.web_search')
def test_fact_checker_run(mock_search, mock_invoke):
    from src.agents.fact_checker import fact_checker, FactCheckResult
    
    # Mock LLM and Search
    mock_invoke.return_value = FactCheckResult(issues_found=[], verified_facts=["Times Square is open."])
    mock_search.search_attractions.return_value = "Results"
    
    draft = ItineraryResponse(
        destination="NYC",
        summary="A city trip.",
        days=[],
        budget=BudgetBreakdown(flightsTransit=0, accommodation=0, foodDining=0, activities=0, total=0)
    )
    prefs = UserPreferences(destination="NYC", duration=1, budget="budget", style="culture")
    
    state: AgentState = {
        "user_prefs": prefs,
        "current_destination": "NYC",
        "destination_profile": "",
        "metadata_tags": [],
        "fact_check_results": [],
        "critic_feedback": "",
        "critic_score": 0.0,
        "revision_count": 0,
        "draft_itinerary": draft,
        "final_itinerary": None
    }
    
    result = fact_checker.run(state)
    
    assert "fact_check_results" in result
    assert result["fact_check_results"] == []
    mock_invoke.assert_called_once()
    mock_search.search_attractions.assert_called_with("NYC attractions info: ")
