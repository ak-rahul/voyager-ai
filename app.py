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
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --accent-color: #f43f5e;
    --success-color: #10b981;
    --dark-bg: #0f172a;
    --dark-card: #1e293b;
    --dark-surface: #334155;
}

html, body, p, h1, h2, h3, h4, label, li, .stMarkdown {
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Backgrounds */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
    color: #e2e8f0 !important;
}

.main .block-container {
    max-width: 1400px !important;
    padding-top: 2rem !important;
}

[data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
}

[data-testid="stSidebar"] h2 {
    background: none !important;
    -webkit-text-fill-color: #f1f5f9 !important;
    color: #f1f5f9 !important;
    font-size: 1.5rem !important;
    border-bottom: 2px solid #6366f1 !important;
    margin-bottom: 1.5rem !important;
}

[data-testid="stSidebar"] .stForm {
    background: transparent !important;
    border: 1px solid rgba(148, 163, 184, 0.1) !important;
    padding: 1rem !important;
    box-shadow: none !important;
}

[data-testid="stSidebarNav"] {
    background: transparent !important;
}

.stSidebar [data-testid="stMarkdownContainer"] p {
    font-size: 0.9rem !important;
    color: #94a3b8 !important;
    line-height: 1.6 !important;
}

/* Typography Gradient */
h1 {
    margin-top: -30px !important;
    color: #f1f5f9 !important;
    font-weight: 900 !important;
    letter-spacing: -1.5px !important;
    text-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
}
.title-gradient {
    background: linear-gradient(135deg, #fff 0%, #a78bfa 50%, #8b5cf6 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}
h2 {
    color: #f1f5f9 !important;
    font-weight: 700 !important;
    border-bottom: 2px solid transparent !important;
    border-image: linear-gradient(90deg, #8b5cf6, #ec4899) 1 !important;
    padding-bottom: 0.5rem !important;
}
h3, h4 {
    color: #cbd5e1 !important;
}
p, span, div, label {
    color: #cbd5e1 !important;
}

/* Input Fields */
.stTextInput input, .stSelectbox div[data-baseweb="select"], .stSlider div {
    border-radius: 12px !important;
    border: 2px solid #334155 !important;
    background: #1e293b !important;
    color: #e2e8f0 !important;
    padding: 0.2rem 0.5rem !important;
    transition: all 0.3s ease !important;
}

.stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.3) !important;
    background: #334155 !important;
}

/* Selectbox Dropdowns */
ul[data-baseweb="menu"] {
    background: #1e293b !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: 8px !important;
}
ul[data-baseweb="menu"] li {
    color: #e2e8f0 !important;
}
ul[data-baseweb="menu"] li:hover {
    background: rgba(139, 92, 246, 0.2) !important;
}

/* Submit Primary Button */
.stButton>button {
    width: 100% !important;
    background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 50%, #ec4899 100%) !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.8rem 1.5rem !important;
    box-shadow: 0 10px 40px rgba(139, 92, 246, 0.5) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton>button * {
    color: white !important;
    font-weight: 600 !important;
}
.stButton>button::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: -100% !important;
    width: 100% !important;
    height: 100% !important;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent) !important;
    transition: left 0.5s !important;
}
.stButton>button:hover::before {
    left: 100% !important;
}
.stButton>button:hover {
    transform: translateY(-4px) scale(1.02) !important;
    box-shadow: 0 15px 50px rgba(139, 92, 246, 0.7) !important;
}
.stButton>button:active {
    transform: translateY(-2px) scale(0.98) !important;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background: #1e293b !important;
    border-radius: 18px !important;
    padding: 1.5rem !important;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4) !important;
    border: 1px solid rgba(148, 163, 184, 0.1) !important;
    border-top: 2px solid #6366f1 !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-5px) scale(1.02) !important;
    border-color: rgba(99, 102, 241, 0.4) !important;
}
[data-testid="metric-container"] > div > div > div > p {
    color: #94a3b8 !important; 
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] > div > div > div:nth-child(2) > span {
    color: #f1f5f9 !important;
    font-weight: 800 !important;
    font-size: 1.8rem !important;
}

