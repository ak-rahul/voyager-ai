from typing import TypedDict, Optional, List, Dict, Any
from src.models.schemas import UserPreferences, ItineraryResponse

class AgentState(TypedDict):
    """
    Central State Machine for the robust LangGraph orchestrator.
    This tracks the entire workflow of the itinerary generation.
    """
    # Inputs
    user_prefs: UserPreferences
    
    # Intemediary state variables
    current_destination: Optional[str]
    research_context: str
    weather_forecast: Optional[str]
    flights_data: Optional[Dict[str, Any]]
    
    # Feedback loop control for retry logic
    critic_feedback: Optional[str]
    iteration_count: int
    
    # Final Output
    final_itinerary: Optional[ItineraryResponse]
