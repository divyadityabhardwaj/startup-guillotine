# import logging
# import time
# from typing import Optional, Dict, Any, List
# from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
# from tavily import TavilyClient
# from urllib.parse import urlparse
# from app.core.config import settings

# logger = logging.getLogger(__name__)

# class TavilyService:
#     """Robust Tavily service for competitor research"""
    
#     def __init__(self):
#         self.is_available = False
#         self.client = None
#         self._initialize()
    
#     def _initialize(self):
#         """Initialize Tavily client"""
#         try:
#             if not settings.TAVILY_API_KEY:
#                 logger.warning("Tavily API key not provided")
#                 return
            
#             self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)
            
#             # Test connection with a simple search
#             test_response = self.client.search("test", max_results=1)
            
#             if test_response and "results" in test_response:
#                 self.is_available = True
#                 logger.info("Tavily service initialized successfully")
#             else:
#                 logger.error("Tavily test request failed")
                
#         except Exception as e:
#             logger.error(f"Failed to initialize Tavily service: {str(e)}")
#             self.is_available = False
    
#     @retry(
#         wait=wait_exponential(multiplier=1, min=2, max=30),
#         stop=stop_after_attempt(3),
#         retry=retry_if_exception_type(Exception),
#         before_sleep=lambda retry_state: logger.warning(f"Retrying Tavily request (attempt {retry_state.attempt_number})")
#     )
#     def search_competitors(self, idea: str, max_results: Optional[int] = None) -> Dict[str, Any]:
#         """Search for competitors and alternatives"""
        
#         if not self.is_available:
#             logger.error("Tavily service not available")
#             return {
#                 "query": idea,
#                 "error": "Tavily service not available",
#                 "top_domains": [],
#                 "competitor_count": 0
#             }
        
#         try:
#             # Build search query
#             search_query = self._build_competitor_query(idea)
#             max_results = max_results or settings.MAX_TAVILY_RESULTS
            
#             logger.info(f"Searching for competitors: {search_query}")
            
#             # Perform search
#             start_time = time.time()
#             response = self.client.search(
#                 search_query,
#                 max_results=max_results,
#                 search_depth="advanced"
#             )
#             search_time = time.time() - start_time
            
#             if not response or "results" not in response:
#                 logger.error("Tavily response is invalid")
#                 return {
#                     "query": idea,
#                     "error": "Invalid response from Tavily",
#                     "top_domains": [],
#                     "competitor_count": 0
#                 }
            
#             # Process results
#             results = response.get("results", [])
#             processed_results = self._process_search_results(results)
            
#             # Extract domains
#             domains = [result["domain"] for result in processed_results if result["domain"]]
#             unique_domains = list(dict.fromkeys(domains))  # Remove duplicates while preserving order
            
#             result = {
#                 "query": idea,
#                 "search_query": search_query,
#                 "top_domains": unique_domains,
#                 "competitor_count": len(processed_results),
#                 "search_time": search_time,
#                 "raw_results": processed_results
#             }
            
#             logger.info(f"Tavily search completed in {search_time:.2f}s, found {len(processed_results)} results")
#             return result
            
#         except Exception as e:
#             error_msg = f"Tavily search failed: {str(e)}"
#             logger.error(error_msg)
#             return {
#                 "query": idea,
#                 "error": error_msg,
#                 "top_domains": [],
#                 "competitor_count": 0
#             }
    
#     def _build_competitor_query(self, idea: str) -> str:
#         """Build optimized search query for competitor research"""
        
#         # Extract key terms
#         key_terms = idea.lower().split()
        
#         # Common competitor-related terms
#         competitor_terms = [
#             "competitors", "alternatives", "similar", "competition",
#             "companies", "apps", "tools", "platforms", "solutions"
#         ]
        
#         # Build query
#         if len(key_terms) <= 3:
#             # Short idea, add more context
#             query = f"{idea} competitors alternatives similar companies"
#         else:
#             # Longer idea, be more specific
#             query = f"{idea} competitors alternatives"
        
#         # Add industry-specific terms if idea is short
#         if len(query.split()) < 5:
#             query += " companies tools platforms"
        
#         return query
    
#     def _process_search_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         """Process and clean search results"""
#         processed = []
        
