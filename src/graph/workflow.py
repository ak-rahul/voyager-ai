from langgraph.graph import StateGraph, END
from typing import Dict, Any

from src.graph.state import AgentState
from src.agents.destination_analyzer import destination_analyzer
from src.agents.metadata_recommender import metadata_recommender
from src.agents.content_improver import content_improver
from src.agents.reviewer_critic import reviewer_critic
from src.agents.fact_checker import fact_checker
from src.utils.config import setup_logger

logger = setup_logger(__name__)

def analyze_destination_node(state: AgentState) -> Dict[str, Any]:
    return destination_analyzer.run(state)

def recommend_metadata_node(state: AgentState) -> Dict[str, Any]:
    return metadata_recommender.run(state)

def generate_draft_node(state: AgentState) -> Dict[str, Any]:
    # Increment revision count
    rev_count = state.get("revision_count", 0) + 1
    result = content_improver.run(state)
    result["revision_count"] = rev_count
    return result

def fact_check_node(state: AgentState) -> Dict[str, Any]:
    return fact_checker.run(state)

def critique_node(state: AgentState) -> Dict[str, Any]:
    return reviewer_critic.run(state)

def route_after_critique(state: AgentState) -> str:
    """
    Decides whether the itinerary is good enough or needs revision.
    """
    score = state.get("critic_score", 0.0)
    rev_count = state.get("revision_count", 0)
    
    logger.info(f"Routing logic: Score={score}, Revision={rev_count}")
    
    if score >= 8.0 or rev_count >= 3:
        # High score, or we've hit our max retries
        return "finalize"
    else:
        # Needs another pass by the Content Improver
        return "generate_draft"

def finalize_node(state: AgentState) -> Dict[str, Any]:
    """
    Finalizes the state output.
    """
    draft = state.get("draft_itinerary")
    return {"final_itinerary": draft}

def build_workflow() -> StateGraph:
    """Builds and compiles the Multi-Agent LangGraph workflow."""
    logger.info("Building workflow graph...")
    
    builder = StateGraph(AgentState)
    
    # Add Nodes
    builder.add_node("analyze_destination", analyze_destination_node)
    builder.add_node("recommend_metadata", recommend_metadata_node)
    builder.add_node("generate_draft", generate_draft_node)
    builder.add_node("fact_check", fact_check_node)
    builder.add_node("critique", critique_node)
    builder.add_node("finalize", finalize_node)
    
    # Define Edges (The standard path)
    builder.set_entry_point("analyze_destination")
    builder.add_edge("analyze_destination", "recommend_metadata")
    builder.add_edge("recommend_metadata", "generate_draft")
    builder.add_edge("generate_draft", "fact_check")
    builder.add_edge("fact_check", "critique")
    
    # Define Conditional Branches
    builder.add_conditional_edges(
        "critique",
        route_after_critique,
        {
            "generate_draft": "generate_draft",
            "finalize": "finalize"
        }
    )
    
    builder.add_edge("finalize", END)
    
    # Compile the graph
    graph = builder.compile()
    logger.info("Workflow successfully compiled.")
    return graph

# Expose compiled graph
workflow = build_workflow()

# Alias for main.py
create_workflow = build_workflow
