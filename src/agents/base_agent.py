from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableSerializable

from src.utils.config import settings
from src.utils.config import setup_logger
from src.utils.retry import retry_with_backoff

logger = setup_logger(__name__)

class BaseAgent:
    """
    Abstract base class for all Voyager AI agents.
    Handles LLM initialization, prompt rendering, and structured parsing execution.
    """
    
    def __init__(self, name: str, model_name: str = "llama-3.3-70b-versatile", temperature: float = 0.2):
        self.name = name
        self.model_name = model_name
        self.temperature = temperature

    @property
    def llm(self):
        if not hasattr(self, "_llm"):
            self._llm = ChatGroq(
                temperature=self.temperature,
                model_name=self.model_name,
                api_key=settings.GROQ_API_KEY,
                max_tokens=4096
            )
            logger.info(f"Initialized agent {self.name} with model {self.model_name}")
        return self._llm

    def create_chain(
        self, 
        system_prompt: str, 
        output_schema: Optional[Type[BaseModel]] = None
    ) -> RunnableSerializable:
        """
        Creates a LangChain runnable chain. If output_schema is provided, 
        it enforces structured Pydantic output.
        """
        if output_schema:
            parser = PydanticOutputParser(pydantic_object=output_schema)
            format_instructions = parser.get_format_instructions()
            
            messages = [
                ("system", system_prompt + "\n\n{format_instructions}"),
                ("human", "{human_input}")
            ]
            
            prompt = ChatPromptTemplate.from_messages(messages)
            prompt = prompt.partial(format_instructions=format_instructions)
            
            # Create typed chain
            chain = prompt | self.llm | parser
            return chain
            
        else:
            messages = [
                ("system", system_prompt),
                ("human", "{human_input}")
            ]
            prompt = ChatPromptTemplate.from_messages(messages)
            
            # Standard string output chain
            from langchain_core.output_parsers import StrOutputParser
            chain = prompt | self.llm | StrOutputParser()
            return chain

    @retry_with_backoff(retries=3)
    def invoke(
        self, 
        chain: RunnableSerializable, 
        inputs: Dict[str, Any]
    ) -> Any:
        """
        Executes the chain with retry logic for robust API calls.
        """
        try:
            logger.info(f"Agent {self.name} started thinking...")
            result = chain.invoke(inputs)
            logger.info(f"Agent {self.name} completed successfully.")
            return result
        except Exception as e:
            logger.error(f"Agent {self.name} encountered an error: {e}")
            raise
