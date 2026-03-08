from pydantic import BaseModel, Field

from src.agents.base_agent import BaseAgent
from src.graph.state import AgentState, ItineraryResponse
from src.utils.config import setup_logger

logger = setup_logger(__name__)

class ReviewScore(BaseModel):
    score: float = Field(description="Score from 0.0 to 10.0 representing the quality of the itinerary.")
    critic_feedback: str = Field(description="Actionable feedback for the Content Improver. Point out unrealistic travel times, budget overruns, or mismatch with user prefs.")

class ReviewerCritic(BaseAgent):
    """
    Agent responsible for evaluating the draft itinerary and providing feedback.
    """
    def __init__(self):
        super().__init__(name="ReviewerCritic", model_name="llama3-70b-8192")
        self.system_prompt = """
        You are a strict, hyper-critical Travel Critic and Logistics Expert.
        
        Your goal is to tear down the drafted itinerary if it violates the user's constraints
        (budget, duration, style) OR if the logistics (travel time between places) are impossible.
        
        Be ruthlessly objective. If the itinerary is perfect, score it a 10 and return empty feedback.
        If it needs work, explain EXACTLY what the Content Improver needs to change.
        """
        self.chain = self.create_chain(
            system_prompt=self.system_prompt,
            output_schema=ReviewScore
        )

    def run(self, state: AgentState) -> dict:
        """
        Executes the critic logic.
        """
        draft: ItineraryResponse = state.get("draft_itinerary")
        if not draft:
            logger.error("Critic called without a draft itinerary.")
            return {"critic_score": 0.0, "critic_feedback": "Missing draft."}

        prefs = state["user_prefs"]
        logger.info(f"Critiquing itinerary for {draft.destination}...")
        
        context = (
            f"User Preferences:\n"
            f"- Budget Level: {prefs.budget}\n"
            f"- Travel Style: {prefs.style}\n"
            f"- Duration: {prefs.duration} days\n\n"
            f"Drafted Itinerary:\n"
            f"Duration generated: {len(draft.days)} days\n"
            f"Estimated Budget: Flights=${draft.budget.flightsTransit}, Hotels=${draft.budget.accommodation}, Food=${draft.budget.foodDining}, Activities=${draft.budget.activities}, Total=${draft.budget.total}\n\n"
            f"Day Plans Summary:\n"
        )
        
        for day in draft.days:
            activities = ", ".join([a.title for a in day.activities])
            context += f"Day {day.dayNumber} ({day.theme}): {activities}\n"
            
        input_data = {
            "human_input": context
        }
        
        # 2. Generate Critique
        review: ReviewScore = self.invoke(chain=self.chain, inputs=input_data)
        
        # Store feedback. If score is high enough, workflow resolves.
        return {
            "critic_score": review.score,
            "critic_feedback": review.critic_feedback
        }

# Global instance
reviewer_critic = ReviewerCritic()
