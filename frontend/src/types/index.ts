// Types for the improved backend API structure

export interface AnalysisMetadata {
  confidence_score: number;
  analysis_depth: string;
  data_sources_used: string[];
  analysis_timestamp?: string;
}

export interface MarketAssessment {
  overall_score: number;
  verdict: string;
  market_saturation: string;
  entry_barriers: string;
  market_timing: string;
}

export interface CompetitorAnalysis {
  name: string;
  strengths: string[];
  weaknesses: string[];
  market_position: string;
  customer_pain_points: string[];
  differentiation_gaps: string[];
}

export interface CompetitiveLandscape {
  existing_solutions: CompetitorAnalysis[];
  market_gaps: string[];
  competitive_advantages: string[];
  market_saturation_level: string;
}

export interface UniquenessAnalysis {
  novelty_score: number;
  differentiation_factors: string[];
  copycat_risk: string;
  innovation_level: string;
  unique_value_proposition: string;
}

export interface BusinessViability {
  customer_value_proposition: string;
  target_market_size: string;
  monetization_potential: string;
  pricing_strategy: string;
  customer_acquisition_cost: string;
  unit_economics: string;
}

export interface RiskAssessment {
  market_risks: string[];
  execution_risks: string[];
  competitive_risks: string[];
  mitigation_strategies: string[];
  risk_level: string;
}

export interface ValueEnhancementRoadmap {
  current_gaps: string[];
  differentiation_opportunities: string[];
  feature_prioritization: string[];
  market_positioning: string[];
  competitive_response_strategy: string[];
}

export interface StrategicRecommendations {
  market_entry_strategy: string;
  pivot_suggestions: string[];
  success_factors: string[];
  next_steps: string[];
  timeline_recommendations: string;
}

export interface ComprehensiveAnalysis {
  analysis_metadata: AnalysisMetadata;
  market_assessment: MarketAssessment;
  competitive_landscape: CompetitiveLandscape;
  uniqueness_analysis: UniquenessAnalysis;
  business_viability: BusinessViability;
  risk_assessment: RiskAssessment;
  value_enhancement_roadmap: ValueEnhancementRoadmap;
  strategic_recommendations: StrategicRecommendations;
}

export interface RawData {
  trends: any;
  competitors: any;
  reddit: any;
}

export interface ValidationResult {
  idea: string;
  analysis: ComprehensiveAnalysis | null;
  raw_data: RawData;
  timestamp: string;
  api_status: {
    gemini: boolean;
    tavily: boolean;
    google_trends: boolean;
    reddit: boolean;
  };
  execution_time: number;
  error: string | null;
}

// File upload types
export interface FileUpload {
  file: File;
  content: string;
  type: "text" | "pdf" | "docx";
}

// Processing status types
export type ProcessingStatus = "idle" | "processing" | "completed" | "error";
