#!/bin/bash

# Quick container runner with proper environment
set -e

echo "🚀 Starting Tech News Backend Container"
echo "======================================"

# Function to print colored output
print_status() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

print_success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

print_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

print_warning() {
    echo -e "\033[1;33m[WARNING]\033[0m $1"
}

# Check if .env file exists and source it
if [ -f .env ]; then
    print_status "Loading environment from .env file..."
    export $(grep -v '^#' .env | xargs)
else
    print_warning ".env file not found, using defaults"
    export OPENAI_API_KEY=${OPENAI_API_KEY:-"demo_key"}
fi

# Remove existing database to avoid conflicts
if [ -f backend/tech_news.db ]; then
    print_status "Removing existing database to avoid conflicts..."
    rm backend/tech_news.db
fi

# Option 1: Run with docker-compose (recommended)
if command -v docker-compose &> /dev/null; then
    print_status "Starting with docker-compose..."
    
    if [ -f docker-compose.simple.yml ]; then
        OPENAI_API_KEY=${OPENAI_API_KEY} docker-compose -f docker-compose.simple.yml up --build -d
        
        print_success "Services started successfully!"
        echo ""
        echo "🌐 Available services:"
        echo "  - API: http://localhost:8000"
        echo "  - API Docs: http://localhost:8000/docs"
        echo "  - Health Check: http://localhost:8000/health"
        echo "  - Redis: localhost:6379"
        echo ""
        echo "📊 View logs:"
        echo "  docker-compose -f docker-compose.simple.yml logs -f"
        echo ""
        echo "⏹️  Stop services:"
        echo "  docker-compose -f docker-compose.simple.yml down"
        
    else
        print_error "docker-compose.simple.yml not found"
        exit 1
    fi
    
else
    # Option 2: Run with plain docker
    print_status "docker-compose not found, using plain docker..."
    
    # Start Redis
    print_status "Starting Redis..."
    docker run -d --name tech_news_redis_manual -p 6379:6379 redis:7-alpine redis-server --appendonly yes
    
    # Wait for Redis
    sleep 3
    
    # Build and run backend
    print_status "Building and starting backend..."
    cd backend
    docker build -f Dockerfile.working -t tech_news_backend .
    
    docker run -d \
        --name tech_news_api_manual \
        -p 8000:8000 \
        -e "REDIS_URL=redis://host.docker.internal:6379" \
        -e "OPENAI_API_KEY=${OPENAI_API_KEY}" \
        -e "DATABASE_URL=sqlite:///./tech_news.db" \
        tech_news_backend
    
    cd ..
    
    print_success "Containers started successfully!"
    echo ""
    echo "🌐 Available services:"
    echo "  - API: http://localhost:8000"
    echo "  - API Docs: http://localhost:8000/docs"
    echo "  - Health Check: http://localhost:8000/health"
    echo ""
    echo "📊 View logs:"
    echo "  docker logs -f tech_news_api_manual"
    echo ""
    echo "⏹️  Stop services:"
    echo "  docker stop tech_news_api_manual tech_news_redis_manual"
    echo "  docker rm tech_news_api_manual tech_news_redis_manual"
fi

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 10

# Test the API
print_status "Testing API health..."
if curl -f http://localhost:8000/health >/dev/null 2>&1; then
    print_success "✅ API is healthy and running!"
    
    echo ""
    echo "🧪 Quick test commands:"
    echo "  curl http://localhost:8000/health"
    echo "  curl http://localhost:8000/"
    echo "  open http://localhost:8000/docs"
    
else
    print_warning "❌ API health check failed"
    echo ""
    echo "🔍 Troubleshooting:"
    echo "  - Check logs: docker logs tech_news_api_simple"
    echo "  - Check if port 8000 is available"
    echo "  - Verify Redis is running: docker logs tech_news_redis_simple"
fi

echo ""
print_success "Setup complete! Your backend is ready for development."