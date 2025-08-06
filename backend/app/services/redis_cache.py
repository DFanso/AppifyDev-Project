"""
Redis caching service for the tech news aggregator
Provides centralized caching functionality for API responses
"""

import json
import logging
from typing import Any, Optional, Union, List, Dict
from datetime import timedelta
import redis
import os
from functools import wraps

logger = logging.getLogger(__name__)

class RedisCache:
    """Redis cache manager with JSON serialization support"""
    
    def __init__(self):
        self.redis_client = None
        self.is_connected = False
        self._connect()
    
    def _connect(self):
        """Initialize Redis connection with fallback handling"""
        try:
            redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
            
            # Parse Redis URL for different deployment scenarios
            if redis_url.startswith('redis://'):
                self.redis_client = redis.from_url(
                    redis_url,
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    retry_on_timeout=True
                )
            else:
                # Fallback to localhost
                self.redis_client = redis.Redis(
                    host='localhost',
                    port=6379,
                    db=0,
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    retry_on_timeout=True
                )
            
            # Test connection
            self.redis_client.ping()
            self.is_connected = True
            logger.info("✅ Redis cache connected successfully")
            
        except Exception as e:
            logger.warning(f"⚠️ Redis connection failed: {e}")
            logger.info("📝 Continuing without cache (fallback mode)")
            self.is_connected = False
    
    def _serialize_value(self, value: Any) -> str:
        """Serialize value to JSON string"""
        try:
            return json.dumps(value, default=str, separators=(',', ':'))
        except Exception as e:
            logger.error(f"❌ Serialization failed: {e}")
            return ""
    
    def _deserialize_value(self, value: str) -> Any:
        """Deserialize JSON string to Python object"""
        try:
            return json.loads(value)
        except Exception as e:
            logger.error(f"❌ Deserialization failed: {e}")
            return None
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.is_connected:
            return None
        
        try:
            cached_value = self.redis_client.get(key)
            if cached_value is None:
                return None
            
            return self._deserialize_value(cached_value)
        except Exception as e:
            logger.error(f"❌ Cache GET failed for key '{key}': {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Set value in cache with TTL in seconds"""
        if not self.is_connected:
            return False
        
        try:
            serialized_value = self._serialize_value(value)
            if not serialized_value:
                return False
            
            self.redis_client.setex(key, ttl, serialized_value)
            return True
        except Exception as e:
            logger.error(f"❌ Cache SET failed for key '{key}': {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.is_connected:
            return False
        
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.error(f"❌ Cache DELETE failed for key '{key}': {e}")
            return False
    
    def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern"""
        if not self.is_connected:
            return 0
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"❌ Cache DELETE PATTERN failed for '{pattern}': {e}")
            return 0
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        if not self.is_connected:
            return False
        
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error(f"❌ Cache EXISTS failed for key '{key}': {e}")
            return False
    
    def get_ttl(self, key: str) -> int:
        """Get TTL for key (-1 if no expire, -2 if not exists)"""
        if not self.is_connected:
            return -2
        
        try:
            return self.redis_client.ttl(key)
        except Exception as e:
            logger.error(f"❌ Cache TTL failed for key '{key}': {e}")
            return -2

# Global cache instance
cache = RedisCache()

def cached(ttl: int = 300, key_prefix: str = ""):
    """
    Decorator for caching function results
    
    Args:
        ttl: Time to live in seconds (default: 5 minutes)
        key_prefix: Optional prefix for cache keys
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"🎯 Cache HIT: {cache_key}")
                return cached_result
            
            # Cache miss - execute function
            logger.debug(f"💭 Cache MISS: {cache_key}")
            result = await func(*args, **kwargs)
            
            # Cache the result
            cache.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator

# Cache key generators for consistent naming
class CacheKeys:
    """Centralized cache key generation"""
    
    @staticmethod
    def articles_list(page: int, page_size: int, category: str = None, source: str = None) -> str:
        params = f"page={page}&size={page_size}"
        if category:
            params += f"&cat={category}"
        if source:
            params += f"&src={source}"
        return f"articles:list:{params}"
    
    @staticmethod
    def article_detail(article_id: int) -> str:
        return f"articles:detail:{article_id}"
    
    @staticmethod
    def trending_topics(hours: int = 24, limit: int = 10) -> str:
        return f"trending:topics:h={hours}&l={limit}"
    
    @staticmethod
    def trending_categories(hours: int = 24) -> str:
        return f"trending:categories:h={hours}"
    
    @staticmethod
    def trending_sources(hours: int = 24) -> str:
        return f"trending:sources:h={hours}"
    
    @staticmethod
    def search_results(query: str, page: int = 1, filters: str = "") -> str:
        return f"search:results:{query}:p={page}&f={filters}"
    
    @staticmethod
    def search_suggestions(query: str, limit: int = 10) -> str:
        return f"search:suggestions:{query}:l={limit}"
    
    @staticmethod
    def bookmarks_list(user_id: str) -> str:
        return f"bookmarks:list:{user_id}"

# Cache invalidation helpers
class CacheInvalidator:
    """Helper for cache invalidation patterns"""
    
    @staticmethod
    def invalidate_articles():
        """Invalidate all articles-related cache"""
        cache.delete_pattern("articles:*")
        logger.info("🗑️ Invalidated articles cache")
    
    @staticmethod
    def invalidate_trending():
        """Invalidate all trending-related cache"""
        cache.delete_pattern("trending:*")
        logger.info("🗑️ Invalidated trending cache")
    
    @staticmethod
    def invalidate_search():
        """Invalidate all search-related cache"""
        cache.delete_pattern("search:*")
        logger.info("🗑️ Invalidated search cache")
    
    @staticmethod
    def invalidate_user_bookmarks(user_id: str):
        """Invalidate specific user's bookmarks cache"""
        key = CacheKeys.bookmarks_list(user_id)
        cache.delete(key)
        logger.info(f"🗑️ Invalidated bookmarks cache for user: {user_id}")
    
    @staticmethod
    def invalidate_all():
        """Nuclear option - clear all cache"""
        if cache.is_connected:
            try:
                cache.redis_client.flushdb()
                logger.warning("💥 CLEARED ALL CACHE")
            except Exception as e:
                logger.error(f"❌ Failed to clear all cache: {e}")

logger.info("📦 Redis cache service initialized")