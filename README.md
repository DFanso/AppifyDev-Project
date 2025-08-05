# Tech News Aggregator with AI Chat

A modern, interactive tech news aggregation platform that pulls trending stories and enables AI-powered discussions around them. Built with Next.js frontend and FastAPI backend.

## 🚀 Features

### News Aggregation & Display
- **Multi-Source RSS Feeds**: Aggregates from TechCrunch, The Verge, Ars Technica, and more
- **Smart Categorization**: Auto-categorizes articles (AI/ML, Startups, Cybersecurity, Mobile, Web3)
- **Responsive Design**: Clean, modern interface optimized for all devices
- **Advanced Filtering**: Filter by category, source, sentiment, and date ranges
- **Full-Text Search**: Search across article titles, content, and summaries
- **Bookmark System**: Save articles for later reading

### AI-Powered News Chat
- **Context-Aware Conversations**: AI assistant understands the articles being discussed
- **Article Summarization**: Get concise summaries of complex tech articles
- **Q&A Capabilities**: Ask specific questions about news stories
- **Topic Analysis**: Explore related topics and trends
- **Chat History**: Persistent conversation history for reference

### Smart Features
- **Trending Topics Dashboard**: See what's hot in tech right now
- **Sentiment Analysis**: Understand the tone of tech news (positive/negative/neutral)
- **Related Articles**: Discover connected stories and developments
- **Real-time Updates**: Fresh content aggregated regularly
- **Analytics**: Track trending topics and categories over time

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

### Frontend
- **Next.js 14** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **React Query/SWR** for data fetching
- **Lucide Icons** for UI icons

### Backend
- **FastAPI** for high-performance API
- **UV** for modern Python package management
- **SQLAlchemy** for database ORM
- **SQLite** for development database
- **Pydantic** for data validation

### AI & ML
- **OpenAI GPT-3.5/4** for chat functionality
- **LangChain** for context management
- **Custom sentiment analysis** for article classification

### News Sources
- **RSS Feeds** from major tech publications
- **BeautifulSoup** for content extraction
- **Feedparser** for RSS processing

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- UV package manager (`pip install uv`)
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AppifyDev-Project
   ```

2. **Set up the backend**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   
   # Install dependencies
   uv sync
   
   # Initialize database
   uv run python -c "from app.database import init_db; init_db()"
   
   # Fetch initial news data
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

### Environment Variables

**Backend (.env)**
```bash
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./tech_news.db
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:3000
```

**Frontend (.env.local)**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📰 Adding News Sources

To add new RSS sources, edit `backend/app/services/rss_aggregator.py`:

```python
self.sources = {
    "Your Source": {
        "url": "https://yoursource.com/rss",
        "category_mapping": {
            "tech": "General",
            "ai": "AI/ML",
            # ... more mappings
        }
    }
}
```

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

## 📈 Performance Considerations

- **Caching**: API responses cached for better performance
- **Pagination**: Large datasets paginated to reduce load times
- **Rate Limiting**: RSS fetching respects source rate limits
- **Database Indexing**: Key fields indexed for fast queries
- **Content Truncation**: Long articles truncated for AI processing

## 🚀 Deployment

### Production Setup
1. Use PostgreSQL instead of SQLite
2. Set up Redis for caching
3. Configure proper CORS origins
4. Use environment-specific API keys
5. Set up automated news fetching with cron jobs

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- News sources: TechCrunch, The Verge, Ars Technica
- OpenAI for GPT API
- FastAPI and Next.js communities
- All open-source contributors

---

**Built for the modern tech professional who wants to stay informed and engage with the latest technology trends through AI-powered discussions.**