from typing import TypedDict, Optional, List, Dict, Any, Annotated
import operator
from src.models.schemas import UserPreferences, ItineraryResponse

class AgentState(TypedDict):
    """
    State for the Voyager AI LangGraph workflow.
    """
    # Inputs
    user_prefs: UserPreferences
    
    # Intemediary state variables
    current_destination: str
    destination_profile: str
    metadata_tags: List[str]
    
    # Fact Checking and Critic
    fact_check_results: List[str]
    critic_feedback: str
    critic_score: float
    
    # Iteration control
    revision_count: int
    
    # Final Output
    draft_itinerary: Optional[ItineraryResponse]
    final_itinerary: Optional[ItineraryResponse]
