"""
Mock database implementation for demonstration purposes
This replaces MongoDB with in-memory storage
"""
from datetime import datetime
import uuid
from typing import List, Dict, Optional

class MockDatabase:
    def __init__(self):
        self.users = {}
        self.posts = {}
        self.comments = {}
        self.verification_codes = {}
    
    # User operations
    async def create_user(self, user_data: dict) -> str:
        user_id = str(uuid.uuid4())
        user_data['_id'] = user_id
        user_data['created_at'] = datetime.now()
        self.users[user_id] = user_data
        return user_id
    
    async def find_user_by_email(self, email: str) -> Optional[dict]:
        for user in self.users.values():
            if user.get('email') == email:
                return user
        return None
    
    async def find_user_by_id(self, user_id: str) -> Optional[dict]:
        return self.users.get(user_id)
    
    async def update_user(self, user_id: str, update_data: dict):
        if user_id in self.users:
            self.users[user_id].update(update_data)
            return True
        return False
    
    # Post operations
    async def create_post(self, post_data: dict) -> str:
        post_id = str(uuid.uuid4())
        post_data['_id'] = post_id
        post_data['created_at'] = datetime.now()
        post_data['likes'] = []
        post_data['bookmarks'] = []
        post_data['comments'] = []
        self.posts[post_id] = post_data
        return post_id
    
    async def get_all_posts(self) -> List[dict]:
        posts = list(self.posts.values())
        # Sort by created_at desc
        posts.sort(key=lambda x: x.get('created_at', datetime.now()), reverse=True)
        return posts
    
    async def find_post_by_id(self, post_id: str) -> Optional[dict]:
        return self.posts.get(post_id)
    
    async def update_post(self, post_id: str, update_data: dict):
        if post_id in self.posts:
            self.posts[post_id].update(update_data)
            return True
        return False
    
    # Search operations
    async def search_posts(self, query: str, department: str = None, year: int = None) -> List[dict]:
        results = []
        for post in self.posts.values():
            # Search in content
            if query.lower() in post.get('content', '').lower():
                # Filter by department and year if specified
                author_id = post.get('author_id')
                if author_id and author_id in self.users:
                    author = self.users[author_id]
                    if department and author.get('department') != department:
                        continue
                    if year and author.get('year') != year:
                        continue
                results.append(post)
        
        # Sort by created_at desc
        results.sort(key=lambda x: x.get('created_at', datetime.now()), reverse=True)
        return results
    
    # Verification codes
    async def store_verification_code(self, email: str, code: str):
        self.verification_codes[email] = {
            'code': code,
            'created_at': datetime.now()
        }
    
    async def get_verification_code(self, email: str) -> Optional[str]:
        code_data = self.verification_codes.get(email)
        if code_data:
            return code_data['code']
        return None
    
    async def remove_verification_code(self, email: str):
        if email in self.verification_codes:
            del self.verification_codes[email]

# Global mock database instance
mock_db = MockDatabase()

# Add some demo data
async def init_demo_data():
    # Demo user
    demo_user = {
        'name': 'Demo Student',
        'email': '953624104113@ritrjpm.ac.in',
        'roll_number': '953624104113',
        'department': 'CSE',
        'year': 3,
        'is_verified': True,
        'hashed_password': '$2b$12$example_hashed_password',
        'profile_image': None
    }
    user_id = await mock_db.create_user(demo_user)
    
    # Demo posts
    demo_posts = [
        {
            'content': 'Welcome to StudentMedia! This is a demo post to show the platform functionality.',
            'author_id': user_id,
            'author_name': 'Demo Student',
            'author_department': 'CSE',
            'author_year': 3,
            'author_profile_image': None,
            'image': None
        },
        {
            'content': 'Looking for study group for Data Structures and Algorithms. Anyone interested?',
            'author_id': user_id,
            'author_name': 'Demo Student',
            'author_department': 'CSE',
            'author_year': 3,
            'author_profile_image': None,
            'image': None
        },
        {
            'content': 'Check out this cool project I built using React and Python! 🚀',
            'author_id': user_id,
            'author_name': 'Demo Student',
            'author_department': 'CSE',
            'author_year': 3,
            'author_profile_image': None,
            'image': None
        }
    ]
    
    for post_data in demo_posts:
        await mock_db.create_post(post_data)

# Initialize demo data when called
# This will be called from the FastAPI startup event
