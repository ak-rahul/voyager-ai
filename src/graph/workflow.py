import logging
from langgraph.graph import StateGraph, END
from src.graph.state import AgentState
from src.agents.base_agent import DestinationAgent, PlannerAgent
from src.tools.weather_tool import get_weather_forecast
from src.tools.rag_retriever import retrieve_travel_blogs
from src.models.schemas import ItineraryResponse, BudgetBreakdown, DailyPlan

logger = logging.getLogger(__name__)

# --- Graph Nodes ---
def node_destination(state: AgentState) -> dict:
    """Determine the optimal destination if blank, else passthrough."""
    logger.info("Executing DesignationNode")
    dest_agent = DestinationAgent()
    destination = dest_agent.process(state["user_prefs"])
    return {"current_destination": destination}

def node_context_builder(state: AgentState) -> dict:
    """Fetches real-time weather and localized Hidden Gems via RAG."""
    logger.info("Executing ContextBuilderNode (Weather & RAG)")
    dest = state["current_destination"]
    prefs = state["user_prefs"]
    
    # Tool execution
    weather = get_weather_forecast(dest, prefs.duration)
    rag_docs = retrieve_travel_blogs(query=f"best local secrets in {dest}")
    rag_context = "\\n".join([doc.page_content for doc in rag_docs])
    
    return {
        "weather_forecast": weather,
        "research_context": rag_context
    }

def node_planner(state: AgentState) -> dict:
    """Uses LLM Planner Agent to generate daily themes."""
    logger.info("Executing PlannerNode")
    planner = PlannerAgent()
    
    days = planner.process(
        state["current_destination"], 
        state["user_prefs"], 
        state["weather_forecast"], 
        state["research_context"]
    )
    
    # Mock generation of final itinerary to meet robust schema requirement
    budget_mock = BudgetBreakdown(
        flightsTransit=600,
        accommodation=state["user_prefs"].duration * 100,
        foodDining=state["user_prefs"].duration * 60,
        activities=state["user_prefs"].duration * 40,
        total=600 + (state["user_prefs"].duration * 200)
    )
    
    summary = f"A beautiful {state['user_prefs'].duration}-day {state['user_prefs'].style} journey in {state['current_destination']} tailored to a {state['user_prefs'].budget} budget. Includes RAG insights and weather adaptations!"

    final_itinerary = ItineraryResponse(
        destination=state["current_destination"],
        summary=summary,
        days=days,
        budget=budget_mock
    )
    
    return {"final_itinerary": final_itinerary}

# --- Graph Compilation ---
def create_workflow() -> StateGraph:
    """Builds and compiles the Master LangGraph."""
    logger.info("Compiling Enterprise Master Workflow DAG")
    workflow = StateGraph(AgentState)
    
    workflow.add_node("DestinationAgent", node_destination)
    workflow.add_node("ContextBuilder", node_context_builder)
    workflow.add_node("PlannerAgent", node_planner)
    
    # Define Edges (Directed Acyclic Graph logic)
    workflow.set_entry_point("DestinationAgent")
    workflow.add_edge("DestinationAgent", "ContextBuilder")
    workflow.add_edge("ContextBuilder", "PlannerAgent")
    workflow.add_edge("PlannerAgent", END)
    
    return workflow.compile()
