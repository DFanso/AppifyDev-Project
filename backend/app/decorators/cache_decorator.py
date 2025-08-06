"""
Simple cache decorator to eliminate duplicated caching logic
"""

import logging
import hashlib
from typing import Any, Callable, Optional
from functools import wraps

from ..services.redis_cache import cache

logger = logging.getLogger(__name__)

def cached(ttl: int = 300, key_prefix: str = ""):
    """
    Simple cache decorator for FastAPI endpoints
    
    Args:
        ttl: Time to live in seconds (default: 5 minutes)
        key_prefix: Optional prefix for cache keys
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate a simple cache key from function name and all arguments
            func_name = f"{key_prefix}:{func.__name__}" if key_prefix else func.__name__
            
            # Create a deterministic hash from all arguments
            args_str = str(args) + str(sorted(kwargs.items()))
            args_hash = hashlib.md5(args_str.encode()).hexdigest()[:12]  # Short hash
            cache_key = f"{func_name}:{args_hash}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"🎯 Cache HIT: {cache_key}")
                return cached_result
            
            # Cache miss - execute function
            logger.debug(f"💭 Cache MISS: {cache_key}")
            result = await func(*args, **kwargs)
            
            # Serialize result for caching
            if hasattr(result, 'dict'):
                # Pydantic models
                cache_data = result.dict()
            elif isinstance(result, list) and result and hasattr(result[0], 'dict'):
                # List of Pydantic models
                cache_data = [item.dict() for item in result]
            elif hasattr(result, '__dict__') and not isinstance(result, type):
                # SQLAlchemy objects
                cache_data = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}
            else:
                # Plain Python objects (dict, list, etc.)
                cache_data = result
            
            # Cache the result
            cache.set(cache_key, cache_data, ttl)
            
            return result
        return wrapper
    return decorator