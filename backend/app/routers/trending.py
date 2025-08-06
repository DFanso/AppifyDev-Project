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
    """Extract meaningful tech-focused keywords from text"""
    if not text:
        return []
    
    # Comprehensive stop words list for better filtering
    stop_words = {
        # Articles, prepositions, conjunctions
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
        'after', 'above', 'below', 'between', 'among', 'within', 'without',
        
        # Pronouns and determiners
        'this', 'that', 'these', 'those', 'they', 'them', 'their', 'there',
        'here', 'where', 'when', 'what', 'which', 'who', 'whom', 'whose', 'why',
        'how', 'your', 'you', 'yours', 'our', 'ours', 'his', 'her', 'hers',
        'its', 'their', 'theirs', 'some', 'any', 'all', 'each', 'every',
        'both', 'either', 'neither', 'one', 'two', 'three', 'first', 'second',
        'other', 'another', 'such', 'same', 'different', 'various', 'several',
        
        # Modal and auxiliary verbs
        'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
        'are', 'was', 'were', 'been', 'have', 'has', 'had', 'did', 'does',
        'do', 'done', 'being', 'is', 'am', 'are', 'was', 'were', 'get', 'got',
        'give', 'given', 'take', 'taken', 'make', 'made', 'come', 'came',
        'go', 'went', 'gone', 'see', 'seen', 'know', 'known', 'think',
        'thought', 'find', 'found', 'tell', 'told', 'ask', 'asked', 'try',
        'tried', 'seem', 'seemed', 'feel', 'felt', 'leave', 'left', 'put',
        
        # Common adjectives and adverbs
        'more', 'most', 'less', 'least', 'much', 'many', 'few', 'little',
        'good', 'better', 'best', 'bad', 'worse', 'worst', 'big', 'bigger',
        'small', 'smaller', 'large', 'larger', 'great', 'greater', 'high',
        'higher', 'low', 'lower', 'long', 'longer', 'short', 'shorter',
        'new', 'newer', 'old', 'older', 'young', 'younger', 'early', 'earlier',
        'late', 'later', 'last', 'next', 'previous', 'current', 'recent',
        'important', 'main', 'major', 'minor', 'real', 'right', 'wrong',
        'true', 'false', 'sure', 'certain', 'possible', 'impossible',
        'available', 'free', 'open', 'close', 'closed', 'full', 'empty',
        'easy', 'hard', 'difficult', 'simple', 'complex', 'clear', 'dark',
        'light', 'heavy', 'quick', 'fast', 'slow', 'strong', 'weak',
        
        # Generic tech words that aren't meaningful
        'using', 'used', 'use', 'uses', 'way', 'ways', 'time', 'times',
        'work', 'works', 'working', 'worked', 'thing', 'things', 'stuff',
        'part', 'parts', 'kind', 'type', 'types', 'sort', 'example',
        'examples', 'case', 'cases', 'point', 'points', 'place', 'places',
        'end', 'ends', 'start', 'starts', 'beginning', 'middle', 'side',
        'sides', 'top', 'bottom', 'left', 'right', 'front', 'back',
        'inside', 'outside', 'around', 'near', 'far', 'away', 'together',
        'alone', 'only', 'just', 'even', 'still', 'yet', 'already',
        'always', 'never', 'sometimes', 'often', 'usually', 'probably',
        'perhaps', 'maybe', 'definitely', 'certainly', 'exactly', 'quite',
        'very', 'too', 'so', 'such', 'really', 'actually', 'basically',
        'generally', 'specifically', 'particularly', 'especially', 'mainly',
        'mostly', 'partly', 'completely', 'totally', 'fully', 'nearly',
        'almost', 'hardly', 'barely', 'rather', 'pretty', 'fairly',
        
        # Common verbs that don't add meaning
        'said', 'say', 'says', 'saying', 'call', 'called', 'calling',
        'look', 'looked', 'looking', 'looks', 'like', 'liked', 'liking',
        'want', 'wanted', 'wanting', 'need', 'needed', 'needing',
        'help', 'helped', 'helping', 'show', 'showed', 'showing',
        'turn', 'turned', 'turning', 'keep', 'kept', 'keeping',
        'let', 'lets', 'letting', 'play', 'played', 'playing',
        'move', 'moved', 'moving', 'live', 'lived', 'living',
        'bring', 'brought', 'bringing', 'happen', 'happened', 'happening',
        'write', 'wrote', 'written', 'writing', 'read', 'reading',
        'hear', 'heard', 'hearing', 'listen', 'listened', 'listening',
        'talk', 'talked', 'talking', 'speak', 'spoke', 'speaking',
        'understand', 'understood', 'understanding', 'mean', 'meant', 'meaning',
        'include', 'included', 'including', 'follow', 'followed', 'following',
        'change', 'changed', 'changing', 'become', 'became', 'becoming',
        'seem', 'seems', 'seemed', 'seeming', 'appear', 'appeared', 'appearing',
        'continue', 'continued', 'continuing', 'remain', 'remained', 'remaining',
        'stay', 'stayed', 'staying', 'stop', 'stopped', 'stopping',
        'begin', 'began', 'beginning', 'finish', 'finished', 'finishing'
    }
    
    # Extract potential keywords (4+ characters, letters/numbers/hyphens)
    potential_keywords = re.findall(r'\b[A-Za-z][A-Za-z0-9\-]{3,}\b', text)
    
    # Filter and process keywords
    keywords = []
    for word in potential_keywords:
        word_lower = word.lower()
        
        # Skip stop words
        if word_lower in stop_words:
            continue
        
        # Skip pure numbers
        if word.isdigit():
            continue
            
        # Keep capitalized words (likely proper nouns/tech terms)
        if word[0].isupper():
            keywords.append(word)
        # Keep tech-looking terms (contain numbers/hyphens)
        elif any(char.isdigit() or char == '-' for char in word):
            keywords.append(word.upper() if len(word) <= 6 else word.title())
        # Keep long words that might be technical
        elif len(word) >= 6:
            keywords.append(word.title())
    
    return keywords

