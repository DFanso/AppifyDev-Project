#!/usr/bin/env python3
"""
Simple CORS test script for the Tech News Aggregator API
"""

import requests
import sys

def test_cors(base_url, frontend_origin):
    """Test CORS configuration"""
    
    print(f"Testing CORS for:")
    print(f"Backend: {base_url}")
    print(f"Frontend: {frontend_origin}")
    print("-" * 50)
    
    # Test 1: Check CORS debug endpoint
    try:
        print("1. Testing CORS debug endpoint...")
        response = requests.get(f"{base_url}/cors-debug")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ CORS debug endpoint accessible")
            print(f"   Environment: {data.get('environment', 'unknown')}")
            print(f"   Allowed origins: {data.get('allowed_origins', [])}")
            print(f"   Frontend URL env: {data.get('frontend_url_env', 'not set')}")
        else:
            print(f"   ❌ CORS debug endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error accessing debug endpoint: {e}")
    
    print()
    
    # Test 2: Preflight request
    try:
        print("2. Testing preflight OPTIONS request...")
        headers = {
            'Origin': frontend_origin,
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'content-type'
        }
        response = requests.options(f"{base_url}/api/trending/topics", headers=headers)
        
        print(f"   Status Code: {response.status_code}")
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        
        for header, value in cors_headers.items():
            if value:
                print(f"   ✅ {header}: {value}")
            else:
                print(f"   ❌ {header}: Missing")
                
    except Exception as e:
        print(f"   ❌ Error in preflight request: {e}")
    
    print()
    
    # Test 3: Actual API request with Origin header
    try:
        print("3. Testing actual API request with Origin header...")
        headers = {
            'Origin': frontend_origin,
            'Content-Type': 'application/json'
        }
        response = requests.get(f"{base_url}/api/trending/topics?hours=168&limit=8", headers=headers)
        
        print(f"   Status Code: {response.status_code}")
        
        if 'Access-Control-Allow-Origin' in response.headers:
            print(f"   ✅ Access-Control-Allow-Origin: {response.headers['Access-Control-Allow-Origin']}")
        else:
            print(f"   ❌ Access-Control-Allow-Origin: Missing")
            
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API response received successfully")
            print(f"   Response type: {type(data)}")
        else:
            print(f"   ❌ API request failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ Error in API request: {e}")

if __name__ == "__main__":
    backend_url = "https://appify.australsolar.click"
    frontend_url = "https://appify-app.australsolar.click"
    
    if len(sys.argv) >= 2:
        backend_url = sys.argv[1]
    if len(sys.argv) >= 3:
        frontend_url = sys.argv[2]
    
    test_cors(backend_url, frontend_url)