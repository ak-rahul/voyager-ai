# Troubleshooting Guide 🚑

## Common Issues

### 1. Missing API Keys
**Error:** `ValueError: GROQ_API_KEY must be set in the environment.`
**Fix:** Ensure you have created a `.env` file in the root directory and populated it with real keys for Groq and Tavily.

### 2. Streamlit Port Already in Use
**Error:** `OSError: [Errno 98] Address already in use`
**Fix:** Kill the existing process grabbing port 8501. 
On Linux/Mac: `lsof -i :8501`, then `kill -9 <PID>`.
Or run Streamlit on a different port: `streamlit run app.py --server.port 8502`.

### 3. Agent Hallucinations
**Observation:** The agent suggests an impossible travel time (e.g., driving from NY to Paris).
**Fix:** The ReviewerCritic is designed to catch this. If it slips through, try lowering the `temperature` in `src/agents/base_agent.py` to 0.1 for more deterministic results.

### 4. Search Tool Rate Limits
**Error:** HTTP 429 Too Many Requests from Tavily.
**Fix:** Our system implements exponential backoff in `src/utils/retry.py`. If it completely fails, wait a few minutes before retrying, or check your Tavily tier.
