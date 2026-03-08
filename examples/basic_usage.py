from src.graph.state import AgentState
from src.models.schemas import UserPreferences
from src.graph.workflow import workflow

def run_basic_app():
    print("Starting Voyager AI Workflow...")
    prefs = UserPreferences(
        destination="Kyoto",
        duration=3,
        budget="luxury",
        style="relaxation"
    )
    
    initial_state: AgentState = {
        "user_prefs": prefs,
        "current_destination": "Kyoto",
        "destination_profile": "",
        "metadata_tags": [],
        "fact_check_results": [],
        "critic_feedback": "",
        "critic_score": 0.0,
        "revision_count": 0,
        "draft_itinerary": None,
        "final_itinerary": None
    }

    final_result = None
    for event in workflow.stream(initial_state):
        for node_name, state_update in event.items():
            print(f"Completed node: {node_name}")
            final_result = state_update
            
    print("Final Output Generated!")
    
if __name__ == "__main__":
    run_basic_app()
