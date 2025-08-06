#!/bin/bash

# Docker Network Fix Script for Tech News Aggregator
set -e

echo "🔧 Docker Network Troubleshooting Script"
echo "========================================"

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

# Check Docker status
print_status "Checking Docker status..."
if ! docker info >/dev/null 2>&1; then
    print_error "Docker is not running! Please start Docker Desktop."
    exit 1
fi
print_success "Docker is running"

# Test Docker Hub connectivity
print_status "Testing Docker Hub connectivity..."
if curl -s --max-time 10 https://registry-1.docker.io/v2/ >/dev/null; then
    print_success "Docker Hub is accessible"
else
    print_warning "Docker Hub connectivity issues detected"
    
    echo ""
    print_status "Trying alternative solutions..."
    
    # Solution 1: Restart Docker Desktop
    echo "1. Restart Docker Desktop:"
    echo "   - Close Docker Desktop completely"
    echo "   - Restart Docker Desktop"
    echo "   - Wait for it to fully start"
    echo ""
    
    # Solution 2: Use alternative registry
    echo "2. Try using a mirror registry:"
    echo "   docker build . -t backend --build-arg DOCKER_REGISTRY=ghcr.io"
    echo ""
    
    # Solution 3: Use local Dockerfile
    echo "3. Use the local Dockerfile variant:"
    echo "   cd backend"
    echo "   docker build -f Dockerfile.local -t backend ."
    echo ""
    
    # Solution 4: Check DNS
    echo "4. Check DNS resolution:"
    echo "   nslookup registry-1.docker.io"
    echo ""
    
    read -p "Do you want me to try alternative Dockerfiles automatically? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Trying robust Dockerfile..."
        cd backend
        docker build -f Dockerfile.robust -t tech_news_backend .
        if [ $? -eq 0 ]; then
            print_success "Robust build successful!"
            echo "You can now run: docker run -p 8000:8000 tech_news_backend"
        else
            print_warning "Robust build failed, trying local Dockerfile..."
            docker build -f Dockerfile.local -t tech_news_backend .
            if [ $? -eq 0 ]; then
                print_success "Local build successful!"
                echo "You can now run: docker run -p 8000:8000 tech_news_backend"
            else
                print_error "All alternative builds failed"
            fi
        fi
        cd ..
    fi
    
    exit 1
fi

# Check specific Python image
print_status "Checking Python 3.11 slim image availability..."
if docker pull python:3.11-slim >/dev/null 2>&1; then
    print_success "Python 3.11 slim image pulled successfully"
    
    print_status "Building backend with original Dockerfile..."
    cd backend
    docker build -t tech_news_backend .
    if [ $? -eq 0 ]; then
        print_success "Backend build successful!"
        echo ""
        echo "🚀 You can now run:"
        echo "   docker run -p 8000:8000 tech_news_backend"
        echo "   OR"
        echo "   ./build.sh dev up"
    else
        print_error "Build failed. Check the logs above."
    fi
    cd ..
else
    print_warning "Cannot pull Python 3.11 slim image"
    
    print_status "Trying with full Python image..."
    cd backend
    docker build -f Dockerfile.local -t tech_news_backend .
    if [ $? -eq 0 ]; then
        print_success "Backend build successful with alternative image!"
    else
        print_error "Build failed with alternative image too"
    fi
    cd ..
fi

# Check for UV permission issues
print_status "Checking for UV permission issues..."
if docker build . -t test-build --no-cache 2>&1 | grep -q "Permission denied.*\.venv"; then
    print_warning "UV virtual environment permission issue detected!"
    
    echo ""
    echo "🔧 UV Permission Fix Options:"
    echo "1. Use robust Dockerfile: docker build -f backend/Dockerfile.robust -t backend ."
    echo "2. Use no-cache Dockerfile: docker build -f backend/Dockerfile.no-cache -t backend ."
    echo "3. Run as root during build: use the updated Dockerfile (should be fixed now)"
    echo ""
    
    read -p "Try the robust Dockerfile now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd backend
        docker build -f Dockerfile.robust -t backend .
        if [ $? -eq 0 ]; then
            print_success "UV permission issue resolved!"
        fi
        cd ..
    fi
fi

echo ""
print_status "Docker troubleshooting complete!"
echo ""
echo "🔍 If problems persist, try:"
echo "1. Restart Docker Desktop"
echo "2. Clear Docker cache: docker system prune -a"
echo "3. Check your internet connection"
echo "4. Try a VPN if behind corporate firewall"
echo "5. Use: docker build --no-cache for fresh build"
echo "6. For UV issues: docker build -f backend/Dockerfile.robust -t backend ."