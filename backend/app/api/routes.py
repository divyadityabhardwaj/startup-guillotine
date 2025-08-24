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

 
from app.models.schemas import (
    ValidationResult, 
    ComprehensiveAnalysis,
    ValidationError
)
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
    logger.info(f"Validating idea: {idea}")

    try:
        # Run the agent
        response = await agentic_service.validate_idea(idea)

        if not response or not response.content:
            raise HTTPException(status_code=500, detail="Agent did not return a valid response.")

        # Extract raw text
        raw_text = response.content.strip()

        # Remove markdown fences
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```json", 1)[-1]
            raw_text = raw_text.split("```", 1)[0].strip()

        # Remove JS-style comments
        cleaned_text = re.sub(r"//.*", "", raw_text)

        # Remove trailing commas before } or ]
        cleaned_text = re.sub(r",\s*([}\]])", r"\1", cleaned_text)

        # Parse JSON
        try:
            result_dict = json.loads(cleaned_text)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e} | Raw: {cleaned_text}")
            raise HTTPException(status_code=500, detail="Agent returned invalid JSON")

        if not result_dict or "market_trends" not in result_dict:
            raise HTTPException(status_code=500, detail="Invalid response from agent")

        # Construct validation result
        # validation_result = ValidationResult(
        #     idea=idea,
        #     analysis=result_dict,
        #     raw_data=cleaned_text,
        #     timestamp=datetime.utcnow(),
        #     api_status=agentic_service.get_services_status(),
        #     execution_time=time.time() - start_time,
        #     error=result_dict.get("error"),
        # )

        return result_dict

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Validation endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
