from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging

from app.api.routes import router
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create FastAPI app
app = FastAPI(
    title="Startup Guillotine Validation API v2.0",
    description="AI-powered startup idea validation using pure LLM analysis with comprehensive business insights",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for security
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logging.info("Startup Guillotine Validation API v2.0 starting up...")
    logging.info("Approach: Pure LLM-driven analysis with no fallback logic")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logging.info("Startup Guillotine Validation API v2.0 shutting down...") 