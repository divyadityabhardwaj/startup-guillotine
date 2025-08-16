"use client";

import { ValidationResult as ValidationResultType } from "@/types";
import { motion } from "framer-motion";
import {
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  Lightbulb,
  Users,
  DollarSign,
  Target,
  Shield,
  Zap,
  Clock,
  BarChart3,
  Eye,
  CheckCircle,
  XCircle,
  Info,
} from "lucide-react";

interface ValidationResultProps {
  result: ValidationResultType;
}

export default function ValidationResult({ result }: ValidationResultProps) {
  if (!result.analysis) {
    return (
      <div className="card text-center">
        <AlertTriangle className="w-16 h-16 text-red-500 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-red-600 mb-2">
          Analysis Failed
        </h3>
        <p className="text-secondary-600">
          {result.error ||
            "Unable to analyze this startup idea. Please try again."}
        </p>
      </div>
    );
  }

  const { analysis, raw_data, execution_time } = result;

  const getScoreColor = (score: number) => {
    if (score >= 75) return "text-green-600 bg-green-100";
    if (score >= 50) return "text-yellow-600 bg-yellow-100";
    return "text-red-600 bg-red-100";
  };

  const getScoreEmoji = (score: number) => {
    if (score >= 75) return "🚀";
    if (score >= 50) return "🤔";
    return "💀";
  };

  const getConfidenceColor = (score: number) => {
    if (score >= 0.7) return "text-green-600 bg-green-100";
    if (score >= 0.4) return "text-yellow-600 bg-yellow-100";
    return "text-red-600 bg-red-100";
  };

  const getRiskColor = (risk: string) => {
    const riskLower = risk.toLowerCase();
    if (riskLower.includes("low")) return "text-green-600 bg-green-100";
    if (riskLower.includes("medium")) return "text-yellow-600 bg-yellow-100";
    return "text-red-600 bg-red-100";
  };

  return (
    <div className="space-y-6">
      {/* Header with Overall Score */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card text-center"
      >
        <div className="text-6xl mb-4">
          {getScoreEmoji(analysis.market_assessment.overall_score)}
        </div>
        <h2 className="text-2xl font-bold mb-2">Market Assessment Score</h2>
        <div
          className={`inline-flex items-center px-4 py-2 rounded-full text-lg font-bold ${getScoreColor(
            analysis.market_assessment.overall_score
          )}`}
        >
          {analysis.market_assessment.overall_score}/100
        </div>
        <p className="text-lg font-medium text-secondary-700 mt-2">
          {analysis.market_assessment.verdict}
        </p>
        <div className="mt-4 flex justify-center space-x-4 text-sm text-secondary-500">
          <span>Execution time: {execution_time.toFixed(1)}s</span>
          <span>
            Confidence:{" "}
            {(analysis.analysis_metadata.confidence_score * 100).toFixed(0)}%
          </span>
        </div>
      </motion.div>

      {/* Market Assessment */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card"
      >
        <h3 className="text-xl font-semibold mb-4 flex items-center">
          <BarChart3 className="w-5 h-5 mr-2 text-primary-600" />
          Market Assessment
        </h3>
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">
              Market Saturation
            </h4>
            <p className="text-secondary-600">
              {analysis.market_assessment.market_saturation}
            </p>
          </div>
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">
              Entry Barriers
            </h4>
            <p className="text-secondary-600">
              {analysis.market_assessment.entry_barriers}
            </p>
          </div>
          <div className="md:col-span-2">
            <h4 className="font-medium text-secondary-700 mb-2">
              Market Timing
            </h4>
            <p className="text-secondary-600">
              {analysis.market_assessment.market_timing}
            </p>
          </div>
        </div>
      </motion.div>

      {/* Uniqueness Analysis */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="card"
      >
        <h3 className="text-xl font-semibold mb-4 flex items-center">
          <Zap className="w-5 h-5 mr-2 text-primary-600" />
          Uniqueness Analysis
        </h3>
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">
              Novelty Score
            </h4>
            <div
              className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(
                analysis.uniqueness_analysis.novelty_score * 10
              )}`}
            >
              {analysis.uniqueness_analysis.novelty_score}/10
            </div>
          </div>
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">
              Innovation Level
            </h4>
            <p className="text-secondary-600">
              {analysis.uniqueness_analysis.innovation_level}
            </p>
          </div>
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">
              Copycat Risk
            </h4>
            <span
              className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(
                analysis.uniqueness_analysis.copycat_risk
              )}`}
            >
              {analysis.uniqueness_analysis.copycat_risk}
            </span>
          </div>
          <div className="md:col-span-2">
            <h4 className="font-medium text-secondary-700 mb-2">
              Unique Value Proposition
            </h4>
            <p className="text-secondary-600">
              {analysis.uniqueness_analysis.unique_value_proposition}
            </p>
          </div>
        </div>
      </motion.div>

      {/* Business Viability */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="card"
      >
        <h3 className="text-xl font-semibold mb-4 flex items-center">
          <DollarSign className="w-5 h-5 mr-2 text-primary-600" />
          Business Viability
        </h3>
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">
              Target Market Size
            </h4>
            <p className="text-secondary-600">
              {analysis.business_viability.target_market_size}
            </p>
          </div>
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">
              Monetization Potential
            </h4>
            <p className="text-secondary-600">
              {analysis.business_viability.monetization_potential}
            </p>
          </div>
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">
              Customer Acquisition Cost
            </h4>
            <p className="text-secondary-600">
              {analysis.business_viability.customer_acquisition_cost}
            </p>
          </div>
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">
              Unit Economics
            </h4>
            <p className="text-secondary-600">
              {analysis.business_viability.unit_economics}
            </p>
          </div>
          <div className="md:col-span-2">
            <h4 className="font-medium text-secondary-700 mb-2">
              Customer Value Proposition
            </h4>
            <p className="text-secondary-600">
              {analysis.business_viability.customer_value_proposition}
            </p>
          </div>
          <div className="md:col-span-2">
            <h4 className="font-medium text-secondary-700 mb-2">
              Pricing Strategy
            </h4>
            <p className="text-secondary-600">
              {analysis.business_viability.pricing_strategy}
            </p>
          </div>
        </div>
      </motion.div>

      {/* Competitive Landscape */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="card"
      >
        <h3 className="text-xl font-semibold mb-4 flex items-center">
          <Users className="w-5 h-5 mr-2 text-primary-600" />
          Competitive Landscape
        </h3>

        {analysis.competitive_landscape.existing_solutions.length > 0 ? (
          <div className="space-y-4">
            <h4 className="font-medium text-secondary-700 mb-3">
              Existing Solutions
            </h4>
            {analysis.competitive_landscape.existing_solutions.map(
              (competitor, index) => (
                <div
                  key={index}
                  className="p-4 border border-secondary-200 rounded-lg"
                >
                  <h5 className="font-medium text-secondary-900 mb-2">
                    {competitor.name}
                  </h5>
                  <div className="grid md:grid-cols-2 gap-3 text-sm">
                    <div>
                      <span className="font-medium text-green-700">
                        Strengths:
                      </span>
                      <ul className="mt-1 space-y-1">
                        {competitor.strengths.map((strength, i) => (
                          <li key={i} className="flex items-start">
                            <CheckCircle className="w-3 h-3 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                            <span className="text-secondary-600">
                              {strength}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <span className="font-medium text-red-700">
                        Weaknesses:
                      </span>
                      <ul className="mt-1 space-y-1">
                        {competitor.weaknesses.map((weakness, i) => (
                          <li key={i} className="flex items-start">
                            <XCircle className="w-3 h-3 text-red-500 mr-2 mt-0.5 flex-shrink-0" />
                            <span className="text-secondary-600">
                              {weakness}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                  <div className="mt-3 grid md:grid-cols-3 gap-3 text-sm">
                    <div>
                      <span className="font-medium text-secondary-700">
                        Position:
                      </span>
                      <p className="text-secondary-600">
                        {competitor.market_position}
                      </p>
                    </div>
                    <div>
                      <span className="font-medium text-secondary-700">
                        Pain Points:
                      </span>
                      <p className="text-secondary-600">
                        {competitor.customer_pain_points.join(", ")}
                      </p>
                    </div>
                    <div>
                      <span className="font-medium text-secondary-700">
                        Gaps:
                      </span>
                      <p className="text-secondary-600">
                        {competitor.differentiation_gaps.join(", ")}
                      </p>
                    </div>
                  </div>
                </div>
              )
            )}
          </div>
        ) : (
          <div className="text-center py-6 text-secondary-500">
            <Info className="w-12 h-12 mx-auto mb-2 text-secondary-400" />
            <p>No direct competitors found in this analysis</p>
          </div>
        )}

        <div className="mt-6 grid md:grid-cols-2 gap-4">
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">Market Gaps</h4>
            <ul className="space-y-1">
              {analysis.competitive_landscape.market_gaps.map((gap, index) => (
                <li key={index} className="flex items-start">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                  <span className="text-secondary-600">{gap}</span>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">
              Competitive Advantages
            </h4>
            <ul className="space-y-1">
              {analysis.competitive_landscape.competitive_advantages.map(
                (advantage, index) => (
                  <li key={index} className="flex items-start">
                    <div className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span className="text-secondary-600">{advantage}</span>
                  </li>
                )
              )}
            </ul>
          </div>
        </div>

        <div className="mt-4">
          <h4 className="font-medium text-secondary-700 mb-2">
            Market Saturation Analysis
          </h4>
          <p className="text-secondary-600">
            {analysis.competitive_landscape.market_saturation_level}
          </p>
        </div>
      </motion.div>

      {/* Risk Assessment */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="card"
      >
        <h3 className="text-xl font-semibold mb-4 flex items-center">
          <Shield className="w-5 h-5 mr-2 text-primary-600" />
          Risk Assessment
        </h3>
        <div className="mb-4">
          <span
            className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(
              analysis.risk_assessment.risk_level
            )}`}
          >
            Overall Risk Level: {analysis.risk_assessment.risk_level}
          </span>
        </div>
        <div className="grid md:grid-cols-3 gap-4">
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">
              Market Risks
            </h4>
            <ul className="space-y-1">
              {analysis.risk_assessment.market_risks.map((risk, index) => (
                <li key={index} className="flex items-start">
                  <AlertTriangle className="w-3 h-3 text-red-500 mr-2 mt-0.5 flex-shrink-0" />
                  <span className="text-secondary-600 text-sm">{risk}</span>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">
              Execution Risks
            </h4>
            <ul className="space-y-1">
              {analysis.risk_assessment.execution_risks.map((risk, index) => (
                <li key={index} className="flex items-start">
                  <AlertTriangle className="w-3 h-3 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                  <span className="text-secondary-600 text-sm">{risk}</span>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">
              Competitive Risks
            </h4>
            <ul className="space-y-1">
              {analysis.risk_assessment.competitive_risks.map((risk, index) => (
                <li key={index} className="flex items-start">
                  <AlertTriangle className="w-3 h-3 text-yellow-500 mr-2 mt-0.5 flex-shrink-0" />
                  <span className="text-secondary-600 text-sm">{risk}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
        <div className="mt-4">
          <h4 className="font-medium text-secondary-700 mb-2">
            Mitigation Strategies
          </h4>
          <ul className="space-y-1">
            {analysis.risk_assessment.mitigation_strategies.map(
              (strategy, index) => (
                <li key={index} className="flex items-start">
                  <CheckCircle className="w-3 h-3 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                  <span className="text-secondary-600">{strategy}</span>
                </li>
              )
            )}
          </ul>
        </div>
      </motion.div>

      {/* Strategic Recommendations */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="card"
      >
        <h3 className="text-xl font-semibold mb-4 flex items-center">
          <Target className="w-5 h-5 mr-2 text-primary-600" />
          Strategic Recommendations
        </h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">
              Market Entry Strategy
            </h4>
            <p className="text-secondary-600">
              {analysis.strategic_recommendations.market_entry_strategy}
            </p>
          </div>
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">
              Success Factors
            </h4>
            <ul className="space-y-1">
              {analysis.strategic_recommendations.success_factors.map(
                (factor, index) => (
                  <li key={index} className="flex items-start">
                    <CheckCircle className="w-3 h-3 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-secondary-600 text-sm">{factor}</span>
                  </li>
                )
              )}
            </ul>
          </div>
        </div>

        <div className="mt-6">
          <h4 className="font-medium text-secondary-700 mb-2">Next Steps</h4>
          <ul className="space-y-2">
            {analysis.strategic_recommendations.next_steps.map(
              (step, index) => (
                <li key={index} className="flex items-start">
                  <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                  <span className="text-secondary-600">{step}</span>
                </li>
              )
            )}
          </ul>
        </div>

        <div className="mt-6">
          <h4 className="font-medium text-secondary-700 mb-2">
            Timeline Recommendations
          </h4>
          <p className="text-secondary-600">
            {analysis.strategic_recommendations.timeline_recommendations}
          </p>
        </div>

        {analysis.strategic_recommendations.pivot_suggestions.length > 0 && (
          <div className="mt-6">
            <h4 className="font-medium text-secondary-700 mb-2">
              Pivot Suggestions
            </h4>
            <ul className="space-y-1">
              {analysis.strategic_recommendations.pivot_suggestions.map(
                (pivot, index) => (
                  <li key={index} className="flex items-start">
                    <Lightbulb className="w-3 h-3 text-yellow-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-secondary-600">{pivot}</span>
                  </li>
                )
              )}
            </ul>
          </div>
        )}
      </motion.div>

      {/* Value Enhancement Roadmap */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7 }}
        className="card"
      >
        <h3 className="text-xl font-semibold mb-4 flex items-center">
          <TrendingUp className="w-5 h-5 mr-2 text-primary-600" />
          Value Enhancement Roadmap
        </h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">
              Current Gaps
            </h4>
            <ul className="space-y-1">
              {analysis.value_enhancement_roadmap.current_gaps.map(
                (gap, index) => (
                  <li key={index} className="flex items-start">
                    <div className="w-2 h-2 bg-red-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span className="text-secondary-600">{gap}</span>
                  </li>
                )
              )}
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-secondary-700 mb-2">
              Differentiation Opportunities
            </h4>
            <ul className="space-y-1">
              {analysis.value_enhancement_roadmap.differentiation_opportunities.map(
                (opportunity, index) => (
                  <li key={index} className="flex items-start">
                    <div className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span className="text-secondary-600">{opportunity}</span>
                  </li>
                )
              )}
            </ul>
          </div>
        </div>

        <div className="mt-6">
          <h4 className="font-medium text-secondary-700 mb-2">
            Feature Prioritization
          </h4>
          <ul className="space-y-2">
            {analysis.value_enhancement_roadmap.feature_prioritization.map(
              (feature, index) => (
                <li key={index} className="flex items-start">
                  <Clock className="w-3 h-3 text-blue-500 mr-2 mt-0.5 flex-shrink-0" />
                  <span className="text-secondary-600">{feature}</span>
                </li>
              )
            )}
          </ul>
        </div>
      </motion.div>

      {/* Raw Data Summary */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="card"
      >
        <h3 className="text-xl font-semibold mb-4 flex items-center">
          <Eye className="w-5 h-5 mr-2 text-primary-600" />
          Data Sources Used
        </h3>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="text-center p-4 bg-secondary-50 rounded-lg">
            <h4 className="font-medium text-secondary-700 mb-2">
              Google Trends
            </h4>
            <p className="text-2xl font-bold text-primary-600">
              {raw_data.trends?.interest_score || "N/A"}
            </p>
            <p className="text-sm text-secondary-500">Interest Score</p>
          </div>
          <div className="text-center p-4 bg-secondary-50 rounded-lg">
            <h4 className="font-medium text-secondary-700 mb-2">Competitors</h4>
            <p className="text-2xl font-bold text-primary-600">
              {raw_data.competitors?.competitor_count || "N/A"}
            </p>
            <p className="text-sm text-secondary-500">Found</p>
          </div>
          <div className="text-center p-4 bg-secondary-50 rounded-lg">
            <h4 className="font-medium text-secondary-700 mb-2">Community</h4>
            <p className="text-2xl font-bold text-primary-600">
              {raw_data.reddit?.posts_last_n_days || "N/A"}
            </p>
            <p className="text-sm text-secondary-500">Reddit Posts</p>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
