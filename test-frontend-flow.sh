#!/bin/bash

# Test Frontend Flow Script
echo "======================================"
echo "Testing Full-Stack Todo App Flow"
echo "======================================"
echo ""

# Test 1: Check backend is running
echo "1. Testing Backend (http://localhost:8000)..."
BACKEND_ROOT=$(curl -s http://localhost:8000/)
if [[ $BACKEND_ROOT == *"Todo API is running"* ]]; then
    echo "   ✓ Backend is running"
else
    echo "   ✗ Backend is NOT running"
    exit 1
fi
echo ""

# Test 2: Check frontend is running
echo "2. Testing Frontend (http://localhost:3001)..."
FRONTEND_ROOT=$(curl -s http://localhost:3001/ | head -n 1)
if [[ $FRONTEND_ROOT == *"<!DOCTYPE html>"* ]]; then
    echo "   ✓ Frontend is running"
else
    echo "   ✗ Frontend is NOT running"
    exit 1
fi
echo ""

# Test 3: Test user registration
echo "3. Testing User Registration..."
REGISTER_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"testuser@example.com","password":"testpass123"}')

if [[ $REGISTER_RESPONSE == *"access_token"* ]]; then
    echo "   ✓ Registration successful"
    ACCESS_TOKEN=$(echo $REGISTER_RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    echo "   Token: ${ACCESS_TOKEN:0:20}..."
else
    echo "   ⚠ Registration response: $REGISTER_RESPONSE"
    # Try login instead if user already exists
    echo ""
    echo "3b. Testing User Login (user may already exist)..."
    LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -d "username=testuser@example.com&password=testpass123")

    if [[ $LOGIN_RESPONSE == *"access_token"* ]]; then
        echo "   ✓ Login successful"
        ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
        echo "   Token: ${ACCESS_TOKEN:0:20}..."
    else
        echo "   ✗ Login failed: $LOGIN_RESPONSE"
        exit 1
    fi
fi
echo ""

# Test 4: Test authenticated endpoint
echo "4. Testing Authenticated Endpoint (/api/auth/me)..."
ME_RESPONSE=$(curl -s http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $ACCESS_TOKEN")

if [[ $ME_RESPONSE == *"email"* ]]; then
    echo "   ✓ Authentication working"
    echo "   User: $ME_RESPONSE"
else
    echo "   ✗ Authentication failed: $ME_RESPONSE"
fi
echo ""

# Test 5: Check CORS headers
echo "5. Testing CORS Configuration..."
CORS_RESPONSE=$(curl -s -I -X OPTIONS http://localhost:8000/api/auth/register \
  -H "Origin: http://localhost:3001" \
  -H "Access-Control-Request-Method: POST" | grep -i "access-control")

if [[ $CORS_RESPONSE == *"access-control-allow-origin"* ]]; then
    echo "   ✓ CORS is configured"
else
    echo "   ⚠ CORS may not be configured properly"
fi
echo ""

# Summary
echo "======================================"
echo "Test Summary"
echo "======================================"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3001"
echo "Swagger UI: http://localhost:8000/docs"
echo ""
echo "Manual Testing Steps:"
echo "1. Open http://localhost:3001 in browser"
echo "2. You should be redirected to /login"
echo "3. Toggle to 'Sign up' mode"
echo "4. Register with: testuser2@example.com / password123"
echo "5. You should be redirected to /dashboard"
echo "6. Click 'Add Task' and create a task"
echo "7. Verify task appears in the list"
echo ""
echo "✓ Automated tests complete!"
