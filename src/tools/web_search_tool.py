import os
from langchain_community.tools.tavily_search import TavilySearchResults
from src.utils.config import settings
from src.utils.retry import retry_with_backoff

# Ensure the key is available for the underlying library as well
# even though we validate it in config
if settings.TAVILY_API_KEY:
    os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY

class WebSearchTool:
    """Wrapper around Tavily search specifically tailored for travel research."""
    
    def __init__(self, max_results: int = 5):
        self.search_tool = TavilySearchResults(max_results=max_results)
        
    @retry_with_backoff(retries=3)
    def search(self, query: str) -> str:
        """
        Executes a search using Tavily.
        Returns a stringified version of the search results suitable for LLM consumption.
        """
        return self.search_tool.invoke({"query": query})

    @retry_with_backoff(retries=3)
    def search_destinations(self, query: str) -> str:
        """Optimized search for general destination overviews."""
        enhanced_query = f"{query} travel guide tourism overview best time to visit"
        return self.search(enhanced_query)
        
    @retry_with_backoff(retries=3)
    def search_attractions(self, location: str) -> str:
        """Optimized search for specific attractions and their details."""
        enhanced_query = f"top attractions things to do in {location} reviews opening hours"
        return self.search(enhanced_query)
        
    @retry_with_backoff(retries=3)
    def search_restaurants(self, location: str, food_type: str = "") -> str:
        """Optimized search for food and dining."""
        food_query = food_type if food_type else "best restaurants local food"
        enhanced_query = f"{food_query} in {location} dining recommendations"
        return self.search(enhanced_query)

# Global instance for easy import
web_search = WebSearchTool()
