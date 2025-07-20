#!/usr/bin/env python3
"""
Final Comprehensive Backend Test for StudentMedia Platform
Tests all functionality with verified user to confirm ObjectId fixes work across all endpoints
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

print(f"Final comprehensive testing at: {API_BASE_URL}")

class ComprehensiveTester:
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
    
    def test_authentication_flow(self):
        """Test complete authentication flow"""
        print("\n=== TESTING AUTHENTICATION SYSTEM ===")
        
        # Test 1: Login with verified user
        login_data = {
            "email": "verified@ritrjpm.ac.in",
            "password": "testpass123"
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/auth/login", json=login_data)
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                self.user_data = data.get('user')
                self.log_result('authentication', 'Login with Verified User', True, 
                              f"Successfully authenticated user: {self.user_data.get('name', 'Unknown')}")
            else:
                self.log_result('authentication', 'Login with Verified User', False, 
                              f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result('authentication', 'Login with Verified User', False, str(e))
        
        # Test 2: Test invalid email domain rejection
        invalid_registration = {
            "name": "Test User",
            "email": "test@gmail.com",
            "password": "testpass123",
            "department": "CSE",
            "year": 2,
            "roll_number": "TEST001"
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/auth/register", json=invalid_registration)
            if response.status_code == 422:  # Validation error expected
                self.log_result('authentication', 'Email Domain Validation', True, 
                              "Correctly rejected non-@ritrjpm.ac.in email")
            else:
                self.log_result('authentication', 'Email Domain Validation', False, 
                              f"Should reject invalid domain, got: {response.status_code}")
        except Exception as e:
            self.log_result('authentication', 'Email Domain Validation', False, str(e))
        
        # Test 3: Test department validation
        invalid_dept = invalid_registration.copy()
        invalid_dept["email"] = "test@ritrjpm.ac.in"
        invalid_dept["department"] = "INVALID_DEPT"
        
        try:
            response = self.session.post(f"{API_BASE_URL}/auth/register", json=invalid_dept)
            if response.status_code == 422:  # Validation error expected
                self.log_result('authentication', 'Department Validation', True, 
                              "Correctly rejected invalid department")
            else:
                self.log_result('authentication', 'Department Validation', False, 
                              f"Should reject invalid department, got: {response.status_code}")
        except Exception as e:
            self.log_result('authentication', 'Department Validation', False, str(e))
    
    def test_user_management(self):
        """Test user profile management"""
        print("\n=== TESTING USER MANAGEMENT ===")
        
        if not self.access_token:
            self.log_result('user_management', 'Get User Profile', False, "No access token")
            self.log_result('user_management', 'Update User Profile', False, "No access token")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Test 1: Get current user profile
        try:
            response = self.session.get(f"{API_BASE_URL}/users/me", headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                required_fields = ['id', 'name', 'email', 'department', 'year', 'roll_number']
                missing_fields = [field for field in required_fields if field not in user_data]
                
                if not missing_fields:
                    self.log_result('user_management', 'Get User Profile', True, 
                                  f"All required fields present: {user_data['name']} ({user_data['department']} Year {user_data['year']})")
                else:
                    self.log_result('user_management', 'Get User Profile', False, 
                                  f"Missing fields: {missing_fields}")
            else:
                self.log_result('user_management', 'Get User Profile', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('user_management', 'Get User Profile', False, str(e))
        
        # Test 2: Update user profile
        update_data = {
            "name": "Updated Test User",
            "bio": "Testing profile updates for ObjectId serialization fixes",
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
        """Test posts creation and retrieval with ObjectId fixes"""
        print("\n=== TESTING POSTS SYSTEM ===")
        
        if not self.access_token:
            self.log_result('posts', 'Create Text Post', False, "No access token")
            self.log_result('posts', 'Create Image Post', False, "No access token")
            self.log_result('posts', 'Get Posts Feed', False, "No access token")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Test 1: Create text post
        text_post = {
            "content": "Final comprehensive test post - verifying ObjectId serialization fixes work perfectly!",
            "tags": ["final-test", "objectid-fix", "comprehensive"]
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/posts", json=text_post, headers=headers)
            if response.status_code == 200:
                self.log_result('posts', 'Create Text Post', True, "Text post created successfully")
            else:
                self.log_result('posts', 'Create Text Post', False, 
                              f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result('posts', 'Create Text Post', False, str(e))
        
        # Test 2: Create image post
        image_post = {
            "content": "Image post test - confirming image handling works with ObjectId fixes",
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
            "tags": ["image-test", "final-verification"]
        }
        
        try:
            response = self.session.post(f"{API_BASE_URL}/posts", json=image_post, headers=headers)
            if response.status_code == 200:
                self.log_result('posts', 'Create Image Post', True, "Image post created successfully")
            else:
                self.log_result('posts', 'Create Image Post', False, 
                              f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result('posts', 'Create Image Post', False, str(e))
        
        # Test 3: Get posts feed (critical ObjectId test)
        try:
            response = self.session.get(f"{API_BASE_URL}/posts?skip=0&limit=10", headers=headers)
            if response.status_code == 200:
                posts = response.json()
                if isinstance(posts, list) and posts:
                    first_post = posts[0]
                    
                    # Verify structure
                    required_fields = ['id', 'content', 'user', 'created_at', 'likes_count', 'comments_count']
                    missing_fields = [field for field in required_fields if field not in first_post]
                    
                    if not missing_fields:
                        # Verify user info
                        user_info = first_post.get('user', {})
                        user_fields = ['name', 'department', 'year']
                        missing_user_fields = [field for field in user_fields if field not in user_info]
                        
                        if not missing_user_fields:
                            self.log_result('posts', 'Get Posts Feed with User Info', True, 
                                          f"Retrieved {len(posts)} posts with complete user information")
                        else:
                            self.log_result('posts', 'Get Posts Feed with User Info', False, 
                                          f"Missing user fields: {missing_user_fields}")
                    else:
                        self.log_result('posts', 'Get Posts Feed with User Info', False, 
                                      f"Missing post fields: {missing_fields}")
                else:
                    self.log_result('posts', 'Get Posts Feed with User Info', False, 
                                  f"Invalid response format or empty: {type(posts)}")
            else:
                self.log_result('posts', 'Get Posts Feed with User Info', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('posts', 'Get Posts Feed with User Info', False, str(e))
    
    def test_engagement_features(self):
        """Test engagement features"""
        print("\n=== TESTING ENGAGEMENT FEATURES ===")
        
        if not self.access_token:
            self.log_result('engagement', 'Like/Unlike Post', False, "No access token")
            self.log_result('engagement', 'Bookmark/Unbookmark Post', False, "No access token")
            self.log_result('engagement', 'Add Comment', False, "No access token")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Get a post to interact with
        post_id = None
        try:
            response = self.session.get(f"{API_BASE_URL}/posts?limit=1", headers=headers)
            if response.status_code == 200:
                posts = response.json()
                if posts:
                    post_id = posts[0]['id']
        except Exception:
            pass
        
        if not post_id:
            self.log_result('engagement', 'Like/Unlike Post', False, "No posts available")
            self.log_result('engagement', 'Bookmark/Unbookmark Post', False, "No posts available")
            self.log_result('engagement', 'Add Comment', False, "No posts available")
            return
        
        # Test 1: Like/Unlike functionality
        try:
            # Like
            response = self.session.post(f"{API_BASE_URL}/posts/{post_id}/like", headers=headers)
            if response.status_code == 200:
                like_data = response.json()
                # Unlike
                response = self.session.post(f"{API_BASE_URL}/posts/{post_id}/like", headers=headers)
                if response.status_code == 200:
                    self.log_result('engagement', 'Like/Unlike Post', True, 
                                  "Like toggle functionality working")
                else:
                    self.log_result('engagement', 'Like/Unlike Post', False, 
                                  f"Unlike failed: {response.status_code}")
            else:
                self.log_result('engagement', 'Like/Unlike Post', False, 
                              f"Like failed: {response.status_code}")
        except Exception as e:
            self.log_result('engagement', 'Like/Unlike Post', False, str(e))
        
        # Test 2: Bookmark/Unbookmark functionality
        try:
            # Bookmark
            response = self.session.post(f"{API_BASE_URL}/posts/{post_id}/bookmark", headers=headers)
            if response.status_code == 200:
                # Unbookmark
                response = self.session.post(f"{API_BASE_URL}/posts/{post_id}/bookmark", headers=headers)
                if response.status_code == 200:
                    self.log_result('engagement', 'Bookmark/Unbookmark Post', True, 
                                  "Bookmark toggle functionality working")
                else:
                    self.log_result('engagement', 'Bookmark/Unbookmark Post', False, 
                                  f"Unbookmark failed: {response.status_code}")
            else:
                self.log_result('engagement', 'Bookmark/Unbookmark Post', False, 
                              f"Bookmark failed: {response.status_code}")
        except Exception as e:
            self.log_result('engagement', 'Bookmark/Unbookmark Post', False, str(e))
        
        # Test 3: Add comment
        comment_data = {"content": "Final comprehensive test comment - verifying ObjectId fixes!"}
        
        try:
            response = self.session.post(f"{API_BASE_URL}/posts/{post_id}/comments", 
                                       json=comment_data, headers=headers)
            if response.status_code == 200:
                self.log_result('engagement', 'Add Comment', True, "Comment added successfully")
            else:
                self.log_result('engagement', 'Add Comment', False, 
                              f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result('engagement', 'Add Comment', False, str(e))
    
    def test_search_system(self):
        """Test search and filtering system with ObjectId fixes"""
        print("\n=== TESTING SEARCH AND FILTERING SYSTEM ===")
        
        if not self.access_token:
            self.log_result('search', 'Content Search', False, "No access token")
            self.log_result('search', 'Department Filter', False, "No access token")
            self.log_result('search', 'Year Filter', False, "No access token")
            self.log_result('search', 'Combined Filters', False, "No access token")
            self.log_result('search', 'Departments List', False, "No access token")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Test 1: Content search
        try:
            search_data = {"query": "test"}
            response = self.session.post(f"{API_BASE_URL}/search", json=search_data, headers=headers)
            if response.status_code == 200:
                results = response.json()
                if isinstance(results, list):
                    self.log_result('search', 'Content Search', True, 
                                  f"Found {len(results)} posts matching 'test'")
                else:
                    self.log_result('search', 'Content Search', False, 
                                  f"Invalid response format: {type(results)}")
            else:
                self.log_result('search', 'Content Search', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('search', 'Content Search', False, str(e))
        
        # Test 2: Department filter
        try:
            search_data = {"query": "", "department": "CSE"}
            response = self.session.post(f"{API_BASE_URL}/search", json=search_data, headers=headers)
            if response.status_code == 200:
                results = response.json()
                if isinstance(results, list):
                    self.log_result('search', 'Department Filter', True, 
                                  f"Found {len(results)} posts from CSE department")
                else:
                    self.log_result('search', 'Department Filter', False, 
                                  f"Invalid response format: {type(results)}")
            else:
                self.log_result('search', 'Department Filter', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('search', 'Department Filter', False, str(e))
        
        # Test 3: Year filter
        try:
            search_data = {"query": "", "year": 3}
            response = self.session.post(f"{API_BASE_URL}/search", json=search_data, headers=headers)
            if response.status_code == 200:
                results = response.json()
                if isinstance(results, list):
                    self.log_result('search', 'Year Filter', True, 
                                  f"Found {len(results)} posts from year 3 students")
                else:
                    self.log_result('search', 'Year Filter', False, 
                                  f"Invalid response format: {type(results)}")
            else:
                self.log_result('search', 'Year Filter', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('search', 'Year Filter', False, str(e))
        
        # Test 4: Combined filters
        try:
            search_data = {"query": "test", "department": "CSE", "year": 3}
            response = self.session.post(f"{API_BASE_URL}/search", json=search_data, headers=headers)
            if response.status_code == 200:
                results = response.json()
                if isinstance(results, list):
                    self.log_result('search', 'Combined Filters', True, 
                                  f"Found {len(results)} posts with combined filters")
                else:
                    self.log_result('search', 'Combined Filters', False, 
                                  f"Invalid response format: {type(results)}")
            else:
                self.log_result('search', 'Combined Filters', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('search', 'Combined Filters', False, str(e))
        
        # Test 5: Departments list
        try:
            response = self.session.get(f"{API_BASE_URL}/departments")
            if response.status_code == 200:
                data = response.json()
                if 'departments' in data and isinstance(data['departments'], list):
                    expected_depts = ['CSE', 'ECE', 'MECH', 'CIVIL', 'EEE', 'AIDS', 'AIML', 'IT', 'CHEMICAL']
                    if all(dept in data['departments'] for dept in expected_depts):
                        self.log_result('search', 'Departments List', True, 
                                      f"All {len(expected_depts)} departments available")
                    else:
                        self.log_result('search', 'Departments List', False, 
                                      f"Missing departments: {data['departments']}")
                else:
                    self.log_result('search', 'Departments List', False, 
                                  f"Invalid response format: {data}")
            else:
                self.log_result('search', 'Departments List', False, 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.log_result('search', 'Departments List', False, str(e))
    
    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "="*80)
        print("FINAL COMPREHENSIVE BACKEND TEST SUMMARY")
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
        success_rate = (total_passed/(total_passed+total_failed)*100) if (total_passed+total_failed) > 0 else 0
        print(f"  📊 Success Rate: {success_rate:.1f}%")
        
        # Critical assessment
        critical_tests = ['Get Posts Feed with User Info', 'Content Search', 'Department Filter', 'Year Filter']
        critical_passed = 0
        for category in self.test_results.values():
            for detail in category['details']:
                for critical_test in critical_tests:
                    if critical_test in detail and "✅ PASS" in detail:
                        critical_passed += 1
        
        print(f"\n🎯 CRITICAL OBJECTID FIXES: {critical_passed}/{len(critical_tests)} working")
        
        if critical_passed == len(critical_tests):
            print("🎉 ALL CRITICAL OBJECTID SERIALIZATION FIXES WORKING!")
        else:
            print("⚠️ Some critical ObjectId issues may remain")
        
        print("="*80)
        
        return {
            'total_passed': total_passed,
            'total_failed': total_failed,
            'success_rate': success_rate,
            'critical_fixes_working': critical_passed == len(critical_tests)
        }

def main():
    """Run final comprehensive backend tests"""
    print("🚀 Final Comprehensive StudentMedia Backend API Tests")
    print("🎯 Focus: Verifying ObjectId Serialization Fixes")
    print("="*80)
    
    tester = ComprehensiveTester()
    
    # Run all test suites
    tester.test_authentication_flow()
    tester.test_user_management()
    tester.test_posts_system()
    tester.test_engagement_features()
    tester.test_search_system()
    
    # Print final summary
    results = tester.print_summary()
    
    return results

if __name__ == "__main__":
    main()