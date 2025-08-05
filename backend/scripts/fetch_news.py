#!/usr/bin/env python3
"""
Script to fetch and aggregate news from RSS feeds.
Can be run manually or scheduled with cron.
"""

import sys
import os
import logging
from datetime import datetime

# Add the parent directory to Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.rss_aggregator import aggregator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('news_aggregation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main function to run news aggregation"""
    logger.info("Starting news aggregation...")
    
    try:
        # Run the aggregation
        new_articles_count = aggregator.aggregate_news()
        
        logger.info(f"News aggregation completed. Added {new_articles_count} new articles.")
        
        if new_articles_count > 0:
            print(f"✅ Successfully added {new_articles_count} new articles")
        else:
            print("ℹ️  No new articles found")
            
    except Exception as e:
        logger.error(f"Error during news aggregation: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()