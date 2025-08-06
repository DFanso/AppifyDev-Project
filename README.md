# 🚀 AI-Powered Tech News Aggregator

**A cutting-edge, interactive tech news aggregation platform that intelligently curates trending stories from 150+ premium sources and enables context-aware AI discussions.** Built with modern Next.js frontend, high-performance FastAPI backend, and advanced Redis caching.

## ✨ Key Features

### 🗞️ Advanced News Aggregation
- **150+ Premium Sources**: Curated RSS feeds from top tech publications, engineering blogs, and thought leaders
- **Intelligent Categorization**: AI-powered classification (Learning, Startup, Tech News, Engineering, ML/AI, Design, etc.)
- **Smart Content Extraction**: Clean, readable content with automated HTML processing
- **Real-time Updates**: Automated content aggregation with incremental processing
- **Multi-format Support**: Articles, blog posts, research papers, and announcements

### 🎯 Enhanced User Experience  
- **Drag-to-Scroll Navigation**: Smooth, intuitive category browsing with touch support
- **Dynamic Pagination**: "Load more" functionality with seamless content loading
- **Mobile-First Design**: Responsive interface with auto-scroll for mobile chat
- **Smart Search**: Full-text search with suggestions and advanced filtering
- **Persistent Sessions**: User session management with localStorage integration

### 🤖 Context-Aware AI Chat
- **Article-Aware Conversations**: AI assistant with full article context and memory
- **Instant Summarization**: Get concise summaries of complex technical articles
- **Deep Q&A**: Ask specific questions about technologies, trends, and implications
- **Topic Exploration**: Discover related concepts, companies, and developments
- **Conversation History**: Persistent chat logs with session management

### 📊 Smart Analytics & Discovery
- **Advanced Trending Algorithm**: Tech-focused keyword extraction with 500+ stop words filtering
- **Real-time Sentiment Analysis**: Emotional tone detection (positive/negative/neutral) with visual indicators
- **Bookmark Management**: Save articles with search functionality and user sessions
- **Category Intelligence**: Dynamic titles based on selected filters
- **Performance Monitoring**: Redis-powered caching with sub-second response times

## 🏗️ Architecture

```
AppifyDev-Project/
├── frontend/           # Next.js React application
│   ├── src/
│   │   ├── app/       # App Router pages
│   │   ├── components/ # React components
│   │   ├── lib/       # Utilities and API clients
│   │   └── types/     # TypeScript definitions
│   └── public/        # Static assets
├── backend/           # FastAPI Python application
│   ├── app/
│   │   ├── routers/   # API endpoints
│   │   ├── services/  # Business logic
│   │   ├── database.py # Database models
│   │   └── schemas.py # Pydantic models
│   └── scripts/       # Utility scripts
└── README.md
```

## 🛠️ Tech Stack

### Frontend Architecture
- **Next.js 14** with App Router and Server Components
- **TypeScript** for end-to-end type safety
- **Tailwind CSS** with custom design system
- **React Query** for intelligent data fetching and caching
- **Advanced Touch/Drag Handling** for mobile-first navigation
- **Session Management** with localStorage persistence
- **Component-Based Architecture** with reusable UI components

### Backend Infrastructure  
- **FastAPI** with async/await for high-performance APIs
- **UV Package Manager** for modern Python dependency management
- **SQLAlchemy ORM** with optimized queries and indexing
- **Redis Caching** with decorator pattern for performance optimization
- **Pydantic V2** for advanced data validation and serialization
- **Custom Middleware** for CORS, error handling, and request logging

### AI & Machine Learning
- **OpenAI GPT-3.5/4** integration with LangChain framework
- **Context-Aware Chat** with article content injection
- **Custom Sentiment Analysis** with weighted scoring algorithms
- **Advanced NLP Processing** for keyword extraction and trending analysis
- **Conversation Memory** with persistent session management

### Data Processing & Caching
- **Redis Cache Layer** with automatic serialization and TTL management
- **Incremental RSS Processing** with error handling and retry logic
- **BeautifulSoup + lxml** for robust content extraction
- **Smart Content Cleaning** with HTML sanitization
- **Database Optimization** with proper indexing and query optimization

## 🚀 Quick Start

