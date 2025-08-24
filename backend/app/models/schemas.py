from pydantic import BaseModel, Field
from typing import List, Optional



class ValidationResult(BaseModel):
    idea: str = Field(description="The startup idea that was validated")
    confidence_socre: float = Field(ge=0.0, le=100.0, description="Overall confidence score out of 100 for the startup")
    
    # Market Assessment fields
    market_score: int = Field(ge=0, le=100, description="Overall market opportunity score (0-100)")
    market_verdict: str = Field(description="Market verdict (Strong/Promising/Moderate/Weak/High Risk)")
    market_saturation: str = Field(description="Level of market saturation (Low/Medium/High/Very High)")
    entry_barriers: str = Field(description="Barriers to market entry (Low/Medium/High/Very High)")
    market_timing: str = Field(description="Assessment of market timing (Early/Optimal/Late/Oversaturated)")
    
    # Market trends and basic info
    market_trends: List[str] = Field(description="Current market trends relevant to the idea")
    market_size: str = Field(description="Estimated market size (e.g., $10B, Large, Small)")
    market_growth: str = Field(description="Market growth potential (High/Medium/Low/Stagnant)")
    
    # Competitors
    competitors: List[str] = Field(description="List of main competitors")
    competitive_advantage: str = Field(description="Potential competitive advantage")
    market_gaps: List[str] = Field(description="Underserved market segments or needs")
    competitor_strength: str = Field(description="Competitor strength (Weak/Moderate/Strong/Dominant)")
    
    # Uniqueness
    novelty_score: float = Field(ge=0.0, le=10.0, description="Novelty score out of 10")
    differentiation_factors: List[str] = Field(description="Specific differentiation factors")
    innovation_level: str = Field(description="Level of innovation (Breakthrough/Incremental/Iterative/Minimal)")
    unique_value_proposition: str = Field(description="Clear unique value proposition")
    copycat_risk: str = Field(description="Risk level of being a copycat (Low/Medium/High/Very High)")
    
    # Business viability
    feasibility: str = Field(description="Feasibility assessment (High/Medium/Low/Very Low)")
    customer_value_proposition: str = Field(description="Clear problem-solution fit description")
    target_market_size: str = Field(description="Size of target market")
    monetization_potential: str = Field(description="Potential for monetization (High/Medium/Low/Poor)")
    pricing_strategy: str = Field(description="Recommended pricing strategy")
    customer_acquisition_difficulty: str = Field(description="Customer acquisition difficulty (Easy/Moderate/Difficult/Very Difficult)")
    
    # Risks
    risks: List[str] = Field(description="Potential risks")
    market_risks: List[str] = Field(description="Identified market risks")
    execution_risks: List[str] = Field(description="Technical and execution risks")
    competitive_risks: List[str] = Field(description="Competitive landscape risks")
    mitigation_strategies: List[str] = Field(description="Strategies to mitigate identified risks")
    risk_level: str = Field(description="Overall risk level (Low/Medium/High/Very High)")
    
    # Strategic recommendations
    market_entry_strategy: str = Field(description="Recommended market entry approach")
    success_factors: List[str] = Field(description="Key factors for success")
    next_steps: List[str] = Field(description="Immediate next steps to take")
    timeline_recommendation: str = Field(description="Recommended timeline for execution")
    
    # Data quality indicators
    data_sources_used: List[str] = Field(description="Data sources utilized in analysis")
    analysis_depth: str = Field(description="Depth of analysis performed (Surface/Moderate/Deep/Comprehensive)")
    
    error: Optional[str] = Field(default=None, description="Error message if validation failed")

