import logging
import time
from typing import Optional, Dict, Any, List
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
import httpx
from datetime import datetime, timedelta
from app.core.config import settings

logger = logging.getLogger(__name__)

class RedditService:
    """Robust Reddit service for community activity analysis using public search API"""
    
    def __init__(self):
        self.is_available = True
        self.client = httpx.Client(headers={"User-Agent": "startup-guillotine/1.0"})
        logger.info("Reddit service initialized using public search API.")
    
    def _initialize(self):
        # This method is no longer needed as we are not using praw for authentication
        pass
    
    def _refine_search_query(self, idea: str) -> str:
        """Generate optimized Reddit search query"""
        words = idea.lower().split()
        stop_words = {'a', 'an', 'the', 'and', 'or', 'in', 'on', 'for', 'with', 'to', 'of'}
        meaningful_words = [word for word in words if word not in stop_words and len(word) > 2]
        return " ".join(meaningful_words[:5])

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=30),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(httpx.RequestError),
        before_sleep=lambda retry_state: logger.warning(f"Retrying Reddit request (attempt {retry_state.attempt_number})")
    )
    def get_community_activity(self, idea: str) -> Dict[str, Any]:
        """Get Reddit community activity for the idea using public search API"""
        if not self.is_available:
            return {"query": idea, "error": "Reddit service not available", "posts_last_n_days": 0}

        try:
            search_query = self._refine_search_query(idea)
            url = "https://www.reddit.com/search.json"
            params = {"q": search_query, "sort": "new", "t": "month", "limit": settings.REDDIT_LIMIT}
            
            logger.info(f"Searching Reddit with query: '{search_query}'")
            response = self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            posts = data.get("data", {}).get("children", [])
            cutoff_date = datetime.utcnow() - timedelta(days=settings.REDDIT_DAYS)
            
            processed_posts = []
            subreddit_counts = {}
            for post in posts:
                post_data = post.get("data", {})
                post_date = datetime.utcfromtimestamp(post_data.get("created_utc", 0))
                if post_date >= cutoff_date:
                    subreddit = post_data.get("subreddit")
                    processed_posts.append({
                        "score": post_data.get("score"),
                        "num_comments": post_data.get("num_comments"),
                        "subreddit": subreddit,
                        "title": post_data.get("title"),
                        "created_utc": post_data.get("created_utc"),
                        "url": f"https://www.reddit.com{post_data.get('permalink')}"
                    })
                    if subreddit:
                        subreddit_counts[subreddit] = subreddit_counts.get(subreddit, 0) + 1

            result = {
                "query": idea,
                "search_query": search_query,
                "posts_last_n_days": len(processed_posts),
                "total_score": sum(p["score"] for p in processed_posts),
                "total_comments": sum(p["num_comments"] for p in processed_posts),
                "top_subreddits": sorted(subreddit_counts.items(), key=lambda item: item, reverse=True)[:5],
            }

            if processed_posts:
                result["avg_score"] = round(result["total_score"] / len(processed_posts), 2) if len(processed_posts) > 0 else 0
                result["avg_comments"] = round(result["total_comments"] / len(processed_posts), 2) if len(processed_posts) > 0 else 0
                result["sample_posts"] = processed_posts[:3]

            logger.info(f"Reddit search completed, found {len(processed_posts)} posts")
            return result

        except httpx.HTTPStatusError as e:
            error_msg = f"Reddit API request failed with status {e.response.status_code}: {e.response.text}"
            logger.error(error_msg)
            return {"query": idea, "error": error_msg, "posts_last_n_days": 0}
        except Exception as e:
            error_msg = f"An unexpected error occurred during Reddit search: {str(e)}"
            logger.error(error_msg)
            return {"query": idea, "error": error_msg, "posts_last_n_days": 0}

    def get_activity_with_fallback(self, idea: str) -> Dict[str, Any]:
        """Get activity with a simple fallback"""
        result = self.get_community_activity(idea)
        if not result.get("error") and result["posts_last_n_days"] > 0:
            return result

        logger.info("Primary search failed or returned no results, trying broader fallback")
        broader_query = " ".join(idea.split()[:3])
        fallback_result = self.get_community_activity(broader_query)
        if not fallback_result.get("error"):
            fallback_result["used_fallback"] = True
            return fallback_result
        
        return result

    def get_service_status(self) -> Dict[str, Any]:
        """Get service status"""
        return {
            "available": self.is_available,
            "client_initialized": bool(self.client),
            "search_limit": settings.REDDIT_LIMIT,
            "time_window_days": settings.REDDIT_DAYS,
            "api_type": "public_search"
        }