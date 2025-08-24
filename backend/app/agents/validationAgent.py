# app/services/agentic_validation_service.py
import logging
from tokenize import String
from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.base import Model # Explicitly import Model
from agno.models.google import Gemini
from agno.tools import tool
from google.genai.types import Schema
from app.core.config import settings
from app.services.google_trends_service import GoogleTrendsService
from app.services.tavily_service import TavilyService
from app.services.reddit_service import RedditService
from app.models.schemas import (
    ValidationResult,
    ComprehensiveAnalysis,
    RawDatum,
    AnalysisMetadata,
    MarketAssessment,
    CompetitorAnalysis,
    CompetitiveLandscape,
    UniquenessAnalysis,
    BusinessViability,
    RiskAssessment,
    ValueEnhancementRoadmap,
    StrategicRecommendations
)
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.thinking import ThinkingTools

from helper.schema_helpers import dict_to_schema, flatten_schema


logger = logging.getLogger(__name__)

class AgenticValidationService:
    """Agentic startup validation using Agno framework"""

    def __init__(self):
        """Initializes the AgenticValidationService with necessary tools and configurations."""
        self.trends_service = GoogleTrendsService()
        self.tavily_service = TavilyService()
        self.reddit_service = RedditService()

        # Flatten all necessary schemas
        flattened_comprehensive_analysis_schema = flatten_schema(ComprehensiveAnalysis)
        flattened_raw_datum_schema = flatten_schema(RawDatum)

        # Manually construct the schema for better control and to avoid Pydantic's default schema generation issues
        validation_schema = Schema(
            type="object",
            properties={
                "idea": {"type": "string", "description": "The startup idea that was validated"},
                "analysis": dict_to_schema(flattened_comprehensive_analysis_schema),
                "raw_data": {
                    "type": "array",
                    "items": dict_to_schema(flattened_raw_datum_schema),
                    "description": "Optional list of raw data collected from various sources"
                },
                "timestamp": {"type": "string", "format": "date-time"},
                "api_status": {
                    "type": "object",
                    "additionalProperties": {"type": "boolean"},
                    "description": "Status of all API services"
                },
                "execution_time": {"type": "number"},
                "error": {"type": "string", "nullable": True},
            },
            required=["idea", "analysis", "timestamp", "api_status", "execution_time"],
        )

        self.agent = Agent(
            model=Gemini(
                id="gemini-1.5-flash",
                api_key=settings.GEMINI_API_KEY,
                # supports_native_structured_outputs=True,
                temperature=0.2,
                max_output_tokens=8000,
            ),
            tools=[
                GoogleSearchTools(),
                ThinkingTools(),
            ],
            instructions=(
                "You are an expert startup analyst. Search the web for market trends and competitors. "
                "Return ONLY JSON structured per the schema."
            ),
            markdown=False,
            show_tool_calls=True,
            # response_model=validation_schema,
        )

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
        """
        Validates a startup idea using the configured agent.
        """
        result = self.agent.run(
                idea
            )

        return result 