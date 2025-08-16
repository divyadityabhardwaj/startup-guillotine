from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

# ============================================================================
# REQUEST MODELS
# ============================================================================

class ValidationRequest(BaseModel):
    idea: str = Field(..., min_length=5, max_length=500, description="Startup idea to validate")
    include_reddit: bool = Field(default=True, description="Whether to include Reddit analysis")
    include_trends: bool = Field(default=True, description="Whether to include Google Trends analysis")
    include_competitors: bool = Field(default=True, description="Whether to include competitor analysis")

# ============================================================================
# CORE ANALYSIS MODELS
# ============================================================================

class AnalysisMetadata(BaseModel):
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in the analysis")
    analysis_depth: str = Field(..., description="Depth of analysis performed")
    data_sources_used: List[str] = Field(..., description="Data sources utilized in analysis")
    analysis_timestamp: datetime = Field(default_factory=datetime.utcnow)

class MarketAssessment(BaseModel):
    overall_score: int = Field(..., ge=0, le=100, description="Overall market opportunity score")
    verdict: str = Field(..., description="Market verdict (Strong/Promising/Moderate/Weak/High Risk)")
    market_saturation: str = Field(..., description="Level of market saturation")
    entry_barriers: str = Field(..., description="Barriers to market entry")
    market_timing: str = Field(..., description="Assessment of market timing")

class CompetitorAnalysis(BaseModel):
    name: str = Field(..., description="Competitor name/domain")
    strengths: List[str] = Field(..., description="Competitor strengths")
    weaknesses: List[str] = Field(..., description="Competitor weaknesses")
    market_position: str = Field(..., description="Market position (Leader/Follower/Niche)")
    customer_pain_points: List[str] = Field(..., description="Pain points this competitor doesn't solve well")
    differentiation_gaps: List[str] = Field(..., description="Gaps in their solution")

class CompetitiveLandscape(BaseModel):
    existing_solutions: List[CompetitorAnalysis] = Field(..., description="Detailed competitor analysis")
    market_gaps: List[str] = Field(..., description="Underserved market segments or needs")
    competitive_advantages: List[str] = Field(..., description="What makes this idea unique")
    market_saturation_level: str = Field(..., description="Detailed saturation analysis")

class UniquenessAnalysis(BaseModel):
    novelty_score: float = Field(..., ge=0.0, le=10.0, description="Novelty score out of 10")
    differentiation_factors: List[str] = Field(..., description="Specific differentiation factors")
    copycat_risk: str = Field(..., description="Risk level of being a copycat")
    innovation_level: str = Field(..., description="Level of innovation (Breakthrough/Incremental/Iterative)")
    unique_value_proposition: str = Field(..., description="Clear unique value proposition")

class BusinessViability(BaseModel):
    customer_value_proposition: str = Field(..., description="Clear problem-solution fit description")
    target_market_size: str = Field(..., description="Size of target market")
    monetization_potential: str = Field(..., description="Potential for monetization")
    pricing_strategy: str = Field(..., description="Recommended pricing strategy")
    customer_acquisition_cost: str = Field(..., description="Estimated customer acquisition cost")
    unit_economics: str = Field(..., description="Unit economics assessment")

class RiskAssessment(BaseModel):
    market_risks: List[str] = Field(..., description="Identified market risks")
    execution_risks: List[str] = Field(..., description="Technical and execution risks")
    competitive_risks: List[str] = Field(..., description="Competitive landscape risks")
    mitigation_strategies: List[str] = Field(..., description="Strategies to mitigate identified risks")
    risk_level: str = Field(..., description="Overall risk level")

class ValueEnhancementRoadmap(BaseModel):
    current_gaps: List[str] = Field(..., description="Current gaps in existing solutions")
    differentiation_opportunities: List[str] = Field(..., description="Opportunities to differentiate")
    feature_prioritization: List[str] = Field(..., description="Prioritized feature development")
    market_positioning: List[str] = Field(..., description="Market positioning strategies")
    competitive_response_strategy: List[str] = Field(..., description="How to respond to competitive moves")

class StrategicRecommendations(BaseModel):
    market_entry_strategy: str = Field(..., description="Recommended market entry approach")
    pivot_suggestions: List[str] = Field(..., description="Alternative approaches to consider")
    success_factors: List[str] = Field(..., description="Key factors for success")
    next_steps: List[str] = Field(..., description="Immediate next steps to take")
    timeline_recommendations: str = Field(..., description="Recommended timeline for execution")

# ============================================================================
# COMPREHENSIVE ANALYSIS OUTPUT
# ============================================================================

class ComprehensiveAnalysis(BaseModel):
    analysis_metadata: AnalysisMetadata
    market_assessment: MarketAssessment
    competitive_landscape: CompetitiveLandscape
    uniqueness_analysis: UniquenessAnalysis
    business_viability: BusinessViability
    risk_assessment: RiskAssessment
    value_enhancement_roadmap: ValueEnhancementRoadmap
    strategic_recommendations: StrategicRecommendations

# ============================================================================
# VALIDATION RESULT (MAIN OUTPUT)
# ============================================================================

class ValidationResult(BaseModel):
    idea: str = Field(..., description="The startup idea that was validated")
    analysis: ComprehensiveAnalysis = Field(..., description="Comprehensive analysis results")
    raw_data: Dict[str, Any] = Field(..., description="Raw data collected from all sources")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    api_status: Dict[str, bool] = Field(..., description="Status of all API services")
    execution_time: float = Field(..., description="Total execution time in seconds")
    error: Optional[str] = Field(None, description="Error message if validation failed")

# ============================================================================
# QUICK VALIDATION MODELS
# ============================================================================

class QuickAssessment(BaseModel):
    trends: Dict[str, Any] = Field(..., description="Quick trends summary")
    competitors: Dict[str, Any] = Field(..., description="Quick competitor summary")
    services_available: Dict[str, bool] = Field(..., description="Available services")

class QuickValidationResult(BaseModel):
    idea: str = Field(..., description="The startup idea")
    quick_assessment: QuickAssessment = Field(..., description="Quick assessment results")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# ============================================================================
# HEALTH & STATUS MODELS
# ============================================================================

class HealthCheck(BaseModel):
    status: str = Field(..., description="Overall API health status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    api_status: Dict[str, bool] = Field(..., description="Status of all services")
    version: str = Field(default="2.0.0", description="API version")

class ServiceStatus(BaseModel):
    available: bool = Field(..., description="Whether service is available")
    status_details: Dict[str, Any] = Field(..., description="Detailed service status")
    last_check: datetime = Field(default_factory=datetime.utcnow)

class ServiceHealth(BaseModel):
    overall_status: str = Field(..., description="Overall system health")
    services: Dict[str, ServiceStatus] = Field(..., description="Status of individual services")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# ============================================================================
# ERROR MODELS
# ============================================================================

class ValidationError(BaseModel):
    idea: str = Field(..., description="The startup idea that failed validation")
    error_type: str = Field(..., description="Type of error that occurred")
    error_message: str = Field(..., description="Detailed error message")
    data_collection_status: Dict[str, Any] = Field(..., description="Status of data collection")
    retry_recommendations: List[str] = Field(..., description="Recommendations for retry")
    timestamp: datetime = Field(default_factory=datetime.utcnow) 