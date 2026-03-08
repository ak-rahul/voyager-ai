import logging
from src.utils.config import setup_logger
from src.models.schemas import UserPreferences, ItineraryResponse
from src.graph.workflow import create_workflow

logger = setup_logger("travel_planner.main")

def run_planner(prefs: UserPreferences) -> ItineraryResponse:
    """
    Main entry point for the Travel Planner backend.
    Initializes the LangGraph state machine and executes the multi-agent workflow.
    """
    logger.info("Initializing Agentic Travel Planner...")
    workflow = create_workflow()
    
    # Initialize State
    initial_state = {
        "user_prefs": prefs,
        "current_destination": None,
        "research_context": "",
        "weather_forecast": None,
        "flights_data": None,
        "critic_feedback": None,
        "iteration_count": 0,
        "final_itinerary": None
    }
    
    logger.info("Starting LangGraph orchestration DAG execution...")
    try:
        # Execute the Graph
        result_state = workflow.invoke(initial_state)
        logger.info("Workflow execution complete.")
        return result_state["final_itinerary"]
    except Exception as e:
        logger.error(f"Enterprise Circuit Breaker Triggered - Graph execution failed: {e}")
        raise e
