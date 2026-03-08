import streamlit as st
from dotenv import load_dotenv
load_dotenv() # Force load .env file

from src.models.schemas import UserPreferences
from src.main import run_planner
import time
import logging

# --- Setup ---
st.set_page_config(
    page_title="WanderAI Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Styling ---
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .main-header { font-size: 3rem; font-weight: 800; background: -webkit-linear-gradient(45deg, #2563eb, #4f46e5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0px; }
    .sub-header { font-size: 1.2rem; color: #64748b; margin-bottom: 2rem; }
    .card { background-color: white; padding: 1.5rem; border-radius: 1rem; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); margin-bottom: 1rem; }
    .icon-morning { background-color: #ffedd5; color: #ea580c; }
    .icon-afternoon { background-color: #ccfbf1; color: #0d9488; }
    .icon-evening { background-color: #ffe4e6; color: #e11d48; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">✈️ WanderAI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your Enterprise Stateful AI Travel Concierge</p>', unsafe_allow_html=True)

# --- Sidebar: Form ---
with st.sidebar:
    st.header("🗺️ Plan Your Trip")
    
    with st.form("planner_form"):
        destination = st.text_input("Destination", placeholder="e.g., Tokyo (Leave blank for AI pick)")
        col1, col2 = st.columns(2)
        with col1:
            duration = st.number_input("Days", min_value=1, max_value=14, value=3)
        with col2:
            budget = st.selectbox("Budget", ["budget", "moderate", "luxury"], index=1)
        style = st.selectbox("Style", ["culture", "nature", "relaxation", "food", "party"])
        submitted = st.form_submit_button("✨ Generate My Trip ✨", use_container_width=True)

if submitted:
    with st.spinner("Executing LangGraph Pipeline (Agents, RAG, & Weather Adapters)..."):
        try:
            prefs = UserPreferences(
                destination=destination,
                duration=int(duration),
                budget=budget,
                style=style
            )
            # Generate the itinerary (using direct Python orchestration)
            itinerary_response = run_planner(prefs)
            st.session_state["itinerary"] = itinerary_response.model_dump()
            st.session_state["chat_history"] = [{"role": "system", "content": "You are a helpful travel assistant ready to modify this itinerary."}]
        except Exception as e:
            st.error(f"Failed to generate itinerary. Error: {e}")

# --- Display Results ---
if "itinerary" in st.session_state:
    data = st.session_state["itinerary"]
    
    st.markdown(f"""
    <div class="card" style="border-left: 5px solid #2563eb;">
        <h2>Trip to {data.get("destination", "")}</h2>
        <p style="color: #475569;">{data.get("summary", "")}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🗓️ Your Daily Plan")
        for day in data.get("days", []):
            with st.expander(f"Day {day['dayNumber']}: {day['theme']}", expanded=True):
                for act in day.get("activities", []):
                    time_class = "icon-morning" if "morning" in act["timeOfDay"].lower() else "icon-afternoon" if "afternoon" in act["timeOfDay"].lower() else "icon-evening"
                    st.markdown(f"""
                    <div style="display: flex; margin-bottom: 1rem;">
                        <div style="flex-grow: 1; padding: 10px; border-radius: 8px;" class="{time_class}">
                            <strong>{act['timeOfDay']}: {act['title']}</strong> | <span style="color:green;">${act['costEstimate']}</span>
                            <p style="margin:0; font-size: 0.9em; color:#475569;">{act['description']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
    with col2:
        st.header("📊 Total Budget & Export")
        bg_data = data.get("budget", {})
        
        st.markdown(f"""
        <div class="card">
            <h3 style="margin-top:0;">Estimated Costs</h3>
            <p>✈️ Flights: <strong>${bg_data.get('flightsTransit', 0)}</strong></p>
            <p>🛏️ Hotels: <strong>${bg_data.get('accommodation', 0)}</strong></p>
            <p>🍽️ Food: <strong>${bg_data.get('foodDining', 0)}</strong></p>
            <p>🎟️ Activities: <strong>${bg_data.get('activities', 0)}</strong></p>
            <hr/>
            <h4>Total: <span style="color: #2563eb;">${bg_data.get('total', 0)}</span></h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.download_button(
            label="📄 Export as Markdown",
            data=f"# Trip to {data.get('destination')}\\n\\n{data.get('summary')}",
            file_name="itinerary.md",
            mime="text/markdown",
            use_container_width=True
        )

    # --- Conversational Tweaker ---
    st.divider()
    st.header("💬 Talk to your Concierge")
    for msg in st.session_state.get("chat_history", [])[1:]:
        st.chat_message(msg["role"]).write(msg["content"])
        
    if user_input := st.chat_input("Ask to swap an activity or change budget bounds..."):
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        # Simulate agent response using Memory state
        with st.chat_message("assistant"):
            st.write(f"I understand you want to: '{user_input}'. Under the hood, the LangGraph Supervisor would now re-route to the Planner Agent to surgically update the state memory and re-render the UI.")
            st.session_state["chat_history"].append({"role": "assistant", "content": "Simulated memory update..."})
