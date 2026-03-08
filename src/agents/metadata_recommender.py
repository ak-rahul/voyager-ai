from typing import List
from pydantic import BaseModel, Field

from src.agents.base_agent import BaseAgent
from src.graph.state import AgentState
from src.utils.config import setup_logger

logger = setup_logger(__name__)

class MetadataTags(BaseModel):
    trip_tags: List[str] = Field(description="5-7 categorizing tags (e.g., 'Adventure', 'Nature', 'Budget Travel').")
    travel_style: str = Field(description="A short phrase describing the overall vibe (e.g., 'Fast-paced exploration').")
    recommended_transport: str = Field(description="The primary mode of transport suggested.")
    trip_complexity_score: int = Field(description="Score from 1-10 on how hard this trip is to plan/execute.")

class MetadataRecommender(BaseAgent):
    """
    Agent responsible for categorizing the trip based on user preferences and destination research.
    """
    def __init__(self):
        super().__init__(name="MetadataRecommender")
        self.system_prompt = """
        You are an expert Travel Profiler. Your goal is to analyze the user's preferences 
        alongside the destination profile and generate accurate metadata tags.
        
        These tags will be used by downstream agents to ensure the itinerary matches 
        the expected vibe, budget, and travel style.
        """
        self.chain = self.create_chain(
            system_prompt=self.system_prompt,
            output_schema=MetadataTags
        )

    def run(self, state: AgentState) -> dict:
        """
        Executes the Metadata Recommender logic.
        """
        logger.info("Generating trip metadata...")
        
        # 1. Prepare Input Context
        prefs = state["user_prefs"]
        dest_profile = state.get("destination_profile", "No profile available.")
        
        context = (
            f"User Preferences: Duration: {prefs.duration} days, Budget: {prefs.budget}, Style: {prefs.style}\n"
            f"Destination Profile: {dest_profile}"
        )
        
        input_data = {
            "human_input": context
        }
        
        # 2. Generate Metadata
        metadata: MetadataTags = self.invoke(chain=self.chain, inputs=input_data)
        
        return {"metadata_tags": metadata.trip_tags}

# Global instance
metadata_recommender = MetadataRecommender()
