import os
import logging
from typing import Optional, List, Dict
from datetime import datetime

from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from ..database import SessionLocal, Article, ChatHistory

logger = logging.getLogger(__name__)

class AINewsChat:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            logger.error("Available environment variables: %s", [k for k in os.environ.keys() if 'OPENAI' in k or 'API' in k])
        else:
            logger.info("OpenAI API key found and configured")
            logger.info("API key starts with: %s", self.openai_api_key[:10] + "..." if len(self.openai_api_key) > 10 else "invalid")
        
        # Temporarily disable ChatOpenAI for Docker compatibility
        self.llm = None
        if self.openai_api_key:
            try:
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    api_key=self.openai_api_key,
                    model="gpt-3.5-turbo",
                    temperature=0.7,
                    max_tokens=1000
                )
                logger.info("✅ ChatOpenAI initialized successfully")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize ChatOpenAI: {e}")
                logger.info("📝 Continuing without AI chat (compatibility mode)")
                self.llm = None
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            max_token_limit=2000
        )
        
        # System prompt for the AI assistant
        self.system_prompt = """You are an intelligent tech news assistant. You help users understand and discuss technology news articles.

Your capabilities include:
- Summarizing tech articles in clear, concise language
- Answering questions about specific news stories and their implications
- Providing context and background on technology topics
- Comparing related stories and developments
- Explaining technical concepts in accessible terms
- Analyzing trends and their potential impact

Guidelines:
- Be informative and engaging
- Use clear, professional language
- Provide accurate information based on the article content
- When discussing articles, reference specific details from the content
- If you don't have enough information, say so clearly
- Stay focused on technology and business topics
- Be objective and balanced in your analysis

When a user references a specific article, use the article content provided to give detailed, contextual responses."""

        # Create the chat prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "Article Context: {article_context}\n\nUser Question: {question}")
        ])
        
        # Create the conversation chain
        if self.llm:
            self.chain = (
                RunnablePassthrough() |
                self.prompt |
                self.llm |
                StrOutputParser()
            )
    
    def get_article_context(self, article_id: Optional[int]) -> str:
        """Get article content for context"""
        if not article_id:
            return "No specific article referenced."
        
        db = SessionLocal()
        try:
            article = db.query(Article).filter(Article.id == article_id).first()
            if not article:
                return "Article not found."
            
            context = f"""
            Title: {article.title}
            Source: {article.source}
            Category: {article.category}
            Published: {article.published_at}
            
            Content: {article.content[:2000]}{'...' if len(article.content) > 2000 else ''}
            
            Summary: {article.summary}
            """
            return context.strip()
            
        except Exception as e:
            logger.error(f"Error getting article context: {e}")
            return "Error retrieving article information."
        finally:
            db.close()
    
    def get_chat_history(self, user_id: Optional[str] = None) -> List[BaseMessage]:
        """Load recent chat history for context"""
        if not user_id:
            return []
        
        db = SessionLocal()
        try:
            recent_chats = db.query(ChatHistory).filter(
                ChatHistory.user_id == user_id
            ).order_by(ChatHistory.created_at.desc()).limit(10).all()
            
            messages = []
            for chat in reversed(recent_chats):  # Reverse to get chronological order
                messages.append(HumanMessage(content=chat.message))
                messages.append(AIMessage(content=chat.response))
            
            return messages
            
        except Exception as e:
            logger.error(f"Error loading chat history: {e}")
            return []
        finally:
            db.close()
    
    def save_chat_history(self, user_id: Optional[str], article_id: Optional[int], 
                         message: str, response: str):
        """Save chat interaction to database"""
        db = SessionLocal()
        try:
            chat_record = ChatHistory(
                user_id=user_id or "anonymous",
                article_id=article_id,
                message=message,
                response=response
            )
            db.add(chat_record)
            db.commit()
            
        except Exception as e:
            logger.error(f"Error saving chat history: {e}")
            db.rollback()
        finally:
            db.close()
    
    def generate_response(self, message: str, article_id: Optional[int] = None,
                         user_id: Optional[str] = None) -> Dict[str, any]:
        """Generate AI response with article context"""
        if not self.llm:
            return {
                "response": "AI chat is not available. Please configure OPENAI_API_KEY.",
                "error": "API key not configured"
            }
        
        try:
            # Get article context
            article_context = self.get_article_context(article_id)
            
            # Load chat history for context
            chat_history = self.get_chat_history(user_id)
            
            # Generate response
            response = self.chain.invoke({
                "question": message,
                "article_context": article_context,
                "chat_history": chat_history
            })
            
            # Save to chat history
            self.save_chat_history(user_id, article_id, message, response)
            
            # Update memory with new interaction
            self.memory.chat_memory.add_user_message(message)
            self.memory.chat_memory.add_ai_message(response)
            
            return {
                "response": response,
                "article_id": article_id,
                "sources": [f"Article ID: {article_id}"] if article_id else []
            }
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return {
                "response": "I'm sorry, I encountered an error while processing your request. Please try again.",
                "error": str(e)
            }
    
    def summarize_article(self, article_id: int) -> str:
        """Generate a summary of a specific article"""
        article_context = self.get_article_context(article_id)
        if "Article not found" in article_context:
            return "Article not found."
        
        try:
            summary_prompt = f"""
            Please provide a concise summary of this tech news article in 2-3 sentences:
            
            {article_context}
            
            Focus on: What happened, why it's important, and potential implications.
            """
            
            response = self.generate_response(
                "Please summarize this article.",
                article_id=article_id
            )
            
            return response.get("response", "Unable to generate summary.")
            
        except Exception as e:
            logger.error(f"Error summarizing article: {e}")
            return "Error generating article summary."
    
    def get_related_topics(self, article_id: int) -> List[str]:
        """Extract related topics from an article"""
        db = SessionLocal()
        try:
            article = db.query(Article).filter(Article.id == article_id).first()
            if not article:
                return []
            
            # Extract topics from title and content
            text = f"{article.title} {article.content}".lower()
            
            # Common tech topics
            topics = []
            tech_topics = {
                "artificial intelligence": ["ai", "machine learning", "neural network", "deep learning"],
                "blockchain": ["bitcoin", "ethereum", "cryptocurrency", "web3"],
                "cybersecurity": ["security", "hack", "breach", "vulnerability"],
                "mobile": ["smartphone", "ios", "android", "mobile app"],
                "startups": ["funding", "venture capital", "ipo", "unicorn"],
                "big tech": ["google", "apple", "microsoft", "amazon", "meta"]
            }
            
            for topic, keywords in tech_topics.items():
                if any(keyword in text for keyword in keywords):
                    topics.append(topic)
            
            return topics[:5]  # Return top 5 topics
            
        except Exception as e:
            logger.error(f"Error extracting topics: {e}")
            return []
        finally:
            db.close()

# Global chat instance - lazy loaded
_ai_chat_instance = None

def get_ai_chat():
    """Get or create the AI chat instance"""
    global _ai_chat_instance
    if _ai_chat_instance is None:
        _ai_chat_instance = AINewsChat()
    return _ai_chat_instance

# For backward compatibility
ai_chat = get_ai_chat()