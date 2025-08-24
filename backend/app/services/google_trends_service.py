# import logging
# import re
# import time
# from typing import Optional, Dict, Any, List
# from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
# from pytrends.request import TrendReq
# from app.core.config import settings

# logger = logging.getLogger(__name__)

# class GoogleTrendsService:
#     """Robust Google Trends service for trend analysis"""
    
#     def __init__(self):
#         self.is_available = False
#         self.client = None
#         self._initialize()
    
#     def _initialize(self):
#         """Initialize Google Trends client"""
#         try:
#             self.client = TrendReq(hl="en-US", tz=360)
#             self.is_available = True
#             logger.info("Google Trends service initialized successfully")
#         except Exception as e:
#             logger.error(f"Failed to initialize Google Trends service: {str(e)}")
#             self.is_available = False
#     @retry(
#         wait=wait_exponential(multiplier=1, min=2, max=30),
#         stop=stop_after_attempt(3),
#         retry=retry_if_exception_type(Exception),
#         before_sleep=lambda retry_state: logger.warning(f"Retrying Google Trends request (attempt {retry_state.attempt_number})")
#     )
#     def get_trends(self, query: str, timeframe: str = "today 12-m") -> Dict[str, Any]:
#         """Get Google Trends data with improved query handling"""
        
#         if not self.is_available:
#             logger.error("Google Trends service not available")
#             return {
#                 "query": query,
#                 "error": "Google Trends service not available",
#                 "cleaned_query": "",
#                 "interest_score": 0,
#                 "trend_direction": "unknown",
#                 "trend_velocity": 0
#             }
        
#         try:
#             # Clean and optimize query
#             cleaned_query = self._clean_query(query)
#             logger.info(f"Google Trends query: '{query}' -> '{cleaned_query}'")
            
#             # Build payload
#             self.client.build_payload([cleaned_query], timeframe=timeframe)
            
#             # Get interest over time
#             df = self.client.interest_over_time()
            
#             if df.empty or cleaned_query not in df.columns:
#                 logger.warning(f"No data found for query: {cleaned_query}")
#                 return {
#                     "query": query,
#                     "cleaned_query": cleaned_query,
#                     "interest_score": 0,
#                     "trend_direction": "unknown",
#                     "trend_velocity": 0,
#                     "error": "No data available for this query"
#                 }
            
#             # Process time series data
#             series = df[cleaned_query].fillna(0).astype(int).tolist()
            
#             # Calculate metrics
#             metrics = self._calculate_trend_metrics(series, timeframe)
            
#             result = {
#                 "query": query,
#                 "cleaned_query": cleaned_query,
#                 "interest_score": metrics["interest_score"],
#                 "trend_direction": metrics["trend_direction"],
#                 "trend_velocity": metrics["trend_velocity"],
#                 "timeframe": timeframe,
#                 "data_points": len(series),
#                 "min_score": min(series) if series else 0,
#                 "max_score": max(series) if series else 0
#             }
            
#             logger.info(f"Google Trends result: {result}")
#             return result
            
#         except Exception as e:
#             error_msg = f"Google Trends failed: {str(e)}"
#             logger.error(error_msg)
#             return {
#                 "query": query,
#                 "error": error_msg,
#                 "cleaned_query": "",
#                 "interest_score": 0,
#                 "trend_direction": "unknown",
#                 "trend_velocity": 0
#             }
    
#     def _clean_query(self, query: str) -> str:
#         """Clean and optimize search query for Google Trends"""
        
#         # Extract key terms that work well with Google Trends
#         key_terms = re.findall(
#             r'\b(ai|artificial intelligence|carbon|footprint|tracker|sustainable|eco|green|digital|assistant|app|platform|tool|software|startup|business|company|service|product)\b',
#             query.lower(),
#             re.I
#         )
        
#         # If we found key terms, use them
#         if key_terms:
#             # Limit to 4 terms to avoid overly complex queries
#             cleaned = " ".join(key_terms[:4])
#         else:
#             # Fallback: extract meaningful words
#             words = re.findall(r'\b\w{3,}\b', query.lower())
#             # Filter out common stop words
#             stop_words = {'the', 'and', 'for', 'with', 'that', 'this', 'are', 'was', 'were', 'will', 'have', 'has', 'had', 'been', 'from', 'they', 'their', 'them', 'there', 'here', 'when', 'where', 'what', 'which', 'who', 'why', 'how', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'among', 'within', 'without', 'against', 'toward', 'towards', 'upon', 'under', 'over', 'behind', 'beside', 'beneath', 'beyond', 'inside', 'outside', 'around', 'across', 'along', 'throughout', 'except', 'despite', 'unless', 'until', 'while', 'although', 'because', 'since', 'though', 'whereas', 'wherever', 'whenever', 'however', 'whatever', 'whichever', 'whoever', 'whomever', 'whichever', 'wherever', 'whenever', 'however', 'whatever', 'whichever', 'whoever', 'whomever'}
#             meaningful_words = [word for word in words if word not in stop_words]
#             cleaned = " ".join(meaningful_words[:4]) if meaningful_words else "carbon footprint tracker"
        
