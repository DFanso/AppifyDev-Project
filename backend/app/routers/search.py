from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import Optional, List
from datetime import datetime

from ..database import get_db, Article
from ..schemas import ArticleListResponse, SearchRequest

router = APIRouter()

@router.get("/", response_model=ArticleListResponse)
async def search_articles(
    q: str = Query(..., description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    source: Optional[str] = Query(None, description="Filter by source"),
    sentiment: Optional[str] = Query(None, description="Filter by sentiment"),
    date_from: Optional[datetime] = Query(None, description="Filter articles from this date"),
    date_to: Optional[datetime] = Query(None, description="Filter articles to this date"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Search articles with full-text search and filters"""
    
    # Start with base query
    query = db.query(Article)
    
    # Apply text search (search in title, content, and summary)
    if q and q.strip():
        search_term = f"%{q}%"
        query = query.filter(
            or_(
                Article.title.ilike(search_term),
                Article.content.ilike(search_term),
                Article.summary.ilike(search_term)
            )
        )
    
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
    
    # Order by relevance (articles with search term in title first) and then by date
    if q and q.strip():
        query = query.order_by(
            Article.title.ilike(f"%{q}%").desc(),
            Article.published_at.desc()
        )
    else:
        query = query.order_by(Article.published_at.desc())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
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

@router.post("/", response_model=ArticleListResponse)
async def advanced_search(
    search_request: SearchRequest,
    db: Session = Depends(get_db)
):
    """Advanced search with complex filters"""
    
    query = db.query(Article)
    
    # Apply text search
    if search_request.query and search_request.query.strip():
        search_term = f"%{search_request.query}%"
        query = query.filter(
            or_(
                Article.title.ilike(search_term),
                Article.content.ilike(search_term),
                Article.summary.ilike(search_term)
            )
        )
    
    # Apply filters if provided
    if search_request.filters:
        filters = search_request.filters
        
        if filters.category:
            query = query.filter(Article.category == filters.category)
        
        if filters.source:
            query = query.filter(Article.source == filters.source)
        
        if filters.sentiment:
            query = query.filter(Article.sentiment == filters.sentiment)
        
        if filters.date_from:
            query = query.filter(Article.published_at >= filters.date_from)
        
        if filters.date_to:
            query = query.filter(Article.published_at <= filters.date_to)
        
        if filters.search_query:
            additional_term = f"%{filters.search_query}%"
            query = query.filter(
                or_(
                    Article.title.ilike(additional_term),
                    Article.content.ilike(additional_term),
                    Article.summary.ilike(additional_term)
                )
            )
    
    # Order by relevance and date
    if search_request.query and search_request.query.strip():
        query = query.order_by(
            Article.title.ilike(f"%{search_request.query}%").desc(),
            Article.published_at.desc()
        )
    else:
        query = query.order_by(Article.published_at.desc())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (search_request.page - 1) * search_request.page_size
    articles = query.offset(offset).limit(search_request.page_size).all()
    
    has_next = total > (search_request.page * search_request.page_size)
    
    return ArticleListResponse(
        articles=articles,
        total=total,
        page=search_request.page,
        page_size=search_request.page_size,
        has_next=has_next
    )

@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., min_length=2, description="Partial search query"),
    limit: int = Query(10, ge=1, le=20, description="Number of suggestions"),
    db: Session = Depends(get_db)
):
    """Get search suggestions based on article titles and keywords"""
    
    search_term = f"%{q}%"
    
    # Get article titles that match the search term
    suggestions = db.query(Article.title).filter(
        Article.title.ilike(search_term)
    ).distinct().limit(limit).all()
    
    # Extract unique words from matching titles
    title_words = set()
    for (title,) in suggestions:
        words = title.lower().split()
        for word in words:
            if q.lower() in word and len(word) > 2:
                title_words.add(word)
    
    # Return suggestions sorted by relevance (exact matches first)
    suggestion_list = list(title_words)
    suggestion_list.sort(key=lambda x: (x.startswith(q.lower()), x))
    
    return {"suggestions": suggestion_list[:limit]}

@router.get("/popular")
async def get_popular_searches(
    limit: int = Query(10, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get popular search terms based on article categories and trending topics"""
    
    # Get popular categories
    popular_categories = db.query(
        Article.category,
        func.count(Article.id).label('count')
    ).filter(
        Article.category.isnot(None)
    ).group_by(Article.category).order_by(func.count(Article.id).desc()).limit(5).all()
    
    # Get popular sources
    popular_sources = db.query(
        Article.source,
        func.count(Article.id).label('count')
    ).filter(
        Article.source.isnot(None)
    ).group_by(Article.source).order_by(func.count(Article.id).desc()).limit(5).all()
    
    # Combine and format results
    popular_terms = []
    
    for category, count in popular_categories:
        popular_terms.append({
            "term": category,
            "type": "category",
            "count": count
        })
    
    for source, count in popular_sources:
        popular_terms.append({
            "term": source,
            "type": "source",
            "count": count
        })
    
    # Sort by count and return top results
    popular_terms.sort(key=lambda x: x["count"], reverse=True)
    
    return {"popular_searches": popular_terms[:limit]}