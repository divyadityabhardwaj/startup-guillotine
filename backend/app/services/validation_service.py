import logging
import time
import uuid
from typing import Dict, Any, Optional
from datetime import datetime

from app.services.gemini_service import GeminiService
from app.services.tavily_service import TavilyService
from app.services.google_trends_service import GoogleTrendsService
from app.services.reddit_service import RedditService
from app.models.schemas import (
    ValidationResult, 
    ComprehensiveAnalysis, 
    ValidationError,
    QuickValidationResult,
    QuickAssessment
)
from app.services.output_validators import OutputValidator

logger = logging.getLogger(__name__)

class ValidationService:
    """Pure LLM-driven startup idea validation service"""
    
    def __init__(self):
        self.gemini_service = GeminiService()
        self.tavily_service = TavilyService()
        self.google_trends_service = GoogleTrendsService()
        self.reddit_service = RedditService()
        
        # Track service availability
        self.services_status = self._check_services_status()
        logger.info(f"Validation service initialized. Services status: {self.services_status}")
    
    def _check_services_status(self) -> Dict[str, bool]:
        """Check status of all services"""
        return {
            "gemini": self.gemini_service.is_available,
            "tavily": self.tavily_service.is_available,
            "google_trends": self.google_trends_service.is_available,
            "reddit": self.reddit_service.is_available
        }
    
    def validate_startup_idea(
        self, 
        idea: str, 
        include_reddit: bool = True,
        include_trends: bool = True,
        include_competitors: bool = True
    ) -> ValidationResult:
        """Main validation workflow using pure LLM analysis"""
        
        start_time = time.time()
        job_id = str(uuid.uuid4())
        
        logger.info(f"Starting comprehensive validation for idea: {idea} (Job ID: {job_id})")
        
        # Input validation
        if not idea or len(idea.strip()) < 10:
            error_msg = "Input idea is too short or empty. Please provide a more detailed description."
            logger.error(error_msg)
            return ValidationResult(
                idea=idea,
                analysis=None,
                raw_data={},
                timestamp=datetime.utcnow(),
                api_status=self.services_status,
                execution_time=0,
                error=error_msg
            )

        try:
            # Initialize result structure
            raw_data = {}
            analysis = None
            
            # Step 1: Google Trends Analysis
            if include_trends:
                logger.info("Step 1/3: Analyzing Google Trends...")
                trends_data = self.google_trends_service.get_trends_with_fallback(idea)
                raw_data["trends"] = trends_data
                logger.info(f"Google Trends completed: {trends_data.get('interest_score', 0)} score")
            else:
                logger.info("Google Trends analysis was not requested.")

            time.sleep(1)  # Add delay to avoid rate limiting
            
            # Step 2: Competitor Research
            if include_competitors and self.tavily_service.is_available:
                logger.info("Step 2/3: Researching competitors...")
                competitors_data = self.tavily_service.search_with_fallback(idea)
                raw_data["competitors"] = competitors_data
                logger.info(f"Competitor research completed: {competitors_data.get('competitor_count', 0)} found")
            else:
                logger.warning("Competitor research skipped or unavailable")
                raw_data["competitors"] = {"error": "Service unavailable or disabled"}

            time.sleep(1)  # Add delay to avoid rate limiting
            
            # Step 3: Reddit Community Analysis
            if include_reddit and self.reddit_service.is_available:
                logger.info("Step 3/3: Analyzing Reddit activity...")
                reddit_data = self.reddit_service.get_activity_with_fallback(idea)
                raw_data["reddit"] = reddit_data
                logger.info(f"Reddit analysis completed: {reddit_data.get('posts_last_n_days', 0)} posts found")
            elif include_reddit:
                logger.warning("Reddit analysis skipped: service is unavailable.")
                raw_data["reddit"] = {"error": "Reddit service is not configured. Please provide API credentials."}
            else:
                logger.info("Reddit analysis was not requested.")
            
            # Step 4: LLM Comprehensive Analysis
            logger.info(f"Gemini service status: {self.gemini_service.is_available}")
            if self.gemini_service.is_available:
                logger.info("Step 4/4: Performing comprehensive LLM analysis...")
                analysis_data = self.gemini_service.analyze_startup_idea_comprehensive(
                    idea, 
                    raw_data.get("trends", {}),
                    raw_data.get("competitors", {}),
                    raw_data.get("reddit", {})
                )
                
                if analysis_data:
                    try:
                        # Create ComprehensiveAnalysis object
                        analysis = ComprehensiveAnalysis(**analysis_data)
                        logger.info(f"LLM analysis completed: {analysis.market_assessment.overall_score}/100 score, {analysis.market_assessment.verdict} verdict")
                    except Exception as validation_error:
                        logger.error(f"LLM response validation failed: {str(validation_error)}")
                        logger.debug(f"Raw LLM response: {analysis_data}")
                        # Create a minimal error analysis structure
                        analysis = self._create_error_analysis(idea, str(validation_error))
                else:
                    logger.error("LLM analysis failed - no response received")
                    # Create a minimal error analysis structure
                    analysis = self._create_error_analysis(idea, "LLM analysis failed - no response received")
            else:
                logger.error("Gemini service unavailable - no fallback logic available")
                logger.error(f"Services status: {self.services_status}")
                # Create a minimal error analysis structure
                analysis = self._create_error_analysis(idea, "Gemini service unavailable")
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Create final result
            result = ValidationResult(
                idea=idea,
                analysis=analysis,
                raw_data=raw_data,
                timestamp=datetime.utcnow(),
                api_status=self.services_status,
                execution_time=execution_time
            )
            
            logger.info(f"Validation completed successfully in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            error_msg = f"Validation failed: {str(e)}"
            logger.error(error_msg)
            
            # Return error result with minimal analysis structure
            execution_time = time.time() - start_time
            
            # Create minimal error analysis
            error_analysis = self._create_error_analysis(idea, error_msg)
            
            return ValidationResult(
                idea=idea,
                analysis=error_analysis,
                raw_data=raw_data if 'raw_data' in locals() else {},
                timestamp=datetime.utcnow(),
                api_status=self.services_status,
                execution_time=execution_time,
                error=error_msg
            )
    
    def get_quick_validation(
        self, 
        idea: str,
        include_reddit: bool = True,
        include_trends: bool = True,
        include_competitors: bool = True
    ) -> QuickValidationResult:
        """Get quick validation summary using LLM"""
        
        try:
            logger.info(f"Starting quick validation for idea: {idea}")
            
            # Collect minimal data
            trends_summary = {}
            if include_trends and self.google_trends_service.is_available:
                trends_data = self.google_trends_service.get_trends(idea, "today 3-m")
                trends_summary = {
                    "interest_score": trends_data.get("interest_score", 0),
                    "trend_direction": trends_data.get("trend_direction", "unknown")
                }
            
            competitor_summary = {}
            if include_competitors and self.tavily_service.is_available:
                comp_data = self.tavily_service.search_competitors(idea, max_results=5)
                competitor_summary = {
                    "competitor_count": comp_data.get("competitor_count", 0)
                }
            
            reddit_summary = {}
            if include_reddit and self.reddit_service.is_available:
                reddit_data = self.reddit_service.get_community_activity(idea)
                reddit_summary = {
                    "posts_found": reddit_data.get("posts_last_n_days", 0),
                    "engagement": reddit_data.get("avg_score", 0)
                }
            
            # Perform quick LLM analysis
            if self.gemini_service.is_available:
                logger.info("Performing quick LLM analysis...")
                quick_analysis = self.gemini_service.analyze_startup_idea_quick(
                    idea, trends_summary, competitor_summary, reddit_summary
                )
                
                if quick_analysis:
                    logger.info("Quick LLM analysis completed successfully")
                    return QuickValidationResult(
                        idea=idea,
                        quick_assessment=QuickAssessment(
                            trends=trends_summary,
                            competitors=competitor_summary,
                            services_available=self.services_status
                        ),
                        timestamp=datetime.utcnow()
                    )
                else:
                    logger.error("Quick LLM analysis failed")
                    raise Exception("Quick LLM analysis failed")
            else:
                logger.error("Gemini service unavailable for quick analysis")
                raise Exception("Gemini service unavailable")
                
        except Exception as e:
            logger.error(f"Quick validation failed: {str(e)}")
            raise e
    
    def get_service_health(self) -> Dict[str, Any]:
        """Get comprehensive service health status"""
        
        try:
            # Check individual services
            services = {}
            for service_name, is_available in self.services_status.items():
                if service_name == "gemini":
                    services[service_name] = {
                        "status": "healthy" if is_available else "unavailable",
                        "details": "Gemini 1.5 Flash model for LLM analysis"
                    }
                elif service_name == "tavily":
                    services[service_name] = {
                        "status": "healthy" if is_available else "unavailable",
                        "details": "Tavily search for competitor research"
                    }
                elif service_name == "google_trends":
                    services[service_name] = {
                        "status": "healthy" if is_available else "unavailable",
                        "details": "Google Trends for market interest analysis"
                    }
                elif service_name == "reddit":
                    services[service_name] = {
                        "status": "healthy" if is_available else "unavailable",
                        "details": "Reddit API for community sentiment analysis"
                    }
            
            # Determine overall status
            available_services = sum(self.services_status.values())
            total_services = len(self.services_status)
            
            if available_services == total_services:
                overall_status = "healthy"
            elif available_services >= total_services // 2:
                overall_status = "degraded"
            else:
                overall_status = "unhealthy"
            
            return {
                "overall_status": overall_status,
                "services": services,
                "available_services": available_services,
                "total_services": total_services,
                "timestamp": datetime.utcnow().isoformat(),
                "version": "2.0.0"
            }
            
        except Exception as e:
            logger.error(f"Failed to get service health: {str(e)}")
            return {
                "overall_status": "error",
                "services": {},
                "available_services": 0,
                "total_services": len(self.services_status),
                "timestamp": datetime.utcnow().isoformat(),
                "version": "2.0.0",
                "error": str(e)
            }
    
    def _create_error_analysis(self, idea: str, error_message: str) -> ComprehensiveAnalysis:
        """Create a minimal analysis structure when LLM analysis fails"""
        
        from app.models.schemas import (
            AnalysisMetadata, MarketAssessment, CompetitiveLandscape,
            UniquenessAnalysis, BusinessViability, RiskAssessment,
            ValueEnhancementRoadmap, StrategicRecommendations
        )
        
        return ComprehensiveAnalysis(
            analysis_metadata=AnalysisMetadata(
                confidence_score=0.0,
                analysis_depth="error",
                data_sources_used=["error"],
                analysis_timestamp=datetime.utcnow().isoformat()
            ),
            market_assessment=MarketAssessment(
                overall_score=0,
                verdict="Analysis Failed",
                market_saturation="Unknown",
                entry_barriers="Unknown",
                market_timing="Unknown"
            ),
            competitive_landscape=CompetitiveLandscape(
                existing_solutions=[],
                market_gaps=["Analysis failed - unable to identify gaps"],
                competitive_advantages=["Analysis failed - unable to identify advantages"],
                market_saturation_level="Analysis failed - unable to assess market saturation"
            ),
            uniqueness_analysis=UniquenessAnalysis(
                novelty_score=0.0,
                differentiation_factors=["Analysis failed"],
                copycat_risk="Unknown",
                innovation_level="Unknown",
                unique_value_proposition="Analysis failed - unable to assess uniqueness"
            ),
            business_viability=BusinessViability(
                customer_value_proposition="Analysis failed",
                target_market_size="Unknown",
                monetization_potential="Unknown",
                pricing_strategy="Analysis failed",
                customer_acquisition_cost="Unknown",
                unit_economics="Analysis failed"
            ),
            risk_assessment=RiskAssessment(
                market_risks=["Analysis failed - unable to assess risks"],
                execution_risks=["Analysis failed - unable to assess execution risks"],
                competitive_risks=["Analysis failed - unable to assess competitive risks"],
                mitigation_strategies=["Retry the analysis or contact support"],
                risk_level="Unknown"
            ),
            value_enhancement_roadmap=ValueEnhancementRoadmap(
                current_gaps=["Analysis failed"],
                differentiation_opportunities=["Analysis failed"],
                feature_prioritization=["Analysis failed"],
                market_positioning=["Analysis failed"],
                competitive_response_strategy=["Analysis failed"]
            ),
            strategic_recommendations=StrategicRecommendations(
                market_entry_strategy="Analysis failed - unable to provide recommendations",
                pivot_suggestions=["Retry the analysis"],
                success_factors=["Analysis failed"],
                next_steps=["Retry the analysis or contact support"],
                timeline_recommendations="Analysis failed"
            )
        )
    
    def get_validation_summary(self, idea: str) -> Dict[str, Any]:
        """Get validation summary without full analysis"""
        
        try:
            # Quick trends check
            trends_summary = {}
            if self.google_trends_service.is_available:
                trends_data = self.google_trends_service.get_trends(idea, "today 3-m")
                trends_summary = {
                    "interest_score": trends_data.get("interest_score", 0),
                    "trend_direction": trends_data.get("trend_direction", "unknown")
                }
            
            # Quick competitor count
            competitor_summary = {}
            if self.tavily_service.is_available:
                comp_data = self.tavily_service.search_competitors(idea, max_results=5)
                competitor_summary = {
                    "competitor_count": comp_data.get("competitor_count", 0)
                }
            
            return {
                "idea": idea,
                "quick_assessment": {
                    "trends": trends_summary,
                    "competitors": competitor_summary,
                    "services_available": self.services_status
                },
                "timestamp": datetime.utcnow().isoformat(),
                "note": "This is raw data summary, not LLM analysis"
            }
            
        except Exception as e:
            logger.error(f"Quick validation failed: {str(e)}")
            return {
                "idea": idea,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            } 