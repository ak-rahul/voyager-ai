from src.agents.base_agent import BaseAgent
from src.graph.state import AgentState
from src.models.schemas import ItineraryResponse
from src.utils.config import setup_logger

logger = setup_logger(__name__)

class ContentImprover(BaseAgent):
    """
    Agent responsible for generating the initial draft itinerary and 
    improving it based on critic feedback.
    """
    def __init__(self):
        # We might use the 70b model here for complex reasoning
        super().__init__(name="ContentImprover", model_name="llama-3.3-70b-versatile")
        self.system_prompt = """
        You are a Master Travel Planner. Your goal is to generate a detailed, highly 
        personalized day-by-day itinerary based on the destination profile, user preferences, 
        and any previous feedback.
        
        If you receive 'Critic Feedback', you MUST adjust your previous draft to address 
        the concerns raised (e.g., budget too high, pacing too fast).
        
        Ensure activities are logically grouped geographically and the budget breakdown is realistic.
        """
        self.chain = self.create_chain(
            system_prompt=self.system_prompt,
            output_schema=ItineraryResponse
        )

    def run(self, state: AgentState) -> dict:
        """
        Executes the itinerary generation/improvement logic.
        """
        logger.info(f"Generating itinerary for: {state.get('current_destination')}")
        
        # 1. Prepare Input Context
        prefs = state["user_prefs"]
        dest_profile = state.get("destination_profile", "No destination profile available.")
        tags = ", ".join(state.get("metadata_tags", []))
        feedback = state.get("critic_feedback", "No feedback yet - this is the first draft.")
        
        # We'd include RAG context in a fully built out version
        
        context = (
            f"User Preferences: Duration {prefs.duration} days, Budget {prefs.budget}, Style: {prefs.style}\n"
            f"Trip Tags: {tags}\n"
            f"Destination Profile: {dest_profile}\n"
            f"Critic Feedback (Must Address): {feedback}\n"
        )
        
        input_data = {
            "human_input": context
        }
        
        # 2. Generate Itinerary
        draft: ItineraryResponse = self.invoke(chain=self.chain, inputs=input_data)
        
        return {"draft_itinerary": draft}

# Global instance
content_improver = ContentImprover()
