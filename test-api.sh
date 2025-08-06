#!/bin/bash

# Quick API test script
echo "🧪 Testing API Endpoints"
echo "======================="

API_URL="http://localhost:8000"

# Test health endpoint
echo "Testing health endpoint..."
if curl -f $API_URL/health 2>/dev/null | grep -q "healthy"; then
    echo "✅ Health endpoint: PASSED"
else
    echo "❌ Health endpoint: FAILED"
    exit 1
fi

# Test root endpoint
echo "Testing root endpoint..."
if curl -f $API_URL/ 2>/dev/null | grep -q "Tech News Aggregator"; then
    echo "✅ Root endpoint: PASSED"
else
    echo "❌ Root endpoint: FAILED"
fi

# Test articles endpoint (should work even with empty database)
echo "Testing articles endpoint..."
if curl -f $API_URL/api/articles 2>/dev/null; then
    echo "✅ Articles endpoint: PASSED"
else
    echo "❌ Articles endpoint: FAILED"
fi

echo ""
echo "🎉 Basic API tests completed!"
echo "📖 API Documentation: $API_URL/docs"