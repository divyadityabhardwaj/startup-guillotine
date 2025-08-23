# app/api/endpoints/analysis.py
import json
import logging
import time
from typing import Dict, Any
from fastapi import APIRouter, Body, HTTPException, BackgroundTasks
from datetime import datetime
import os
from datetime import datetime

 
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

@router.post("/validate", response_model=ValidationResult)
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
        # Run agentic validation (returns JSON string)
        result = await agentic_service.validate_idea(idea)

        try:
            parsed = json.loads(result) if isinstance(result, str) else result
        except json.JSONDecodeError:
            parsed = None

        if not parsed or "analysis" not in parsed:
            raise HTTPException(status_code=500, detail="Invalid response from agent")

        if parsed.get("success") is False:
            raise HTTPException(status_code=500, detail=parsed.get("error", "Validation failed"))

        validation_result = ValidationResult(
            idea=idea,
            analysis=parsed["analysis"],
            raw_data=parsed.get("raw_data"),
            timestamp=datetime.utcnow(),
            api_status=agentic_service.get_services_status(),
            execution_time=time.time() - start_time,
        )

        return validation_result


    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Validation endpoint error: {str(e)}")

