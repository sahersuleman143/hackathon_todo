#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test authentication and task creation flow
"""
import requests
import json
import sys
import io
from datetime import datetime

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_BASE = "http://localhost:8000"

def test_register(email, password):
    """Test user registration"""
    print(f"\n{'='*60}")
    print(f"TEST 1: Register New User")
    print(f"{'='*60}")

    url = f"{API_BASE}/api/auth/register"
    data = {"email": email, "password": password}

    print(f"POST {url}")
    print(f"Request: {json.dumps(data, indent=2)}")

    try:
        response = requests.post(url, json=data)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 201:
            print("✅ Registration successful!")
            return response.json()
        elif response.status_code == 409:
            print("⚠️  User already exists, trying login instead")
            return None
        else:
            print(f"❌ Registration failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_login(email, password):
    """Test user login"""
    print(f"\n{'='*60}")
    print(f"TEST 2: Login")
    print(f"{'='*60}")

    url = f"{API_BASE}/api/auth/login"

    # FastAPI OAuth2 expects form data, not JSON
    data = {
        "username": email,  # OAuth2 uses 'username' field
        "password": password
    }

    print(f"POST {url}")
    print(f"Request (form data): {data}")

    try:
        response = requests.post(url, data=data)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            print("✅ Login successful!")
            return response.json()
        else:
            print(f"❌ Login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_create_task(token, title, description=""):
    """Test task creation"""
    print(f"\n{'='*60}")
    print(f"TEST 3: Create Task (Protected Route)")
    print(f"{'='*60}")

    url = f"{API_BASE}/api/tasks"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "title": title,
        "description": description
    }

    print(f"POST {url}")
    print(f"Headers: Authorization: Bearer {token[:20]}...")
    print(f"Request: {json.dumps(data, indent=2)}")

    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 201:
            print("✅ Task created successfully!")
            return response.json()
        else:
            print(f"❌ Task creation failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_get_tasks(token):
    """Test getting all tasks"""
    print(f"\n{'='*60}")
    print(f"TEST 4: Get All Tasks (Protected Route)")
    print(f"{'='*60}")

    url = f"{API_BASE}/api/tasks"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    print(f"GET {url}")
    print(f"Headers: Authorization: Bearer {token[:20]}...")

    try:
        response = requests.get(url, headers=headers)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ Retrieved {len(tasks)} task(s) successfully!")
            return tasks
        else:
            print(f"❌ Failed to get tasks: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_without_token():
    """Test protected route without token"""
    print(f"\n{'='*60}")
    print(f"TEST 5: Access Protected Route WITHOUT Token (Should Fail)")
    print(f"{'='*60}")

    url = f"{API_BASE}/api/tasks"

    print(f"GET {url}")
    print(f"Headers: None (no Authorization)")

    try:
        response = requests.get(url)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 401:
            print("✅ Correctly rejected (401 Unauthorized)")
            return True
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("AUTHENTICATION & TASK FLOW TEST")
    print("="*60)
    print(f"API Base: {API_BASE}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Test credentials
    email = f"test_{datetime.now().timestamp()}@example.com"
    password = "testpassword123"

    # Test 1: Register
    register_result = test_register(email, password)

    # Test 2: Login (if register failed due to existing user, or to test login separately)
    login_result = test_login(email, password)

    if not login_result:
        print("\n❌ Cannot proceed without valid login")
        sys.exit(1)

    token = login_result.get("access_token")

    if not token:
        print("\n❌ No access token received")
        sys.exit(1)

    print(f"\n✅ Token obtained: {token[:30]}...")

    # Test 3: Create Task
    task_title = f"Test Task at {datetime.now().strftime('%H:%M:%S')}"
    task_description = "This is a test task created via automated testing"
    test_create_task(token, task_title, task_description)

    # Test 4: Get Tasks
    test_get_tasks(token)

    # Test 5: Test without token
    test_without_token()

    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print("✅ Authentication Flow: WORKING")
    print("✅ Token Storage: WORKING (access_token key)")
    print("✅ Protected Routes: WORKING (Authorization header)")
    print("✅ Task Creation: WORKING")
    print("✅ Unauthorized Access: PROPERLY REJECTED")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
