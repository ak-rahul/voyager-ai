import pytest
from unittest.mock import patch, MagicMock
from src.graph.state import AgentState
from src.models.schemas import UserPreferences

# We will mock the actual LLM API calls so tests run fast and free without needing keys
# in the CI/CD pipeline unless we explicitly run integration tests.

@patch('src.agents.destination_analyzer.web_search')
@patch('src.agents.destination_analyzer.DestinationAnalyzer.invoke')
def test_destination_analyzer(mock_invoke, mock_search):
    """Test the Destination Analyzer agent logic with mocked LLM and Search."""
    from src.agents.destination_analyzer import destination_analyzer, DestinationProfile
    
    # Mock the search tool
    mock_search.search_destinations.return_value = "Tokyo is great in Spring. Lots of sushi."
    
    # Mock the LLM Response
    mock_invoke.return_value = DestinationProfile(
        summary="Tokyo is vibrant.",
        top_attractions=["Shibuya", "Senso-ji"],
        best_travel_months=["March", "April", "May"],
        local_transport_options=["Subway", "Train"],
        travel_risks=["Earthquakes"]
    )
    
    prefs = UserPreferences(destination="Tokyo", duration=5, budget="moderate", style="culture")
    
    state: AgentState = {
        "user_prefs": prefs,
        "current_destination": "Tokyo",
        "destination_profile": "",
        "metadata_tags": [],
        "fact_check_results": [],
        "critic_feedback": "",
        "critic_score": 0.0,
        "revision_count": 0,
        "draft_itinerary": None,
        "final_itinerary": None
    }
    
    result = destination_analyzer.run(state)
    
    # Assertions
    assert "destination_profile" in result
    assert "Shibuya" in result["destination_profile"]
    mock_search.search_destinations.assert_called_once_with("Tokyo")
    mock_invoke.assert_called_once()

def test_workflow_compilation():
    """Verify that the LangGraph workflow compiles correctly and the edges are valid."""
    from src.graph.workflow import workflow
    
    # Check that graph is compiled
    assert workflow is not None
    # Check that nodes exist (This accesses the compiled graph's internal nodes dictionary)
    assert "analyze_destination" in workflow.nodes
    assert "critique" in workflow.nodes
    assert "finalize" in workflow.nodes

def test_route_after_critique():
    """Test the conditional routing logic of the graph."""
    from src.graph.workflow import route_after_critique
    
    # Test High Score
    state_high_score: AgentState = {"critic_score": 8.5, "revision_count": 1}
    assert route_after_critique(state_high_score) == "finalize"
    
    # Test Low Score beneath retry limit
    state_low_score: AgentState = {"critic_score": 4.0, "revision_count": 1}
    assert route_after_critique(state_low_score) == "generate_draft"
    
    # Test Low Score hitting retry limit
    state_max_retry: AgentState = {"critic_score": 4.0, "revision_count": 3}
    assert route_after_critique(state_max_retry) == "finalize"

