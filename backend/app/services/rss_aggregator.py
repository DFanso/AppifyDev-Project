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
        # RSS feeds organized by category from OPML file
        self.sources = {
            # Learning category feeds
            "The Decision Lab": {
                "url": "https://thedecisionlab.com/feed/",
                "category": "Learning"
            },
            "Ness Labs": {
                "url": "https://nesslabs.com/feed",
                "category": "Learning"
            },
            "Farnam Street": {
                "url": "https://fs.blog/feed/",
                "category": "Learning"
            },
            "The Sunday Wisdom": {
                "url": "https://coffeeandjunk.substack.com/feed",
                "category": "Learning"
            },
            "Commonplace - The Commoncog Blog": {
                "url": "https://commoncog.com/blog/rss/",
                "category": "Learning"
            },
            "Scott H Young": {
                "url": "https://feeds.feedburner.com/scotthyoung/HAHx",
                "category": "Learning"
            },
            "Big Think": {
                "url": "https://feeds.feedburner.com/bigthink/main",
                "category": "Learning"
            },
            
            # Startup category feeds
            "Steve Blank": {
                "url": "http://steveblank.com/feed/",
                "category": "Startup"
            },
            "The singularity is nearer": {
                "url": "https://geohot.github.io/blog/feed.xml",
                "category": "Startup"
            },
            "Hacker News": {
                "url": "http://news.ycombinator.com/rss",
                "category": "Startup"
            },
            "Guy Kawasaki": {
                "url": "http://guykawasaki.com/feed/",
                "category": "Startup"
            },
            "Essays - Benedict Evans": {
                "url": "http://ben-evans.com/benedictevans?format=rss",
                "category": "Startup"
            },
            "First Round Review": {
                "url": "http://firstround.com/review/feed.xml",
                "category": "Startup"
            },
            "Sam Altman": {
                "url": "http://blog.samaltman.com/posts.atom",
                "category": "Startup"
            },
            "Andrew Chen": {
                "url": "http://andrewchen.co/feed/",
                "category": "Startup"
            },
            "Both Sides of the Table - Medium": {
                "url": "https://bothsidesofthetable.com/feed",
                "category": "Startup"
            },
            "OnStartups": {
                "url": "http://feed.onstartups.com/onstartups",
                "category": "Startup"
            },
            "Product Life": {
                "url": "https://productlife.to/feed",
                "category": "Startup"
            },
            "Irrational Exuberance": {
                "url": "https://lethain.com/feeds/",
                "category": "Startup"
            },
            
            # Tech News category feeds
            "SlashGear": {
                "url": "http://feeds.slashgear.com/slashgear",
                "category": "Tech News"
            },
            "VentureBeat": {
                "url": "http://venturebeat.com/feed/",
                "category": "Tech News"
            },
            "The Verge": {
                "url": "http://www.theverge.com/rss/full.xml",
                "category": "Tech News"
            },
            "Engadget": {
                "url": "http://www.engadget.com/rss-full.xml",
                "category": "Tech News"
            },
            "Tech in Asia": {
                "url": "https://feeds2.feedburner.com/PennOlson",
                "category": "Tech News"
            },
            "TechCrunch": {
                "url": "https://techcrunch.com/feed/",
                "category": "Tech News"
            },
            "Fast Company": {
                "url": "http://feeds.feedburner.com/fastcompany/headlines",
                "category": "Tech News"
            },
            "Startups – TechCrunch": {
                "url": "https://techcrunch.com/startups/feed/",
                "category": "Tech News"
            },
            "Forbes - Leadership": {
                "url": "https://www.forbes.com/leadership/feed/",
                "category": "Tech News"
            },
            "Forbes - Entrepreneurs": {
                "url": "http://www.forbes.com/entrepreneurs/index.xml",
                "category": "Tech News"
            },
            
            # Products & Ideas category feeds
            "Product Hunt": {
                "url": "http://www.producthunt.com/feed",
                "category": "Products & Ideas"
            },
            "Hacker News: Show HN": {
                "url": "http://hnrss.org/show",
                "category": "Products & Ideas"
            },
            "Hacker News: Launches": {
                "url": "https://hnrss.org/launches",
                "category": "Products & Ideas"
            },
            "Sachin Rekhi's Blog": {
                "url": "http://feeds.feedburner.com/sachinrekhiblog",
                "category": "Products & Ideas"
            },
            
            # Engineering blogs category feeds
            "The Airtable Engineering Blog": {
                "url": "https://medium.com/feed/airtable-eng",
                "category": "Engineering blogs"
            },
            "Medium Engineering": {
                "url": "https://medium.com/feed/medium-eng",
                "category": "Engineering blogs"
            },
            "The PayPal Technology Blog": {
                "url": "https://medium.com/feed/paypal-engineering",
                "category": "Engineering blogs"
            },
            "Pinterest Engineering Blog": {
                "url": "https://medium.com/feed/pinterest-engineering",
                "category": "Engineering blogs"
            },
            "Grab Tech": {
                "url": "https://engineering.grab.com/feed.xml",
                "category": "Engineering blogs"
            },
            "Slack Engineering": {
                "url": "https://slack.engineering/feed",
                "category": "Engineering blogs"
            },
            "Engineering – The GitHub Blog": {
                "url": "http://githubengineering.com/atom.xml",
                "category": "Engineering blogs"
            },
            "Atlassian Developer Blog": {
                "url": "https://developer.atlassian.com/blog/feed.xml",
                "category": "Engineering blogs"
            },
            "Engineering at Meta": {
                "url": "https://engineering.fb.com/feed/",
                "category": "Engineering blogs"
            },
            "eBay Tech Blog": {
                "url": "http://www.ebaytechblog.com/feed/",
                "category": "Engineering blogs"
            },
            "Spotify Engineering": {
                "url": "https://engineering.atspotify.com/feed/",
                "category": "Engineering blogs"
            },
            "Twitter Engineering": {
                "url": "https://blog.twitter.com/engineering/en_us/blog.rss",
                "category": "Engineering blogs"
            },
            "Stripe Blog": {
                "url": "https://stripe.com/blog/feed.rss",
                "category": "Engineering blogs"
            },
            "Instagram Engineering": {
                "url": "https://instagram-engineering.com/feed",
                "category": "Engineering blogs"
            },
            "The Cloudflare Blog": {
                "url": "https://blog.cloudflare.com/rss/",
                "category": "Engineering blogs"
            },
            "Engineering – The Asana Blog": {
                "url": "https://blog.asana.com/category/eng/feed/",
                "category": "Engineering blogs"
            },
            "Canva Engineering Blog": {
                "url": "https://engineering.canva.com/rss",
                "category": "Engineering blogs"
            },
            "The Airbnb Tech Blog": {
                "url": "https://medium.com/feed/airbnb-engineering",
                "category": "Engineering blogs"
            },
            "Dropbox Tech": {
                "url": "https://dropbox.tech/feed",
                "category": "Engineering blogs"
            },
            "Julia Evans": {
                "url": "https://jvns.ca/atom.xml",
                "category": "Engineering blogs"
            },
            "Martin Kleppmann's blog": {
                "url": "https://feeds.feedburner.com/martinkl?format=xml",
                "category": "Engineering blogs"
            },
            "Dan Abramov's Overreacted Blog": {
                "url": "https://overreacted.io/rss.xml",
                "category": "Engineering blogs"
            },
            "Dan Luu": {
                "url": "https://danluu.com/atom.xml",
                "category": "Engineering blogs"
            },
            "Shopify Engineering": {
                "url": "https://shopifyengineering.myshopify.com/blogs/engineering.atom",
                "category": "Engineering blogs"
            },
            "Josh Comeau's blog": {
                "url": "https://joshwcomeau.com/rss.xml",
                "category": "Engineering blogs"
            },
            "Uber Engineering Blog": {
                "url": "https://eng.uber.com/feed/",
                "category": "Engineering blogs"
            },
            "Flurries of latent creativity - Stripe CTO blog": {
                "url": "https://blog.singleton.io/index.xml",
                "category": "Engineering blogs"
            },
            "Sophie Alpert": {
                "url": "https://sophiebits.com/atom.xml",
                "category": "Engineering blogs"
            },
            "Amjad Masad": {
                "url": "https://amasad.me/rss",
                "category": "Engineering blogs"
            },
            "Signal Blog": {
                "url": "https://signal.org/blog/rss.xml",
                "category": "Engineering blogs"
            },
            "Joel on Software": {
                "url": "https://www.joelonsoftware.com/feed/",
                "category": "Engineering blogs"
            },
            "The Pragmatic Engineer": {
                "url": "https://blog.pragmaticengineer.com/rss/",
                "category": "Engineering blogs"
            },
            
            # Machine Learning category feeds
            "Machine Learning Blog | ML@CMU": {
                "url": "https://blog.ml.cmu.edu/feed/",
                "category": "Machine Learning"
            },
            "DeepMind": {
                "url": "https://deepmind.com/blog/feed/basic/",
                "category": "Machine Learning"
            },
            "Jay Alammar": {
                "url": "https://jalammar.github.io/feed.xml",
                "category": "Machine Learning"
            },
            "Lil'Log": {
                "url": "https://lilianweng.github.io/lil-log/feed.xml",
                "category": "Machine Learning"
            },
            "MIT News - Artificial intelligence": {
                "url": "http://news.mit.edu/rss/topic/artificial-intelligence2",
                "category": "Machine Learning"
            },
            "Sebastian Ruder": {
                "url": "http://ruder.io/rss/index.rss",
                "category": "Machine Learning"
            },
            "The Berkeley AI Research Blog": {
                "url": "http://bair.berkeley.edu/blog/feed.xml",
                "category": "Machine Learning"
            },
            "Eric Jang": {
                "url": "https://evjang.com/feed",
                "category": "Machine Learning"
            },
            "OpenAI": {
                "url": "https://blog.openai.com/rss/",
                "category": "Machine Learning"
            },
            "The Gradient": {
                "url": "https://thegradient.pub/rss/",
                "category": "Machine Learning"
            },
            "Google AI Blog": {
                "url": "http://googleresearch.blogspot.com/atom.xml",
                "category": "Machine Learning"
            },
            "Towards Data Science": {
                "url": "https://towardsdatascience.com/feed",
                "category": "Machine Learning"
            },
            "Unite.AI": {
                "url": "https://www.unite.ai/feed/",
                "category": "Machine Learning"
            },
            "Amazon Science Homepage": {
                "url": "https://www.amazon.science/index.rss",
                "category": "Machine Learning"
            },
            
            # Design category feeds
            "UX Planet": {
                "url": "https://uxplanet.org/feed",
                "category": "Design"
            },
            "NN/g latest articles": {
                "url": "https://www.nngroup.com/feed/rss/",
                "category": "Design"
            },
            "UX Movement": {
                "url": "http://feeds.feedburner.com/uxmovement",
                "category": "Design"
            },
            "Inside Design": {
                "url": "http://blog.invisionapp.com/feed/",
                "category": "Design"
            },
            "UXmatters": {
                "url": "https://uxmatters.com/index.xml",
                "category": "Design"
            },
            "Smashing Magazine": {
                "url": "https://www.smashingmagazine.com/feed/",
                "category": "Design"
            },
            "UX Collective": {
                "url": "https://uxdesign.cc/feed",
                "category": "Design"
            },
            "Airbnb Design": {
                "url": "http://airbnb.design/feed/",
                "category": "Design"
            },
            "web.dev": {
                "url": "https://web.dev/feed.xml",
                "category": "Design"
            },
            "Slack Design": {
                "url": "https://slack.design/feed/",
                "category": "Design"
            },
            "CSS-Tricks": {
                "url": "https://feeds.feedburner.com/CssTricks",
                "category": "Design"
            },
            
            # Psychology category feeds
            "PsyBlog": {
                "url": "http://feeds.feedburner.com/PsychologyBlog",
                "category": "Psychology"
            },
            "Psychology Blog": {
                "url": "http://www.all-about-psychology.com/psychology.xml",
                "category": "Psychology"
            },
            "Psychology Headlines Around the World": {
                "url": "http://www.socialpsychology.org/headlines.rss",
                "category": "Psychology"
            },
            "Nautilus": {
                "url": "https://nautil.us/rss/all",
                "category": "Psychology"
            },
            "Psychology Today": {
                "url": "https://www.psychologytoday.com/intl/rss.xml",
                "category": "Psychology"
            },
            
            # Neuroscience category feeds
            "Neuroscience News": {
                "url": "http://neurosciencenews.com/feed/",
                "category": "Neuroscience"
            },
            "Neuroscience News -- ScienceDaily": {
                "url": "https://sciencedaily.com/rss/mind_brain/neuroscience.xml",
                "category": "Neuroscience"
            },
            "SharpBrains": {
                "url": "http://www.sharpbrains.com/feed/",
                "category": "Neuroscience"
            },
            
            # Science category feeds
            "Quanta Magazine": {
                "url": "http://www.quantamagazine.org/feed/",
                "category": "Science"
            },
            "Nature": {
                "url": "http://www.nature.com/nature/current_issue/rss",
                "category": "Science"
            },
            "MIT News": {
                "url": "https://news.mit.edu/rss/research",
                "category": "Science"
            },
            "ScienceAlert": {
                "url": "https://www.sciencealert.com/rss",
                "category": "Science"
            },
            "Singularity Hub": {
                "url": "https://singularityhub.com/feed/",
                "category": "Science"
            },
            
            # Marketing category feeds
            "Moz": {
                "url": "http://feeds.feedburner.com/seomoz",
                "category": "Marketing"
            },
            "Content Marketing Institute": {
                "url": "http://feeds.feedburner.com/cmi-content-marketing",
                "category": "Marketing"
            },
            "Neil Patel": {
                "url": "http://feeds.feedburner.com/KISSmetrics",
                "category": "Marketing"
            },
            "MarketingProfs": {
                "url": "http://rss.marketingprofs.com/marketingprofs/daily",
                "category": "Marketing"
            },
            "Social Media Examiner": {
                "url": "http://www.socialmediaexaminer.com/feed/",
                "category": "Marketing"
            },
            "Seth Godin's Blog": {
                "url": "http://sethgodin.typepad.com/seths_blog/atom.xml",
                "category": "Marketing"
            },
            "Backlinko": {
                "url": "http://backlinko.com/feed",
                "category": "Marketing"
            },
            
            # Others category feeds
            "HBR.org": {
                "url": "http://feeds.harvardbusiness.org/harvardbusiness/",
                "category": "Others"
            }
        }
    
    def categorize_article(self, title: str, content: str, source: str) -> str:
        """Categorize article based on source category from OPML feeds"""
        # Get category from source configuration
        source_config = self.sources.get(source, {})
        if 'category' in source_config:
            return source_config['category']
        
        # Fallback to keyword-based categorization for unknown sources
        text = f"{title} {content}".lower()
        
        # Machine Learning keywords
        ml_keywords = ["artificial intelligence", "machine learning", "ai", "ml", "neural", "llm", "gpt", "openai", "anthropic", "chatgpt", "deep learning"]
        if any(keyword in text for keyword in ml_keywords):
            return "Machine Learning"
        
        # Startup keywords
        startup_keywords = ["funding", "series a", "series b", "venture", "startup", "vc", "investor", "raise", "valuation", "ipo"]
        if any(keyword in text for keyword in startup_keywords):
            return "Startup"
        
        # Engineering keywords
        engineering_keywords = ["engineering", "development", "programming", "software", "architecture", "infrastructure", "devops"]
        if any(keyword in text for keyword in engineering_keywords):
            return "Engineering blogs"
        
        # Design keywords
        design_keywords = ["design", "ux", "ui", "user experience", "interface", "usability", "frontend"]
        if any(keyword in text for keyword in design_keywords):
            return "Design"
        
        # Psychology keywords
        psychology_keywords = ["psychology", "behavior", "cognitive", "mental", "brain", "mind"]
        if any(keyword in text for keyword in psychology_keywords):
            return "Psychology"
        
        # Science keywords
        science_keywords = ["research", "study", "scientific", "experiment", "discovery"]
        if any(keyword in text for keyword in science_keywords):
            return "Science"
        
        return "Tech News"
    
    def parse_date(self, date_string: str) -> Optional[datetime]:
        """Parse various date formats from RSS feeds"""
        try:
            if date_string:
                # Use the correct feedparser method
                import time
                parsed = feedparser._parse_date_time(date_string)
                if parsed:
                    return datetime(*parsed[:6])
        except Exception as e:
            # Fallback to email.utils for RFC 2822 format
            try:
                from email.utils import parsedate_to_datetime
                return parsedate_to_datetime(date_string)
            except Exception:
                logger.warning(f"Failed to parse date {date_string}: {e}")
        return None
    
    def fetch_feed_entries(self, source_name: str, source_config: Dict) -> List[Dict]:
        """Fetch and parse RSS feed entries"""
        try:
            feed_url = source_config['url']
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
            # Extract full content from article URL
            full_content = extract_article_content(article_data["url"])
            if not full_content:
                # Fallback to RSS summary but clean HTML and apply same cleaning
                from .content_extractor import ContentExtractor
                from bs4 import BeautifulSoup
                extractor = ContentExtractor()
                raw_summary = article_data.get("summary", "")
                if raw_summary:
                    # First strip HTML tags from summary
                    soup = BeautifulSoup(raw_summary, 'html.parser')
                    text_only = soup.get_text()
                    # Then apply our text cleaning
                    full_content = extractor.clean_text(text_only)
                else:
                    full_content = ""
            
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
        """Aggregate news from all configured sources with incremental commits"""
        db = SessionLocal()
        total_new_articles = 0
        
        try:
            for source_name, source_config in self.sources.items():
                logger.info(f"Processing source: {source_name}")
                
                # Fetch RSS entries
                entries = self.fetch_feed_entries(source_name, source_config)
                
                for entry_data in entries:
                    try:
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
                            
                            # Commit each article individually
                            try:
                                db.commit()
                                total_new_articles += 1
                                logger.info(f"✅ Added new article: {article.title}")
                            except Exception as commit_error:
                                db.rollback()
                                logger.error(f"❌ Failed to commit article '{entry_data.get('title', 'Unknown')}': {commit_error}")
                                continue
                                
                    except Exception as article_error:
                        logger.error(f"❌ Failed to process article '{entry_data.get('title', 'Unknown')}': {article_error}")
                        # Continue processing other articles
                        continue
            
            logger.info(f"News aggregation completed. Added {total_new_articles} new articles.")
            
        except Exception as e:
            logger.error(f"Error during news aggregation: {e}")
        finally:
            db.close()
        
        return total_new_articles

# Global aggregator instance
aggregator = RSSAggregator()