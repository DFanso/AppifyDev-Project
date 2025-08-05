import re
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        # Positive sentiment keywords
        self.positive_keywords = {
            'breakthrough', 'innovation', 'success', 'growth', 'improvement', 
            'advance', 'progress', 'achievement', 'launch', 'release', 'new',
            'upgrade', 'expansion', 'boost', 'enhance', 'optimize', 'efficient',
            'revolutionary', 'groundbreaking', 'milestone', 'record', 'winning',
            'funding', 'investment', 'acquisition', 'partnership', 'collaboration'
        }
        
        # Negative sentiment keywords
        self.negative_keywords = {
            'breach', 'hack', 'vulnerability', 'attack', 'threat', 'risk',
            'failure', 'decline', 'crash', 'bug', 'issue', 'problem',
            'controversy', 'scandal', 'lawsuit', 'fine', 'penalty',
            'layoffs', 'closure', 'shutdown', 'bankruptcy', 'loss',
            'dangerous', 'harmful', 'concern', 'warning', 'alert'
        }
        
        # Neutral indicators
        self.neutral_keywords = {
            'analysis', 'review', 'report', 'study', 'research', 'survey',
            'announcement', 'statement', 'update', 'information', 'data',
            'conference', 'meeting', 'discussion', 'interview', 'opinion'
        }
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for sentiment analysis"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs, email addresses, and special characters
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def calculate_sentiment_score(self, text: str) -> Dict[str, float]:
        """Calculate sentiment scores based on keyword matching"""
        processed_text = self.preprocess_text(text)
        words = processed_text.split()
        
        if not words:
            return {'positive': 0.0, 'negative': 0.0, 'neutral': 1.0}
        
        positive_count = sum(1 for word in words if word in self.positive_keywords)
        negative_count = sum(1 for word in words if word in self.negative_keywords)
        neutral_count = sum(1 for word in words if word in self.neutral_keywords)
        
        total_words = len(words)
        
        # Calculate normalized scores
        positive_score = positive_count / total_words
        negative_score = negative_count / total_words
        neutral_score = neutral_count / total_words
        
        # Boost scores based on keyword density
        if positive_count > 0:
            positive_score *= 2
        if negative_count > 0:
            negative_score *= 2
        
        return {
            'positive': positive_score,
            'negative': negative_score,
            'neutral': max(0.1, 1.0 - positive_score - negative_score)
        }
    
    def analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment and return classification"""
        if not text or len(text.strip()) < 10:
            return "neutral"
        
        try:
            scores = self.calculate_sentiment_score(text)
            
            # Determine sentiment based on scores
            max_score = max(scores.values())
            
            if scores['positive'] == max_score and scores['positive'] > 0.02:
                return "positive"
            elif scores['negative'] == max_score and scores['negative'] > 0.02:
                return "negative"
            else:
                return "neutral"
                
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return "neutral"
    
    def get_sentiment_confidence(self, text: str) -> float:
        """Get confidence score for sentiment analysis"""
        try:
            scores = self.calculate_sentiment_score(text)
            max_score = max(scores.values())
            return min(max_score * 10, 1.0)  # Scale and cap at 1.0
        except Exception:
            return 0.5

# Global analyzer instance
analyzer = SentimentAnalyzer()

def analyze_sentiment(text: str) -> str:
    """Helper function for sentiment analysis"""
    return analyzer.analyze_sentiment(text)