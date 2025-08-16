import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, File, UploadFile, Form
from fastapi.responses import JSONResponse
from datetime import datetime
import PyPDF2
import io

from app.models.schemas import (
    ValidationRequest, 
    ValidationResult, 
    HealthCheck, 
    ServiceHealth,
    QuickValidationResult
)
from app.services.validation_service import ValidationService

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize validation service
validation_service = ValidationService()

@router.get("/status")
async def get_status():
    """Get simple status of all services"""
    
    try:
        return {
            "status": "ok",
            "services": validation_service.services_status,
            "gemini_available": validation_service.gemini_service.is_available,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    try:
        service_health = validation_service.get_service_health()
        
        return HealthCheck(
            status="healthy" if service_health["overall_status"] == "healthy" else "degraded",
            timestamp=datetime.utcnow(),
            api_status=validation_service.services_status,
            version="2.0.0"
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")

@router.post("/validate", response_model=ValidationResult)
async def validate_startup_idea(request: ValidationRequest):
    """Validate a startup idea using comprehensive LLM analysis"""
    
    try:
        logger.info(f"Comprehensive validation request received for idea: {request.idea}")
        
        # Validate request
        if len(request.idea.strip()) < 5:
            raise HTTPException(
                status_code=400, 
                detail="Idea must be at least 5 characters long"
            )
        
        if len(request.idea.strip()) > 500:
            raise HTTPException(
                status_code=400, 
                detail="Idea must be less than 500 characters"
            )
        
        # Perform comprehensive validation
        result = validation_service.validate_startup_idea(
            idea=request.idea,
            include_reddit=request.include_reddit,
            include_trends=request.include_trends,
            include_competitors=request.include_competitors
        )
        
        # Check if validation failed
        if result.error:
            logger.error(f"Validation failed for idea: {request.idea} - {result.error}")
            raise HTTPException(
                status_code=500, 
                detail=f"Validation failed: {result.error}"
            )
        
        logger.info(f"Comprehensive validation completed for idea: {request.idea}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Validation failed: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@router.post("/validate-file", response_model=ValidationResult)
async def validate_file(
    file: UploadFile = File(...),
    include_reddit: bool = Form(True),
    include_trends: bool = Form(True),
    include_competitors: bool = Form(True)
):
    """Validate a startup idea from uploaded file"""
    
    try:
        logger.info(f"File validation request received for file: {file.filename}")
        
        # Validate file type
        if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX files are supported"
            )
        
        # Read file content
        content = await file.read()
        
        # Extract text based on file type
        if file.content_type == "application/pdf":
            try:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            except Exception as e:
                logger.error(f"Failed to read PDF: {str(e)}")
                raise HTTPException(
                    status_code=400,
                    detail="Failed to read PDF file. Please ensure it's not corrupted."
                )
        else:
            # For DOCX files, we'll need to implement text extraction
            # For now, return an error
            raise HTTPException(
                status_code=400,
                detail="DOCX file support coming soon. Please use PDF files for now."
            )
        
        # Clean and validate extracted text
        text = text.strip()
        if len(text) < 5:
            raise HTTPException(
                status_code=400,
                detail="Extracted text is too short. Please ensure the file contains readable text."
            )
        
        if len(text) > 500:
            text = text[:500] + "..."
        
        logger.info(f"Extracted text from file: {text[:100]}...")
        
        # Perform comprehensive validation
        result = validation_service.validate_startup_idea(
            idea=text,
            include_reddit=include_reddit,
            include_trends=include_trends,
            include_competitors=include_competitors
        )
        
        # Check if validation failed
        if result.error:
            logger.error(f"Validation failed for file: {file.filename} - {result.error}")
            raise HTTPException(
                status_code=500,
                detail=f"Validation failed: {result.error}"
            )
        
        logger.info(f"File validation completed for: {file.filename}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"File validation failed: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@router.post("/validate/quick", response_model=QuickValidationResult)
async def quick_validation(request: ValidationRequest):
    """Get a quick validation summary using LLM analysis"""
    
    try:
        logger.info(f"Quick validation request received for idea: {request.idea}")
        
        # Validate request
        if len(request.idea.strip()) < 5:
            raise HTTPException(
                status_code=400, 
                detail="Idea must be at least 5 characters long"
            )
        
        # Get quick validation
        result = validation_service.get_quick_validation(
            idea=request.idea,
            include_reddit=request.include_reddit,
            include_trends=request.include_trends,
            include_competitors=request.include_competitors
        )
        
        logger.info(f"Quick validation completed for idea: {request.idea}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Quick validation failed: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/services/status", response_model=ServiceHealth)
async def get_services_status():
    """Get detailed status of all services"""
    
    try:
        return validation_service.get_service_health()
    except Exception as e:
        error_msg = f"Failed to get services status: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/services/{service_name}/status")
async def get_service_status(service_name: str):
    """Get status of a specific service"""
    
    try:
        service_health = validation_service.get_service_health()
        
        if service_name not in service_health["services"]:
            raise HTTPException(
                status_code=404, 
                detail=f"Service '{service_name}' not found"
            )
        
        return {
            "service": service_name,
            "status": service_health["services"][service_name]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Failed to get service status: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@router.post("/validate/batch")
async def batch_validation(requests: list[ValidationRequest]):
    """Validate multiple startup ideas in batch (limited to 3 for serverless)"""
    
    try:
        # Limit batch size for serverless environment
        if len(requests) > 3:
            raise HTTPException(
                status_code=400, 
                detail="Batch size limited to 3 ideas for serverless environment"
            )
        
        logger.info(f"Batch validation request received for {len(requests)} ideas")
        
        results = []
        for i, request in enumerate(requests):
            try:
                logger.info(f"Processing idea {i+1}/{len(requests)}: {request.idea}")
                
                result = validation_service.validate_startup_idea(
                    idea=request.idea,
                    include_reddit=request.include_reddit,
                    include_trends=request.include_trends,
                    include_competitors=request.include_competitors
                )
                
                results.append({
                    "index": i,
                    "idea": request.idea,
                    "result": result,
                    "status": "success"
                })
                
            except Exception as e:
                logger.error(f"Failed to validate idea {i+1}: {str(e)}")
                results.append({
                    "index": i,
                    "idea": request.idea,
                    "error": str(e),
                    "status": "failed"
                })
        
        return {
            "batch_size": len(requests),
            "results": results,
            "timestamp": datetime.utcnow().isoformat(),
            "note": "Batch validation using pure LLM approach"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Batch validation failed: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/")
async def root():
    """Root endpoint with API information"""
    
    return {
        "message": "Startup Guillotine Validation API v2.0",
        "version": "2.0.0",
        "description": "AI-powered startup idea validation using pure LLM analysis",
        "approach": "Pure LLM-driven analysis with no fallback logic",
        "endpoints": {
            "POST /validate": "Comprehensive startup idea validation (LLM)",
            "POST /validate-file": "File-based validation (PDF/DOCX)",
            "POST /validate/quick": "Quick validation summary (LLM)",
            "POST /validate/batch": "Batch validation (max 3 ideas)",
            "GET /health": "Health check",
            "GET /services/status": "All services status",
            "GET /services/{service}/status": "Specific service status"
        },
        "features": [
            "Comprehensive market analysis",
            "Competitive landscape assessment",
            "Uniqueness analysis with copycat risk assessment",
            "Business viability evaluation",
            "Risk assessment with mitigation strategies",
            "Value enhancement roadmap for weak ideas",
            "Strategic recommendations and next steps"
        ],
        "timestamp": datetime.utcnow().isoformat()
    } 