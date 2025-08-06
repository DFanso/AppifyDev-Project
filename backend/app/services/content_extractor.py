import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
from typing import Optional
import time
import random
import html
import re

logger = logging.getLogger(__name__)

class ContentExtractor:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.timeout = 10
        self.max_retries = 3
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""
        
        # Decode HTML entities
        text = html.unescape(text)
        
        # Remove extra whitespace and normalize
        text = ' '.join(text.split())
        
        # Remove common footer/navigation patterns
        unwanted_patterns = [
            # Newsletter/subscription text
            "Subscribe to our newsletter",
            "Sign up for our newsletter",
            "Follow us on",
            "Share this article",
            "Related articles",
            "Advertisement",
            "Cookie policy",
            "Privacy policy",
            
            # Blog footer patterns (regex)
            "The post .* appeared first on .*",
            "appeared first on .*",
            "Continue reading .*",
            "Read more.*",
            "Read More.*",
            "View original post.*",
            
            # Comments and social
            "Comments",
            "Share on",
            "Tweet this",
            "Like this:",
            
            # Navigation
            "Skip to content",
            "Skip to main content", 
            "Skip navigation",
            "Go to top",
            "Back to top"
        ]
        
        for pattern in unwanted_patterns:
            # Use regex for patterns containing wildcards
            if '.*' in pattern:
                text = re.sub(pattern, "", text, flags=re.IGNORECASE)
            else:
                text = text.replace(pattern, "")
        
        # Remove leftover HTML-like patterns
        text = re.sub(r'<[^>]+>', '', text)  # Remove any remaining HTML tags
        text = re.sub(r'\s+', ' ', text)     # Normalize whitespace
        
        return text.strip()
    
    def is_hacker_news_url(self, url: str) -> bool:
        """Check if URL is from Hacker News"""
        return 'news.ycombinator.com' in url
    
    def get_site_specific_selectors(self, url: str) -> list:
        """Get site-specific content selectors based on URL"""
        domain = urlparse(url).netloc.lower()
        
        site_selectors = {
            'techcrunch.com': ['.article-content', '.entry-content'],
            'theverge.com': ['.c-entry-content', '.e-content'],
            'engadget.com': ['.article-text', '.o-article_body'],
            'arstechnica.com': ['.article-content', '.post-content'],
            'medium.com': ['.postArticle-content', 'article section'],
            'substack.com': ['.markup', '.post-content'],
            'blog.': ['.post-content', '.entry-content', '.article-content'],
            'fs.blog': ['.entry-content', '.post-content'],
            'scotthyoung.com': ['.entry-content', '.post-content'],
            'nesslabs.com': ['.entry-content', '.post-content'],
            'github.io': ['.post-content', 'article', '.content'],
            'stripe.com': ['.post-content', 'article'],
            'airbnb.': ['.post-content', 'article'],
            'engineering.': ['.post-content', 'article', '.entry-content']
        }
        
        # Find matching selectors
        for site_pattern, selectors in site_selectors.items():
            if site_pattern in domain:
                return selectors
        
        return []
    
    def extract_article_content(self, url: str) -> Optional[str]:
        """Extract main article content from URL"""
        try:
            logger.debug(f"Extracting content from: {url}")
            
            # Special handling for Hacker News - skip since they link to discussions, not articles
            if self.is_hacker_news_url(url):
                logger.debug(f"Skipping Hacker News discussion URL: {url}")
                return "Hacker News discussion link - original article content not available"
            
            # Add random delay to be respectful
            time.sleep(random.uniform(0.5, 1.5))
            
            response = requests.get(
                url, 
                headers=self.headers, 
                timeout=self.timeout,
                allow_redirects=True
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements more aggressively
            unwanted_tags = [
                'script', 'style', 'nav', 'header', 'footer', 'aside', 
                'advertisement', 'ad', 'ads', 'social-share', 'comments',
                'related-posts', 'newsletter', 'subscription', 'popup'
            ]
            
            for tag in unwanted_tags:
                for element in soup.find_all(tag):
                    element.decompose()
            
            # Remove elements with common unwanted classes/ids (but be more careful)
            unwanted_classes = [
                'comment', 'comments', 'social-share', 'share-buttons', 'newsletter-signup', 
                'subscription-box', 'advertisement', 'sidebar-widget',
                'related-posts', 'recommended-posts', 'popular-posts', 'trending-posts'
            ]
            
            for class_name in unwanted_classes:
                # Only remove if class name matches exactly or with common suffixes
                for element in soup.find_all(class_=re.compile(f'^{class_name}(-|_|$)', re.I)):
                    element.decompose()
                for element in soup.find_all(id=re.compile(f'^{class_name}(-|_|$)', re.I)):
                    element.decompose()
            
            # Site-specific content selectors (prioritized)
            site_specific_selectors = self.get_site_specific_selectors(url)
            
            # General content selectors
            general_selectors = [
                'article',
                '.article-content',
                '.post-content', 
                '.entry-content',
                '.article-body',
                '.post-body',
                '.story-body',
                '.content-body',
                'main article',
                'main .content',
                '.main-content',
                '[role="main"]',
                '.post',
                '.article'
            ]
            
            # Combine site-specific and general selectors
            all_selectors = site_specific_selectors + general_selectors
            
            content = None
            for selector in all_selectors:
                elements = soup.select(selector)
                if elements:
                    # Get the element with the most meaningful text
                    best_element = max(elements, key=lambda x: len(x.get_text().strip()))
                    raw_text = best_element.get_text().strip()
                    if len(raw_text) > 50:  # Minimum content length
                        content = raw_text
                        logger.debug(f"Found content using selector '{selector}': {len(content)} chars")
                        break
            
            # Fallback: try to find paragraphs with substantial content
            if not content:
                paragraphs = soup.find_all('p')
                if paragraphs:
                    # Filter out short paragraphs (likely navigation/ads)
                    meaningful_paragraphs = [p.get_text() for p in paragraphs if len(p.get_text().strip()) > 20]
                    if meaningful_paragraphs:
                        content = ' '.join(meaningful_paragraphs)
            
            # Final fallback: get body text but filter heavily
            if not content:
                body = soup.find('body')
                if body:
                    content = body.get_text()
            
            if content:
                content = self.clean_text(content)
                
                # Reject content that's too short (likely navigation/ads)
                if len(content.strip()) < 100:
                    logger.warning(f"Content too short for URL: {url}")
                    return None
                
                # Limit content length
                if len(content) > 10000:
                    content = content[:10000] + "..."
                    
                logger.debug(f"Successfully extracted {len(content)} characters")
                return content
            
            logger.warning(f"No content found for URL: {url}")
            return None
            
        except requests.RequestException as e:
            logger.error(f"Request error for URL {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {e}")
            return None
    
    def extract_with_retry(self, url: str) -> Optional[str]:
        """Extract content with retry logic"""
        for attempt in range(self.max_retries):
            try:
                content = self.extract_article_content(url)
                if content:
                    return content
                logger.warning(f"Attempt {attempt + 1} failed for {url}")
                time.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt == self.max_retries - 1:
                    break
                time.sleep(2 ** attempt)
        
        return None

# Global extractor instance
extractor = ContentExtractor()

def extract_article_content(url: str) -> Optional[str]:
    """Helper function for content extraction"""
    return extractor.extract_with_retry(url)