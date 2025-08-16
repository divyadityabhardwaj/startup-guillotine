import uvicorn
import logging
from app import app
from app.core.config import settings

# Configure logging for Vercel
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# For Vercel deployment, we need to expose the app
# This allows Vercel to import and use the app
app_instance = app

if __name__ == "__main__":
    logger.info("Starting Startup Guillotine Validation API...")
    
    # Run the application locally
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    ) 