from pydantic import BaseModel, Field
from typing import List, Optional



class ValidationResult(BaseModel):
    idea: str = Field(description="The startup idea that was validated")
    
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

class ConfidenceCalculator:
    @staticmethod
    def calculate_confidence(validation_result: ValidationResult) -> float:
        """
        Calculate confidence score based on comprehensive analysis factors.
        Returns a score between 0.0 and 1.0
        """
        confidence = 0.5  # Base confidence
        
        # 1. Market Factors (30% weight)
        market_factors = 0.0
        
        # Market score contribution (0-100 → 0.0-1.0)
        market_factors += (validation_result.market_score / 100) * 0.15
        
        # Market verdict contribution
        verdict_scores = {
            "Strong": 1.0, "Promising": 0.8, "Moderate": 0.6, 
            "Weak": 0.4, "High Risk": 0.2
        }
        market_factors += verdict_scores.get(validation_result.market_verdict.lower().title(), 0.5) * 0.05
        
        # Market saturation contribution (inverse)
        saturation_scores = {"Low": 1.0, "Medium": 0.7, "High": 0.4, "Very High": 0.1}
        market_factors += saturation_scores.get(validation_result.market_saturation.lower().title(), 0.5) * 0.05
        
        # Market growth contribution
        growth_scores = {"High": 1.0, "Medium": 0.7, "Low": 0.4, "Stagnant": 0.1}
        market_factors += growth_scores.get(validation_result.market_growth.lower().title(), 0.5) * 0.05
        
        confidence += market_factors * 0.3
        
        # 2. Competitive Factors (20% weight)
        competitive_factors = 0.0
        
        # Competitor strength (inverse)
        strength_scores = {"Weak": 1.0, "Moderate": 0.7, "Strong": 0.4, "Dominant": 0.1}
        competitive_factors += strength_scores.get(validation_result.competitor_strength.lower().title(), 0.5) * 0.1
        
        # Number of competitors (inverse - more competitors = lower confidence)
        competitor_count = len(validation_result.competitors)
        comp_score = max(0, 1.0 - (competitor_count * 0.05))  # -5% per competitor
        competitive_factors += comp_score * 0.05
        
        # Market gaps (more gaps = higher confidence)
        gap_count = len(validation_result.market_gaps)
        gap_score = min(1.0, gap_count * 0.2)  # +20% per gap, max 100%
        competitive_factors += gap_score * 0.05
        
        confidence += competitive_factors * 0.2
        
        # 3. Innovation Factors (15% weight)
        innovation_factors = 0.0
        
        # Novelty score (0-10 → 0.0-1.0)
        innovation_factors += (validation_result.novelty_score / 10) * 0.05
        
        # Innovation level
        innovation_scores = {
            "Breakthrough": 1.0, "Incremental": 0.7, "Iterative": 0.5, "Minimal": 0.2
        }
        innovation_factors += innovation_scores.get(validation_result.innovation_level.lower().title(), 0.5) * 0.05
        
        # Copycat risk (inverse)
        copycat_scores = {"Low": 1.0, "Medium": 0.7, "High": 0.4, "Very High": 0.1}
        innovation_factors += copycat_scores.get(validation_result.copycat_risk.lower().title(), 0.5) * 0.05
        
        confidence += innovation_factors * 0.15
        
        # 4. Feasibility Factors (20% weight)
        feasibility_factors = 0.0
        
        # Feasibility assessment
        feasibility_scores = {"High": 1.0, "Medium": 0.7, "Low": 0.4, "Very Low": 0.1}
        feasibility_factors += feasibility_scores.get(validation_result.feasibility.lower().title(), 0.5) * 0.1
        
        # Monetization potential
        monetization_scores = {"High": 1.0, "Medium": 0.7, "Low": 0.4, "Poor": 0.1}
        feasibility_factors += monetization_scores.get(validation_result.monetization_potential.lower().title(), 0.5) * 0.05
        
        # Customer acquisition difficulty (inverse)
        acquisition_scores = {"Easy": 1.0, "Moderate": 0.7, "Difficult": 0.4, "Very Difficult": 0.1}
        feasibility_factors += acquisition_scores.get(validation_result.customer_acquisition_difficulty.lower().title(), 0.5) * 0.05
        
        confidence += feasibility_factors * 0.2
        
        # 5. Risk Factors (10% weight) - inverse relationship
        risk_factors = 0.0
        
        risk_scores = {"Low": 1.0, "Medium": 0.7, "High": 0.4, "Very High": 0.1}
        risk_factors += risk_scores.get(validation_result.risk_level.lower().title(), 0.5) * 0.1
        
        confidence += risk_factors * 0.1
        
        # 6. Data Quality Factors (5% weight)
        data_factors = 0.0
        
        analysis_depth_scores = {
            "Comprehensive": 1.0, "Deep": 0.8, "Moderate": 0.6, "Surface": 0.4
        }
        data_factors += analysis_depth_scores.get(validation_result.analysis_depth.lower().title(), 0.5) * 0.05
        
        # Data sources count bonus
        source_count = len(validation_result.data_sources_used)
        source_bonus = min(0.1, source_count * 0.02)  # +2% per source, max +10%
        data_factors += source_bonus
        
        confidence += data_factors * 0.05
        
        # Ensure confidence is within bounds
        confidence = max(0.0, min(1.0, confidence))
        
        return round(confidence, 2)
