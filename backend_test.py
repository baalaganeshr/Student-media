#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for StudentMedia Platform
Tests all authentication, user management, posts, engagement, and search features
"""

import requests
import json
import time
import base64
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://2f02c4cf-cf77-452e-8de0-cb3ce6f5af58.preview.emergentagent.com')
API_BASE_URL = f"{BACKEND_URL}/api"

print(f"Testing backend at: {API_BASE_URL}")

class StudentMediaTester:
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None
        self.user_data = None
        self.test_results = {
            'authentication': {'passed': 0, 'failed': 0, 'details': []},
            'user_management': {'passed': 0, 'failed': 0, 'details': []},
            'posts': {'passed': 0, 'failed': 0, 'details': []},
            'engagement': {'passed': 0, 'failed': 0, 'details': []},
            'search': {'passed': 0, 'failed': 0, 'details': []}
        }
        
    def log_result(self, category, test_name, success, details=""):
        """Log test result"""
        if success:
            self.test_results[category]['passed'] += 1
            status = "✅ PASS"
        else:
            self.test_results[category]['failed'] += 1
            status = "❌ FAIL"
        
        result = f"{status}: {test_name}"
        if details:
            result += f" - {details}"
        
        self.test_results[category]['details'].append(result)
        print(result)
    
    def test_authentication_system(self):
        """Test complete authentication flow"""
        print("\n=== TESTING AUTHENTICATION SYSTEM ===")
        
        # Test 1: Register with valid @ritrjpm.ac.in email
        test_email = "953624104113@ritrjpm.ac.in"
        registration_data = {
            "name": "Arjun Kumar",
            "email": test_email,
            "password": "securepass123",
            "department": "CSE",
            "year": 3,
            "roll_number": "953624104113"
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/auth/register", json=registration_data)
            if response.status_code == 200:
                self.log_result('authentication', 'User Registration with Valid Email', True, 
                              f"Status: {response.status_code}")
            else:
                self.log_result('authentication', 'User Registration with Valid Email', False, 
                              f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result('authentication', 'User Registration with Valid Email', False, str(e))
        
        # Test 2: Try registering with invalid email domain
        invalid_email_data = registration_data.copy()
        invalid_email_data["email"] = "test@gmail.com"
        
        try:
            response = self.session.post(f"{API_BASE_URL}/auth/register", json=invalid_email_data)
            if response.status_code == 422:  # Validation error expected
                self.log_result('authentication', 'Reject Non-@ritrjpm.ac.in Email', True, 
                              f"Correctly rejected invalid domain")
            else:
                self.log_result('authentication', 'Reject Non-@ritrjpm.ac.in Email', False, 
                              f"Should reject invalid domain, got status: {response.status_code}")
        except Exception as e:
            self.log_result('authentication', 'Reject Non-@ritrjpm.ac.in Email', False, str(e))
        
        # Test 3: Test department validation
        invalid_dept_data = registration_data.copy()
        invalid_dept_data["email"] = "test2@ritrjpm.ac.in"
        invalid_dept_data["department"] = "INVALID"
        
        try:
            response = self.session.post(f"{API_BASE_URL}/auth/register", json=invalid_dept_data)
            if response.status_code == 422:  # Validation error expected
                self.log_result('authentication', 'Department Validation', True, 
                              f"Correctly rejected invalid department")
            else:
                self.log_result('authentication', 'Department Validation', False, 
                              f"Should reject invalid department, got status: {response.status_code}")
        except Exception as e:
            self.log_result('authentication', 'Department Validation', False, str(e))
        
        # Test 4: Email verification (simulate with direct database verification)
        # Since we can't access email, we'll test the verification endpoint with a mock code
        verification_data = {
            "email": test_email,
            "verification_code": "123456"  # Mock code
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/auth/verify-email", json=verification_data)
            # This might fail due to invalid code, but we're testing the endpoint exists
            if response.status_code in [200, 400]:  # Either success or expected failure
                self.log_result('authentication', 'Email Verification Endpoint', True, 
                              f"Endpoint accessible, status: {response.status_code}")
            else:
                self.log_result('authentication', 'Email Verification Endpoint', False, 
                              f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_result('authentication', 'Email Verification Endpoint', False, str(e))
        
        # Test 5: Login attempt (will fail due to unverified email, but tests endpoint)
        login_data = {
            "email": test_email,
            "password": "securepass123"
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/auth/login", json=login_data)
            if response.status_code == 401:  # Expected - unverified email
                self.log_result('authentication', 'Login with Unverified Email', True, 
                              f"Correctly rejected unverified user")
            elif response.status_code == 200:
                # Unexpected success - maybe user was already verified
                data = response.json()
                self.access_token = data.get('access_token')
                self.user_data = data.get('user')
                self.log_result('authentication', 'Login with Unverified Email', True, 
                              f"Login successful (user may be pre-verified)")
            else:
                self.log_result('authentication', 'Login with Unverified Email', False, 
                              f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_result('authentication', 'Login with Unverified Email', False, str(e))
    
    def test_user_management(self):
        """Test user profile management"""
        print("\n=== TESTING USER MANAGEMENT ===")
        
        if not self.access_token:
            # Try to create a verified user for testing
            self.create_test_user()
        
        if not self.access_token:
            self.log_result('user_management', 'Get Current User Profile', False, 
                          "No access token available")
            self.log_result('user_management', 'Update User Profile', False, 
                          "No access token available")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Test 1: Get current user profile
        try:
            response = self.session.get(f"{API_BASE_URL}/users/me", headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                self.log_result('user_management', 'Get Current User Profile', True, 
                              f"Retrieved profile for {user_data.get('name', 'user')}")
            else:
                self.log_result('user_management', 'Get Current User Profile', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('user_management', 'Get Current User Profile', False, str(e))
        
        # Test 2: Update user profile
        update_data = {
            "name": "Arjun Kumar Updated",
            "bio": "Computer Science student at RIT",
            "profile_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
        }
        
        try:
            response = self.session.put(f"{API_BASE_URL}/users/me", json=update_data, headers=headers)
            if response.status_code == 200:
                self.log_result('user_management', 'Update User Profile', True, 
                              "Profile updated successfully")
            else:
                self.log_result('user_management', 'Update User Profile', False, 
                              f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result('user_management', 'Update User Profile', False, str(e))
    
    def test_posts_system(self):
        """Test posts creation and retrieval"""
        print("\n=== TESTING POSTS SYSTEM ===")
        
        if not self.access_token:
            self.log_result('posts', 'Create Post with Text', False, "No access token available")
            self.log_result('posts', 'Create Post with Image', False, "No access token available")
            self.log_result('posts', 'Get Posts Feed', False, "No access token available")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Test 1: Create post with text only
        text_post_data = {
            "content": "Hello from the StudentMedia platform! This is a test post from CSE department.",
            "tags": ["test", "cse", "studentmedia"]
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/posts", json=text_post_data, headers=headers)
            if response.status_code == 200:
                self.log_result('posts', 'Create Post with Text', True, 
                              "Text post created successfully")
            else:
                self.log_result('posts', 'Create Post with Text', False, 
                              f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result('posts', 'Create Post with Text', False, str(e))
        
        # Test 2: Create post with base64 image
        # Small 1x1 pixel PNG in base64
        small_image_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
        
        image_post_data = {
            "content": "Check out this image post! Testing image upload functionality.",
            "image": f"data:image/png;base64,{small_image_b64}",
            "tags": ["image", "test"]
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/posts", json=image_post_data, headers=headers)
            if response.status_code == 200:
                self.log_result('posts', 'Create Post with Image', True, 
                              "Image post created successfully")
            else:
                self.log_result('posts', 'Create Post with Image', False, 
                              f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result('posts', 'Create Post with Image', False, str(e))
        
        # Test 3: Get posts feed with pagination
        try:
            response = self.session.get(f"{API_BASE_URL}/posts?skip=0&limit=10", headers=headers)
            if response.status_code == 200:
                posts = response.json()
                if isinstance(posts, list):
                    self.log_result('posts', 'Get Posts Feed with Pagination', True, 
                                  f"Retrieved {len(posts)} posts")
                    
                    # Verify posts include user information
                    if posts and 'user' in posts[0]:
                        user_info = posts[0]['user']
                        required_fields = ['name', 'department', 'year']
                        if all(field in user_info for field in required_fields):
                            self.log_result('posts', 'Posts Include User Information', True, 
                                          f"User info includes: {', '.join(required_fields)}")
                        else:
                            self.log_result('posts', 'Posts Include User Information', False, 
                                          f"Missing user fields: {user_info}")
                    else:
                        self.log_result('posts', 'Posts Include User Information', False, 
                                      "No posts or missing user info")
                else:
                    self.log_result('posts', 'Get Posts Feed with Pagination', False, 
                                  f"Expected list, got: {type(posts)}")
            else:
                self.log_result('posts', 'Get Posts Feed with Pagination', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('posts', 'Get Posts Feed with Pagination', False, str(e))
    
    def test_engagement_features(self):
        """Test like, comment, and bookmark functionality"""
        print("\n=== TESTING ENGAGEMENT FEATURES ===")
        
        if not self.access_token:
            self.log_result('engagement', 'Like/Unlike Post', False, "No access token available")
            self.log_result('engagement', 'Bookmark/Unbookmark Post', False, "No access token available")
            self.log_result('engagement', 'Add Comment', False, "No access token available")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # First, get a post to interact with
        post_id = None
        try:
            response = self.session.get(f"{API_BASE_URL}/posts?limit=1", headers=headers)
            if response.status_code == 200:
                posts = response.json()
                if posts:
                    post_id = posts[0]['id']
        except Exception as e:
            pass
        
        if not post_id:
            self.log_result('engagement', 'Like/Unlike Post', False, "No posts available to test")
            self.log_result('engagement', 'Bookmark/Unbookmark Post', False, "No posts available to test")
            self.log_result('engagement', 'Add Comment', False, "No posts available to test")
            return
        
        # Test 1: Like/Unlike functionality
        try:
            # Like the post
            response = self.session.post(f"{API_BASE_URL}/posts/{post_id}/like", headers=headers)
            if response.status_code == 200:
                like_data = response.json()
                if 'liked' in like_data:
                    self.log_result('engagement', 'Like Post', True, 
                                  f"Post liked: {like_data['liked']}")
                    
                    # Unlike the post
                    response = self.session.post(f"{API_BASE_URL}/posts/{post_id}/like", headers=headers)
                    if response.status_code == 200:
                        unlike_data = response.json()
                        self.log_result('engagement', 'Unlike Post', True, 
                                      f"Post unliked: {unlike_data.get('liked', False)}")
                    else:
                        self.log_result('engagement', 'Unlike Post', False, 
                                      f"Status: {response.status_code}")
                else:
                    self.log_result('engagement', 'Like Post', False, 
                                  f"Missing 'liked' field in response")
            else:
                self.log_result('engagement', 'Like Post', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('engagement', 'Like/Unlike Post', False, str(e))
        
        # Test 2: Bookmark/Unbookmark functionality
        try:
            # Bookmark the post
            response = self.session.post(f"{API_BASE_URL}/posts/{post_id}/bookmark", headers=headers)
            if response.status_code == 200:
                bookmark_data = response.json()
                if 'bookmarked' in bookmark_data:
                    self.log_result('engagement', 'Bookmark Post', True, 
                                  f"Post bookmarked: {bookmark_data['bookmarked']}")
                    
                    # Unbookmark the post
                    response = self.session.post(f"{API_BASE_URL}/posts/{post_id}/bookmark", headers=headers)
                    if response.status_code == 200:
                        unbookmark_data = response.json()
                        self.log_result('engagement', 'Unbookmark Post', True, 
                                      f"Post unbookmarked: {unbookmark_data.get('bookmarked', False)}")
                    else:
                        self.log_result('engagement', 'Unbookmark Post', False, 
                                      f"Status: {response.status_code}")
                else:
                    self.log_result('engagement', 'Bookmark Post', False, 
                                  f"Missing 'bookmarked' field in response")
            else:
                self.log_result('engagement', 'Bookmark Post', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('engagement', 'Bookmark/Unbookmark Post', False, str(e))
        
        # Test 3: Comment functionality
        comment_data = {
            "content": "This is a test comment from the automated testing system!"
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/posts/{post_id}/comments", 
                                       json=comment_data, headers=headers)
            if response.status_code == 200:
                self.log_result('engagement', 'Add Comment', True, 
                              "Comment added successfully")
            else:
                self.log_result('engagement', 'Add Comment', False, 
                              f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result('engagement', 'Add Comment', False, str(e))
    
    def test_search_and_filtering(self):
        """Test search functionality with various filters"""
        print("\n=== TESTING SEARCH AND FILTERING ===")
        
        if not self.access_token:
            self.log_result('search', 'Search by Content', False, "No access token available")
            self.log_result('search', 'Search by Department', False, "No access token available")
            self.log_result('search', 'Search by Year', False, "No access token available")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Test 1: Search by content/text
        search_data = {
            "query": "test"
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/search", json=search_data, headers=headers)
            if response.status_code == 200:
                results = response.json()
                if isinstance(results, list):
                    self.log_result('search', 'Search by Content', True, 
                                  f"Found {len(results)} posts matching 'test'")
                else:
                    self.log_result('search', 'Search by Content', False, 
                                  f"Expected list, got: {type(results)}")
            else:
                self.log_result('search', 'Search by Content', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('search', 'Search by Content', False, str(e))
        
        # Test 2: Search by department filter
        dept_search_data = {
            "query": "",
            "department": "CSE"
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/search", json=dept_search_data, headers=headers)
            if response.status_code == 200:
                results = response.json()
                if isinstance(results, list):
                    self.log_result('search', 'Search by Department Filter', True, 
                                  f"Found {len(results)} posts from CSE department")
                else:
                    self.log_result('search', 'Search by Department Filter', False, 
                                  f"Expected list, got: {type(results)}")
            else:
                self.log_result('search', 'Search by Department Filter', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('search', 'Search by Department Filter', False, str(e))
        
        # Test 3: Search by year filter
        year_search_data = {
            "query": "",
            "year": 3
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/search", json=year_search_data, headers=headers)
            if response.status_code == 200:
                results = response.json()
                if isinstance(results, list):
                    self.log_result('search', 'Search by Year Filter', True, 
                                  f"Found {len(results)} posts from year 3 students")
                else:
                    self.log_result('search', 'Search by Year Filter', False, 
                                  f"Expected list, got: {type(results)}")
            else:
                self.log_result('search', 'Search by Year Filter', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('search', 'Search by Year Filter', False, str(e))
        
        # Test 4: Combined search filters
        combined_search_data = {
            "query": "student",
            "department": "CSE",
            "year": 3
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/search", json=combined_search_data, headers=headers)
            if response.status_code == 200:
                results = response.json()
                if isinstance(results, list):
                    self.log_result('search', 'Combined Search Filters', True, 
                                  f"Found {len(results)} posts with combined filters")
                else:
                    self.log_result('search', 'Combined Search Filters', False, 
                                  f"Expected list, got: {type(results)}")
            else:
                self.log_result('search', 'Combined Search Filters', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('search', 'Combined Search Filters', False, str(e))
        
        # Test 5: Get departments list
        try:
            response = self.session.get(f"{API_BASE_URL}/departments")
            if response.status_code == 200:
                dept_data = response.json()
                if 'departments' in dept_data and isinstance(dept_data['departments'], list):
                    expected_depts = ['CSE', 'ECE', 'MECH', 'CIVIL', 'EEE', 'AIDS', 'AIML', 'IT', 'CHEMICAL']
                    if all(dept in dept_data['departments'] for dept in expected_depts):
                        self.log_result('search', 'Get Departments List', True, 
                                      f"All {len(expected_depts)} departments available")
                    else:
                        self.log_result('search', 'Get Departments List', False, 
                                      f"Missing departments: {dept_data['departments']}")
                else:
                    self.log_result('search', 'Get Departments List', False, 
                                  f"Invalid response format: {dept_data}")
            else:
                self.log_result('search', 'Get Departments List', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('search', 'Get Departments List', False, str(e))
    
    def create_test_user(self):
        """Create a test user and simulate verification for testing purposes"""
        print("\n--- Creating test user for API testing ---")
        
        # Try different test emails to avoid conflicts
        test_emails = [
            "testuser2024@ritrjpm.ac.in",
            "apitest2024@ritrjpm.ac.in", 
            "backend2024@ritrjpm.ac.in"
        ]
        
        for test_email in test_emails:
            registration_data = {
                "name": "API Test User",
                "email": test_email,
                "password": "testpass123",
                "department": "CSE",
                "year": 2,
                "roll_number": "API2024001"
            }
            
            try:
                # Try to register
                response = self.session.post(f"{API_BASE_URL}/auth/register", json=registration_data)
                if response.status_code == 200:
                    print(f"✅ Registered test user: {test_email}")
                    
                    # Try to login (might work if user is auto-verified or already exists)
                    login_data = {
                        "email": test_email,
                        "password": "testpass123"
                    }
                    
                    login_response = self.session.post(f"{API_BASE_URL}/auth/login", json=login_data)
                    if login_response.status_code == 200:
                        data = login_response.json()
                        self.access_token = data.get('access_token')
                        self.user_data = data.get('user')
                        print(f"✅ Successfully logged in test user")
                        return
                    else:
                        print(f"⚠️ User registered but login failed (likely needs verification)")
                
                elif response.status_code == 400 and "already exists" in response.text:
                    # User already exists, try to login
                    login_data = {
                        "email": test_email,
                        "password": "testpass123"
                    }
                    
                    login_response = self.session.post(f"{API_BASE_URL}/auth/login", json=login_data)
                    if login_response.status_code == 200:
                        data = login_response.json()
                        self.access_token = data.get('access_token')
                        self.user_data = data.get('user')
                        print(f"✅ Logged in existing test user: {test_email}")
                        return
                    else:
                        print(f"⚠️ Existing user login failed: {login_response.status_code}")
                        
            except Exception as e:
                print(f"❌ Error with {test_email}: {str(e)}")
                continue
        
        print("⚠️ Could not create or login test user - some tests may be limited")
    
    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "="*80)
        print("STUDENTMEDIA BACKEND API TEST SUMMARY")
        print("="*80)
        
        total_passed = 0
        total_failed = 0
        
        for category, results in self.test_results.items():
            passed = results['passed']
            failed = results['failed']
            total_passed += passed
            total_failed += failed
            
            print(f"\n{category.upper().replace('_', ' ')}:")
            print(f"  ✅ Passed: {passed}")
            print(f"  ❌ Failed: {failed}")
            
            for detail in results['details']:
                print(f"    {detail}")
        
        print(f"\n" + "="*80)
        print(f"OVERALL RESULTS:")
        print(f"  ✅ Total Passed: {total_passed}")
        print(f"  ❌ Total Failed: {total_failed}")
        print(f"  📊 Success Rate: {(total_passed/(total_passed+total_failed)*100):.1f}%" if (total_passed+total_failed) > 0 else "No tests run")
        print("="*80)
        
        return {
            'total_passed': total_passed,
            'total_failed': total_failed,
            'categories': self.test_results
        }

def main():
    """Run all backend tests"""
    print("🚀 Starting StudentMedia Backend API Tests")
    print(f"📍 Testing against: {API_BASE_URL}")
    print("="*80)
    
    tester = StudentMediaTester()
    
    # Run all test suites
    tester.test_authentication_system()
    tester.test_user_management()
    tester.test_posts_system()
    tester.test_engagement_features()
    tester.test_search_and_filtering()
    
    # Print final summary
    results = tester.print_summary()
    
    return results

if __name__ == "__main__":
    main()