/* Containers (Status, Form, etc.) */
[data-testid="stForm"] {
    background: #1e293b !important;
    border-radius: 20px !important;
    border: 1px solid rgba(148, 163, 184, 0.2) !important;
    padding: 1.5rem !important;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.3s ease !important;
}
[data-testid="stForm"]:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3) !important;
    border-color: rgba(139, 92, 246, 0.3) !important;
}
[data-testid="stStatusWidget"] [data-testid="stMarkdown"] p {
     color: #cbd5e1 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 8px !important;
}
.stTabs [data-baseweb="tab"] {
    background: #1e293b !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
    padding: 8px 16px !important;
    border-radius: 12px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(139, 92, 246, 0.2) !important;
    color: #a78bfa !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%) !important;
    color: white !important;
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5) !important;
}

/* Expanders */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
    color: #f1f5f9 !important;
    font-weight: 600 !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: 12px !important;
    margin-bottom: 0.5rem !important;
    transition: all 0.3s ease !important;
}
.streamlit-expanderHeader:hover {
    background: rgba(139, 92, 246, 0.1) !important;
    border-color: rgba(139, 92, 246, 0.5) !important;
}
.streamlit-expanderContent {
    background: #1e293b !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    border-top: none !important;
    border-bottom-left-radius: 12px !important;
    border-bottom-right-radius: 12px !important;
    color: #cbd5e1 !important;
    padding: 1rem !important;
}

/* Markdown styling inside components */
.stMarkdown hr, hr {
    border-bottom: 1px solid rgba(139, 92, 246, 0.2) !important;
}
.stMarkdown strong {
    color: #f1f5f9 !important;
    font-weight: 600;
}

/* Scrollbars */
::-webkit-scrollbar {
    width: 10px !important;
    height: 10px !important;
}
::-webkit-scrollbar-track {
    background: #1e293b !important;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%) !important;
    border-radius: 10px !important;
}

/* Animations */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

