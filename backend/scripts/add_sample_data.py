#!/usr/bin/env python3
"""
Add sample data to the database for testing
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, Article, init_db

def add_sample_articles():
    """Add sample articles for testing"""
    init_db()
    db = SessionLocal()
    
    sample_articles = [
        {
            "title": "OpenAI Releases New GPT-4 Turbo Model with Enhanced Capabilities",
            "url": "https://example.com/openai-gpt4-turbo",
            "content": "OpenAI has announced the release of GPT-4 Turbo, featuring improved reasoning capabilities and reduced hallucinations. The new model shows significant improvements in code generation and mathematical reasoning tasks.",
            "summary": "OpenAI releases GPT-4 Turbo with enhanced reasoning and reduced errors.",
            "author": "Tech Reporter",
            "published_at": datetime.utcnow() - timedelta(hours=2),
            "source": "TechCrunch",
            "category": "AI/ML",
            "sentiment": "positive",
            "image_url": "https://example.com/images/openai.jpg"
        },
        {
            "title": "Tesla's Full Self-Driving Beta Expands to More Cities",
            "url": "https://example.com/tesla-fsd-expansion",
            "content": "Tesla continues its rollout of Full Self-Driving beta software to additional metropolitan areas. The expansion includes improved navigation and safety features based on real-world driving data.",
            "summary": "Tesla expands FSD beta to more cities with improved safety features.",
            "author": "Auto News",
            "published_at": datetime.utcnow() - timedelta(hours=4),
            "source": "The Verge",
            "category": "Mobile",
            "sentiment": "positive",
            "image_url": "https://example.com/images/tesla.jpg"
        },
        {
            "title": "Major Security Vulnerability Discovered in Popular Web Framework",
            "url": "https://example.com/security-vulnerability",
            "content": "Security researchers have identified a critical vulnerability in a widely-used web framework that could allow remote code execution. Patches are being rolled out immediately.",
            "summary": "Critical security flaw found in popular web framework, patches available.",
            "author": "Security Team",
            "published_at": datetime.utcnow() - timedelta(hours=6),
            "source": "Ars Technica",
            "category": "Cybersecurity",
            "sentiment": "negative",
            "image_url": "https://example.com/images/security.jpg"
        },
        {
            "title": "Startup Raises $50M Series B for AI-Powered Healthcare Platform",
            "url": "https://example.com/startup-funding",
            "content": "Healthcare AI startup MedTech Solutions has closed a $50 million Series B funding round led by venture capital firm Innovation Partners. The funds will be used to expand their diagnostic AI platform.",
            "summary": "MedTech Solutions raises $50M for AI healthcare platform expansion.",
            "author": "Funding News",
            "published_at": datetime.utcnow() - timedelta(hours=8),
            "source": "TechCrunch",
            "category": "Startups",
            "sentiment": "positive",
            "image_url": "https://example.com/images/medtech.jpg"
        },
        {
            "title": "New Cryptocurrency Exchange Launches with Advanced Trading Features",
            "url": "https://example.com/crypto-exchange",
            "content": "CryptoTrade Pro has launched with institutional-grade trading tools and enhanced security measures. The platform supports over 200 digital assets and offers advanced order types.",
            "summary": "New crypto exchange CryptoTrade Pro launches with advanced features.",
            "author": "Crypto Reporter",
            "published_at": datetime.utcnow() - timedelta(hours=12),
            "source": "Hacker News",
            "category": "Web3",
            "sentiment": "neutral",
            "image_url": "https://example.com/images/crypto.jpg"
        },
        {
            "title": "Apple Announces New MacBook Pro with M3 Chip",
            "url": "https://example.com/apple-macbook-m3",
            "content": "Apple has unveiled the new MacBook Pro lineup featuring the powerful M3 chip with improved performance and battery life. The new models offer up to 22 hours of battery life.",
            "summary": "Apple launches new MacBook Pro with M3 chip and extended battery life.",
            "author": "Apple News",
            "published_at": datetime.utcnow() - timedelta(hours=16),
            "source": "The Verge",
            "category": "General",
            "sentiment": "positive",
            "image_url": "https://example.com/images/macbook.jpg"
        },
        {
            "title": "Machine Learning Breakthrough in Medical Diagnosis",
            "url": "https://example.com/ml-medical-breakthrough",
            "content": "Researchers have developed a new machine learning model that can diagnose rare diseases with 95% accuracy, potentially revolutionizing medical diagnosis for conditions that currently take months to identify.",
            "summary": "New ML model achieves 95% accuracy in diagnosing rare diseases.",
            "author": "Medical AI Team",
            "published_at": datetime.utcnow() - timedelta(hours=20),
            "source": "Ars Technica",
            "category": "AI/ML",
            "sentiment": "positive",
            "image_url": "https://example.com/images/medical-ai.jpg"
        },
        {
            "title": "Data Breach Affects Millions of Users on Social Platform",
            "url": "https://example.com/data-breach-social",
            "content": "A major social media platform has confirmed a data breach affecting 10 million user accounts. The company is implementing additional security measures and notifying affected users.",
            "summary": "Social platform reports data breach affecting 10 million users.",
            "author": "Security News",
            "published_at": datetime.utcnow() - timedelta(hours=24),
            "source": "TechCrunch",
            "category": "Cybersecurity",
            "sentiment": "negative",
            "image_url": "https://example.com/images/breach.jpg"
        }
    ]
    
    try:
        added_count = 0
        for article_data in sample_articles:
            # Check if article already exists
            existing = db.query(Article).filter(Article.url == article_data["url"]).first()
            if not existing:
                article = Article(**article_data)
                db.add(article)
                added_count += 1
        
        db.commit()
        print(f"✅ Added {added_count} sample articles to the database")
        
        # Show summary
        total_articles = db.query(Article).count()
        print(f"📊 Total articles in database: {total_articles}")
        
        # Show category distribution
        from sqlalchemy import func
        categories = db.query(Article.category, func.count(Article.id)).group_by(Article.category).all()
        print("\n📈 Category distribution:")
        for category, count in categories:
            print(f"  - {category}: {count} articles")
            
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_articles()