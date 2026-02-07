#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete UI Flow Test - Login to Task Creation
"""
import requests
import json
import sys
import io
from datetime import datetime

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_BASE = "http://localhost:8000"

def print_header(title):
    print(f"\n{'='*70}")
    print(f"   {title}")
    print(f"{'='*70}\n")

def test_complete_flow():
    """Test complete user flow"""

    print_header("🎨 COMPLETE UI FLOW TEST")

    # Test credentials
    timestamp = datetime.now().timestamp()
    email = f"uitest_{timestamp}@example.com"
    password = "testpass123"

    print(f"📧 Test User: {email}")
    print(f"🔒 Password: {password}")

    # Step 1: Register
    print_header("Step 1: User Registration")

    register_url = f"{API_BASE}/api/auth/register"
    register_data = {"email": email, "password": password}

    try:
        response = requests.post(register_url, json=register_data)
        print(f"POST {register_url}")
        print(f"Status: {response.status_code}")

        if response.status_code == 201:
            data = response.json()
            token = data['access_token']
            print(f"✅ Registration successful!")
            print(f"🎫 Token: {token[:30]}...")
        else:
            print(f"❌ Registration failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    # Step 2: Create First Task
    print_header("Step 2: Create First Task")

    task1_url = f"{API_BASE}/api/tasks"
    task1_data = {
        "title": "Buy groceries",
        "description": "Milk, eggs, bread, and butter"
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(task1_url, json=task1_data, headers=headers)
        print(f"POST {task1_url}")
        print(f"Status: {response.status_code}")

        if response.status_code == 201:
            task1 = response.json()
            print(f"✅ Task created successfully!")
            print(f"   ID: {task1['id']}")
            print(f"   Title: {task1['title']}")
            print(f"   Description: {task1['description']}")
        else:
            print(f"❌ Task creation failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    # Step 3: Create Second Task
    print_header("Step 3: Create Second Task")

    task2_data = {
        "title": "Finish project report",
        "description": "Complete the Q4 analysis and submit by Friday"
    }

    try:
        response = requests.post(task1_url, json=task2_data, headers=headers)
        print(f"POST {task1_url}")
        print(f"Status: {response.status_code}")

        if response.status_code == 201:
            task2 = response.json()
            print(f"✅ Task created successfully!")
            print(f"   ID: {task2['id']}")
            print(f"   Title: {task2['title']}")
        else:
            print(f"❌ Task creation failed")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    # Step 4: Get All Tasks
    print_header("Step 4: Get All Tasks (Verify Auto-Refresh)")

    try:
        response = requests.get(task1_url, headers=headers)
        print(f"GET {task1_url}")
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ Tasks retrieved successfully!")
            print(f"📋 Total tasks: {len(tasks)}")
            print(f"\nTask List:")
            for i, task in enumerate(tasks, 1):
                print(f"  {i}. [{task['id']}] {task['title']}")
                print(f"     Status: {'✓ Done' if task['completed'] else '○ Pending'}")
                print(f"     Created: {task['created_at'][:19]}")
        else:
            print(f"❌ Failed to get tasks")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    # Final Summary
    print_header("✅ TEST SUMMARY")

    print("✅ User Registration: PASSED")
    print("✅ Task Creation #1: PASSED")
    print("✅ Task Creation #2: PASSED")
    print("✅ Task List Retrieval: PASSED")
    print(f"✅ Total Tasks Created: {len(tasks)}")

    print(f"\n{'='*70}")
    print("   🎉 ALL BACKEND TESTS PASSED!")
    print(f"{'='*70}\n")

    print("📱 NOW TEST IN BROWSER:")
    print(f"   1. Open: http://localhost:3000/login")
    print(f"   2. Login with: {email}")
    print(f"   3. Password: {password}")
    print(f"   4. Should see {len(tasks)} tasks in dashboard")
    print(f"   5. Add new task → should appear immediately!\n")

    return True

if __name__ == "__main__":
    success = test_complete_flow()
    sys.exit(0 if success else 1)
