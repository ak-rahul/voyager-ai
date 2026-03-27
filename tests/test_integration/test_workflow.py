import pytest
from unittest.mock import patch, MagicMock
from src.graph.state import AgentState
from src.models.schemas import UserPreferences, ItineraryResponse

class MagicMockItinerary:
    pass

@patch('src.agents.destination_analyzer.destination_analyzer.run')
@patch('src.agents.metadata_recommender.metadata_recommender.run')
@patch('src.agents.content_improver.content_improver.run')
@patch('src.agents.fact_checker.fact_checker.run')
@patch('src.agents.reviewer_critic.reviewer_critic.run')
def test_full_workflow_happy_path(mock_critic, mock_fact, mock_improver, mock_meta, mock_analyzer):
    from src.graph.workflow import workflow
    
    mock_analyzer.return_value = {"destination_profile": "Dest"}
    mock_meta.return_value = {"metadata_tags": ["Fun"]}
    mock_improver.return_value = {"draft_itinerary": MagicMockItinerary()}
    mock_fact.return_value = {"fact_check_results": []}
    mock_critic.return_value = {"critic_score": 9.0, "critic_feedback": "Perfect"}
    
    prefs = UserPreferences(destination="Austin", duration=2, budget="budget", style="culture")
    
    initial_state = {
        "user_prefs": prefs,
        "current_destination": "Austin",
        "revision_count": 0
    }
    
    # Run the generator fully
    final_output = None
    for step in workflow.stream(initial_state):
        for k, v in step.items():
            final_output = v
            
    assert final_output is not None
    assert "final_itinerary" in final_output
    
    # Verify graph routing executed the expected nodes
    assert mock_analyzer.call_count == 1
    assert mock_meta.call_count == 1
    assert mock_improver.call_count == 1
    assert mock_fact.call_count == 1
    assert mock_critic.call_count == 1

    assert mock_critic.call_count == 1
