from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List
from enum import Enum

class SentimentEnum(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"

class CategoryEnum(str, Enum):
    ai_ml = "AI/ML"
    startups = "Startups"
    cybersecurity = "Cybersecurity"
    mobile = "Mobile"
    web3 = "Web3"
    general = "General"

class SourceEnum(str, Enum):
    techcrunch = "TechCrunch"
    the_verge = "The Verge"
    hacker_news = "Hacker News"
    ars_technica = "Ars Technica"

# Article Schemas
class ArticleBase(BaseModel):
    title: str
    url: HttpUrl
    content: Optional[str] = None
    summary: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    source: Optional[str] = None
    category: Optional[str] = None
    sentiment: Optional[SentimentEnum] = None
    image_url: Optional[HttpUrl] = None

class ArticleCreate(ArticleBase):
    pass

class ArticleResponse(ArticleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ArticleListResponse(BaseModel):
    articles: List[ArticleResponse]
    total: int
    page: int
    page_size: int
    has_next: bool

# Chat Schemas
class ChatMessage(BaseModel):
    message: str
    article_id: Optional[int] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    article_context: Optional[ArticleResponse] = None
    sources: Optional[List[str]] = None

class ChatHistoryResponse(BaseModel):
    id: int
    message: str
    response: str
    article_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Bookmark Schemas
class BookmarkCreate(BaseModel):
    article_id: int
    user_id: Optional[str] = None

class BookmarkResponse(BaseModel):
    id: int
    article_id: int
    article: ArticleResponse
    created_at: datetime
    
    class Config:
        from_attributes = True

# Search and Filter Schemas
class ArticleFilter(BaseModel):
    category: Optional[str] = None
    source: Optional[str] = None
    sentiment: Optional[SentimentEnum] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search_query: Optional[str] = None

class SearchRequest(BaseModel):
    query: str
    filters: Optional[ArticleFilter] = None
    page: int = 1
    page_size: int = 20

# Trending Topics Schema
class TrendingTopicResponse(BaseModel):
    topic: str
    count: int
    score: float
    articles: List[ArticleResponse]
    
    class Config:
        from_attributes = True

# Error Schema
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None