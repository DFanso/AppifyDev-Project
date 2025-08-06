from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db, Bookmark, Article
from ..schemas import BookmarkCreate, BookmarkResponse
from ..services.redis_cache import CacheInvalidator
from ..decorators import cached

router = APIRouter()

@router.post("/", response_model=BookmarkResponse)
async def create_bookmark(
    bookmark: BookmarkCreate,
    db: Session = Depends(get_db)
):
    """Create a new bookmark"""
    # Check if article exists
    article = db.query(Article).filter(Article.id == bookmark.article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Check if bookmark already exists
    existing_bookmark = db.query(Bookmark).filter(
        Bookmark.article_id == bookmark.article_id,
        Bookmark.user_id == (bookmark.user_id or "anonymous")
    ).first()
    
    if existing_bookmark:
        raise HTTPException(status_code=409, detail="Article already bookmarked")
    
    # Create new bookmark
    db_bookmark = Bookmark(
        article_id=bookmark.article_id,
        user_id=bookmark.user_id or "anonymous"
    )
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    
    # Invalidate user's bookmarks cache
    CacheInvalidator.invalidate_user_bookmarks(db_bookmark.user_id)
    
    # Return bookmark with article data
    return BookmarkResponse(
        id=db_bookmark.id,
        article_id=db_bookmark.article_id,
        article=article,
        created_at=db_bookmark.created_at
    )

@router.get("/", response_model=List[BookmarkResponse])
@cached(ttl=300, key_prefix="bookmarks")  # 5 minutes
async def get_bookmarks(
    user_id: str = "anonymous",
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get all bookmarks for a user"""
    bookmarks = db.query(Bookmark).filter(
        Bookmark.user_id == user_id
    ).order_by(Bookmark.created_at.desc()).offset(skip).limit(limit).all()
    
    # Fetch articles for each bookmark
    result = []
    for bookmark in bookmarks:
        article = db.query(Article).filter(Article.id == bookmark.article_id).first()
        if article:
            result.append(BookmarkResponse(
                id=bookmark.id,
                article_id=bookmark.article_id,
                article=article,
                created_at=bookmark.created_at
            ))
    
    return result

@router.delete("/{bookmark_id}")
async def delete_bookmark(bookmark_id: int, db: Session = Depends(get_db)):
    """Delete a bookmark"""
    bookmark = db.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    user_id = bookmark.user_id
    db.delete(bookmark)
    db.commit()
    
    # Invalidate user's bookmarks cache
    CacheInvalidator.invalidate_user_bookmarks(user_id)
    
    return {"message": "Bookmark deleted successfully"}

@router.delete("/article/{article_id}")
async def delete_bookmark_by_article(
    article_id: int,
    user_id: str = "anonymous",
    db: Session = Depends(get_db)
):
    """Delete a bookmark by article ID"""
    bookmark = db.query(Bookmark).filter(
        Bookmark.article_id == article_id,
        Bookmark.user_id == user_id
    ).first()
    
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    db.delete(bookmark)
    db.commit()
    
    # Invalidate user's bookmarks cache
    CacheInvalidator.invalidate_user_bookmarks(user_id)
    
    return {"message": "Bookmark deleted successfully"}

@router.get("/check/{article_id}")
async def check_bookmark(
    article_id: int,
    user_id: str = "anonymous",
    db: Session = Depends(get_db)
):
    """Check if an article is bookmarked"""
    bookmark = db.query(Bookmark).filter(
        Bookmark.article_id == article_id,
        Bookmark.user_id == user_id
    ).first()
    
    return {"is_bookmarked": bookmark is not None}