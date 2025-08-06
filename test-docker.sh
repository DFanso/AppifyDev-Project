#!/bin/bash

# Test Docker Build Script
set -e

echo "🧪 Testing Docker Build Options"
echo "==============================="

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

cd backend

print_status "Testing Dockerfile options..."

# Test 1: Working Dockerfile (Pure pip with fixed versions)
echo ""
print_status "1. Testing working Dockerfile (Pure pip with fixed versions)..."
if docker build -f Dockerfile.working -t test-working . --quiet; then
    print_success "Working Dockerfile: PASSED"
    WORKING_SUCCESS=true
else
    print_error "Working Dockerfile: FAILED"
    WORKING_SUCCESS=false
fi

# Test 2: Main Dockerfile (Pure pip)
echo ""
print_status "2. Testing main Dockerfile (Pure pip)..."
if docker build -f Dockerfile -t test-main . --quiet; then
    print_success "Main Dockerfile: PASSED"
    MAIN_SUCCESS=true
else
    print_error "Main Dockerfile: FAILED"
    MAIN_SUCCESS=false
fi

# Test 3: System Dockerfile (Pure pip)
echo ""
print_status "3. Testing system Dockerfile (Pure pip)..."
if docker build -f Dockerfile.system -t test-system . --quiet; then
    print_success "System Dockerfile: PASSED"
    SYSTEM_SUCCESS=true
else
    print_error "System Dockerfile: FAILED" 
    SYSTEM_SUCCESS=false
fi

# Test 3: Robust Dockerfile (UV with explicit venv)
echo ""
print_status "3. Testing robust Dockerfile (UV with explicit venv)..."
if docker build -f Dockerfile.robust -t test-robust . --quiet; then
    print_success "Robust Dockerfile: PASSED"
    ROBUST_SUCCESS=true
else
    print_error "Robust Dockerfile: FAILED"
    ROBUST_SUCCESS=false
fi

# Test 4: No-cache Dockerfile (Fallback)
echo ""
print_status "4. Testing no-cache Dockerfile (Fallback)..."
if docker build -f Dockerfile.no-cache -t test-nocache . --quiet; then
    print_success "No-cache Dockerfile: PASSED"
    NOCACHE_SUCCESS=true
else
    print_error "No-cache Dockerfile: FAILED"
    NOCACHE_SUCCESS=false
fi

echo ""
echo "📊 Build Results Summary:"
echo "========================="

if [ "$MAIN_SUCCESS" = true ]; then
    echo "✅ Main Dockerfile (UV system) - RECOMMENDED"
else
    echo "❌ Main Dockerfile (UV system) - FAILED"
fi

if [ "$SYSTEM_SUCCESS" = true ]; then
    echo "✅ System Dockerfile (Pure pip) - BACKUP OPTION"
else
    echo "❌ System Dockerfile (Pure pip) - FAILED"
fi

if [ "$ROBUST_SUCCESS" = true ]; then
    echo "✅ Robust Dockerfile (UV venv) - ALTERNATIVE"
else
    echo "❌ Robust Dockerfile (UV venv) - FAILED" 
fi

if [ "$NOCACHE_SUCCESS" = true ]; then
    echo "✅ No-cache Dockerfile (Fallback) - LAST RESORT"
else
    echo "❌ No-cache Dockerfile (Fallback) - FAILED"
fi

echo ""

# Provide recommendations
if [ "$WORKING_SUCCESS" = true ]; then
    echo "🎯 RECOMMENDATION: Use the working Dockerfile"
    echo "   docker build -f Dockerfile.working -t backend ."
elif [ "$MAIN_SUCCESS" = true ]; then
    echo "🎯 RECOMMENDATION: Use the main Dockerfile"
    echo "   docker build . -t backend"
elif [ "$SYSTEM_SUCCESS" = true ]; then
    echo "🎯 RECOMMENDATION: Use the system Dockerfile"
    echo "   docker build -f Dockerfile.system -t backend ."
elif [ "$ROBUST_SUCCESS" = true ]; then
    echo "🎯 RECOMMENDATION: Use the robust Dockerfile"
    echo "   docker build -f Dockerfile.robust -t backend ."
elif [ "$NOCACHE_SUCCESS" = true ]; then
    echo "🎯 RECOMMENDATION: Use the no-cache Dockerfile"
    echo "   docker build -f Dockerfile.no-cache -t backend ."
else
    echo "❌ All Docker builds failed. Check your Docker installation and network connectivity."
    exit 1
fi

# Test run one of the successful images
echo ""
print_status "Testing container startup..."

if [ "$WORKING_SUCCESS" = true ]; then
    TEST_IMAGE="test-working"
elif [ "$MAIN_SUCCESS" = true ]; then
    TEST_IMAGE="test-main"
elif [ "$SYSTEM_SUCCESS" = true ]; then
    TEST_IMAGE="test-system"
elif [ "$ROBUST_SUCCESS" = true ]; then
    TEST_IMAGE="test-robust"
else
    TEST_IMAGE="test-nocache"
fi

echo "Starting container with image: $TEST_IMAGE"
CONTAINER_ID=$(docker run -d -p 8001:8000 $TEST_IMAGE)

sleep 5

if curl -f http://localhost:8001/health >/dev/null 2>&1; then
    print_success "Container health check: PASSED"
    echo "✅ Backend is running successfully on http://localhost:8001"
else
    print_error "Container health check: FAILED"
    echo "❌ Container started but health check failed"
    docker logs $CONTAINER_ID
fi

# Cleanup
print_status "Cleaning up test container..."
docker stop $CONTAINER_ID >/dev/null 2>&1
docker rm $CONTAINER_ID >/dev/null 2>&1

echo ""
print_success "Docker testing complete!"

cd ..