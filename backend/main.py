from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from app.database import init_db
from app.routers import articles, chat, bookmarks, trending, search

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup (with error handling)
    try:
        init_db()
    except Exception as e:
        print(f"Database initialization: {e}")
    yield

app = FastAPI(
    title="Tech News Aggregator API",
    description="AI-powered tech news aggregation platform with intelligent chat features",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend communication
# Configure allowed origins based on environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    # Production: Only allow specific origins
    allowed_origins = [
        "https://appify-dev-project.vercel.app",
        os.getenv("FRONTEND_URL", "https://appify-dev-project.vercel.app")
    ]
    # Remove any None values and duplicates
    allowed_origins = list(set([url for url in allowed_origins if url]))
else:
    # Development: Allow common development origins
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "https://appify-dev-project.vercel.app"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,  # Allow credentials for session management
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=[
        "accept",
        "accept-encoding",
        "authorization",
        "content-type",
        "dnt",
        "origin",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
    ],
    expose_headers=["*"],
)

# Include routers
app.include_router(articles.router, prefix="/api/articles", tags=["articles"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(bookmarks.router, prefix="/api/bookmarks", tags=["bookmarks"])
app.include_router(trending.router, prefix="/api/trending", tags=["trending"])
app.include_router(search.router, prefix="/api/search", tags=["search"])

@app.get("/")
async def root():
    return {"message": "Tech News Aggregator API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/cors-debug")
async def cors_debug():
    """Debug endpoint to check CORS configuration"""
    return {
        "environment": ENVIRONMENT,
        "allowed_origins": allowed_origins,
        "cors_settings": {
            "allow_credentials": True,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
            "allow_headers": ["accept", "accept-encoding", "authorization", "content-type", "dnt", "origin", "user-agent", "x-csrftoken", "x-requested-with"],
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
