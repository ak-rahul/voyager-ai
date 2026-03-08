import streamlit as st
import time
from typing import Dict, Any

from src.models.schemas import UserPreferences
from src.graph.state import AgentState
from src.graph.workflow import workflow
from src.utils.config import setup_logger

logger = setup_logger(__name__)

st.set_page_config(
    page_title="Voyager AI | Smart Travel Agent",
    page_icon="🌍",
    layout="wide"
)

# Initialize Session State
if "itinerary" not in st.session_state:
    st.session_state.itinerary = None
if "logs" not in st.session_state:
    st.session_state.logs = []

def add_log(message: str):
    """Helper to keep track of agent thought process in UI."""
    st.session_state.logs.append(f"{time.strftime('%H:%M:%S')} - {message}")

st.title("🌍 Voyager AI Platform")
st.subheader("Your Autonomous Team of Travel Agents")

with st.sidebar:
    st.header("Trip Details")
    
    with st.form("trip_form"):
        destination = st.text_input("Destination", placeholder="e.g., Tokyo, Japan")
        duration = st.slider("Duration (Days)", min_value=1, max_value=14, value=5)
        budget = st.selectbox("Budget Level", ["budget", "moderate", "luxury"])
        style = st.selectbox("Travel Style", ["culture", "nature", "relaxation", "food", "party", "adventure"])
        
        submitted = st.form_submit_button("Plan My Trip")

if submitted and destination:
    st.session_state.logs = [] # Reset logs
    st.session_state.itinerary = None
    
    prefs = UserPreferences(
        destination=destination,
        duration=duration,
        budget=budget,
        style=style
    )
    
    initial_state: AgentState = {
        "user_prefs": prefs,
        "current_destination": destination,
        "destination_profile": "",
        "metadata_tags": [],
        "fact_check_results": [],
        "critic_feedback": "",
        "critic_score": 0.0,
        "revision_count": 0,
        "draft_itinerary": None,
        "final_itinerary": None
    }

    # Execute Graph Workflow
    with st.status("Agents are working...", expanded=True) as status:
        try:
            # LangGraph provides a generator for streaming execution steps
            for event in workflow.stream(initial_state):
                for node_name, state_update in event.items():
                    log_msg = f"Completed node: **{node_name}**"
                    if node_name == "critique":
                        score = state_update.get('critic_score', 0)
                        log_msg += f" (Score: {score}/10)"
                    
                    st.write(log_msg)
                    add_log(log_msg)
                    
                    # Persist the final state update to pull out the itinerary later
                    final_result = state_update
            
            st.session_state.itinerary = final_result.get("final_itinerary")
            status.update(label="Trip Planning Complete!", state="complete", expanded=False)
            
        except Exception as e:
            logger.error(f"Workflow error: {e}")
            status.update(label=f"Error: {e}", state="error")

# Display Results
if st.session_state.itinerary:
    itinerary = st.session_state.itinerary
    
    st.success(f"Generated Itinerary for {itinerary.destination}")
    st.markdown(f"**Trip Summary:** {itinerary.summary}")
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.info("💰 Budget Estimate")
        st.metric("Flights & Transit", f"${itinerary.budget.flightsTransit}")
        st.metric("Accommodation", f"${itinerary.budget.accommodation}")
        st.metric("Food & Dining", f"${itinerary.budget.foodDining}")
        st.metric("Activities", f"${itinerary.budget.activities}")
        st.markdown(f"### Total: ${itinerary.budget.total}")
        
    with col1:
        st.subheader("📅 Intinerary Details")
        for day in itinerary.days:
            with st.expander(f"Day {day.dayNumber}: {day.theme}"):
                for activity in day.activities:
                    st.markdown(f"**{activity.timeOfDay}**: {activity.title}")
                    st.caption(f"_{activity.description}_ - Est: ${activity.costEstimate}")
