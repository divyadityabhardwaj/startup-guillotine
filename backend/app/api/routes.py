# app/api/endpoints/analysis.py
import json
import logging
import time
from typing import Dict, Any
from fastapi import APIRouter, Body, HTTPException, BackgroundTasks
from datetime import datetime
import os
from datetime import datetime
import re

from app.core.config import settings
from app.agents.validationAgent import AgenticValidationService

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize the agentic service
agentic_service = AgenticValidationService()

@router.post("/validate")

async def validate_startup_idea(
    idea: str = Body(..., embed=True, description="The startup idea to validate"),
):
    """
    Validate a startup idea using AI agents.
    """
    start_time = time.time()

    if not idea or len(idea.strip()) < 10:
        raise HTTPException(status_code=400, detail="Idea must be at least 10 characters long")
    
    try:
        # Run the agent - returns ValidationResult
        response = await agentic_service.validate_idea(idea)
        validation_result = response.content
        # Build comprehensive response data
        response_data = {
            "idea": validation_result.idea,
            "analysis": {
                "analysis_metadata": {
                    "confidence_score": validation_result.confidence_socre,
                    "analysis_depth": validation_result.analysis_depth,
                    "data_sources_used": validation_result.data_sources_used,
                    "analysis_timestamp": datetime.utcnow().isoformat()
                },
                "market_assessment": {
                    "overall_score": validation_result.market_score,
                    "verdict": validation_result.market_verdict,
                    "market_saturation": validation_result.market_saturation,
                    "entry_barriers": validation_result.entry_barriers,
                    "market_timing": validation_result.market_timing,
                    "market_trends": validation_result.market_trends,
                    "market_size": validation_result.market_size,
                    "market_growth": validation_result.market_growth
                },
                "competitive_landscape": {
                    "existing_solutions": [{"name": comp} for comp in validation_result.competitors],
                    "market_gaps": validation_result.market_gaps,
                    "competitive_advantages": [validation_result.competitive_advantage],
                    "market_saturation_level": validation_result.market_saturation,
                    "competitor_strength": validation_result.competitor_strength
                },
                "uniqueness_analysis": {
                    "novelty_score": validation_result.novelty_score,
                    "differentiation_factors": validation_result.differentiation_factors,
                    "copycat_risk": validation_result.copycat_risk,
                    "innovation_level": validation_result.innovation_level,
                    "unique_value_proposition": validation_result.unique_value_proposition
                },
                "business_viability": {
                    "customer_value_proposition": validation_result.customer_value_proposition,
                    "target_market_size": validation_result.target_market_size,
                    "monetization_potential": validation_result.monetization_potential,
                    "pricing_strategy": validation_result.pricing_strategy,
                    "customer_acquisition_difficulty": validation_result.customer_acquisition_difficulty,
                    "feasibility": validation_result.feasibility
                },
                "risk_assessment": {
                    "market_risks": validation_result.market_risks,
                    "execution_risks": validation_result.execution_risks,
                    "competitive_risks": validation_result.competitive_risks,
                    "mitigation_strategies": validation_result.mitigation_strategies,
                    "risk_level": validation_result.risk_level,
                    "general_risks": validation_result.risks
                },
                "strategic_recommendations": {
                    "market_entry_strategy": validation_result.market_entry_strategy,
                    "success_factors": validation_result.success_factors,
                    "next_steps": validation_result.next_steps,
                    "timeline_recommendation": validation_result.timeline_recommendation
                }
            },
            "error": validation_result.error,
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time": round(time.time() - start_time, 2)
        }

        return response_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Validation endpoint error: {str(e)}")
        
        # Return a structured error response
        error_response = {
            "idea": idea,
            "analysis": {
                "analysis_metadata": {
                    "confidence_score": 0.0,
                    "analysis_depth": "Failed",
                    "data_sources_used": [],
                    "analysis_timestamp": datetime.utcnow().isoformat()
                },
                "market_assessment": {
                    "overall_score": 0,
                    "verdict": "Unknown",
                    "market_saturation": "Unknown",
                    "entry_barriers": "Unknown",
                    "market_timing": "Unknown",
                    "market_trends": [],
                    "market_size": "Unknown",
                    "market_growth": "Unknown"
                },
                "competitive_landscape": {
                    "existing_solutions": [],
                    "market_gaps": [],
                    "competitive_advantages": [],
                    "market_saturation_level": "Unknown",
                    "competitor_strength": "Unknown"
                },
                "uniqueness_analysis": {
                    "novelty_score": 0.0,
                    "differentiation_factors": [],
                    "copycat_risk": "Unknown",
                    "innovation_level": "Unknown",
                    "unique_value_proposition": ""
                },
                "business_viability": {
                    "customer_value_proposition": "",
                    "target_market_size": "Unknown",
                    "monetization_potential": "Unknown",
                    "pricing_strategy": "Unknown",
                    "customer_acquisition_difficulty": "Unknown",
                    "feasibility": "Unknown"
                },
                "risk_assessment": {
                    "market_risks": [],
                    "execution_risks": [],
                    "competitive_risks": [],
                    "mitigation_strategies": [],
                    "risk_level": "Unknown",
                    "general_risks": []
                },
                "strategic_recommendations": {
                    "market_entry_strategy": "",
                    "success_factors": [],
                    "next_steps": [],
                    "timeline_recommendation": ""
                }
            },
            "error": f"Validation failed: {str(e)}",
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time": round(time.time() - start_time, 2)
        }
        
        return error_response