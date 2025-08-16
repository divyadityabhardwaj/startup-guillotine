"""
Structured prompts for LLM analysis of startup ideas
Provides comprehensive business analysis with clear output schemas
"""

from typing import Dict, Any

class AnalysisPrompts:
    """Structured prompts for comprehensive startup idea analysis"""
    
    @staticmethod
    def get_comprehensive_analysis_prompt(idea: str, context: str) -> str:
        """Generate comprehensive analysis prompt with output schema"""
        
        return f"""
You are an expert startup analyst and business strategist with deep experience in market analysis, competitive intelligence, and business model validation. Your task is to provide a comprehensive, data-driven analysis of the following startup idea.

## STARTUP IDEA TO ANALYZE:
"{idea}"

## AVAILABLE DATA:
{context}

## CRITICAL INSTRUCTIONS - READ CAREFULLY:

⚠️ **DO NOT COPY EXAMPLE VALUES** - You must perform actual analysis and provide real, computed scores and insights based on the data provided.

⚠️ **ANALYZE THE ACTUAL DATA** - Use the trends, competitor, and community data to inform your assessment. Don't make assumptions.

⚠️ **PROVIDE DYNAMIC INSIGHTS** - Every field should contain unique, thoughtful analysis specific to this startup idea.

## ANALYSIS FRAMEWORKS TO APPLY:

1. **Porter's 5 Forces Analysis** - Evaluate competitive rivalry, supplier power, buyer power, threat of new entrants, threat of substitutes
2. **Value Chain Analysis** - Identify where value can be added or costs reduced in the business model
3. **Blue Ocean Strategy** - Find uncontested market spaces and differentiation opportunities
4. **Customer Journey Mapping** - Identify pain points, needs, and opportunities in the customer experience
5. **Market Timing Assessment** - Evaluate if the market is ready for this solution

## OUTPUT SCHEMA (MUST FOLLOW EXACTLY):

Return a valid JSON object with this exact structure. Fill every field with thoughtful, data-driven analysis:

{{
  "analysis_metadata": {{
    "confidence_score": "A calculated value between 0 and 1 based on data quality and idea strength. Consider: data completeness, market clarity, competitive landscape, and execution feasibility",
    "analysis_depth": "comprehensive",
    "data_sources_used": ["List the actual data sources you used from the provided context"]
  }},
  "market_assessment": {{
    "overall_score": "A calculated score from 0-100 based on your analysis. Consider market size, timing, barriers, and opportunity",
    "verdict": "Your professional assessment: 'Exceptional opportunity', 'Strong potential', 'Promising with caveats', 'Moderate opportunity', 'Weak opportunity', or 'High risk'",
    "market_saturation": "Your assessment: 'Low', 'Moderate', 'High', or 'Oversaturated' with reasoning",
    "entry_barriers": "Your assessment: 'Low', 'Medium', 'High' with specific barriers identified",
    "market_timing": "Your assessment of market readiness with specific reasoning"
  }},
  "competitive_landscape": {{
    "existing_solutions": [
      {{
        "name": "Actual competitor name from your research",
        "strengths": ["Specific strengths based on your analysis"],
        "weaknesses": ["Specific weaknesses or gaps you identified"],
        "market_position": "Your assessment: 'Market Leader', 'Strong Challenger', 'Niche Player', or 'Emerging'",
        "customer_pain_points": ["Specific pain points this competitor doesn't solve well"],
        "differentiation_gaps": ["Specific opportunities where this competitor falls short"]
      }}
    ],
    "market_gaps": ["Specific underserved segments or unmet needs you identified"],
    "competitive_advantages": ["Specific advantages this startup idea has over existing solutions"],
    "market_saturation_level": "Your detailed analysis of market saturation with specific evidence"
  }},
  "uniqueness_analysis": {{
    "novelty_score": "A calculated score from 0-10 based on how unique this idea is compared to existing solutions",
    "differentiation_factors": ["Specific factors that make this idea different from competitors"],
    "copycat_risk": "Your assessment: 'Low', 'Medium', or 'High' with reasoning",
    "innovation_level": "Your assessment: 'Breakthrough', 'Incremental', or 'Iterative' with explanation",
    "unique_value_proposition": "Your clear statement of the unique value this startup provides"
  }},
  "business_viability": {{
    "customer_value_proposition": "Your analysis of the problem-solution fit with specific customer benefits",
    "target_market_size": "Your assessment: 'Large', 'Medium', or 'Small' with specific reasoning and numbers if available",
    "monetization_potential": "Your assessment: 'High', 'Medium', or 'Low' with specific strategy suggestions",
    "pricing_strategy": "Your recommended pricing approach based on the market analysis",
    "customer_acquisition_cost": "Your estimate of CAC with reasoning based on the competitive landscape",
    "unit_economics": "Your assessment of unit economics feasibility"
  }},
  "risk_assessment": {{
    "market_risks": ["Specific market risks you identified with evidence"],
    "execution_risks": ["Specific technical or operational challenges you foresee"],
    "competitive_risks": ["Specific competitive threats or market responses you anticipate"],
    "mitigation_strategies": ["Specific strategies to address each major risk"],
    "risk_level": "Your overall risk assessment: 'Low', 'Medium', or 'High' with reasoning"
  }},
  "value_enhancement_roadmap": {{
    "current_gaps": ["Specific gaps in existing solutions that this startup can address"],
    "differentiation_opportunities": ["Specific opportunities to differentiate from competitors"],
    "feature_prioritization": ["Your recommended feature development phases with reasoning"],
    "market_positioning": ["Your recommended positioning strategies based on competitive analysis"],
    "competitive_response_strategy": ["Your strategy for responding to competitive moves"]
  }},
  "strategic_recommendations": {{
    "market_entry_strategy": "Your specific recommendation for how to enter the market",
    "pivot_suggestions": ["Specific pivot options if the current approach has issues"],
    "success_factors": ["Key factors that will determine success for this startup"],
    "next_steps": ["Immediate, actionable next steps you recommend"],
    "timeline_recommendations": "Your recommended timeline for execution with milestones"
  }}
}}

## ANALYSIS QUALITY REQUIREMENTS:

1. **Data-Driven**: Base every assessment on the provided data, not assumptions
2. **Specific**: Avoid generic statements. Provide concrete examples and specific insights
3. **Honest**: Be truthful about risks and challenges, even if negative
4. **Constructive**: Even negative assessments should provide improvement paths
5. **Actionable**: Every recommendation must be specific and implementable
6. **Balanced**: Consider both opportunities and risks objectively

## SCORING GUIDELINES:

- **90-100**: Exceptional opportunity with clear competitive advantages and strong market timing
- **75-89**: Strong opportunity with good differentiation and manageable risks
- **60-74**: Promising opportunity with some caveats and specific improvement areas
- **40-59**: Moderate opportunity requiring significant changes or better timing
- **20-39**: Weak opportunity with high risk or poor market fit
- **0-19**: High risk with limited potential or poor market timing

## FINAL REMINDER:

⚠️ **DO NOT COPY EXAMPLE VALUES** - Every field must contain your actual analysis and insights.
⚠️ **USE THE PROVIDED DATA** - Reference specific data points from trends, competitors, and community analysis.
⚠️ **BE THOUGHTFUL** - This is a real business analysis, not a template exercise.

Now perform your comprehensive analysis of this startup idea and provide your professional assessment in the required JSON format.
"""

    @staticmethod
    def get_quick_analysis_prompt(idea: str, context: str) -> str:
        """Generate quick analysis prompt for rapid assessment"""
        
        return f"""
You are a startup analyst. Provide a quick but insightful assessment of this startup idea:

## IDEA: "{idea}"

## DATA: {context}

## INSTRUCTIONS:
- Analyze the actual data provided
- Provide specific insights, not generic statements
- Base your assessment on the trends, competitors, and community data

## OUTPUT SCHEMA (JSON):
{{
  "quick_assessment": {{
    "market_potential": "Your assessment: High/Medium/Low with specific reasoning based on the data",
    "competitive_landscape": "Your analysis of the competitive situation with specific insights",
    "key_risks": ["Specific risks you identified from the data"],
    "immediate_concerns": "Main concern if any, or 'None identified'",
    "next_step": "Specific, actionable next step based on your analysis"
  }}
}}

Provide a concise but insightful quick assessment based on the actual data provided.
"""

    @staticmethod
    def get_error_analysis_prompt(idea: str, error_context: str) -> str:
        """Generate prompt for analyzing failed validations"""
        
        return f"""
Analyze why this startup idea validation failed and provide recovery guidance:

## IDEA: "{idea}"

## ERROR CONTEXT: {error_context}

## OUTPUT SCHEMA (JSON):
{{
  "error_analysis": {{
    "failure_reason": "Specific reason why the validation failed",
    "data_quality_issues": ["Specific data quality problems you identified"],
    "recovery_strategies": ["Specific strategies to address the failure"],
    "alternative_approaches": ["Alternative approaches to get the analysis"],
    "retry_recommendations": ["Specific recommendations for retrying the validation"]
  }}
}}

Provide specific guidance on how to recover from this validation failure.
"""

    @staticmethod
    def get_context_enrichment_prompt(data: Dict[str, Any]) -> str:
        """Generate prompt to enrich raw data with business context"""
        
        return f"""
Enrich the following raw data with business insights and market context:

## RAW DATA:
{data}

## ENRICHMENT REQUIREMENTS:

1. **Market Context**: Add market size, growth trends, industry insights based on the data
2. **Competitive Intelligence**: Identify market leaders, positioning, gaps from the competitor data
3. **Customer Insights**: Identify pain points, needs, willingness to pay from community data
4. **Business Model Context**: Suggest monetization approaches, pricing strategies based on the market
5. **Risk Factors**: Identify market, competitive, and execution risks from the data

## OUTPUT SCHEMA (JSON):
{{
  "enriched_context": {{
    "market_insights": ["Specific insights derived from the data"],
    "competitive_intelligence": ["Specific competitive intelligence from the data"],
    "customer_insights": ["Specific customer insights from the data"],
    "business_model_suggestions": ["Specific business model suggestions based on the data"],
    "risk_identification": ["Specific risks identified from the data"]
  }}
}}

Enrich the raw data with specific business intelligence and market context derived from the provided data.
"""

    @staticmethod
    def get_validation_instructions() -> str:
        """Get validation instructions for the LLM"""
        
        return """
## VALIDATION INSTRUCTIONS:

1. **Data-Driven Analysis**: Use all provided data sources for comprehensive analysis
2. **Business Frameworks**: Apply Porter's 5 Forces, Value Chain, Blue Ocean Strategy
3. **Market Reality**: Be honest about market saturation and competitive intensity
4. **Constructive Feedback**: Even negative assessments should provide improvement paths
5. **Actionable Insights**: Every recommendation must be specific and implementable
6. **Risk Awareness**: Identify real risks but also suggest mitigation strategies
7. **Timing Consideration**: Assess market timing and readiness
8. **Execution Feasibility**: Consider technical and resource requirements

## OUTPUT QUALITY STANDARDS:

- **Specificity**: Avoid generic statements, provide concrete examples
- **Completeness**: Fill all required fields with meaningful content
- **Accuracy**: Base analysis on provided data, not assumptions
- **Actionability**: Every insight should lead to a specific action
- **Honesty**: Provide truthful assessment, even if negative
- **Constructiveness**: Negative feedback should include improvement suggestions
""" 