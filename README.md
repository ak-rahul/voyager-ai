# Voyager AI 🌍✈️🤖

An Autonomous, Stateful, Multi-Agent Travel Planning Platform built with LongChain, LangGraph, and Groq.

Voyager AI goes beyond standard "chat wrapper" travel planners by simulating an entire agency of experts working together to research, build, critique, and finalize an itinerary.

## 🌟 Architecture Overview

This project implements an advanced **Plan-and-Solve with Actor-Critic** architecture using a stateful graph engine (LangGraph). The system consists of five distinct AI agents:

1. **Destination Analyzer:** Acts as the researcher. Gathers real-time intelligence about the destination using web search tools, identifying attractions, travel risks, and optimal visiting months.
2. **Metadata Recommender:** Acts as the categorizer. Determines the "vibe" and complexity of the trip based on user inputs.
3. **Content Improver (Actor):** Generates the actual day-by-day itinerary draft. It must adapt to restrictive feedback from the Critic.
4. **Fact Checker:** Scours the live internet (via Tavily Search) to cross-reference the draft itinerary against real-world data, ensuring venues actually exist, are open, and match the budget.
5. **Reviewer Critic:** Evaluates the draft itinerary directly against the Fact Checker's live intelligence and the user's constraints using a strict point-deduction rubric. If it scores below a 8.0/10, it forces the Content Improver to rewrite the draft. Includes graceful UI exhaustion warnings if impossible constraints are provided.

```mermaid
graph TD
    A[Input: User Preferences] --> B[Destination Analyzer]
    B --> C[Metadata Recommender]
    C --> D[Content Improver Drafts Itinerary]
    D --> E[Fact Checker]
    E --> F[Reviewer Critic]
    F -- Score < 8.0 & Revisions < 3 --> D
    F -- Score >= 8.0 --> G[Final Itinerary]
```

## 🛠️ Technology Stack

* **Core Engine:** Python 3.11+, LangChain, LangGraph
* **LLM Provider:** Groq (Llama 3 70B & 8B for ultra-fast, cheap inference necessary for multi-agent loops)
* **Tools:** Tavily (Optimized Agentic Web Search)
* **Frontend:** Streamlit (Custom Premium Glassmorphism UI)
* **Validation:** Pydantic & Pydantic-Settings (Strict schema and environment variable enforcement)
* **CI/CD:** GitHub Actions (Automated pytest & flake8)

## 🗂️ Project Structure

```text
├── .github/workflows/ci.yml # Automated CI pipeline
├── src/
│   ├── agents/              # The 5 specialized LLM agents
│   ├── graph/               # LangGraph state machine and workflow definition
│   ├── tools/               # External tool integrations (Search, Markdown)
│   └── utils/               # Enterprise resilience (Circuit Breaker, Retry, Logger)
├── tests/                   # Pytest suite
└── app.py                   # Streamlit UI
```

## 🚀 Getting Started

### Prerequisites

You will need API keys for Groq and Tavily.
1. [Groq API Key](https://console.groq.com)
2. [Tavily API Key](https://tavily.com/)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/voyager-ai.git
cd voyager-ai

# Set up virtual environment
python -m venv venv
source venv/bin/activate # (Or .\venv\Scripts\activate on Windows)

# Install dependencies
pip install -r requirements.txt
```

### Configuration
Create a `.env` file in the root directory and add your keys:
```env
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
```

### Running the App
```bash
python -m streamlit run app.py
```

## 🧠 Why This Project Stands Out (For Recruiters/Hiring Managers)
* **Stateful Execution:** Uses a state graph instead of standard chain execution, allowing for infinite loops, internal memory, and human-in-the-loop capabilities.
* **Resilient Tooling & Architecture:** Implements custom `retry` and `circuit_breaker` decorators to handle volatile external APIs gracefully. Employs lazy LLM instantiation to protect the application from environment-driven crash loops.
* **Adversarial Multi-Agent Validation:** Deeply decouples the "Actor" (doing the work) from the "Critic" (evaluating the work). The Critic leverages live internet data from the Fact Checker to ruthlessly strip points for LLM hallucinations, ensuring structural and geographical accuracy.
