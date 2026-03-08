import pytest
from unittest.mock import patch, MagicMock, ANY
from pydantic import BaseModel, Field

class MockSchema(BaseModel):
    test_field: str = Field(description="A test field")

@patch('src.agents.base_agent.ChatGroq')
def test_base_agent_initialization(mock_chatgroq):
    from src.agents.base_agent import BaseAgent
    
    agent = BaseAgent(name="TestAgent", model_name="test-model", temperature=0.5)
    
    assert agent.name == "TestAgent"
    mock_chatgroq.assert_called_once_with(
        temperature=0.5,
        model_name="test-model",
        api_key=ANY, # Checks it accesses settings properly
        max_tokens=4096
    )

@patch('src.agents.base_agent.ChatGroq')
def test_base_agent_create_chain(mock_chatgroq):
    from src.agents.base_agent import BaseAgent
    agent = BaseAgent(name="TestAgent")
    
    # Create chain with schema
    chain = agent.create_chain(system_prompt="Test prompt", output_schema=MockSchema)
    assert chain is not None

def test_base_agent_invoke():
    from src.agents.base_agent import BaseAgent
    
    # Mocking out the LLM to prevent actual API calls during CI
    agent = BaseAgent(name="TestAgent")
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = MockSchema(test_field="Success")
    
    result = agent.invoke(chain=mock_chain, inputs={"human_input": "Hello"})
    
    assert result.test_field == "Success"
    mock_chain.invoke.assert_called_once_with({"human_input": "Hello"})
