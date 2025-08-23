# app/services/agentic_validation_service.py
import logging
from typing import Dict, Any, Optional
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools import tool
from google.genai.types import Schema
from app.core.config import settings
from app.services.google_trends_service import GoogleTrendsService
from app.services.tavily_service import TavilyService
from app.services.reddit_service import RedditService
from app.services.output_validators import OutputValidator
from app.models.schemas import  ValidationResult
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.thinking import ThinkingTools


# from app.models.schemas import ComprehensiveAnalysis

logger = logging.getLogger(__name__)

class AgenticValidationService:
    """Agentic startup validation using Agno framework"""


    def __init__(self):
        self.trends_service = GoogleTrendsService()
        self.tavily_service = TavilyService()
        self.reddit_service = RedditService()

        # Initialize Agno Agent
        validation_schema = ValidationResult.model_json_schema()

        self.agent = Agent(
            model=Gemini(
                id="gemini-1.5-flash",
                api_key=settings.GEMINI_API_KEY,
                supports_native_structured_outputs=True,
                temperature=0.2,
                max_output_tokens=8000,
            ),
            tools=[GoogleSearchTools(), ThinkingTools()],
            instructions=(
                "You are an expert startup analyst. Search the web for market trends and competitors. "
                "Return ONLY JSON structured per the schema:\n"
                f"{validation_schema}"
            ),
            markdown=False,
            show_tool_calls=True,
            response_model=ValidationResult,
        )

    def get_services_status(self) -> Dict[str, Any]:
        """Get service status for API response"""
        return {
            "gemini": self.trends_service.is_available,
            "tavily": self.tavily_service.is_available,
            "google_trends": self.trends_service.is_available,
            "reddit": self.reddit_service.is_available,
            "agentic": True,  # New flag indicating agentic mode
            "framework": "Agno"
        }

    @tool
    def get_google_trends(self, idea: str) -> Dict[str, Any]:
        """Fetch Google Trends data for a startup idea. Returns interest score, direction, and velocity."""
        return self.trends_service.get_trends_with_fallback(idea)

    @tool
    def search_competitors(self, idea: str) -> Dict[str, Any]:
        """Search for competitors and similar companies for a startup idea."""
        return self.tavily_service.search_with_fallback(idea)

    @tool
    def get_reddit_sentiment(self, idea: str) -> Dict[str, Any]:
        """Get recent Reddit posts and community sentiment about a topic."""
        return self.reddit_service.get_activity_with_fallback(idea)

    async def validate_idea(self, idea: str) -> Dict[str, Any]:
        """Run agentic validation and return structured results"""
        try:
            logger.info(f"Starting agentic validation for idea: {idea}")
            
            # Run the agent
            response = await self.agent.arun(
                f"Comprehensively validate this startup idea: '{idea}'. "
                "Provide a detailed analysis in the required JSON format."
            )
            
            # Extract and validate the JSON response
            # validated_data = self._validate_and_parse_response(response.content, idea)
            
            logger.info("Agentic validation completed successfully")
            return {
                "success": True,
                "analysis": response,
                "raw_response": response.content,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Agentic validation failed: {str(e)}")
            return {
                "success": False,
                "analysis": None,
                "raw_response": None,
                "error": str(e)
            }

    # def _validate_and_parse_response(self, response_text: str, idea: str) -> ComprehensiveAnalysis:
    #     """Validate the agent's response against our schema"""
    #     is_valid, parsed_data, error_message = OutputValidator.validate_comprehensive_analysis(response_text)
        
    #     if not is_valid:
    #         logger.warning(f"Agent response validation failed, attempting to fix: {error_message}")
    #         # Try to extract JSON from the response
    #         parsed_data = OutputValidator.extract_json_from_response(response_text)
    #         if not parsed_data:
    #             raise ValueError(f"Failed to validate or extract JSON from agent response: {error_message}")
        
    #     # Convert to Pydantic model for consistency
    #     return ComprehensiveAnalysis(**parsed_data)