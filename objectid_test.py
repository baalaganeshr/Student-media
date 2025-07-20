#!/usr/bin/env python3
"""
Focused ObjectId Serialization Testing for StudentMedia Platform
Tests the specific fixes for ObjectId serialization in posts feed and search endpoints
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

print(f"Testing ObjectId serialization fixes at: {API_BASE_URL}")

class ObjectIdTester:
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None
        self.user_data = None
        
    def login_test_user(self):
        """Login with the verified test user"""
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
                print("✅ Successfully logged in test user")
                return True
            else:
                print(f"❌ Login failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            return False
    
    def create_test_posts(self):
        """Create some test posts for testing"""
        if not self.access_token:
            return False
            
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Create multiple test posts
        test_posts = [
            {
                "content": "Testing ObjectId serialization fix #1 - This post should appear in feed without errors",
                "tags": ["objectid", "test", "serialization"]
            },
            {
                "content": "Another test post for ObjectId fix #2 - CSE department post",
                "tags": ["cse", "test"]
            },
            {
                "content": "Third test post with image for comprehensive testing",
                "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
                "tags": ["image", "test"]
            }
        ]
        
        created_posts = 0
        for i, post_data in enumerate(test_posts):
            try:
                response = self.session.post(f"{API_BASE_URL}/posts", json=post_data, headers=headers)
                if response.status_code == 200:
                    created_posts += 1
                    print(f"✅ Created test post {i+1}")
                else:
                    print(f"❌ Failed to create test post {i+1}: {response.status_code}")
            except Exception as e:
                print(f"❌ Error creating test post {i+1}: {str(e)}")
        
        print(f"Created {created_posts} test posts")
        return created_posts > 0
    
    def test_posts_feed_objectid_fix(self):
        """Test the posts feed endpoint for ObjectId serialization fixes"""
        print("\n=== TESTING POSTS FEED OBJECTID SERIALIZATION ===")
        
        if not self.access_token:
            print("❌ No access token available")
            return False
            
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            # Test posts feed endpoint
            response = self.session.get(f"{API_BASE_URL}/posts?skip=0&limit=10", headers=headers)
            
            print(f"Posts feed response status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    posts = response.json()
                    print(f"✅ Posts feed returned valid JSON")
                    print(f"✅ Retrieved {len(posts)} posts")
                    
                    if posts:
                        # Check first post structure
                        first_post = posts[0]
                        print(f"✅ First post structure: {list(first_post.keys())}")
                        
                        # Verify user information is included
                        if 'user' in first_post:
                            user_info = first_post['user']
                            print(f"✅ User info included: {list(user_info.keys())}")
                            
                            # Check for required user fields
                            required_fields = ['name', 'department', 'year']
                            missing_fields = [field for field in required_fields if field not in user_info]
                            if not missing_fields:
                                print(f"✅ All required user fields present")
                            else:
                                print(f"⚠️ Missing user fields: {missing_fields}")
                        else:
                            print(f"❌ No user information in posts")
                        
                        # Check for comments
                        if 'comments' in first_post:
                            comments = first_post['comments']
                            print(f"✅ Comments included: {len(comments)} comments")
                            if comments:
                                comment_structure = list(comments[0].keys())
                                print(f"✅ Comment structure: {comment_structure}")
                        else:
                            print(f"⚠️ No comments field in posts")
                        
                        # Check engagement fields
                        engagement_fields = ['is_liked', 'is_bookmarked', 'likes_count', 'comments_count']
                        present_engagement = [field for field in engagement_fields if field in first_post]
                        print(f"✅ Engagement fields present: {present_engagement}")
                        
                    return True
                    
                except json.JSONDecodeError as e:
                    print(f"❌ Posts feed returned invalid JSON: {str(e)}")
                    print(f"Response content: {response.text[:500]}...")
                    return False
            else:
                print(f"❌ Posts feed failed with status {response.status_code}")
                print(f"Error response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Posts feed test error: {str(e)}")
            return False
    
    def test_search_objectid_fix(self):
        """Test the search endpoint for ObjectId serialization fixes"""
        print("\n=== TESTING SEARCH OBJECTID SERIALIZATION ===")
        
        if not self.access_token:
            print("❌ No access token available")
            return False
            
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Test different search scenarios
        search_tests = [
            {
                "name": "Content Search",
                "data": {"query": "test"}
            },
            {
                "name": "Department Filter",
                "data": {"query": "", "department": "CSE"}
            },
            {
                "name": "Year Filter", 
                "data": {"query": "", "year": 3}
            },
            {
                "name": "Combined Filters",
                "data": {"query": "test", "department": "CSE", "year": 3}
            }
        ]
        
        all_passed = True
        
        for test in search_tests:
            try:
                print(f"\n--- Testing {test['name']} ---")
                response = self.session.post(f"{API_BASE_URL}/search", json=test['data'], headers=headers)
                
                print(f"Search response status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        results = response.json()
                        print(f"✅ {test['name']} returned valid JSON")
                        print(f"✅ Found {len(results)} results")
                        
                        if results:
                            # Check result structure
                            first_result = results[0]
                            print(f"✅ Result structure: {list(first_result.keys())}")
                            
                            # Verify user information
                            if 'user' in first_result:
                                user_info = first_result['user']
                                print(f"✅ User info in search results: {list(user_info.keys())}")
                            else:
                                print(f"❌ No user information in search results")
                                all_passed = False
                        
                    except json.JSONDecodeError as e:
                        print(f"❌ {test['name']} returned invalid JSON: {str(e)}")
                        print(f"Response content: {response.text[:500]}...")
                        all_passed = False
                else:
                    print(f"❌ {test['name']} failed with status {response.status_code}")
                    print(f"Error response: {response.text}")
                    all_passed = False
                    
            except Exception as e:
                print(f"❌ {test['name']} test error: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_departments_endpoint(self):
        """Test the departments endpoint (should work without auth)"""
        print("\n=== TESTING DEPARTMENTS ENDPOINT ===")
        
        try:
            response = self.session.get(f"{API_BASE_URL}/departments")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'departments' in data and isinstance(data['departments'], list):
                        departments = data['departments']
                        expected_depts = ['CSE', 'ECE', 'MECH', 'CIVIL', 'EEE', 'AIDS', 'AIML', 'IT', 'CHEMICAL']
                        
                        if all(dept in departments for dept in expected_depts):
                            print(f"✅ Departments endpoint working: {len(departments)} departments")
                            return True
                        else:
                            print(f"❌ Missing expected departments: {departments}")
                            return False
                    else:
                        print(f"❌ Invalid departments response format: {data}")
                        return False
                except json.JSONDecodeError as e:
                    print(f"❌ Departments endpoint returned invalid JSON: {str(e)}")
                    return False
            else:
                print(f"❌ Departments endpoint failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Departments endpoint error: {str(e)}")
            return False
    
    def test_engagement_with_posts(self):
        """Test engagement features to ensure they still work after ObjectId fixes"""
        print("\n=== TESTING ENGAGEMENT FEATURES ===")
        
        if not self.access_token:
            print("❌ No access token available")
            return False
            
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # First get a post to interact with
        try:
            response = self.session.get(f"{API_BASE_URL}/posts?limit=1", headers=headers)
            if response.status_code != 200:
                print("❌ Could not get posts for engagement testing")
                return False
                
            posts = response.json()
            if not posts:
                print("❌ No posts available for engagement testing")
                return False
                
            post_id = posts[0]['id']
            print(f"Testing engagement with post: {post_id}")
            
            # Test like functionality
            like_response = self.session.post(f"{API_BASE_URL}/posts/{post_id}/like", headers=headers)
            if like_response.status_code == 200:
                print("✅ Like functionality working")
            else:
                print(f"❌ Like failed: {like_response.status_code}")
                return False
            
            # Test bookmark functionality
            bookmark_response = self.session.post(f"{API_BASE_URL}/posts/{post_id}/bookmark", headers=headers)
            if bookmark_response.status_code == 200:
                print("✅ Bookmark functionality working")
            else:
                print(f"❌ Bookmark failed: {bookmark_response.status_code}")
                return False
            
            # Test comment functionality
            comment_data = {"content": "Test comment for ObjectId fix verification"}
            comment_response = self.session.post(f"{API_BASE_URL}/posts/{post_id}/comments", 
                                               json=comment_data, headers=headers)
            if comment_response.status_code == 200:
                print("✅ Comment functionality working")
                return True
            else:
                print(f"❌ Comment failed: {comment_response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Engagement testing error: {str(e)}")
            return False

def main():
    """Run focused ObjectId serialization tests"""
    print("🔍 Starting ObjectId Serialization Fix Testing")
    print("="*80)
    
    tester = ObjectIdTester()
    
    # Step 1: Login
    if not tester.login_test_user():
        print("❌ Cannot proceed without authentication")
        return
    
    # Step 2: Create test data
    tester.create_test_posts()
    
    # Step 3: Test critical endpoints
    results = {
        'posts_feed': tester.test_posts_feed_objectid_fix(),
        'search_system': tester.test_search_objectid_fix(),
        'departments': tester.test_departments_endpoint(),
        'engagement': tester.test_engagement_with_posts()
    }
    
    # Summary
    print("\n" + "="*80)
    print("OBJECTID SERIALIZATION FIX TEST SUMMARY")
    print("="*80)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name.replace('_', ' ').title()}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if results['posts_feed'] and results['search_system']:
        print("\n🎉 CRITICAL OBJECTID FIXES WORKING!")
        print("✅ Posts feed now returns proper JSON")
        print("✅ Search system now returns proper JSON")
    else:
        print("\n⚠️ CRITICAL ISSUES REMAIN:")
        if not results['posts_feed']:
            print("❌ Posts feed still has ObjectId serialization issues")
        if not results['search_system']:
            print("❌ Search system still has ObjectId serialization issues")
    
    return results

if __name__ == "__main__":
    main()