def extract_tech_phrases(text: str) -> List[str]:
    """Extract multi-word tech phrases and company names"""
    if not text:
        return []
    
    phrases = []
    
    # Common 2-3 word tech phrases
    tech_patterns = [
        r'\b(artificial intelligence|machine learning|deep learning|neural network|natural language|computer vision|data science|cloud computing|edge computing|quantum computing)\b',
        r'\b(software development|web development|mobile development|app development|game development|software engineering)\b',
        r'\b(cyber security|information security|network security|data privacy|data protection|identity management)\b',
        r'\b(user experience|user interface|user research|design thinking|design system|design patterns)\b',
        r'\b(business intelligence|data analytics|data mining|big data|data warehouse|data lake)\b',
        r'\b(internet of things|augmented reality|virtual reality|mixed reality|extended reality)\b',
        r'\b(social media|social network|social platform|content management|digital marketing)\b',
        r'\b(open source|version control|continuous integration|continuous deployment|agile development)\b',
        r'\b(api integration|api management|microservices|serverless|container orchestration)\b',
        r'\b(digital transformation|automation|process automation|robotic process|workflow automation)\b'
    ]
    
    # Company and product patterns
    company_patterns = [
        r'\b(Apple|Google|Microsoft|Amazon|Meta|Facebook|Tesla|Netflix|Spotify|Adobe|Oracle|Salesforce)\b',
        r'\b(OpenAI|ChatGPT|GPT-\d+|Claude|Gemini|Anthropic|DeepMind|Midjourney)\b',
        r'\b(iPhone|iPad|MacBook|Windows|Android|iOS|Chrome|Safari|Firefox)\b',
        r'\b(AWS|Azure|Google Cloud|Firebase|Vercel|Netlify|Heroku|Docker|Kubernetes)\b',
        r'\b(React|Vue|Angular|Node\.js|Python|JavaScript|TypeScript|Java|Swift|Kotlin)\b',
        r'\b(GitHub|GitLab|Stack Overflow|Reddit|Twitter|LinkedIn|TikTok|Instagram|YouTube)\b'
    ]
    
    all_patterns = tech_patterns + company_patterns
    
    for pattern in all_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                match = ' '.join(match)
            phrases.append(match.title())
    
    return phrases

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
    
    # Extract and count keywords with tech focus
    keyword_counter = Counter()
    article_keywords = {}
    
    for article in recent_articles:
        # Extract both single keywords and tech phrases
        title_keywords = extract_keywords(article.title)
        content_keywords = extract_keywords(article.content or "")
        title_phrases = extract_tech_phrases(article.title)
        content_phrases = extract_tech_phrases(article.content or "")
        
        # Prioritize tech phrases (highest weight), then title keywords, then content keywords
        all_terms = (
            title_phrases * 5 +        # Tech phrases in title get highest weight
            content_phrases * 3 +      # Tech phrases in content get high weight
            title_keywords * 2 +       # Single keywords in title get medium weight  
            content_keywords           # Single keywords in content get base weight
        )
        
        # Store all terms for this article
        all_article_terms = set(title_keywords + content_keywords + title_phrases + content_phrases)
        article_keywords[article.id] = all_article_terms
        
        # Update global counter
        keyword_counter.update(all_terms)
    
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