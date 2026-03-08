from typing import List
from pydantic import BaseModel, Field

from src.agents.base_agent import BaseAgent
from src.tools.web_search_tool import web_search
from src.graph.state import AgentState, ItineraryResponse
from src.utils.config import setup_logger

logger = setup_logger(__name__)

class FactCheckResult(BaseModel):
    issues_found: List[str] = Field(description="List of factual errors found (e.g., 'Louvre is closed on Tuesdays'). Empty if none.")
    verified_facts: List[str] = Field(description="Important verified facts that support the itinerary.")

class FactChecker(BaseAgent):
    """
    Agent responsible for verifying specific attractions mentioned in the itinerary.
    """
    def __init__(self):
        super().__init__(name="FactChecker", model_name="llama3-70b-8192")
        self.system_prompt = """
        You are an expert Fact Checker for a prominent travel publication.
        Your job is to take the drafted itinerary and cross-reference the major attractions
        mentioned against real-world data (search results).
        
        Look for:
        1. Are these places actually open during the suggested days?
        2. Are the estimated costs wildly inaccurate?
        3. Do these places geographically make sense together on the same day?
        """
        self.chain = self.create_chain(
            system_prompt=self.system_prompt,
            output_schema=FactCheckResult
        )

    def run(self, state: AgentState) -> dict:
        """
        Executes the Fact Checking logic.
        """
        draft: ItineraryResponse = state.get("draft_itinerary")
        if not draft:
            logger.error("FactChecker called without a draft itinerary.")
            return {"fact_check_results": ["Missing draft."]}

        logger.info(f"Fact-checking itinerary for {draft.destination}...")
        
        # 1. Extract main attractions from the draft
        attractions = []
        for day in draft.days:
            for activity in day.activities:
                attractions.append(activity.title)
                
        # Limit the number of attractions to search to avoid rate limits
        top_attractions = attractions[:5] 
        search_query = f"{draft.destination} attractions info: " + ", ".join(top_attractions)
        
        # 2. Gather factual data
        real_world_data = web_search.search_attractions(search_query)
        
        # 3. Request Verification
        context = (
            f"Drafted Attractions: {', '.join(top_attractions)}\n\n"
            f"Search Results (Real-world data):\n{real_world_data}"
        )
        
        input_data = {
            "human_input": context
        }
        
        result: FactCheckResult = self.invoke(chain=self.chain, inputs=input_data)
        
        return {
            "fact_check_results": result.issues_found
        }

# Global instance
fact_checker = FactChecker()
