from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from ..database import get_db, Article
from ..schemas import ArticleResponse, ArticleListResponse, ArticleFilter
from ..services.redis_cache import cache, CacheKeys

router = APIRouter()

@router.get("/", response_model=ArticleListResponse)
async def get_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    sentiment: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Get paginated list of articles with optional filtering"""
    # Generate cache key
    cache_key = CacheKeys.articles_list(
        page=page, 
        page_size=page_size, 
        category=category, 
        source=source
    )
    
    # Add date filters to cache key if present
    if date_from or date_to or sentiment:
        cache_key += f"&df={date_from}&dt={date_to}&sent={sentiment}"
    
    # Try cache first (5 minute TTL for articles)
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    
    # Cache miss - query database
    query = db.query(Article)
    
    # Apply filters
    if category:
        query = query.filter(Article.category == category)
    if source:
        query = query.filter(Article.source == source)
    if sentiment:
        query = query.filter(Article.sentiment == sentiment)
    if date_from:
        query = query.filter(Article.published_at >= date_from)
    if date_to:
        query = query.filter(Article.published_at <= date_to)
    
    # Order by published date (newest first)
    query = query.order_by(Article.published_at.desc())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    articles = query.offset(offset).limit(page_size).all()
    
    has_next = total > (page * page_size)
    
    result = ArticleListResponse(
        articles=articles,
        total=total,
        page=page,
        page_size=page_size,
        has_next=has_next
    )
    
    # Cache the result for 5 minutes
    cache.set(cache_key, result.dict(), ttl=300)
    
    return result

@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get a specific article by ID"""
    # Try cache first (longer TTL for individual articles - 15 minutes)
    cache_key = CacheKeys.article_detail(article_id)
    cached_article = cache.get(cache_key)
    if cached_article is not None:
        return cached_article
    
    # Cache miss - query database
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Cache the article for 15 minutes (individual articles change less frequently)
    cache.set(cache_key, article.__dict__, ttl=900)
    
    return article

@router.get("/category/{category}", response_model=ArticleListResponse)
async def get_articles_by_category(
    category: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get articles filtered by category"""
    query = db.query(Article).filter(Article.category == category)
    query = query.order_by(Article.published_at.desc())
    
    total = query.count()
    offset = (page - 1) * page_size
    articles = query.offset(offset).limit(page_size).all()
    
    has_next = total > (page * page_size)
    
    return ArticleListResponse(
        articles=articles,
        total=total,
        page=page,
        page_size=page_size,
        has_next=has_next
    )

@router.get("/source/{source}", response_model=ArticleListResponse)
async def get_articles_by_source(
    source: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get articles filtered by source"""
    query = db.query(Article).filter(Article.source == source)
    query = query.order_by(Article.published_at.desc())
    
    total = query.count()
    offset = (page - 1) * page_size
    articles = query.offset(offset).limit(page_size).all()
    
    has_next = total > (page * page_size)
    
    return ArticleListResponse(
        articles=articles,
        total=total,
        page=page,
        page_size=page_size,
        has_next=has_next
    )

@router.get("/recent/{hours}", response_model=ArticleListResponse)
async def get_recent_articles(
    hours: int = 24,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get articles from the last N hours"""
    since = datetime.utcnow() - timedelta(hours=hours)
    query = db.query(Article).filter(Article.published_at >= since)
    query = query.order_by(Article.published_at.desc())
    
    total = query.count()
    offset = (page - 1) * page_size
    articles = query.offset(offset).limit(page_size).all()
    
    has_next = total > (page * page_size)
    
    return ArticleListResponse(
        articles=articles,
        total=total,
        page=page,
        page_size=page_size,
        has_next=has_next
    )