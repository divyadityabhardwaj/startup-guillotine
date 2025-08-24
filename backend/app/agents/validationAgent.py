from agno.agent import Agent
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.thinking import ThinkingTools
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from agno.models.google import Gemini
from app.core.config import settings
import json
import re
from datetime import datetime

from app.models.schemas import ValidationResult

class AgenticValidationService:
    def __init__(self):
        self.agent = Agent(
            model=Gemini(
                id="gemini-1.5-flash",
                api_key=settings.GEMINI_API_KEY,
                temperature=0.2,
                max_output_tokens=8000,
            ),
            tools=[
                GoogleSearchTools(),
                ThinkingTools(),
            ],
            instructions=(
                "You are an expert startup analyst. Search the web for market trends and competitors. "
                "Analyze the startup idea comprehensively and return a JSON object with these exact fields:\n"
                "\n## BASIC INFO:\n"
                "- idea: the original idea\n"
                "\n## MARKET ASSESSMENT:\n"
                "- market_score: number 0-100 (overall market opportunity score)\n"
                "- market_verdict: string (Strong/Promising/Moderate/Weak/High Risk)\n"
                "- market_saturation: string (Low/Medium/High/Very High)\n"
                "- entry_barriers: string (Low/Medium/High/Very High)\n"
                "- market_timing: string (Early/Optimal/Late/Oversaturated)\n"
                "- market_trends: array of market trends\n"
                "- market_size: string describing market size (e.g., $10B, Large, Small)\n"
                "- market_growth: string (High/Medium/Low/Stagnant)\n"
                "\n## COMPETITIVE LANDSCAPE:\n"
                "- competitors: array of competitor names\n"
                "- competitive_advantage: string describing unique advantages\n"
                "- market_gaps: array of underserved market segments or needs\n"
                "- competitor_strength: string (Weak/Moderate/Strong/Dominant)\n"
                "\n## UNIQUENESS ANALYSIS:\n"
                "- novelty_score: number 0.0-10.0 (novelty score out of 10)\n"
                "- differentiation_factors: array of specific differentiation factors\n"
                "- innovation_level: string (Breakthrough/Incremental/Iterative/Minimal)\n"
                "- unique_value_proposition: string (clear unique value proposition)\n"
                "- copycat_risk: string (Low/Medium/High/Very High)\n"
                "\n## BUSINESS VIABILITY:\n"
                "- feasibility: string (High/Medium/Low/Very Low)\n"
                "- customer_value_proposition: string (clear problem-solution fit description)\n"
                "- target_market_size: string (size of target market)\n"
                "- monetization_potential: string (High/Medium/Low/Poor)\n"
                "- pricing_strategy: string (recommended pricing strategy)\n"
                "- customer_acquisition_difficulty: string (Easy/Moderate/Difficult/Very Difficult)\n"
                "\n## RISK ASSESSMENT:\n"
                "- risks: array of potential risks\n"
                "- market_risks: array of identified market risks\n"
                "- execution_risks: array of technical and execution risks\n"
                "- competitive_risks: array of competitive landscape risks\n"
                "- mitigation_strategies: array of strategies to mitigate identified risks\n"
                "- risk_level: string (Low/Medium/High/Very High)\n"
                "\n## STRATEGIC RECOMMENDATIONS:\n"
                "- market_entry_strategy: string (recommended market entry approach)\n"
                "- success_factors: array of key factors for success\n"
                "- next_steps: array of immediate next steps to take\n"
                "- timeline_recommendation: string (recommended timeline for execution)\n"
                "\n## DATA QUALITY:\n"
                "- data_sources_used: array of data sources utilized\n"
                "- analysis_depth: string (Surface/Moderate/Deep/Comprehensive)\n"
                "\n- error: null or error message\n\n"
                "Return ONLY valid JSON, no other text. All fields must be present with appropriate values."
            ),
            markdown=False,
            show_tool_calls=True,
            response_model=ValidationResult,
        )

    async def validate_idea(self, idea: str):
        """Validates a startup idea using the configured agent."""
        try:
            result = self.agent.run(idea)
            return result
        except Exception as e:
            # Return a validation result with error
            return ValidationResult(
                idea=idea,
                market_score=0,
                market_verdict="",
                market_saturation="",
                entry_barriers="",
                market_timing="",
                market_trends=[],
                market_size="",
                market_growth="",
                competitors=[],
                competitive_advantage="",
                market_gaps=[],
                competitor_strength="",
                novelty_score=0.0,
                differentiation_factors=[],
                innovation_level="",
                unique_value_proposition="",
                copycat_risk="",
                feasibility="",
                customer_value_proposition="",
                target_market_size="",
                monetization_potential="",
                pricing_strategy="",
                customer_acquisition_difficulty="",
                risks=[],
                market_risks=[],
                execution_risks=[],
                competitive_risks=[],
                mitigation_strategies=[],
                risk_level="",
                market_entry_strategy="",
                success_factors=[],
                next_steps=[],
                timeline_recommendation="",
                data_sources_used=[],
                analysis_depth="",
                error=f"Validation failed: {str(e)}"
            )