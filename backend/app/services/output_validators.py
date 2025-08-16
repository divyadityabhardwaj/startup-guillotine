"""
Output validation for LLM responses
Ensures structured outputs match expected schemas
"""

import json
import logging
from typing import Dict, Any, Optional, Tuple
from app.models.schemas import ComprehensiveAnalysis, ValidationError

logger = logging.getLogger(__name__)

class OutputValidator:
    """Validates LLM outputs against expected schemas"""
    
    @staticmethod
    def validate_comprehensive_analysis(response_text: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Validate comprehensive analysis response
        
        Returns:
            Tuple of (is_valid, parsed_data, error_message)
        """
        try:
            # First, try to parse as JSON
            if not response_text.strip():
                return False, None, "Empty response from LLM"
            
            # Try to extract JSON if response contains extra text
            json_start = response_text.find('{')
            json_end = response_text.rfind('}')
            
            if json_start == -1 or json_end == -1:
                return False, None, "No JSON structure found in response"
            
            json_text = response_text[json_start:json_end + 1]
            parsed_data = json.loads(json_text)
            
            # Validate against our schema
            validation_result = OutputValidator._validate_schema_structure(parsed_data)
            if not validation_result[0]:
                return False, None, f"Schema validation failed: {validation_result[1]}"
            
            # Validate data quality
            quality_result = OutputValidator._validate_data_quality(parsed_data)
            if not quality_result[0]:
                logger.warning(f"Data quality issues: {quality_result[1]}")
                # Continue with warnings, but mark as valid
            
            return True, parsed_data, None
            
        except json.JSONDecodeError as e:
            return False, None, f"JSON parsing failed: {str(e)}"
        except Exception as e:
            return False, None, f"Validation error: {str(e)}"
    
    @staticmethod
    def _validate_schema_structure(data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate that all required fields are present"""
        
        required_sections = [
            "analysis_metadata",
            "market_assessment", 
            "competitive_landscape",
            "uniqueness_analysis",
            "business_viability",
            "risk_assessment",
            "value_enhancement_roadmap",
            "strategic_recommendations"
        ]
        
        for section in required_sections:
            if section not in data:
                return False, f"Missing required section: {section}"
            
            if not isinstance(data[section], dict):
                return False, f"Section {section} must be an object"
        
        # Validate critical fields in each section
        critical_fields = {
            "analysis_metadata": ["confidence_score", "analysis_depth", "data_sources_used"],
            "market_assessment": ["overall_score", "verdict", "market_saturation"],
            "uniqueness_analysis": ["novelty_score", "copycat_risk", "unique_value_proposition"],
            "business_viability": ["customer_value_proposition", "target_market_size"],
            "risk_assessment": ["risk_level", "mitigation_strategies"],
            "strategic_recommendations": ["next_steps", "market_entry_strategy"]
        }
        
        for section, fields in critical_fields.items():
            for field in fields:
                if field not in data[section]:
                    return False, f"Missing critical field: {section}.{field}"
        
        return True, None
    
    @staticmethod
    def _validate_data_quality(data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate data quality and completeness"""
        
        issues = []
        
        # Check for empty or generic content
        for section_name, section_data in data.items():
            if isinstance(section_data, dict):
                for field_name, field_value in section_data.items():
                    if isinstance(field_value, str) and len(field_value.strip()) < 10:
                        issues.append(f"{section_name}.{field_name}: Content too short")
                    elif isinstance(field_value, list) and len(field_value) == 0:
                        issues.append(f"{section_name}.{field_name}: Empty list")
                    elif field_value in ["N/A", "None", "TBD", "To be determined"]:
                        issues.append(f"{section_name}.{field_value}: Generic placeholder value")
                    
                    # Check for copied example values
                    if isinstance(field_value, str):
                        # Check for generic example patterns
                        generic_patterns = [
                            "Factor 1", "Factor 2", "Strength 1", "Strength 2",
                            "Weakness 1", "Weakness 2", "Pain point 1", "Pain point 2",
                            "Gap 1", "Gap 2", "Risk 1", "Risk 2", "Strategy 1", "Strategy 2",
                            "Opportunity 1", "Opportunity 2", "Approach 1", "Approach 2",
                            "Recommendation 1", "Recommendation 2", "Action 1", "Action 2",
                            "Insight 1", "Insight 2", "Intelligence 1", "Intelligence 2",
                            "Suggestion 1", "Suggestion 2", "Phase 1", "Phase 2"
                        ]
                        
                        for pattern in generic_patterns:
                            if pattern in field_value:
                                issues.append(f"{section_name}.{field_name}: Contains generic example value '{pattern}'")
                                break
                        
                        # Check for overly generic statements
                        generic_statements = [
                            "Clear statement of unique value",
                            "Brief competitive overview", 
                            "Specific pricing approach",
                            "Detailed analysis of market saturation",
                            "Clear problem-solution fit description",
                            "Unit economics assessment"
                        ]
                        
                        for statement in generic_statements:
                            if statement.lower() in field_value.lower():
                                issues.append(f"{section_name}.{field_name}: Contains generic template text")
                                break
        
        # Check score ranges and detect copied example values
        if "market_assessment" in data:
            score = data["market_assessment"].get("overall_score")
            if score is not None:
                if isinstance(score, str):
                    # Check if it's a copied example value
                    if "calculated score from 0-100" in score.lower() or "your assessment" in score.lower():
                        issues.append("market_assessment.overall_score: Contains copied example text instead of actual score")
                    elif score.isdigit():
                        score = int(score)
                    else:
                        issues.append("market_assessment.overall_score: Should be a numeric value, not text")
                
                if isinstance(score, (int, float)) and (score < 0 or score > 100):
                    issues.append("market_assessment.overall_score: Score out of range (0-100)")
        
        if "uniqueness_analysis" in data:
            novelty = data["uniqueness_analysis"].get("novelty_score")
            if novelty is not None:
                if isinstance(novelty, str):
                    # Check if it's a copied example value
                    if "calculated score from 0-10" in novelty.lower() or "your assessment" in novelty.lower():
                        issues.append("uniqueness_analysis.novelty_score: Contains copied example text instead of actual score")
                    elif novelty.replace('.', '').isdigit():
                        novelty = float(novelty)
                    else:
                        issues.append("uniqueness_analysis.novelty_score: Should be a numeric value, not text")
                
                if isinstance(novelty, (int, float)) and (novelty < 0 or novelty > 10):
                    issues.append("uniqueness_analysis.novelty_score: Novelty score out of range (0-10)")
        
        # Check confidence score
        if "analysis_metadata" in data:
            confidence = data["analysis_metadata"].get("confidence_score")
            if confidence is not None:
                if isinstance(confidence, str):
                    # Check if it's a copied example value
                    if "calculated value between 0 and 1" in confidence.lower() or "your assessment" in confidence.lower():
                        issues.append("analysis_metadata.confidence_score: Contains copied example text instead of actual score")
                    elif confidence.replace('.', '').isdigit():
                        confidence = float(confidence)
                    else:
                        issues.append("analysis_metadata.confidence_score: Should be a numeric value, not text")
                
                if isinstance(confidence, (int, float)) and (confidence < 0 or confidence > 1):
                    issues.append("analysis_metadata.confidence_score: Confidence score out of range (0-1)")
        
        if issues:
            return False, "; ".join(issues)
        
        return True, None
    
    @staticmethod
    def create_validation_error(idea: str, error_message: str, data_collection_status: Dict[str, Any]) -> ValidationError:
        """Create a structured validation error response"""
        
        return ValidationError(
            idea=idea,
            error_type="LLM_VALIDATION_FAILED",
            error_message=error_message,
            data_collection_status=data_collection_status,
            retry_recommendations=[
                "Check if the startup idea is clear and specific",
                "Ensure all data sources are working properly",
                "Try with a different startup idea to test the system",
                "Contact support if the issue persists"
            ]
        )
    
    @staticmethod
    def extract_json_from_response(response_text: str) -> Optional[Dict[str, Any]]:
        """Try to extract JSON from response text"""
        
        try:
            # Look for JSON markers
            json_start = response_text.find('{')
            json_end = response_text.rfind('}')
            
            if json_start != -1 and json_end != -1:
                json_text = response_text[json_start:json_end + 1]
                return json.loads(json_text)
            
            # Try to find JSON-like content
            lines = response_text.split('\n')
            json_lines = []
            in_json = False
            
            for line in lines:
                if '{' in line:
                    in_json = True
                if in_json:
                    json_lines.append(line)
                if '}' in line and in_json:
                    break
            
            if json_lines:
                json_text = '\n'.join(json_lines)
                return json.loads(json_text)
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to extract JSON: {str(e)}")
            return None
    
    @staticmethod
    def sanitize_response(response_text: str) -> str:
        """Clean and sanitize LLM response text"""
        
        # Remove markdown formatting
        cleaned = response_text.replace('```json', '').replace('```', '')
        
        # Remove extra whitespace
        cleaned = cleaned.strip()
        
        # Fix common JSON formatting issues
        cleaned = cleaned.replace('\n', ' ').replace('\r', ' ')
        cleaned = ' '.join(cleaned.split())  # Normalize whitespace
        
        return cleaned
    
    @staticmethod
    def validate_quick_assessment(response_text: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """Validate quick assessment response"""
        
        try:
            # Clean response
            cleaned_response = OutputValidator.sanitize_response(response_text)
            
            # Try to parse JSON
            json_start = cleaned_response.find('{')
            json_end = cleaned_response.rfind('}')
            
            if json_start == -1 or json_end == -1:
                return False, None, "No JSON structure found in quick assessment"
            
            json_text = cleaned_response[json_start:json_end + 1]
            parsed_data = json.loads(json_text)
            
            # Validate quick assessment structure
            if "quick_assessment" not in parsed_data:
                return False, None, "Missing quick_assessment section"
            
            required_fields = ["market_potential", "competitive_landscape", "next_step"]
            for field in required_fields:
                if field not in parsed_data["quick_assessment"]:
                    return False, None, f"Missing required field: {field}"
            
            return True, parsed_data, None
            
        except json.JSONDecodeError as e:
            return False, None, f"JSON parsing failed: {str(e)}"
        except Exception as e:
            return False, None, f"Validation error: {str(e)}" 