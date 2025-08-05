from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict
from datetime import datetime, timedelta
from collections import Counter
import re

from ..database import get_db, Article, TrendingTopic
from ..schemas import TrendingTopicResponse, ArticleResponse

router = APIRouter()

def extract_keywords(text: str) -> List[str]:
    """Extract keywords from text for trending analysis"""
    if not text:
        return []
    
    # Convert to lowercase and extract words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Common stop words to filter out
    stop_words = {
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
        'after', 'above', 'below', 'between', 'among', 'this', 'that', 'these',
        'those', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
        'can', 'are', 'was', 'were', 'been', 'have', 'has', 'had', 'did', 'does'
    }
    
    # Filter out stop words and keep relevant terms
    keywords = [word for word in words if word not in stop_words and len(word) > 3]
    
    return keywords

@router.get("/topics", response_model=List[TrendingTopicResponse])
async def get_trending_topics(
    hours: int = 24,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get trending topics from recent articles"""
    # Get articles from the last N hours
    since = datetime.utcnow() - timedelta(hours=hours)
    recent_articles = db.query(Article).filter(
        Article.published_at >= since
    ).all()
    
    if not recent_articles:
        return []
    
    # Extract and count keywords
    keyword_counter = Counter()
    article_keywords = {}
    
    for article in recent_articles:
        # Extract keywords from title and content
        title_keywords = extract_keywords(article.title)
        content_keywords = extract_keywords(article.content or "")
        
        # Combine keywords (title keywords get higher weight)
        all_keywords = title_keywords * 3 + content_keywords
        
        # Store keywords for this article
        article_keywords[article.id] = set(title_keywords + content_keywords)
        
        # Update global counter
        keyword_counter.update(all_keywords)
    
    # Get top trending keywords
    trending_keywords = keyword_counter.most_common(limit)
    
    # Build response with related articles
    trending_topics = []
    
    for keyword, count in trending_keywords:
        if count < 2:  # Only include keywords that appear in multiple articles
            continue
        
        # Find articles related to this keyword
        related_articles = [
            article for article in recent_articles
            if article.id in article_keywords and keyword in article_keywords[article.id]
        ]
        
        # Sort by published date (newest first)
        related_articles.sort(key=lambda x: x.published_at or datetime.min, reverse=True)
        
        # Calculate trending score (count + recency factor)
        recency_factor = sum(
            1 / max(1, (datetime.utcnow() - (article.published_at or datetime.utcnow())).total_seconds() / 3600)
            for article in related_articles
        )
        
        score = count + recency_factor
        
        trending_topics.append(TrendingTopicResponse(
            topic=keyword.title(),
            count=count,
            score=score,
            articles=related_articles[:5]  # Limit to top 5 articles per topic
        ))
    
    # Sort by score (highest first)
    trending_topics.sort(key=lambda x: x.score, reverse=True)
    
    return trending_topics

@router.get("/categories")
async def get_trending_categories(
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get trending categories based on article count"""
    since = datetime.utcnow() - timedelta(hours=hours)
    
    category_stats = db.query(
        Article.category,
        func.count(Article.id).label('count')
    ).filter(
        Article.published_at >= since,
        Article.category.isnot(None)
    ).group_by(Article.category).order_by(desc('count')).all()
    
    return [
        {"category": category, "count": count}
        for category, count in category_stats
    ]

@router.get("/sources")
async def get_trending_sources(
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get trending sources based on article count"""
    since = datetime.utcnow() - timedelta(hours=hours)
    
    source_stats = db.query(
        Article.source,
        func.count(Article.id).label('count')
    ).filter(
        Article.published_at >= since,
        Article.source.isnot(None)
    ).group_by(Article.source).order_by(desc('count')).all()
    
    return [
        {"source": source, "count": count}
        for source, count in source_stats
    ]

@router.get("/sentiment")
async def get_sentiment_trends(
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get sentiment distribution for recent articles"""
    since = datetime.utcnow() - timedelta(hours=hours)
    
    sentiment_stats = db.query(
        Article.sentiment,
        func.count(Article.id).label('count')
    ).filter(
        Article.published_at >= since,
        Article.sentiment.isnot(None)
    ).group_by(Article.sentiment).all()
    
    total_articles = sum(count for _, count in sentiment_stats)
    
    return [
        {
            "sentiment": sentiment,
            "count": count,
            "percentage": round((count / total_articles) * 100, 1) if total_articles > 0 else 0
        }
        for sentiment, count in sentiment_stats
    ]

@router.get("/timeline")
async def get_trending_timeline(
    hours: int = 168,  # 7 days
    interval_hours: int = 24,  # Group by day
    db: Session = Depends(get_db)
):
    """Get trending timeline showing article counts over time"""
    since = datetime.utcnow() - timedelta(hours=hours)
    
    # This is a simplified version - in production, you might want to use proper time buckets
    articles = db.query(Article).filter(
        Article.published_at >= since
    ).order_by(Article.published_at).all()
    
    # Group articles by time intervals
    timeline = {}
    for article in articles:
        if not article.published_at:
            continue
        
        # Round to nearest interval
        interval_start = article.published_at.replace(minute=0, second=0, microsecond=0)
        interval_hours_diff = (interval_start.hour // interval_hours) * interval_hours
        interval_start = interval_start.replace(hour=interval_hours_diff)
        
        interval_key = interval_start.isoformat()
        
        if interval_key not in timeline:
            timeline[interval_key] = {
                "timestamp": interval_start,
                "count": 0,
                "categories": Counter()
            }
        
        timeline[interval_key]["count"] += 1
        if article.category:
            timeline[interval_key]["categories"][article.category] += 1
    
    # Convert to list and sort by timestamp
    timeline_data = [
        {
            "timestamp": data["timestamp"],
            "count": data["count"],
            "top_categories": dict(data["categories"].most_common(3))
        }
        for data in timeline.values()
    ]
    
    timeline_data.sort(key=lambda x: x["timestamp"])
    
    return timeline_data