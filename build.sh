#!/bin/bash

# Tech News Aggregator - Build and Deploy Script
set -e

echo "🚀 Tech News Aggregator - Build Script"
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

# Check if .env file exists
if [ ! -f .env ]; then
    print_error ".env file not found!"
    echo "Please copy .env.example to .env and configure your settings:"
    echo "  cp .env.example .env"
    echo "  # Edit .env with your configuration"
    exit 1
fi

# Load environment variables
source .env

# Check required environment variables
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
    print_error "OPENAI_API_KEY is not configured!"
    echo "Please set your OpenAI API key in the .env file"
    exit 1
fi

# Parse command line arguments
ENVIRONMENT=${1:-development}
COMMAND=${2:-up}

print_status "Environment: $ENVIRONMENT"
print_status "Command: $COMMAND"

case $ENVIRONMENT in
    "development"|"dev")
        print_status "Building for development..."
        
        case $COMMAND in
            "up"|"start")
                print_status "Starting development environment..."
                docker-compose up --build -d
                print_success "Development environment started!"
                echo ""
                echo "🌐 Services:"
                echo "  - API: http://localhost:8000"
                echo "  - API Docs: http://localhost:8000/docs"
                echo "  - Redis: localhost:6379"
                echo "  - PostgreSQL: localhost:5432"
                echo ""
                echo "📋 Useful commands:"
                echo "  - View logs: docker-compose logs -f"
                echo "  - Stop: docker-compose down"
                echo "  - Restart: docker-compose restart"
                ;;
            "down"|"stop")
                print_status "Stopping development environment..."
                docker-compose down
                print_success "Development environment stopped!"
                ;;
            "logs")
                docker-compose logs -f
                ;;
            "restart")
                docker-compose restart
                ;;
            *)
                print_error "Unknown command: $COMMAND"
                echo "Available commands: up, down, logs, restart"
                exit 1
                ;;
        esac
        ;;
        
    "production"|"prod")
        print_status "Building for production..."
        
        case $COMMAND in
            "up"|"start")
                print_status "Starting production environment..."
                docker-compose -f docker-compose.prod.yml up --build -d
                print_success "Production environment started!"
                echo ""
                echo "🌐 Services:"
                echo "  - API: http://localhost:8000"
                echo "  - Load Balancer: http://localhost:80"
                echo "  - Redis: localhost:6379"
                echo "  - PostgreSQL: localhost:5432"
                echo ""
                echo "📊 Monitoring:"
                echo "  - Health: curl http://localhost:8000/health"
                echo "  - Logs: docker-compose -f docker-compose.prod.yml logs -f"
                ;;
            "down"|"stop")
                print_status "Stopping production environment..."
                docker-compose -f docker-compose.prod.yml down
                print_success "Production environment stopped!"
                ;;
            "logs")
                docker-compose -f docker-compose.prod.yml logs -f
                ;;
            "scale")
                REPLICAS=${3:-2}
                print_status "Scaling API to $REPLICAS replicas..."
                docker-compose -f docker-compose.prod.yml up --scale api=$REPLICAS -d
                print_success "Scaled to $REPLICAS API replicas!"
                ;;
            *)
                print_error "Unknown command: $COMMAND"
                echo "Available commands: up, down, logs, scale"
                exit 1
                ;;
        esac
        ;;
        
    "test")
        print_status "Running tests..."
        cd backend
        
        # Check if UV is installed
        if ! command -v uv &> /dev/null; then
            print_error "UV is not installed!"
            echo "Please install UV: pip install uv"
            exit 1
        fi
        
        # Run tests (if test framework is set up)
        print_status "Installing dependencies..."
        uv sync
        
        print_status "Running API health check..."
        if curl -f http://localhost:8000/health > /dev/null 2>&1; then
            print_success "API is healthy!"
        else
            print_error "API is not responding. Please start the development environment first."
            exit 1
        fi
        
        cd ..
        print_success "Tests completed!"
        ;;
        
    "clean")
        print_status "Cleaning up Docker resources..."
        
        print_status "Stopping all containers..."
        docker-compose down 2>/dev/null || true
        docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
        
        print_status "Removing unused images..."
        docker image prune -f
        
        print_status "Removing unused volumes..."
        docker volume prune -f
        
        print_status "Removing unused networks..."
        docker network prune -f
        
        print_success "Cleanup completed!"
        ;;
        
    "help"|"-h"|"--help")
        echo "Usage: $0 <environment> <command> [options]"
        echo ""
        echo "Environments:"
        echo "  development, dev    - Development environment with hot reload"
        echo "  production, prod    - Production environment with load balancing"
        echo "  test               - Run tests and health checks"
        echo "  clean              - Clean up Docker resources"
        echo ""
        echo "Commands:"
        echo "  up, start          - Start the environment"
        echo "  down, stop         - Stop the environment"
        echo "  logs               - View logs"
        echo "  restart            - Restart services"
        echo "  scale <replicas>   - Scale API service (production only)"
        echo ""
        echo "Examples:"
        echo "  $0 dev up         - Start development environment"
        echo "  $0 prod up        - Start production environment"
        echo "  $0 prod scale 4   - Scale production API to 4 replicas"
        echo "  $0 test           - Run health checks"
        echo "  $0 clean          - Clean up Docker resources"
        ;;
        
    *)
        print_error "Unknown environment: $ENVIRONMENT"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac