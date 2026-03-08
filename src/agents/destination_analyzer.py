from typing import List
from pydantic import BaseModel, Field

from src.agents.base_agent import BaseAgent
from src.tools.web_search_tool import web_search
from src.graph.state import AgentState
from src.utils.config import setup_logger

logger = setup_logger(__name__)

class DestinationProfile(BaseModel):
    summary: str = Field(description="A comprehensive summary of the destination including culture, climate, and general vibe.")
    top_attractions: List[str] = Field(description="List of 5-10 must-see attractions.")
    best_travel_months: List[str] = Field(description="The ideal months to visit considering weather and crowds.")
    local_transport_options: List[str] = Field(description="Recommended ways to get around (e.g., Subway, Taxis, Walking).")
    travel_risks: List[str] = Field(description="Potential risks such as weather events, high crime areas, or health advisories.")

class DestinationAnalyzer(BaseAgent):
    """
    Agent responsible for gathering broad intelligence about a destination using Web Search.
    """
    def __init__(self):
        super().__init__(name="DestinationAnalyzer")
        self.system_prompt = """
        You are an expert Travel Researcher. Your goal is to analyze the provided search 
        data about a destination and synthesize it into a structured, comprehensive profile.
        
        Focus on accuracy, practical advice, and highlighting what makes the destination unique.
        If the data mentions risks or bad times to visit, you MUST include them.
        """
        self.chain = self.create_chain(
            system_prompt=self.system_prompt,
            output_schema=DestinationProfile
        )

    def run(self, state: AgentState) -> dict:
        """
        Executes the Destination Analyzer logic.
        """
        destination = state["current_destination"]
        logger.info(f"Analyzing destination: {destination}")
        
        # 1. Gather Intelligence
        raw_data = web_search.search_destinations(destination)
        
        # 2. Analyze and Structure
        input_data = {
            "human_input": f"Destination: {destination}\n\nSearch Results:\n{raw_data}"
        }
        
        profile: DestinationProfile = self.invoke(chain=self.chain, inputs=input_data)
        
        # 3. Format output for state update
        formatted_profile = (
            f"**Destination Summary:** {profile.summary}\n\n"
            f"**Top Attractions:** {', '.join(profile.top_attractions)}\n\n"
            f"**Best Months:** {', '.join(profile.best_travel_months)}\n\n"
            f"**Transport:** {', '.join(profile.local_transport_options)}\n\n"
            f"**Risks:** {', '.join(profile.travel_risks)}"
        )
        
        return {"destination_profile": formatted_profile}

# Global instance
destination_analyzer = DestinationAnalyzer()
