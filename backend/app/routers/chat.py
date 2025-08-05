from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db, ChatHistory
from ..schemas import ChatMessage, ChatResponse, ChatHistoryResponse
from ..services.ai_chat import get_ai_chat

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_with_ai(
    chat_message: ChatMessage,
    db: Session = Depends(get_db)
):
    """Send a message to the AI chat assistant"""
    try:
        ai_chat = get_ai_chat()
        response_data = ai_chat.generate_response(
            message=chat_message.message,
            article_id=chat_message.article_id,
            user_id=chat_message.user_id
        )
        
        if "error" in response_data:
            raise HTTPException(status_code=500, detail=response_data["error"])
        
        # Get article context if article_id provided
        article_context = None
        if chat_message.article_id:
            from ..database import Article
            article = db.query(Article).filter(Article.id == chat_message.article_id).first()
            article_context = article
        
        return ChatResponse(
            response=response_data["response"],
            article_context=article_context,
            sources=response_data.get("sources", [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat message: {str(e)}")

@router.post("/summarize/{article_id}")
async def summarize_article(article_id: int):
    """Get an AI-generated summary of a specific article"""
    try:
        ai_chat = get_ai_chat()
        summary = ai_chat.summarize_article(article_id)
        return {"summary": summary, "article_id": article_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing article: {str(e)}")

@router.get("/history/{user_id}", response_model=List[ChatHistoryResponse])
async def get_chat_history(
    user_id: str,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get chat history for a specific user"""
    try:
        history = db.query(ChatHistory).filter(
            ChatHistory.user_id == user_id
        ).order_by(ChatHistory.created_at.desc()).limit(limit).all()
        
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chat history: {str(e)}")

@router.delete("/history/{user_id}")
async def clear_chat_history(user_id: str, db: Session = Depends(get_db)):
    """Clear chat history for a specific user"""
    try:
        deleted = db.query(ChatHistory).filter(
            ChatHistory.user_id == user_id
        ).delete()
        db.commit()
        
        return {"message": f"Deleted {deleted} chat messages", "user_id": user_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error clearing chat history: {str(e)}")

@router.get("/topics/{article_id}")
async def get_article_topics(article_id: int):
    """Get related topics for an article"""
    try:
        ai_chat = get_ai_chat()
        topics = ai_chat.get_related_topics(article_id)
        return {"article_id": article_id, "topics": topics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting article topics: {str(e)}")