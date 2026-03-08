import time
from typing import Dict, Any

def get_weather_forecast(destination: str, days: int) -> str:
    """
    Mock external API tool that simulates hitting OpenWeather API.
    In a real app, uses src.utils.config.settings.OPENWEATHER_API_KEY
    """
    # Simulate network latency
    time.sleep(0.5)
    
    # Simple semantic mock
    if "london" in destination.lower() or "seattle" in destination.lower():
        return "Rainy and overcast, 15°C. Advise indoor activities."
    elif "bali" in destination.lower() or "maldives" in destination.lower():
        return "Sunny and clear, 30°C. Perfect for beaches."
    else:
        return "Mild and pleasant, 22°C. Good for walking tours."

def get_flight_estimates(destination: str) -> Dict[str, Any]:
    """
    Mock external tool for grabbing flight metadata.
    """
    time.sleep(0.5)
    return {
        "status": "success",
        "avg_price_usd": 450,
        "recommended_airlines": ["Delta", "Emirates", "Local Carrier"]
    }
