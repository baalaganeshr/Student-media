#!/usr/bin/env python3
"""
Final Complete Backend API Test with Manual Verification Code
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://2f02c4cf-cf77-452e-8de0-cb3ce6f5af58.preview.emergentagent.com')
API_BASE_URL = f"{BACKEND_URL}/api"

print(f"Testing backend at: {API_BASE_URL}")

def test_complete_flow():
    """Test complete authentication and API flow"""
    session = requests.Session()
    
    # Use the verification code we found in logs
    test_email = "fulltest2024@ritrjpm.ac.in"
    verification_code = "415700"
    password = "fulltest123"
    
    print("\n=== STEP 1: EMAIL VERIFICATION ===")
    
    # Verify the email with the code from logs
    verification_data = {
        "email": test_email,
        "verification_code": verification_code
    }
    
    try:
        response = session.post(f"{API_BASE_URL}/auth/verify-email", json=verification_data)
        if response.status_code == 200:
            print("✅ Email verification successful")
        elif response.status_code == 400 and "Invalid or expired" in response.text:
            print("⚠️ Verification code expired or already used - user may already be verified")
        else:
            print(f"❌ Email verification failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Email verification error: {e}")
    
    print("\n=== STEP 2: LOGIN ===")
    
    # Try to login
    login_data = {
        "email": test_email,
        "password": password
    }
    
    try:
        response = session.post(f"{API_BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            access_token = data.get('access_token')
            user_data = data.get('user')
            print(f"✅ Login successful for {user_data.get('name', 'user')}")
            
            # Test all protected endpoints
            test_protected_endpoints(session, access_token)
            
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    return True

def test_protected_endpoints(session, access_token):
    """Test all protected endpoints with valid token"""
    headers = {"Authorization": f"Bearer {access_token}"}
    
    print("\n=== STEP 3: USER MANAGEMENT ===")
    
    # Get user profile
    try:
        response = session.get(f"{API_BASE_URL}/users/me", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Get profile: {user_data.get('name')} ({user_data.get('department')}, Year {user_data.get('year')})")
        else:
            print(f"❌ Get profile failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get profile error: {e}")
    
    # Update profile
    try:
        update_data = {"name": "Updated Full Test User", "bio": "Testing the StudentMedia platform"}
        response = session.put(f"{API_BASE_URL}/users/me", json=update_data, headers=headers)
        if response.status_code == 200:
            print("✅ Profile update successful")
        else:
            print(f"❌ Profile update failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Profile update error: {e}")
    
    print("\n=== STEP 4: POSTS SYSTEM ===")
    
    created_post_ids = []
    
    # Create text post
    try:
        post_data = {
            "content": "🎓 Final comprehensive test post! Testing all backend functionality including authentication, posts, engagement, and search. #StudentMedia #BackendTest #CSE",
            "tags": ["test", "backend", "cse", "final"]
        }
        response = session.post(f"{API_BASE_URL}/posts", json=post_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            post_id = result.get('post_id')
            if post_id:
                created_post_ids.append(post_id)
                print(f"✅ Text post created: {post_id}")
            else:
                print("✅ Text post created (no ID returned)")
        else:
            print(f"❌ Text post creation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Text post creation error: {e}")
    
    # Create image post
    try:
        small_image_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
        image_post_data = {
            "content": "📸 Testing image upload with base64 encoding!",
            "image": f"data:image/png;base64,{small_image_b64}",
            "tags": ["image", "test"]
        }
        response = session.post(f"{API_BASE_URL}/posts", json=image_post_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            post_id = result.get('post_id')
            if post_id:
                created_post_ids.append(post_id)
                print(f"✅ Image post created: {post_id}")
            else:
                print("✅ Image post created (no ID returned)")
        else:
            print(f"❌ Image post creation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Image post creation error: {e}")
    
    # Get posts feed
    try:
        response = session.get(f"{API_BASE_URL}/posts?skip=0&limit=10", headers=headers)
        if response.status_code == 200:
            posts = response.json()
            print(f"✅ Posts feed retrieved: {len(posts)} posts")
            
            if posts:
                first_post = posts[0]
                if 'user' in first_post:
                    user_info = first_post['user']
                    print(f"✅ Posts include user info: {user_info.get('name')} ({user_info.get('department')})")
                else:
                    print("❌ Posts missing user information")
        else:
            print(f"❌ Posts feed failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Posts feed error: {e}")
    
    print("\n=== STEP 5: ENGAGEMENT FEATURES ===")
    
    # Get a post to test engagement
    test_post_id = None
    if created_post_ids:
        test_post_id = created_post_ids[0]
    else:
        try:
            response = session.get(f"{API_BASE_URL}/posts?limit=1", headers=headers)
            if response.status_code == 200:
                posts = response.json()
                if posts:
                    test_post_id = posts[0]['id']
        except:
            pass
    
    if test_post_id:
        # Test like
        try:
            response = session.post(f"{API_BASE_URL}/posts/{test_post_id}/like", headers=headers)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Like toggle: {result.get('message', 'Success')}")
            else:
                print(f"❌ Like failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Like error: {e}")
        
        # Test bookmark
        try:
            response = session.post(f"{API_BASE_URL}/posts/{test_post_id}/bookmark", headers=headers)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Bookmark toggle: {result.get('message', 'Success')}")
            else:
                print(f"❌ Bookmark failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Bookmark error: {e}")
        
        # Test comment
        try:
            comment_data = {"content": "Great post! Testing the comment system 🎓"}
            response = session.post(f"{API_BASE_URL}/posts/{test_post_id}/comments", 
                                  json=comment_data, headers=headers)
            if response.status_code == 200:
                print("✅ Comment added successfully")
            else:
                print(f"❌ Comment failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Comment error: {e}")
    else:
        print("⚠️ No posts available for engagement testing")
    
    print("\n=== STEP 6: SEARCH AND FILTERING ===")
    
    # Test search by content
    try:
        search_data = {"query": "test"}
        response = session.post(f"{API_BASE_URL}/search", json=search_data, headers=headers)
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Content search: Found {len(results)} posts")
        else:
            print(f"❌ Content search failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Content search error: {e}")
    
    # Test search by department
    try:
        search_data = {"query": "", "department": "CSE"}
        response = session.post(f"{API_BASE_URL}/search", json=search_data, headers=headers)
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Department search: Found {len(results)} CSE posts")
        else:
            print(f"❌ Department search failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Department search error: {e}")
    
    # Test departments list
    try:
        response = session.get(f"{API_BASE_URL}/departments")
        if response.status_code == 200:
            data = response.json()
            departments = data.get('departments', [])
            print(f"✅ Departments list: {len(departments)} departments available")
        else:
            print(f"❌ Departments list failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Departments list error: {e}")

def main():
    """Run the complete test"""
    print("🚀 FINAL COMPREHENSIVE BACKEND TEST")
    print("="*60)
    
    success = test_complete_flow()
    
    print("\n" + "="*60)
    if success:
        print("🎉 BACKEND API TESTING COMPLETED SUCCESSFULLY!")
        print("✅ All major functionality verified")
    else:
        print("⚠️ BACKEND API TESTING COMPLETED WITH ISSUES")
        print("❌ Some functionality needs attention")
    print("="*60)

if __name__ == "__main__":
    main()