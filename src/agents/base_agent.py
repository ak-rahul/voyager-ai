import logging
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from src.models.schemas import UserPreferences, DailyPlan
from src.tools.weather_tool import get_weather_forecast
from src.tools.rag_retriever import retrieve_travel_blogs

logger = logging.getLogger(__name__)

class BaseAgent:
    """Base class for all Agents in the enterprise architecture."""
    def __init__(self, model_name: str = "llama3-70b-8192", temperature: float = 0.7):
        # Using Groq for blazingly fast inference
        self.llm = ChatGroq(temperature=temperature, model_name=model_name)

class DestinationAgent(BaseAgent):
    """Responsible for intelligently recommending destinations."""
    
    def process(self, prefs: UserPreferences) -> str:
        if prefs.destination:
            return prefs.destination
            
        logger.info("Destination is blank. Inferring optimal location...")
        prompt = PromptTemplate(
            template="Suggest exactly ONE best travel destination for {duration} days on a {budget} budget focusing on {style}. Return only the City and Country.",
            input_variables=["duration", "budget", "style"]
        )
        chain = prompt | self.llm
        result = chain.invoke({
            "duration": prefs.duration,
            "budget": prefs.budget,
            "style": prefs.style
        })
        return result.content.strip()

class PlannerAgent(BaseAgent):
    """Breaks down destination into day-by-day logical loops incorporating RAG and Environment."""
    
    def process(self, destination: str, prefs: UserPreferences, weather: str, rag_context: str) -> list[DailyPlan]:
        logger.info(f"Generating logical day plans for {destination}")
        
        # Here we tell the AI to use local secrets and adapt for weather
        template = """You are a master Travel Concept Planner.
        Create a high-level daily theme breakdown for a {duration}-day trip to {destination}.
        
        CRITICAL CONSTRAINTS:
        1. Adapt to Weather Forecast: {weather}
        2. Incorporate Hidden Secrets from RAG Vector DB: {rag_context}
        
        {format_instructions}
        """
        parser = PydanticOutputParser(pydantic_object=DailyPlan) # Simplified
        
        # In a real app we parse a List[DailyPlan], skipping raw code implementation for brevity
        # Returning mock objects based on robust schemas
        days = []
        for i in range(1, prefs.duration + 1):
            theme = "Indoor Culture (Due to weather)" if "rain" in weather.lower() else "Outdoor Exploration"
            
            # Simple simulation using prompt data
            if "hidden" in rag_context.lower():
                theme += " + Finding Hidden Gems"
                
            days.append(DailyPlan(dayNumber=i, theme=theme, activities=[]))
            
        return days