#         for result in results:
#             try:
#                 # Extract basic info
#                 title = result.get("title", "").strip()
#                 url = result.get("url", "").strip()
#                 content = result.get("content", "").strip()
                
#                 if not title or not url:
#                     continue
                
#                 # Extract domain
#                 domain = self._extract_domain(url)
                
#                 # Skip if no valid domain
#                 if not domain:
#                     continue
                
#                 # Filter out common non-competitor domains
#                 if self._is_non_competitor_domain(domain):
#                     continue
                
#                 processed_result = {
#                     "title": title,
#                     "url": url,
#                     "domain": domain,
#                     "content_preview": content[:200] + "..." if len(content) > 200 else content
#                 }
                
#                 processed.append(processed_result)
                
#             except Exception as e:
#                 logger.warning(f"Failed to process result: {str(e)}")
#                 continue
        
#         return processed
    
#     def _extract_domain(self, url: str) -> str:
#         """Extract domain from URL"""
#         try:
#             parsed = urlparse(url)
#             domain = parsed.netloc.lower()
            
#             # Remove www prefix
#             if domain.startswith("www."):
#                 domain = domain[4:]
            
#             # Basic validation
#             if "." in domain and len(domain) > 2:
#                 return domain
#             else:
#                 return ""
                
#         except Exception as e:
#             logger.warning(f"Failed to extract domain from {url}: {str(e)}")
#             return ""
    
#     def _is_non_competitor_domain(self, domain: str) -> bool:
#         """Check if domain should be filtered out"""
        
#         # Common non-competitor domains
#         non_competitor_patterns = [
#             "wikipedia.org",
#             "youtube.com",
#             "facebook.com",
#             "twitter.com",
#             "linkedin.com",
#             "reddit.com",
#             "medium.com",
#             "quora.com",
#             "stackoverflow.com",
#             "github.com",
#             "crunchbase.com",
#             "angel.co",
#             "producthunt.com",
#             "techcrunch.com",
#             "venturebeat.com",
#             "forbes.com",
#             "bloomberg.com",
#             "reuters.com",
#             "cnn.com",
#             "bbc.com"
#         ]
        
#         return any(pattern in domain for pattern in non_competitor_patterns)
    
#     def search_with_fallback(self, idea: str) -> Dict[str, Any]:
#         """Search with multiple fallback strategies"""
        
#         # Try primary search
#         result = self.search_competitors(idea)
        
#         if result.get("error") or result["competitor_count"] == 0:
#             logger.info("Primary search failed or returned no results, trying fallback")
            
#             # Fallback 1: Broader search
#             fallback_result = self.search_competitors(f"{idea} companies", max_results=20)
            
#             if fallback_result.get("error") or fallback_result["competitor_count"] == 0:
#                 # Fallback 2: Industry-based search
#                 industry_terms = self._extract_industry_terms(idea)
#                 if industry_terms:
#                     fallback_result = self.search_competitors(f"{industry_terms} companies", max_results=15)
            
#             # Use fallback if it has better results
#             if (not fallback_result.get("error") and 
#                 fallback_result["competitor_count"] > result["competitor_count"]):
#                 result = fallback_result
#                 result["used_fallback"] = True
        
#         return result
    
#     def _extract_industry_terms(self, idea: str) -> Optional[str]:
#         """Extract industry-related terms from idea"""
        
#         # Common industry keywords
#         industry_keywords = [
#             "ai", "artificial intelligence", "machine learning", "ml",
#             "fintech", "healthtech", "edtech", "proptech", "legaltech",
#             "ecommerce", "marketplace", "saas", "b2b", "b2c",
#             "mobile app", "web app", "platform", "tool", "software",
#             "sustainability", "green tech", "clean tech", "renewable",
#             "blockchain", "crypto", "defi", "web3",
#             "iot", "internet of things", "smart home", "wearables"
#         ]
        
#         idea_lower = idea.lower()
#         found_terms = [term for term in industry_keywords if term in idea_lower]
        
#         if found_terms:
#             return " ".join(found_terms[:3])  # Return top 3 terms
        
#         return None
    
#     def get_service_status(self) -> Dict[str, Any]:
#         """Get service status"""
#         return {
#             "available": self.is_available,
#             "api_key_configured": bool(settings.TAVILY_API_KEY),
#             "max_results": settings.MAX_TAVILY_RESULTS
#         } 