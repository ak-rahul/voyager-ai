import pytest
from unittest.mock import patch, MagicMock
from src.tools.web_search_tool import WebSearchTool

@patch('src.tools.web_search_tool.TavilySearchResults')
def test_web_search_tool_initialization(mock_tavily):
    tool = WebSearchTool(max_results=3)
    mock_tavily.assert_called_once_with(max_results=3)
    assert tool.search_tool is not None

@patch('src.tools.web_search_tool.TavilySearchResults')
def test_search_destinations(mock_tavily_class):
    mock_instance = MagicMock()
    mock_instance.invoke.return_value = "Mocked Paris data"
    mock_tavily_class.return_value = mock_instance
    
    tool = WebSearchTool()
    result = tool.search_destinations("Paris")
    
    assert result == "Mocked Paris data"
    mock_instance.invoke.assert_called_once_with({"query": "Paris travel guide tourism overview best time to visit"})

@patch('src.tools.web_search_tool.TavilySearchResults')
def test_search_attractions(mock_tavily_class):
    mock_instance = MagicMock()
    mock_instance.invoke.return_value = "Mocked Eiffel Tower data"
    mock_tavily_class.return_value = mock_instance
    
    tool = WebSearchTool()
    result = tool.search_attractions("Paris")
    
    assert result == "Mocked Eiffel Tower data"
    mock_instance.invoke.assert_called_once_with({"query": "top attractions things to do in Paris reviews opening hours"})

@patch('src.tools.web_search_tool.TavilySearchResults')
def test_search_restaurants(mock_tavily_class):
    mock_instance = MagicMock()
    mock_instance.invoke.return_value = "Mocked Sushi data"
    mock_tavily_class.return_value = mock_instance
    
    tool = WebSearchTool()
    result = tool.search_restaurants("Tokyo", "Sushi")
    
    assert result == "Mocked Sushi data"
    mock_instance.invoke.assert_called_once_with({"query": "Sushi in Tokyo dining recommendations"})
