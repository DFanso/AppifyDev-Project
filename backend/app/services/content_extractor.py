import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
from typing import Optional
import time
import random

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
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove common unwanted patterns
        unwanted_patterns = [
            "Subscribe to our newsletter",
            "Sign up for our newsletter",
            "Follow us on",
            "Share this article",
            "Related articles",
            "Advertisement",
            "Cookie policy",
            "Privacy policy"
        ]
        
        for pattern in unwanted_patterns:
            text = text.replace(pattern, "")
        
        return text.strip()
    
    def extract_article_content(self, url: str) -> Optional[str]:
        """Extract main article content from URL"""
        try:
            logger.debug(f"Extracting content from: {url}")
            
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
            
            # Remove unwanted elements
            unwanted_tags = ['script', 'style', 'nav', 'header', 'footer', 'aside', 'advertisement']
            for tag in unwanted_tags:
                for element in soup.find_all(tag):
                    element.decompose()
            
            # Try different selectors for article content
            content_selectors = [
                'article',
                '.article-content',
                '.post-content',
                '.entry-content',
                '.content',
                '.story-body',
                '.article-body',
                '.post-body',
                'main',
                '.main-content'
            ]
            
            content = None
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    # Get the element with the most text
                    best_element = max(elements, key=lambda x: len(x.get_text()))
                    content = best_element.get_text()
                    break
            
            # Fallback: try to find paragraphs
            if not content:
                paragraphs = soup.find_all('p')
                if paragraphs:
                    content = ' '.join([p.get_text() for p in paragraphs])
            
            # Final fallback: get body text
            if not content:
                body = soup.find('body')
                if body:
                    content = body.get_text()
            
            if content:
                content = self.clean_text(content)
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