.stForm, .stButton, [data-testid="metric-container"], .streamlit-expanderHeader {
    animation: fadeInUp 0.6s ease-out !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "itinerary" not in st.session_state:
    st.session_state.itinerary = None
if "logs" not in st.session_state:
    st.session_state.logs = []

def add_log(message: str):
    """Helper to keep track of agent thought process in UI."""
    st.session_state.logs.append(f"{time.strftime('%H:%M:%S')} - {message}")

# --- HEADER SECTION ---
st.markdown("<h1 style='text-align: center;'>🌌 <span class='title-gradient'>Voyager AI</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.15rem; color: #94a3b8;'>Your Autonomous, Multi-Agent Travel Consultant Engine</p>", unsafe_allow_html=True)

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.markdown("<h2 style='border:none; border-bottom: 2px solid #6366f1; padding-bottom:10px;'>✈️ Trip Parameters</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size: 0.95rem; margin-bottom: 2rem;'>Specify your destination to generate a curated travel experience.</p>", unsafe_allow_html=True)
    
    with st.form("trip_form"):
        destination = st.text_input("Destination", placeholder="e.g., Tokyo, Japan")
        duration = st.slider("Duration (Days)", min_value=1, max_value=14, value=5)
        
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        budget = st.selectbox("Budget Tier", ["budget", "moderate", "luxury"])
        style = st.selectbox("Travel Style", ["culture", "nature", "relaxation", "food", "adventure"])
            
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Launch Agents 🚀")

# --- MAIN LOGIC EXECUTION ---
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

    st.markdown("### 🤖 Live Agent Telemetry")
    # Execute Graph Workflow within a stylized status container
    with st.status("Initializing LangGraph Engine...", expanded=True) as status:
        try:
            final_result = None
            # LangGraph provides a generator for streaming execution steps
            for event in workflow.stream(initial_state):
                for node_name, state_update in event.items():
                    
                    # Beautiful terminal-like log output
                    if node_name == "analyze_destination":
                        icon = "🔍"
                        desc = "Analyzing live destination data..."
                    elif node_name == "recommend_metadata":
                        icon = "🏷️"
                        desc = "Categorizing trip complexity..."
                    elif node_name == "generate_draft":
                        icon = "📝"
                        desc = "Content Improver drafting itinerary..."
                    elif node_name == "fact_check":
                        icon = "✅"
                        desc = "Verifying locations exist in reality..."
                    elif node_name == "critique":
                        icon = "⚖️"
                        score = state_update.get('critic_score', 0)
                        desc = f"Reviewing constraints. Score: **{score}/10**"
                    else:
                        icon = "⚡"
                        desc = f"Processing {node_name}..."

                    log_msg = f"{icon} **[{node_name.upper()}]** - {desc}"
                    st.markdown(log_msg)
                    add_log(log_msg)
                    
                    final_result = state_update
            
            if final_result is not None:
                st.session_state.itinerary = final_result.get("final_itinerary")
                st.session_state.final_score = final_result.get("critic_score", 10.0)
            status.update(label="Workflow Complete. Final Itinerary Ready!", state="complete", expanded=False)
            
        except Exception as e:
            logger.error(f"Workflow error: {e}")
            status.update(label=f"Critical Agent Failure: {e}", state="error")

st.markdown("<br>", unsafe_allow_html=True)

# --- DISPLAY RESULTS IN TABS ---
if st.session_state.itinerary:
    itinerary = st.session_state.itinerary
    score = st.session_state.get("final_score", 10.0)
    
    if score < 8.0:
        st.warning(f"⚠️ **Compromised Itinerary Warning:** The agents hit the maximum retries before passing the critic threshold (Final Critic Score: {score}/10). The itinerary below may contain minor unverified logistics or budget mismatches.")

    st.header(f"✨ Custom Itinerary: {itinerary.destination}")
    st.markdown(f"*{itinerary.summary}*")
    
    # Use tabs for a cleaner presentation
    tab_overview, tab_daily, tab_export = st.tabs(["💰 Budget & Overview", "📅 Daily Plan", "📤 Export"])
    
    with tab_overview:
        st.subheader("Financial Breakdown")
        
        # Display metrics in a beautiful row
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric(label="✈️ Flights/Transit", value=f"${itinerary.budget.flightsTransit}")
        with m2:
            st.metric(label="🏨 Accommodation", value=f"${itinerary.budget.accommodation}")
        with m3:
            st.metric(label="🍽️ Food & Dining", value=f"${itinerary.budget.foodDining}")
        with m4:
            st.metric(label="🎫 Activities", value=f"${itinerary.budget.activities}")
            
        st.divider()
        st.markdown(f"### 💵 Estimated Total: **${itinerary.budget.total}**")
        
        # Add metadata chips
        st.markdown(f"**Duration:** {duration} Days | **Tier:** {budget.title()} | **Style:** {style.title()}")

    with tab_daily:
        st.subheader("Your Day-by-Day Adventure")
        # Ensure we iterate correctly over the generated days
        for day in itinerary.days:
            with st.expander(f"Day {day.dayNumber} — {day.theme}", expanded=True if day.dayNumber==1 else False):
                for activity in day.activities:
                    # Layout each activity nicely with columns
                    c1, c2 = st.columns([1, 5])
                    with c1:
                        st.markdown(f"**{activity.timeOfDay}**<br>💰 Est: ${activity.costEstimate}", unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"#### {activity.title}")
                        st.markdown(f"{activity.description}")
                    st.markdown("---")
                    
    with tab_export:
        st.subheader("Download Your Plan")
        st.markdown("Take your itinerary offline. The agents have compiled this into a neat markdown file.")
        
        # Generate the raw markdown for download
        from src.tools.markdown_tool import markdown_tool
        
        md_content = f"# Voyager AI Itinerary: {itinerary.destination}\n\n"
        md_content += f"**Summary:** {itinerary.summary}\n\n"
        md_content += f"## Budget\n* Total: ${itinerary.budget.total}\n\n"
        for day in itinerary.days:
            md_content += f"### Day {day.dayNumber}: {day.theme}\n"
            for activity in day.activities:
                md_content += f"- **{activity.timeOfDay}** ({activity.title}): {activity.description} (${activity.costEstimate})\n"
        
        st.download_button(
            label="Download Markdown File",
            data=md_content,
            file_name=f"voyager_{destination.replace(' ', '_').lower()}.md",
            mime="text/markdown",
            use_container_width=True
        )
