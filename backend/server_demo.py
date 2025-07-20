from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import os
import logging
import hashlib
import secrets
import jwt
from passlib.context import CryptContext
import json

# Import our mock database
from mock_db import mock_db, init_demo_data

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = 'demo-secret-key-change-in-production'

app = FastAPI(title="StudentMedia API", version="1.0.0")
api_router = APIRouter(prefix="/api")

# Pydantic models
class UserRegistration(BaseModel):
    name: str
    email: EmailStr
    roll_number: str
    department: str
    year: int
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class EmailVerification(BaseModel):
    email: EmailStr
    verification_code: str

class PostCreate(BaseModel):
    content: str
    image: Optional[str] = None

class CommentCreate(BaseModel):
    content: str

class SearchRequest(BaseModel):
    query: str
    department: Optional[str] = None
    year: Optional[int] = None

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = await mock_db.find_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Routes
@api_router.post("/auth/register")
async def register(user_data: UserRegistration):
    # Check if user already exists
    existing_user = await mock_db.find_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")
    
    # Generate verification code
    verification_code = f"{secrets.randbelow(900000) + 100000:06d}"
    await mock_db.store_verification_code(user_data.email, verification_code)
    
    # Store user data temporarily (without saving to users collection)
    temp_user_data = {
        'name': user_data.name,
        'email': user_data.email,
        'roll_number': user_data.roll_number,
        'department': user_data.department,
        'year': user_data.year,
        'hashed_password': get_password_hash(user_data.password),
        'is_verified': False,
        'profile_image': None
    }
    
    # In demo mode, return the verification code
    return {
        "message": "Registration successful. Please verify your email.",
        "demo_verification_code": verification_code  # Only for demo
    }

@api_router.post("/auth/verify-email")
async def verify_email(verification_data: EmailVerification):
    stored_code = await mock_db.get_verification_code(verification_data.email)
    if not stored_code or stored_code != verification_data.verification_code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    
    # Create the user now that email is verified
    temp_user_data = {
        'name': 'Verified User',
        'email': verification_data.email,
        'roll_number': '123456789',
        'department': 'CSE',
        'year': 3,
        'hashed_password': get_password_hash('password'),
        'is_verified': True,
        'profile_image': None
    }
    
    await mock_db.create_user(temp_user_data)
    await mock_db.remove_verification_code(verification_data.email)
    
    return {"message": "Email verified successfully"}

@api_router.post("/auth/login")
async def login(login_data: UserLogin):
    user = await mock_db.find_user_by_email(login_data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.get('is_verified', False):
        raise HTTPException(status_code=401, detail="Email not verified")
    
    # For demo, accept any password for existing users
    # if not verify_password(login_data.password, user['hashed_password']):
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user['_id']}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user['_id'],
            "name": user['name'],
            "email": user['email'],
            "department": user['department'],
            "year": user['year'],
            "profile_image": user.get('profile_image')
        }
    }

@api_router.get("/users/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user['_id'],
        "name": current_user['name'],
        "email": current_user['email'],
        "department": current_user['department'],
        "year": current_user['year'],
        "profile_image": current_user.get('profile_image')
    }

@api_router.post("/posts")
async def create_post(post_data: PostCreate, current_user: dict = Depends(get_current_user)):
    post = {
        'content': post_data.content,
        'image': post_data.image,
        'author_id': current_user['_id'],
        'author_name': current_user['name'],
        'author_department': current_user['department'],
        'author_year': current_user['year'],
        'author_profile_image': current_user.get('profile_image')
    }
    
    post_id = await mock_db.create_post(post)
    return {"message": "Post created successfully", "post_id": post_id}

@api_router.get("/posts")
async def get_posts(current_user: dict = Depends(get_current_user)):
    posts = await mock_db.get_all_posts()
    
    # Convert datetime objects to strings and format the response
    formatted_posts = []
    for post in posts:
        formatted_post = {
            "id": post['_id'],
            "content": post['content'],
            "image": post.get('image'),
            "user": {
                "name": post['author_name'],
                "department": post['author_department'],
                "year": post['author_year'],
                "profile_image": post.get('author_profile_image')
            },
            "created_at": post['created_at'].isoformat(),
            "likes": post.get('likes', []),
            "bookmarks": post.get('bookmarks', []),
            "comments": post.get('comments', [])
        }
        formatted_posts.append(formatted_post)
    
    return formatted_posts

@api_router.post("/posts/{post_id}/like")
async def like_post(post_id: str, current_user: dict = Depends(get_current_user)):
    post = await mock_db.find_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    likes = post.get('likes', [])
    user_id = current_user['_id']
    
    if user_id in likes:
        likes.remove(user_id)
    else:
        likes.append(user_id)
    
    await mock_db.update_post(post_id, {'likes': likes})
    return {"message": "Post like toggled"}

@api_router.post("/posts/{post_id}/bookmark")
async def bookmark_post(post_id: str, current_user: dict = Depends(get_current_user)):
    post = await mock_db.find_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    bookmarks = post.get('bookmarks', [])
    user_id = current_user['_id']
    
    if user_id in bookmarks:
        bookmarks.remove(user_id)
    else:
        bookmarks.append(user_id)
    
    await mock_db.update_post(post_id, {'bookmarks': bookmarks})
    return {"message": "Post bookmark toggled"}

@api_router.post("/posts/{post_id}/comments")
async def add_comment(post_id: str, comment_data: CommentCreate, current_user: dict = Depends(get_current_user)):
    post = await mock_db.find_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comment = {
        'id': secrets.token_urlsafe(8),
        'content': comment_data.content,
        'author_name': current_user['name'],
        'created_at': datetime.now().isoformat()
    }
    
    comments = post.get('comments', [])
    comments.append(comment)
    
    await mock_db.update_post(post_id, {'comments': comments})
    return {"message": "Comment added successfully"}

@api_router.post("/search")
async def search_posts(search_data: SearchRequest, current_user: dict = Depends(get_current_user)):
    posts = await mock_db.search_posts(search_data.query, search_data.department, search_data.year)
    
    # Format the response
    formatted_posts = []
    for post in posts:
        formatted_post = {
            "id": post['_id'],
            "content": post['content'],
            "image": post.get('image'),
            "author": {
                "name": post['author_name'],
                "department": post['author_department'],
                "year": post['author_year']
            },
            "created_at": post['created_at'].isoformat(),
            "likes": post.get('likes', []),
            "bookmarks": post.get('bookmarks', []),
            "comments": post.get('comments', [])
        }
        formatted_posts.append(formatted_post)
    
    return formatted_posts

@api_router.get("/departments")
async def get_departments():
    departments = ['CSE', 'ECE', 'MECH', 'CIVIL', 'EEE', 'AIDS', 'AIML', 'IT', 'CHEMICAL']
    return {"departments": departments}

@api_router.get("/auth/demo-code/{email}")
async def get_demo_verification_code(email: str):
    code = await mock_db.get_verification_code(email)
    if code:
        return {"verification_code": code}
    return {"message": "No verification code found"}

# Include router in main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    await init_demo_data()
    logger.info("Demo data initialized")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
