import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import re
from urllib.parse import urljoin, urlparse
import logging

from ..database import SessionLocal, Article
from ..services.sentiment_analyzer import analyze_sentiment
from ..services.content_extractor import extract_article_content

logger = logging.getLogger(__name__)

class RSSAggregator:
    def __init__(self):
        self.sources = {
            "TechCrunch": {
                "url": "https://techcrunch.com/feed/",
                "category_mapping": {
                    "artificial-intelligence": "AI/ML",
                    "startups": "Startups",
                    "security": "Cybersecurity",
                    "mobile": "Mobile",
                    "apps": "Mobile",
                    "fintech": "Startups",
                    "biotech": "Startups",
                }
            },
            "The Verge": {
                "url": "https://www.theverge.com/rss/index.xml",
                "category_mapping": {
                    "tech": "General",
                    "ai": "AI/ML",
                    "security": "Cybersecurity",
                    "mobile": "Mobile",
                    "web": "Web3",
                }
            },
            "Ars Technica": {
                "url": "https://feeds.arstechnica.com/arstechnica/index",
                "category_mapping": {
                    "technology": "General",
                    "security": "Cybersecurity",
                    "ai": "AI/ML",
                    "mobile": "Mobile",
                }
            }
        }
    
    def categorize_article(self, title: str, content: str, source: str) -> str:
        """Categorize article based on title and content keywords"""
        text = f"{title} {content}".lower()
        
        # AI/ML keywords
        ai_keywords = ["artificial intelligence", "machine learning", "ai", "ml", "neural", "llm", "gpt", "openai", "anthropic", "chatgpt", "deep learning"]
        if any(keyword in text for keyword in ai_keywords):
            return "AI/ML"
        
        # Startup keywords
        startup_keywords = ["funding", "series a", "series b", "venture", "startup", "vc", "investor", "raise", "valuation", "ipo"]
        if any(keyword in text for keyword in startup_keywords):
            return "Startups"
        
        # Cybersecurity keywords
        security_keywords = ["security", "hack", "breach", "vulnerability", "cyberattack", "malware", "ransomware", "phishing"]
        if any(keyword in text for keyword in security_keywords):
            return "Cybersecurity"
        
        # Mobile keywords
        mobile_keywords = ["mobile", "smartphone", "iphone", "android", "ios", "app store", "google play"]
        if any(keyword in text for keyword in mobile_keywords):
            return "Mobile"
        
        # Web3 keywords
        web3_keywords = ["blockchain", "crypto", "bitcoin", "ethereum", "nft", "web3", "defi", "dao"]
        if any(keyword in text for keyword in web3_keywords):
            return "Web3"
        
        return "General"
    
    def parse_date(self, date_string: str) -> Optional[datetime]:
        """Parse various date formats from RSS feeds"""
        try:
            if date_string:
                parsed = feedparser._parse_date(date_string)
                if parsed:
                    return datetime(*parsed[:6])
        except Exception as e:
            logger.warning(f"Failed to parse date {date_string}: {e}")
        return None
    
    def fetch_feed_entries(self, source_name: str, feed_url: str) -> List[Dict]:
        """Fetch and parse RSS feed entries"""
        try:
            logger.info(f"Fetching RSS feed from {source_name}: {feed_url}")
            feed = feedparser.parse(feed_url)
            
            if feed.bozo:
                logger.warning(f"RSS feed parsing warning for {source_name}: {feed.bozo_exception}")
            
            entries = []
            for entry in feed.entries:
                # Extract basic information
                article_data = {
                    "title": entry.get("title", "").strip(),
                    "url": entry.get("link", "").strip(),
                    "summary": entry.get("summary", "").strip(),
                    "author": entry.get("author", "").strip(),
                    "published_at": self.parse_date(entry.get("published", "")),
                    "source": source_name,
                }
                
                # Extract image URL
                if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                    article_data["image_url"] = entry.media_thumbnail[0].get("url", "")
                elif hasattr(entry, 'media_content') and entry.media_content:
                    article_data["image_url"] = entry.media_content[0].get("url", "")
                
                entries.append(article_data)
            
            logger.info(f"Successfully fetched {len(entries)} entries from {source_name}")
            return entries
            
        except Exception as e:
            logger.error(f"Error fetching RSS feed from {source_name}: {e}")
            return []
    
    def process_article(self, article_data: Dict) -> Optional[Article]:
        """Process a single article: extract content, categorize, analyze sentiment"""
        try:
            # Extract full content
            full_content = extract_article_content(article_data["url"])
            if not full_content:
                full_content = article_data.get("summary", "")
            
            # Categorize article
            category = self.categorize_article(
                article_data["title"], 
                full_content, 
                article_data["source"]
            )
            
            # Analyze sentiment
            sentiment = analyze_sentiment(f"{article_data['title']} {full_content}")
            
            # Create article object
            article = Article(
                title=article_data["title"],
                url=article_data["url"],
                content=full_content,
                summary=article_data.get("summary", ""),
                author=article_data.get("author", ""),
                published_at=article_data.get("published_at"),
                source=article_data["source"],
                category=category,
                sentiment=sentiment,
                image_url=article_data.get("image_url", "")
            )
            
            return article
            
        except Exception as e:
            logger.error(f"Error processing article {article_data.get('title', 'Unknown')}: {e}")
            return None
    
    def aggregate_news(self) -> int:
        """Aggregate news from all configured sources"""
        db = SessionLocal()
        total_new_articles = 0
        
        try:
            for source_name, source_config in self.sources.items():
                logger.info(f"Processing source: {source_name}")
                
                # Fetch RSS entries
                entries = self.fetch_feed_entries(source_name, source_config["url"])
                
                for entry_data in entries:
                    # Check if article already exists
                    existing_article = db.query(Article).filter(
                        Article.url == entry_data["url"]
                    ).first()
                    
                    if existing_article:
                        logger.debug(f"Article already exists: {entry_data['title']}")
                        continue
                    
                    # Process new article
                    article = self.process_article(entry_data)
                    if article:
                        db.add(article)
                        total_new_articles += 1
                        logger.info(f"Added new article: {article.title}")
            
            db.commit()
            logger.info(f"News aggregation completed. Added {total_new_articles} new articles.")
            
        except Exception as e:
            logger.error(f"Error during news aggregation: {e}")
            db.rollback()
        finally:
            db.close()
        
        return total_new_articles

# Global aggregator instance
aggregator = RSSAggregator()