#         # Ensure query is not too long (Google Trends has limits)
#         if len(cleaned) > 50:
#             cleaned = " ".join(cleaned.split()[:4])
        
#         return cleaned
    
#     def _calculate_trend_metrics(self, series: List[int], timeframe: str) -> Dict[str, Any]:
#         """Calculate trend metrics from time series data"""
        
#         if not series:
#             return {
#                 "interest_score": 0,
#                 "trend_direction": "unknown",
#                 "trend_velocity": 0
#             }
        
#         # Calculate average interest score
#         avg_score = int(sum(series) / len(series))
        
#         # Determine trend direction and velocity
#         if len(series) >= 6:
#             # Split into halves for trend analysis
#             first_half = sum(series[:len(series)//2]) / (len(series)//2)
#             last_half = sum(series[len(series)//2:]) / (len(series)//2)
            
#             # Calculate trend direction
#             if last_half > first_half * 1.15:  # 15% increase threshold
#                 direction = "rising"
#             elif last_half < first_half * 0.85:  # 15% decrease threshold
#                 direction = "falling"
#             else:
#                 direction = "steady"
            
#             # Calculate trend velocity (recent vs previous period)
#             if len(series) >= 12:
#                 recent_period = sum(series[-3:]) / 3
#                 previous_period = sum(series[-6:-3]) / 3
                
#                 if previous_period > 0:
#                     velocity = int(((recent_period - previous_period) / previous_period) * 100)
#                 else:
#                     velocity = 0
#             else:
#                 velocity = 0
                
#         else:
#             direction = "steady"
#             velocity = 0
        
#         return {
#             "interest_score": avg_score,
#             "trend_direction": direction,
#             "trend_velocity": velocity
#         }
    
#     def get_trends_with_fallback(self, query: str) -> Dict[str, Any]:
#         """Get trends with multiple fallback strategies"""
        
#         # Try primary timeframe
#         result = self.get_trends(query, "today 12-m")
        
#         if result.get("error") or result["interest_score"] == 0:
#             logger.info("Primary timeframe failed, trying fallback timeframes")
            
#             # Fallback timeframes
#             fallback_timeframes = [
#                 "today 6-m",
#                 "today 3-m", 
#                 "today 1-m",
#                 "today 5-y"
#             ]
            
#             for timeframe in fallback_timeframes:
#                 fallback_result = self.get_trends(query, timeframe)
                
#                 if (not fallback_result.get("error") and 
#                     fallback_result["interest_score"] > result["interest_score"]):
#                     result = fallback_result
#                     result["used_fallback"] = True
#                     logger.info(f"Used fallback timeframe: {timeframe}")
#                     break
        
#         return result
    
#     def get_related_queries(self, query: str) -> Dict[str, Any]:
#         """Get related queries for additional insights"""
        
#         if not self.is_available:
#             return {"error": "Google Trends service not available"}
        
#         try:
#             cleaned_query = self._clean_query(query)
#             self.client.build_payload([cleaned_query], timeframe="today 12-m")
            
#             # Get related queries
#             related_queries = self.client.related_queries()
            
#             if cleaned_query in related_queries:
#                 top_queries = related_queries[cleaned_query].get("top", [])
#                 rising_queries = related_queries[cleaned_query].get("rising", [])
                
#                 return {
#                     "query": query,
#                     "cleaned_query": cleaned_query,
#                     "top_queries": top_queries.to_dict("records") if not top_queries.empty else [],
#                     "rising_queries": rising_queries.to_dict("records") if not rising_queries.empty else []
#                 }
#             else:
#                 return {
#                     "query": query,
#                     "cleaned_query": cleaned_query,
#                     "error": "No related queries found"
#                 }
                
#         except Exception as e:
#             error_msg = f"Failed to get related queries: {str(e)}"
#             logger.error(error_msg)
#             return {"query": query, "error": error_msg}
    
#     def get_service_status(self) -> Dict[str, Any]:
#         """Get service status"""
#         return {
#             "available": self.is_available,
#             "client_initialized": bool(self.client),
#             "default_timeframe": "today 12-m"
#         } 