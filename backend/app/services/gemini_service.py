import logging
import json
import time
from typing import Optional, Dict, Any
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from app.core.config import settings
from app.services.analysis_prompts import AnalysisPrompts
from app.services.output_validators import OutputValidator

logger = logging.getLogger(__name__)

class GeminiService:
    """Comprehensive Gemini service for startup idea analysis"""
    
    def __init__(self):
        self.is_available = False
        self.flash_model = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Gemini Flash client"""
        try:
            if not settings.GEMINI_API_KEY:
                logger.warning("Gemini API key not provided")
                return
            
            genai.configure(api_key=settings.GEMINI_API_KEY)
            
            # Test connection with a simple request
            test_model = genai.GenerativeModel(settings.GEMINI_FLASH_MODEL)
            test_response = test_model.generate_content("Hello")
            
            if test_response.text:
                self.is_available = True
                self.flash_model = genai.GenerativeModel(settings.GEMINI_FLASH_MODEL)
                logger.info("Gemini Flash service initialized successfully")
            else:
                logger.error("Gemini test request failed")
                
        except Exception as e:
            logger.error(f"Failed to initialize Gemini service: {str(e)}")
            self.is_available = False
    
    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=30),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(Exception),
        before_sleep=lambda retry_state: logger.warning(f"Retrying Gemini request (attempt {retry_state.attempt_number})")
    )
    def generate_content(
        self, 
        prompt: str, 
        max_tokens: int = 4000,
        temperature: float = 0.1,
        response_format: str = "json"
    ) -> Optional[str]:
        """Generate content using Gemini Flash model"""
        
        if not self.is_available:
            logger.error("Gemini service not available")
            return None
        
        try:
            # Configure generation for structured output
            config = GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature
            )
            
            if response_format == "json":
                config.response_mime_type = "application/json"
            
            # Generate content
            start_time = time.time()
            logger.info("Sending request to Gemini Flash model...")
            
            response = self.flash_model.generate_content(prompt, generation_config=config)
            generation_time = time.time() - start_time
            
            if response.text:
                logger.info(f"Gemini Flash generation successful in {generation_time:.2f}s")
                logger.debug(f"Response length: {len(response.text)} characters")
                return response.text
            else:
                logger.error("Gemini response is empty")
                return None
                
        except Exception as e:
            logger.error(f"Gemini Flash generation failed: {str(e)}")
            return None
    
    def analyze_startup_idea_comprehensive(
        self, 
        idea: str, 
        trends_data: Dict[str, Any], 
        competitors_data: Dict[str, Any], 
        reddit_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Perform comprehensive startup idea analysis"""
        
        if not self.is_available:
            logger.error("Cannot analyze startup idea - Gemini service unavailable")
            return None
        
        try:
            logger.info(f"Starting comprehensive analysis for idea: {idea}")
            
            # Prepare rich context with all data
            context = self._prepare_comprehensive_context(idea, trends_data, competitors_data, reddit_data)
            
            # Generate comprehensive analysis prompt
            prompt = AnalysisPrompts.get_comprehensive_analysis_prompt(idea, context)
            
            # Add additional prompting to encourage dynamic responses
            prompt += "\n\n## FINAL REMINDER - CRITICAL:\n"
            prompt += "⚠️ You MUST provide actual analysis, not copy example values.\n"
            prompt += "⚠️ Every field must contain your real insights based on the data.\n"
            prompt += "⚠️ If you copy example values, the response will be rejected.\n"
            prompt += "⚠️ Think critically and provide your professional business analysis.\n"
            
            logger.info("Sending comprehensive analysis request to Gemini...")
            
            # Generate analysis with higher temperature for more creative, dynamic responses
            response_text = self.generate_content(
                prompt=prompt,
                max_tokens=4000,
                temperature=0.7,
                response_format="json"
            )
            
            if not response_text:
                logger.error("No response received from Gemini")
                return None
            
            # Validate and parse response
            logger.info("Validating Gemini response...")
            is_valid, parsed_data, error_message = OutputValidator.validate_comprehensive_analysis(response_text)
            
            if not is_valid:
                logger.error(f"Response validation failed: {error_message}")
                logger.debug(f"Raw response: {response_text[:500]}...")
                return None
            
            logger.info("Comprehensive analysis completed successfully")
            return parsed_data
                
        except Exception as e:
            logger.error(f"Comprehensive startup idea analysis failed: {str(e)}")
            return None
    
    def analyze_startup_idea_quick(
        self, 
        idea: str, 
        trends_data: Dict[str, Any], 
        competitors_data: Dict[str, Any], 
        reddit_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Perform quick startup idea assessment"""
        
        if not self.is_available:
            logger.error("Cannot perform quick analysis - Gemini service unavailable")
            return None
        
        try:
            logger.info(f"Starting quick analysis for idea: {idea}")
            
            # Prepare simplified context
            context = self._prepare_quick_context(trends_data, competitors_data, reddit_data)
            
            # Generate quick analysis prompt
            prompt = AnalysisPrompts.get_quick_analysis_prompt(idea, context)
            
            # Add additional prompting to encourage dynamic responses
            prompt += "\n\n## FINAL REMINDER:\n"
            prompt += "⚠️ Provide actual analysis based on the data, not generic statements.\n"
            prompt += "⚠️ Every field must contain your real insights.\n"
            
            logger.info("Sending quick analysis request to Gemini...")
            
            # Generate analysis with higher temperature for more creative, dynamic responses
            response_text = self.generate_content(
                prompt=prompt,
                max_tokens=1500,
                temperature=0.7,
                response_format="json"
            )
            
            if not response_text:
                logger.error("No response received from Gemini for quick analysis")
                return None
            
            # Validate and parse response
            logger.info("Validating quick analysis response...")
            is_valid, parsed_data, error_message = OutputValidator.validate_quick_assessment(response_text)
            
            if not is_valid:
                logger.error(f"Quick analysis validation failed: {error_message}")
                return None
            
            logger.info("Quick analysis completed successfully")
            return parsed_data
                
        except Exception as e:
            logger.error(f"Quick startup idea analysis failed: {str(e)}")
            return None
    
    def _prepare_comprehensive_context(
        self, 
        idea: str, 
        trends_data: Dict[str, Any], 
        competitors_data: Dict[str, Any], 
        reddit_data: Dict[str, Any]
    ) -> str:
        """Prepare comprehensive context for LLM analysis"""
        
        def safe_format(data_dict: Dict[str, Any], name: str) -> str:
            if data_dict.get("error"):
                return f"Error fetching {name} data: {data_dict['error']}"
            
            # Include all raw data for comprehensive analysis
            return json.dumps(data_dict, indent=2, default=str)
        
        context = f"""
## COMPREHENSIVE DATA FOR ANALYSIS

### STARTUP IDEA: "{idea}"

### GOOGLE TRENDS DATA (Public Interest & Market Timing)
{safe_format(trends_data, 'Google Trends')}

### COMPETITIVE LANDSCAPE DATA (Market Analysis)
{safe_format(competitors_data, 'Tavily Competitor Research')}

### COMMUNITY SENTIMENT DATA (Customer Insights)
{safe_format(reddit_data, 'Reddit Community Analysis')}

### KEY ANALYSIS QUESTIONS TO ANSWER:
1. What does the trends data tell us about market timing and public interest?
2. Who are the main competitors and what gaps do they leave?
3. What customer pain points and needs are evident from community data?
4. How does this idea differentiate from existing solutions?
5. What are the real risks and opportunities based on the data?

### ANALYSIS INSTRUCTIONS
{AnalysisPrompts.get_validation_instructions()}
        """
        
        return context
    
    def _prepare_quick_context(
        self, 
        trends_data: Dict[str, Any], 
        competitors_data: Dict[str, Any], 
        reddit_data: Dict[str, Any]
    ) -> str:
        """Prepare simplified context for quick analysis"""
        
        def extract_key_metrics(data_dict: Dict[str, Any], name: str) -> str:
            if data_dict.get("error"):
                return f"{name}: Error - {data_dict['error']}"
            
            # Extract key metrics for quick analysis
            if name == "Google Trends":
                return f"Interest Score: {data_dict.get('interest_score', 'N/A')}, Direction: {data_dict.get('trend_direction', 'N/A')}"
            elif name == "Competitors":
                return f"Found: {data_dict.get('competitor_count', 'N/A')} competitors, Top domains: {data_dict.get('top_domains', [])[:3]}"
            elif name == "Reddit":
                return f"Posts: {data_dict.get('posts_last_n_days', 'N/A')}, Engagement: {data_dict.get('avg_score', 'N/A')}"
            else:
                return f"{name}: {json.dumps(data_dict, default=str)}"
        
        context = f"""
## QUICK ASSESSMENT DATA

### TRENDS: {extract_key_metrics(trends_data, 'Google Trends')}
### COMPETITION: {extract_key_metrics(competitors_data, 'Competitors')}
### COMMUNITY: {extract_key_metrics(reddit_data, 'Reddit')}

### QUICK ANALYSIS FOCUS:
- What do these metrics tell us about market potential?
- What competitive challenges does this idea face?
- What customer interest or concerns are evident?
- What's the immediate next step based on this data?
        """
        
        return context
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get service status"""
        return {
            "available": self.is_available,
            "models": {
                "flash": bool(self.flash_model),
                "pro": False  # Pro model disabled for reliability
            },
            "api_key_configured": bool(settings.GEMINI_API_KEY),
            "model_strategy": "flash_only",
            "capabilities": [
                "comprehensive_startup_analysis",
                "quick_assessment",
                "structured_json_outputs",
                "business_framework_analysis"
            ]
        } 