### Prerequisites
- **Node.js 18+** and npm/yarn
- **Python 3.9+** (recommended 3.11+)
- **UV package manager** (`pip install uv`)
- **Redis server** (for caching - optional but recommended)
- **OpenAI API key** (for AI chat functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AppifyDev-Project
   ```

2. **Set up the backend**
   ```bash
   cd backend
   
   # Create environment file
   cp .env.example .env
   # Edit .env and add your configuration:
   # OPENAI_API_KEY=your_openai_api_key_here
   # REDIS_URL=redis://localhost:6379 (optional)
   
   # Install dependencies with UV
   uv sync
   
   # Initialize database
   uv run python -c "from app.database import init_db; init_db()"
   
   # Fetch initial news data (150+ sources)
   uv run python scripts/fetch_news.py
   ```

3. **Set up the frontend**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Start the development servers**
   
   In one terminal (backend):
   ```bash
   cd backend
   uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   In another terminal (frontend):
   ```bash
   cd frontend
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API docs: http://localhost:8000/docs

## 📊 API Endpoints

### Articles
- `GET /api/articles` - Get paginated articles with filters
- `GET /api/articles/{id}` - Get specific article
- `GET /api/articles/category/{category}` - Filter by category
- `GET /api/articles/recent/{hours}` - Get recent articles

### Chat
- `POST /api/chat` - Send message to AI assistant
- `POST /api/chat/summarize/{article_id}` - Get article summary
- `GET /api/chat/history/{user_id}` - Get chat history
- `GET /api/chat/topics/{article_id}` - Get related topics

### Search
- `GET /api/search` - Search articles with filters
- `POST /api/search` - Advanced search with complex filters
- `GET /api/search/suggestions` - Get search suggestions

### Bookmarks
- `POST /api/bookmarks` - Create bookmark
- `GET /api/bookmarks` - Get user bookmarks
- `DELETE /api/bookmarks/{id}` - Delete bookmark

### Trending
- `GET /api/trending/topics` - Get trending topics
- `GET /api/trending/categories` - Get trending categories
- `GET /api/trending/sentiment` - Get sentiment trends

## 🔧 Configuration

### Environment Configuration

**Backend (.env)**
```bash
# AI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database
DATABASE_URL=sqlite:///./tech_news.db

# Redis Cache (optional but recommended)
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=

# API Configuration  
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:3000

# News Processing
MAX_ARTICLES_PER_BATCH=50
RSS_TIMEOUT=30
```

**Frontend (.env.local)**
```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional: Analytics
# NEXT_PUBLIC_GA_ID=your_google_analytics_id
```

## 📰 News Sources

Our platform aggregates from **150+ premium tech sources** curated from the [awesome-tech-rss](https://github.com/tuan3w/awesome-tech-rss) repository:

### 🎓 Learning (7 sources)
- Ness Labs, Farnam Street, Big Think, Scott H Young, and more

### 🚀 Startup (14 sources) 
- Hacker News, TechCrunch Startups, First Round Review, Sam Altman, Andrew Chen

### 📱 Tech News (10 sources)
- The Verge, Engadget, VentureBeat, TechCrunch, Fast Company

### ⚙️ Engineering Blogs (39 sources)
- GitHub, Meta, Google, Stripe, Uber, Airbnb, Netflix, and many more

### 🤖 Machine Learning (23 sources)
- OpenAI, DeepMind, Google AI, MIT News AI, Berkeley AI Research

### 🎨 Design (12 sources)
- UX Planet, Smashing Magazine, Airbnb Design, CSS-Tricks

### 📊 Other Categories
- Psychology, Neuroscience, Science, Marketing, and more

### Adding Custom Sources
Edit `backend/app/services/rss_aggregator.py`:

```python
self.sources = {
    "Your Custom Source": {
        "url": "https://example.com/rss",
        "category_mapping": {
            "engineering": "Engineering blogs",
            "ai": "Machine Learning"
        }
    }
}
```

> 📋 **Complete Source List**: See the full list of 150+ sources in our [RSS Sources Documentation](https://github.com/tuan3w/awesome-tech-rss)

## 🤖 AI Chat Features

The AI assistant can:
- **Summarize articles**: "Can you summarize this article about AI?"
- **Answer questions**: "What are the implications of this funding round?"
- **Compare stories**: "How does this relate to the OpenAI news from last week?"
- **Explain concepts**: "What is quantum computing?"
- **Analyze trends**: "What's the trend in AI startup funding?"

## 🔄 Data Flow

1. **RSS Aggregation**: `scripts/fetch_news.py` pulls from configured sources
2. **Content Processing**: Articles are cleaned, categorized, and analyzed for sentiment
3. **Database Storage**: Processed articles stored with metadata
4. **API Serving**: FastAPI serves data to frontend with filtering/search
5. **AI Integration**: LangChain provides context-aware chat with article knowledge
6. **Real-time Updates**: Frontend polls for new content and updates

## 🧪 Development

### Running Tests
```bash
# Backend tests
cd backend
uv run pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality
```bash
# Backend linting
cd backend
uv run black . && uv run isort . && uv run flake8

# Frontend linting
cd frontend
npm run lint
```

### Database Management
```bash
# Reset database
cd backend
rm tech_news.db
uv run python -c "from app.database import init_db; init_db()"

# Fetch fresh news
uv run python scripts/fetch_news.py
```

## ⚡ Performance & Architecture

### 🚀 Caching Strategy
- **Redis-Powered Caching**: Intelligent caching with decorator pattern
- **Multi-Level TTL**: Different cache durations for different data types
  - Articles: 10 minutes
  - Trending topics: 10 minutes  
  - Search results: 10 minutes
  - Bookmarks: 5 minutes
  - Suggestions: 30 minutes
- **Cache Invalidation**: Smart cache busting on data updates
- **Fallback Handling**: Graceful degradation when Redis is unavailable

### 📊 Database Optimization
- **Strategic Indexing**: Optimized queries on published_at, category, source
- **Incremental Processing**: Batch RSS processing with commit-per-article
- **Connection Pooling**: Efficient database connection management
- **Query Optimization**: Selective field loading and join optimization

### 🔄 Real-time Processing
- **Async Processing**: Non-blocking RSS aggregation
- **Error Recovery**: Retry logic with exponential backoff
- **Rate Limiting**: Respectful RSS fetching (1-2 second delays)
- **Content Sanitization**: HTML cleaning and content extraction

### 📱 Frontend Performance
- **React Query Caching**: Intelligent client-side data management
- **Virtual Scrolling**: Efficient rendering of large article lists
- **Touch Optimization**: Smooth drag interactions with momentum scrolling
- **Lazy Loading**: Progressive image and content loading
- **Bundle Optimization**: Code splitting and tree shaking

## 🚀 Deployment

### 🏭 Production Deployment

#### Infrastructure Requirements
1. **Database**: PostgreSQL 13+ (replace SQLite)
2. **Cache**: Redis 6+ with persistence enabled
3. **Server**: Python 3.9+ with UV package manager
4. **Frontend**: Node.js 18+ for Next.js build
5. **Load Balancer**: Nginx or similar for production traffic

#### Environment Setup
```bash
# Production environment variables
export DATABASE_URL="postgresql://user:pass@localhost:5432/technews"
export REDIS_URL="redis://localhost:6379"
export OPENAI_API_KEY="your_production_key"
export FRONTEND_URL="https://yourdomain.com"
```

#### Automated News Processing
```bash
# Setup cron job for regular news fetching
# Add to crontab: crontab -e

# Fetch news every 30 minutes
*/30 * * * * cd /path/to/backend && uv run python scripts/fetch_news.py

# Daily trending analysis at 6 AM
0 6 * * * cd /path/to/backend && uv run python scripts/analyze_trends.py
```

#### Docker Deployment
```bash
# Production deployment with Docker Compose
docker-compose -f docker-compose.prod.yml up --build -d

# With scaling
docker-compose up --scale api=3 --scale worker=2
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🔥 Recent Major Updates

### v2.0 - Performance & UX Overhaul
- ✅ **Redis Caching System**: Sub-second API response times
- ✅ **Smart Session Management**: Persistent user sessions with localStorage
- ✅ **Drag Navigation**: Touch-optimized category scrolling
- ✅ **Mobile Chat UX**: Auto-scroll to chat on mobile devices
- ✅ **Advanced Trending**: Tech-focused algorithm with 500+ stop words
- ✅ **Working Pagination**: Seamless "Load more" functionality
- ✅ **Bookmark Search**: Full-text search within saved articles
- ✅ **Dynamic Titles**: Context-aware page titles based on filters
- ✅ **Message Ordering Fix**: Proper chronological chat display
- ✅ **Enhanced Sentiment UI**: Improved visual contrast for all themes

### v1.5 - Foundation
- ✅ **150+ RSS Sources**: Comprehensive tech news aggregation
- ✅ **AI Chat Integration**: Context-aware article discussions
- ✅ **Full-Text Search**: Advanced filtering and suggestions
- ✅ **Responsive Design**: Mobile-first user interface
- ✅ **Sentiment Analysis**: Automated article tone detection

## 🏆 Key Metrics

- **150+ RSS Sources** across 12 categories
- **Sub-second response times** with Redis caching
- **Mobile-optimized** touch interactions
- **Real-time trending** topic analysis
- **Context-aware AI** with article memory
- **Production-ready** codebase with comprehensive testing

## 🙏 Acknowledgments

- **RSS Sources**: [awesome-tech-rss](https://github.com/tuan3w/awesome-tech-rss) community collection
- **AI Platform**: OpenAI GPT-3.5/4 API
- **Frameworks**: FastAPI, Next.js, React Query, Tailwind CSS
- **Infrastructure**: Redis, SQLAlchemy, UV package manager
- **Open Source**: All the amazing contributors and maintainers

---

**🚀 Built for the modern tech professional who demands intelligent news curation and AI-powered insights into the rapidly evolving technology landscape.**