#!/usr/bin/env python3
"""
Complete Backend API Testing with Email Verification
Uses verification codes from backend logs to test full authentication flow
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

class CompleteBackendTester:
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
    
    def complete_authentication_flow(self):
        """Complete authentication flow with email verification"""
        print("\n=== COMPLETE AUTHENTICATION FLOW ===")
        
        # Use a unique test email
        test_email = "fulltest2024@ritrjpm.ac.in"
        registration_data = {
            "name": "Full Test User",
            "email": test_email,
            "password": "fulltest123",
            "department": "CSE",
            "year": 3,
            "roll_number": "FULL2024001"
        }
        
        # Step 1: Register user
        try:
            response = self.session.post(f"{API_BASE_URL}/auth/register", json=registration_data)
            if response.status_code == 200:
                self.log_result('authentication', 'User Registration', True, 
                              f"User registered successfully")
            elif response.status_code == 400 and "already exists" in response.text:
                self.log_result('authentication', 'User Registration', True, 
                              f"User already exists - proceeding with verification")
            else:
                self.log_result('authentication', 'User Registration', False, 
                              f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_result('authentication', 'User Registration', False, str(e))
            return False
        
        # Step 2: Get verification code from logs (simulate email verification)
        print("📧 Checking backend logs for verification code...")
        try:
            import subprocess
            result = subprocess.run(['tail', '-n', '20', '/var/log/supervisor/backend.out.log'], 
                                  capture_output=True, text=True)
            log_content = result.stdout
            
            verification_code = None
            for line in log_content.split('\n'):
                if test_email in line and 'Verification code' in line:
                    # Extract code from line like: "Verification code for email: 123456"
                    verification_code = line.split(': ')[-1].strip()
                    break
            
            if verification_code:
                print(f"📧 Found verification code: {verification_code}")
                
                # Step 3: Verify email
                verification_data = {
                    "email": test_email,
                    "verification_code": verification_code
                }
                
                response = self.session.post(f"{API_BASE_URL}/auth/verify-email", json=verification_data)
                if response.status_code == 200:
                    self.log_result('authentication', 'Email Verification', True, 
                                  f"Email verified successfully")
                else:
                    self.log_result('authentication', 'Email Verification', False, 
                                  f"Status: {response.status_code}, Response: {response.text}")
                    return False
            else:
                print("⚠️ Could not find verification code in logs - trying with existing verified user")
                # Try with a user that might already be verified
                test_email = "backend2024@ritrjpm.ac.in"
                registration_data["email"] = test_email
                registration_data["password"] = "testpass123"
                
        except Exception as e:
            print(f"⚠️ Could not access logs: {e}")
            # Try with existing user
            test_email = "backend2024@ritrjpm.ac.in"
            registration_data["email"] = test_email
            registration_data["password"] = "testpass123"
        
        # Step 4: Login with verified credentials
        login_data = {
            "email": test_email,
            "password": registration_data["password"]
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/auth/login", json=login_data)
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                self.user_data = data.get('user')
                self.log_result('authentication', 'Login with Verified Email', True, 
                              f"Login successful, token received")
                return True
            else:
                self.log_result('authentication', 'Login with Verified Email', False, 
                              f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_result('authentication', 'Login with Verified Email', False, str(e))
            return False
    
    def test_jwt_authentication(self):
        """Test JWT token authentication for protected endpoints"""
        print("\n=== TESTING JWT AUTHENTICATION ===")
        
        if not self.access_token:
            self.log_result('authentication', 'JWT Token Authentication', False, 
                          "No access token available")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Test protected endpoint
        try:
            response = self.session.get(f"{API_BASE_URL}/users/me", headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                self.log_result('authentication', 'JWT Token Authentication', True, 
                              f"Protected endpoint accessible with JWT")
            else:
                self.log_result('authentication', 'JWT Token Authentication', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('authentication', 'JWT Token Authentication', False, str(e))
    
    def test_user_management_complete(self):
        """Test complete user management functionality"""
        print("\n=== TESTING USER MANAGEMENT ===")
        
        if not self.access_token:
            self.log_result('user_management', 'All User Management Tests', False, 
                          "No access token available")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Test 1: Get current user profile
        try:
            response = self.session.get(f"{API_BASE_URL}/users/me", headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                required_fields = ['id', 'name', 'email', 'department', 'year', 'roll_number']
                if all(field in user_data for field in required_fields):
                    self.log_result('user_management', 'Get User Profile with Required Fields', True, 
                                  f"All required fields present: {', '.join(required_fields)}")
                else:
                    missing = [f for f in required_fields if f not in user_data]
                    self.log_result('user_management', 'Get User Profile with Required Fields', False, 
                                  f"Missing fields: {missing}")
            else:
                self.log_result('user_management', 'Get User Profile', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('user_management', 'Get User Profile', False, str(e))
        
        # Test 2: Update user profile
        update_data = {
            "name": "Updated Test User",
            "bio": "I am a Computer Science student at Ramco Institute of Technology, testing the StudentMedia platform.",
            "profile_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
        }
        
        try:
            response = self.session.put(f"{API_BASE_URL}/users/me", json=update_data, headers=headers)
            if response.status_code == 200:
                self.log_result('user_management', 'Update User Profile', True, 
                              "Profile updated successfully")
                
                # Verify the update
                verify_response = self.session.get(f"{API_BASE_URL}/users/me", headers=headers)
                if verify_response.status_code == 200:
                    updated_user = verify_response.json()
                    if updated_user.get('name') == update_data['name'] and updated_user.get('bio') == update_data['bio']:
                        self.log_result('user_management', 'Verify Profile Update', True, 
                                      "Profile changes persisted correctly")
                    else:
                        self.log_result('user_management', 'Verify Profile Update', False, 
                                      "Profile changes not persisted")
            else:
                self.log_result('user_management', 'Update User Profile', False, 
                              f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result('user_management', 'Update User Profile', False, str(e))
    
    def test_posts_system_complete(self):
        """Test complete posts system functionality"""
        print("\n=== TESTING POSTS SYSTEM ===")
        
        if not self.access_token:
            self.log_result('posts', 'All Posts Tests', False, "No access token available")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        created_post_ids = []
        
        # Test 1: Create post with text only
        text_post_data = {
            "content": "🎓 Hello from the StudentMedia platform! This is a comprehensive test post from the CSE department. Testing the complete backend functionality including posts, engagement, and search features. #StudentMedia #CSE #RIT",
            "tags": ["test", "cse", "studentmedia", "backend"]
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/posts", json=text_post_data, headers=headers)
            if response.status_code == 200:
                post_data = response.json()
                if 'post_id' in post_data:
                    created_post_ids.append(post_data['post_id'])
                    self.log_result('posts', 'Create Text Post', True, 
                                  f"Post created with ID: {post_data['post_id']}")
                else:
                    self.log_result('posts', 'Create Text Post', False, 
                                  "Post created but no ID returned")
            else:
                self.log_result('posts', 'Create Text Post', False, 
                              f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result('posts', 'Create Text Post', False, str(e))
        
        # Test 2: Create post with base64 image
        # Create a small test image (1x1 pixel PNG)
        small_image_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
        
        image_post_data = {
            "content": "📸 Testing image upload functionality! This post includes a base64 encoded image to verify the image handling system works correctly.",
            "image": f"data:image/png;base64,{small_image_b64}",
            "tags": ["image", "test", "upload"]
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/posts", json=image_post_data, headers=headers)
            if response.status_code == 200:
                post_data = response.json()
                if 'post_id' in post_data:
                    created_post_ids.append(post_data['post_id'])
                    self.log_result('posts', 'Create Image Post', True, 
                                  f"Image post created with ID: {post_data['post_id']}")
                else:
                    self.log_result('posts', 'Create Image Post', False, 
                                  "Image post created but no ID returned")
            else:
                self.log_result('posts', 'Create Image Post', False, 
                              f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result('posts', 'Create Image Post', False, str(e))
        
        # Test 3: Get posts feed with pagination
        try:
            response = self.session.get(f"{API_BASE_URL}/posts?skip=0&limit=10", headers=headers)
            if response.status_code == 200:
                posts = response.json()
                if isinstance(posts, list) and len(posts) > 0:
                    self.log_result('posts', 'Get Posts Feed', True, 
                                  f"Retrieved {len(posts)} posts")
                    
                    # Test 4: Verify posts include user information
                    first_post = posts[0]
                    if 'user' in first_post:
                        user_info = first_post['user']
                        required_user_fields = ['name', 'department', 'year']
                        if all(field in user_info for field in required_user_fields):
                            self.log_result('posts', 'Posts Include User Information', True, 
                                          f"User info complete: {user_info['name']} ({user_info['department']}, Year {user_info['year']})")
                        else:
                            missing = [f for f in required_user_fields if f not in user_info]
                            self.log_result('posts', 'Posts Include User Information', False, 
                                          f"Missing user fields: {missing}")
                    else:
                        self.log_result('posts', 'Posts Include User Information', False, 
                                      "Posts missing user information")
                    
                    # Test 5: Verify MongoDB aggregation pipeline results
                    required_post_fields = ['id', 'content', 'created_at', 'likes_count', 'comments_count']
                    if all(field in first_post for field in required_post_fields):
                        self.log_result('posts', 'MongoDB Aggregation Pipeline', True, 
                                      f"All required post fields present")
                    else:
                        missing = [f for f in required_post_fields if f not in first_post]
                        self.log_result('posts', 'MongoDB Aggregation Pipeline', False, 
                                      f"Missing post fields: {missing}")
                        
                elif isinstance(posts, list) and len(posts) == 0:
                    self.log_result('posts', 'Get Posts Feed', True, 
                                  "Retrieved empty posts list (no posts yet)")
                else:
                    self.log_result('posts', 'Get Posts Feed', False, 
                                  f"Expected list, got: {type(posts)}")
            else:
                self.log_result('posts', 'Get Posts Feed', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('posts', 'Get Posts Feed', False, str(e))
        
        return created_post_ids
    
    def test_engagement_features_complete(self, post_ids):
        """Test complete engagement functionality"""
        print("\n=== TESTING ENGAGEMENT FEATURES ===")
        
        if not self.access_token:
            self.log_result('engagement', 'All Engagement Tests', False, "No access token available")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Get a post to test with
        test_post_id = None
        if post_ids:
            test_post_id = post_ids[0]
        else:
            # Try to get any existing post
            try:
                response = self.session.get(f"{API_BASE_URL}/posts?limit=1", headers=headers)
                if response.status_code == 200:
                    posts = response.json()
                    if posts:
                        test_post_id = posts[0]['id']
            except:
                pass
        
        if not test_post_id:
            self.log_result('engagement', 'All Engagement Tests', False, "No posts available to test")
            return
        
        # Test 1: Like functionality
        try:
            response = self.session.post(f"{API_BASE_URL}/posts/{test_post_id}/like", headers=headers)
            if response.status_code == 200:
                like_data = response.json()
                if 'liked' in like_data and like_data['liked']:
                    self.log_result('engagement', 'Like Post', True, 
                                  f"Post liked successfully")
                    
                    # Test unlike
                    unlike_response = self.session.post(f"{API_BASE_URL}/posts/{test_post_id}/like", headers=headers)
                    if unlike_response.status_code == 200:
                        unlike_data = unlike_response.json()
                        if 'liked' in unlike_data and not unlike_data['liked']:
                            self.log_result('engagement', 'Unlike Post', True, 
                                          f"Post unliked successfully")
                        else:
                            self.log_result('engagement', 'Unlike Post', False, 
                                          f"Unlike response incorrect: {unlike_data}")
                    else:
                        self.log_result('engagement', 'Unlike Post', False, 
                                      f"Unlike failed: {unlike_response.status_code}")
                else:
                    self.log_result('engagement', 'Like Post', False, 
                                  f"Like response incorrect: {like_data}")
            else:
                self.log_result('engagement', 'Like Post', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('engagement', 'Like/Unlike Post', False, str(e))
        
        # Test 2: Bookmark functionality
        try:
            response = self.session.post(f"{API_BASE_URL}/posts/{test_post_id}/bookmark", headers=headers)
            if response.status_code == 200:
                bookmark_data = response.json()
                if 'bookmarked' in bookmark_data and bookmark_data['bookmarked']:
                    self.log_result('engagement', 'Bookmark Post', True, 
                                  f"Post bookmarked successfully")
                    
                    # Test unbookmark
                    unbookmark_response = self.session.post(f"{API_BASE_URL}/posts/{test_post_id}/bookmark", headers=headers)
                    if unbookmark_response.status_code == 200:
                        unbookmark_data = unbookmark_response.json()
                        if 'bookmarked' in unbookmark_data and not unbookmark_data['bookmarked']:
                            self.log_result('engagement', 'Unbookmark Post', True, 
                                          f"Post unbookmarked successfully")
                        else:
                            self.log_result('engagement', 'Unbookmark Post', False, 
                                          f"Unbookmark response incorrect: {unbookmark_data}")
                    else:
                        self.log_result('engagement', 'Unbookmark Post', False, 
                                      f"Unbookmark failed: {unbookmark_response.status_code}")
                else:
                    self.log_result('engagement', 'Bookmark Post', False, 
                                  f"Bookmark response incorrect: {bookmark_data}")
            else:
                self.log_result('engagement', 'Bookmark Post', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('engagement', 'Bookmark/Unbookmark Post', False, str(e))
        
        # Test 3: Comment functionality
        comment_data = {
            "content": "This is a comprehensive test comment! 🎓 Testing the comment system to ensure it works correctly with user information and proper threading. Great post!"
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/posts/{test_post_id}/comments", 
                                       json=comment_data, headers=headers)
            if response.status_code == 200:
                self.log_result('engagement', 'Add Comment', True, 
                              "Comment added successfully")
                
                # Verify comment appears in posts feed
                posts_response = self.session.get(f"{API_BASE_URL}/posts?limit=5", headers=headers)
                if posts_response.status_code == 200:
                    posts = posts_response.json()
                    target_post = next((p for p in posts if p['id'] == test_post_id), None)
                    if target_post and 'comments' in target_post and len(target_post['comments']) > 0:
                        comment = target_post['comments'][-1]  # Get latest comment
                        if 'user' in comment and 'content' in comment:
                            self.log_result('engagement', 'Comment with User Info', True, 
                                          f"Comment includes user info: {comment['user'].get('name', 'Unknown')}")
                        else:
                            self.log_result('engagement', 'Comment with User Info', False, 
                                          "Comment missing user information")
                    else:
                        self.log_result('engagement', 'Comment Retrieval', False, 
                                      "Comment not found in posts feed")
            else:
                self.log_result('engagement', 'Add Comment', False, 
                              f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result('engagement', 'Add Comment', False, str(e))
    
    def test_search_and_filtering_complete(self):
        """Test complete search and filtering functionality"""
        print("\n=== TESTING SEARCH AND FILTERING ===")
        
        if not self.access_token:
            self.log_result('search', 'All Search Tests', False, "No access token available")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Test 1: Search by content/text
        search_queries = ["test", "student", "CSE", "platform"]
        
        for query in search_queries:
            search_data = {"query": query}
            try:
                response = self.session.post(f"{API_BASE_URL}/search", json=search_data, headers=headers)
                if response.status_code == 200:
                    results = response.json()
                    if isinstance(results, list):
                        self.log_result('search', f'Search by Content "{query}"', True, 
                                      f"Found {len(results)} posts")
                        break  # At least one search worked
                    else:
                        self.log_result('search', f'Search by Content "{query}"', False, 
                                      f"Expected list, got: {type(results)}")
                else:
                    self.log_result('search', f'Search by Content "{query}"', False, 
                                  f"Status: {response.status_code}")
            except Exception as e:
                self.log_result('search', f'Search by Content "{query}"', False, str(e))
        
        # Test 2: Search by department filter
        departments_to_test = ["CSE", "ECE", "MECH"]
        
        for dept in departments_to_test:
            dept_search_data = {
                "query": "",
                "department": dept
            }
            try:
                response = self.session.post(f"{API_BASE_URL}/search", json=dept_search_data, headers=headers)
                if response.status_code == 200:
                    results = response.json()
                    if isinstance(results, list):
                        self.log_result('search', f'Search by Department "{dept}"', True, 
                                      f"Found {len(results)} posts from {dept}")
                        break  # At least one department search worked
                    else:
                        self.log_result('search', f'Search by Department "{dept}"', False, 
                                      f"Expected list, got: {type(results)}")
                else:
                    self.log_result('search', f'Search by Department "{dept}"', False, 
                                  f"Status: {response.status_code}")
            except Exception as e:
                self.log_result('search', f'Search by Department "{dept}"', False, str(e))
        
        # Test 3: Search by year filter
        years_to_test = [1, 2, 3, 4]
        
        for year in years_to_test:
            year_search_data = {
                "query": "",
                "year": year
            }
            try:
                response = self.session.post(f"{API_BASE_URL}/search", json=year_search_data, headers=headers)
                if response.status_code == 200:
                    results = response.json()
                    if isinstance(results, list):
                        self.log_result('search', f'Search by Year {year}', True, 
                                      f"Found {len(results)} posts from year {year}")
                        break  # At least one year search worked
                    else:
                        self.log_result('search', f'Search by Year {year}', False, 
                                      f"Expected list, got: {type(results)}")
                else:
                    self.log_result('search', f'Search by Year {year}', False, 
                                  f"Status: {response.status_code}")
            except Exception as e:
                self.log_result('search', f'Search by Year {year}', False, str(e))
        
        # Test 4: Combined search filters
        combined_search_data = {
            "query": "test",
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
                    received_depts = dept_data['departments']
                    if all(dept in received_depts for dept in expected_depts):
                        self.log_result('search', 'Get Departments List', True, 
                                      f"All {len(expected_depts)} departments available: {', '.join(received_depts)}")
                    else:
                        missing = [d for d in expected_depts if d not in received_depts]
                        self.log_result('search', 'Get Departments List', False, 
                                      f"Missing departments: {missing}")
                else:
                    self.log_result('search', 'Get Departments List', False, 
                                  f"Invalid response format: {dept_data}")
            else:
                self.log_result('search', 'Get Departments List', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('search', 'Get Departments List', False, str(e))
    
    def print_comprehensive_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "="*80)
        print("STUDENTMEDIA BACKEND API - COMPREHENSIVE TEST RESULTS")
        print("="*80)
        
        total_passed = 0
        total_failed = 0
        
        for category, results in self.test_results.items():
            passed = results['passed']
            failed = results['failed']
            total_passed += passed
            total_failed += failed
            
            print(f"\n{category.upper().replace('_', ' ')} ({passed + failed} tests):")
            print(f"  ✅ Passed: {passed}")
            print(f"  ❌ Failed: {failed}")
            
            for detail in results['details']:
                print(f"    {detail}")
        
        print(f"\n" + "="*80)
        print(f"FINAL RESULTS:")
        print(f"  ✅ Total Passed: {total_passed}")
        print(f"  ❌ Total Failed: {total_failed}")
        success_rate = (total_passed/(total_passed+total_failed)*100) if (total_passed+total_failed) > 0 else 0
        print(f"  📊 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print(f"  🎉 EXCELLENT: Backend API is working very well!")
        elif success_rate >= 60:
            print(f"  ✅ GOOD: Backend API is mostly functional with minor issues")
        elif success_rate >= 40:
            print(f"  ⚠️ FAIR: Backend API has some significant issues")
        else:
            print(f"  ❌ POOR: Backend API has major issues requiring attention")
        
        print("="*80)
        
        return {
            'total_passed': total_passed,
            'total_failed': total_failed,
            'success_rate': success_rate,
            'categories': self.test_results
        }

def main():
    """Run comprehensive backend tests"""
    print("🚀 Starting Comprehensive StudentMedia Backend API Tests")
    print(f"📍 Testing against: {API_BASE_URL}")
    print("="*80)
    
    tester = CompleteBackendTester()
    
    # Step 1: Complete authentication flow
    auth_success = tester.complete_authentication_flow()
    
    if auth_success:
        # Step 2: Test JWT authentication
        tester.test_jwt_authentication()
        
        # Step 3: Test user management
        tester.test_user_management_complete()
        
        # Step 4: Test posts system
        post_ids = tester.test_posts_system_complete()
        
        # Step 5: Test engagement features
        tester.test_engagement_features_complete(post_ids)
        
        # Step 6: Test search and filtering
        tester.test_search_and_filtering_complete()
    else:
        print("⚠️ Authentication failed - skipping protected endpoint tests")
    
    # Print final comprehensive summary
    results = tester.print_comprehensive_summary()
    
    return results

if __name__ == "__main__":
    main()