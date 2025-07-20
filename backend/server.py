from fastapi import FastAPI, APIRouter, HTTPException, Depends, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import os
import logging
import uuid
import hashlib
import secrets
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import jwt
from passlib.context import CryptContext
import json
from bson import ObjectId

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

app = FastAPI(title="StudentMedia API", version="1.0.0")
api_router = APIRouter(prefix="/api")

# Models
class UserRegistration(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    department: str = Field(..., min_length=2)
    year: int = Field(..., ge=1, le=4)
    roll_number: str = Field(..., min_length=5)
    
    @validator('email')
    def validate_email_domain(cls, v):
        if not v.endswith('@ritrjpm.ac.in'):
            raise ValueError('Only Ramco Institute of Technology students can register (@ritrjpm.ac.in)')
        return v
    
    @validator('department')
    def validate_department(cls, v):
        allowed_departments = ['CSE', 'ECE', 'MECH', 'CIVIL', 'EEE', 'AIDS', 'AIML', 'IT', 'CHEMICAL']
        if v.upper() not in allowed_departments:
            raise ValueError(f'Department must be one of: {", ".join(allowed_departments)}')
        return v.upper()

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class EmailVerification(BaseModel):
    email: EmailStr
    verification_code: str

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    department: str
    year: int
    roll_number: str
    profile_image: Optional[str] = None
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    bio: Optional[str] = None

class PostCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    image: Optional[str] = None  # Base64 encoded image
    tags: List[str] = Field(default_factory=list)

class Post(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    content: str
    image: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    likes_count: int = 0
    comments_count: int = 0
    shares_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Comment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    post_id: str
    user_id: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CommentWithUser(BaseModel):
    id: str
    content: str
    created_at: datetime
    user: Dict[str, Any]

class PostWithUser(BaseModel):
    id: str
    content: str
    image: Optional[str]
    tags: List[str]
    likes_count: int
    comments_count: int
    shares_count: int
    created_at: datetime
    user: Dict[str, Any]
    is_liked: bool = False
    is_bookmarked: bool = False
    comments: List[CommentWithUser] = Field(default_factory=list)

class SearchQuery(BaseModel):
    query: str
    department: Optional[str] = None
    year: Optional[int] = None

# Utility Functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def generate_verification_code():
    return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        
        user = await db.users.find_one({"id": user_id})
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return User(**user)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

# Mock email sending function (replace with real email service in production)
async def send_verification_email(email: str, code: str):
    # In production, use services like SendGrid, AWS SES, etc.
    print(f"Verification code for {email}: {code}")
    # Store verification code in database
    await db.verification_codes.insert_one({
        "email": email,
        "code": code,
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(minutes=15)
    })

# Authentication Routes
@api_router.post("/auth/register")
async def register(user_data: UserRegistration, background_tasks: BackgroundTasks):
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    # Hash password
    hashed_password = pwd_context.hash(user_data.password)
    
    # Create user
    user = User(
        name=user_data.name,
        email=user_data.email,
        department=user_data.department,
        year=user_data.year,
        roll_number=user_data.roll_number,
        is_verified=False
    )
    
    # Store user and password
    await db.users.insert_one(user.dict())
    await db.user_passwords.insert_one({
        "user_id": user.id,
        "password_hash": hashed_password
    })
    
    # Generate and send verification code
    verification_code = generate_verification_code()
    background_tasks.add_task(send_verification_email, user_data.email, verification_code)
    
    return {"message": "Registration successful. Please check your email for verification code."}

@api_router.post("/auth/verify-email")
async def verify_email(verification_data: EmailVerification):
    # Check verification code
    code_record = await db.verification_codes.find_one({
        "email": verification_data.email,
        "code": verification_data.verification_code,
        "expires_at": {"$gt": datetime.utcnow()}
    })
    
    if not code_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code"
        )
    
    # Update user verification status
    await db.users.update_one(
        {"email": verification_data.email},
        {"$set": {"is_verified": True}}
    )
    
    # Delete verification code
    await db.verification_codes.delete_one({"_id": code_record["_id"]})
    
    return {"message": "Email verified successfully"}

@api_router.post("/auth/login")
async def login(login_data: UserLogin):
    # Find user
    user = await db.users.find_one({"email": login_data.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not user["is_verified"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please verify your email first"
        )
    
    # Check password
    password_record = await db.user_passwords.find_one({"user_id": user["id"]})
    if not password_record or not pwd_context.verify(login_data.password, password_record["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user["id"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": User(**user).dict()
    }

# User Routes
@api_router.get("/users/me", response_model=User)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@api_router.put("/users/me")
async def update_profile(
    name: Optional[str] = None,
    bio: Optional[str] = None,
    profile_image: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if bio is not None:
        update_data["bio"] = bio
    if profile_image is not None:
        update_data["profile_image"] = profile_image
    
    if update_data:
        await db.users.update_one(
            {"id": current_user.id},
            {"$set": update_data}
        )
    
    return {"message": "Profile updated successfully"}

# Post Routes
@api_router.post("/posts")
async def create_post(post_data: PostCreate, current_user: User = Depends(get_current_user)):
    post = Post(
        user_id=current_user.id,
        content=post_data.content,
        image=post_data.image,
        tags=post_data.tags
    )
    
    await db.posts.insert_one(post.dict())
    return {"message": "Post created successfully", "post_id": post.id}

@api_router.get("/posts", response_model=List[PostWithUser])
async def get_posts(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user)
):
    # Get posts with user information
    pipeline = [
        {"$sort": {"created_at": -1}},
        {"$skip": skip},
        {"$limit": limit},
        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "id",
                "as": "user"
            }
        },
        {"$unwind": "$user"},
        {
            "$addFields": {
                "user": {
                    "id": "$user.id",
                    "name": "$user.name",
                    "department": "$user.department",
                    "year": "$user.year",
                    "profile_image": "$user.profile_image"
                }
            }
        },
        {"$project": {"_id": 0}}
    ]
    
    posts = await db.posts.aggregate(pipeline).to_list(length=limit)
    
    # Check if user liked or bookmarked posts
    for post in posts:
        like = await db.post_likes.find_one({"post_id": post["id"], "user_id": current_user.id})
        bookmark = await db.post_bookmarks.find_one({"post_id": post["id"], "user_id": current_user.id})
        post["is_liked"] = like is not None
        post["is_bookmarked"] = bookmark is not None
        
        # Get recent comments
        comments_pipeline = [
            {"$match": {"post_id": post["id"]}},
            {"$sort": {"created_at": -1}},
            {"$limit": 3},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "id",
                    "as": "user"
                }
            },
            {"$unwind": "$user"},
            {
                "$addFields": {
                    "user": {
                        "name": "$user.name",
                        "department": "$user.department",
                        "year": "$user.year"
                    }
                }
            },
            {"$project": {"_id": 0}}
        ]
        
        comments = await db.comments.aggregate(comments_pipeline).to_list(length=3)
        post["comments"] = comments[::-1]  # Reverse to show oldest first
    
    return posts

@api_router.post("/posts/{post_id}/like")
async def toggle_like(post_id: str, current_user: User = Depends(get_current_user)):
    # Check if already liked
    existing_like = await db.post_likes.find_one({"post_id": post_id, "user_id": current_user.id})
    
    if existing_like:
        # Unlike
        await db.post_likes.delete_one({"post_id": post_id, "user_id": current_user.id})
        await db.posts.update_one(
            {"id": post_id},
            {"$inc": {"likes_count": -1}}
        )
        return {"message": "Post unliked", "liked": False}
    else:
        # Like
        await db.post_likes.insert_one({
            "id": str(uuid.uuid4()),
            "post_id": post_id,
            "user_id": current_user.id,
            "created_at": datetime.utcnow()
        })
        await db.posts.update_one(
            {"id": post_id},
            {"$inc": {"likes_count": 1}}
        )
        return {"message": "Post liked", "liked": True}

@api_router.post("/posts/{post_id}/bookmark")
async def toggle_bookmark(post_id: str, current_user: User = Depends(get_current_user)):
    # Check if already bookmarked
    existing_bookmark = await db.post_bookmarks.find_one({"post_id": post_id, "user_id": current_user.id})
    
    if existing_bookmark:
        # Remove bookmark
        await db.post_bookmarks.delete_one({"post_id": post_id, "user_id": current_user.id})
        return {"message": "Bookmark removed", "bookmarked": False}
    else:
        # Add bookmark
        await db.post_bookmarks.insert_one({
            "id": str(uuid.uuid4()),
            "post_id": post_id,
            "user_id": current_user.id,
            "created_at": datetime.utcnow()
        })
        return {"message": "Post bookmarked", "bookmarked": True}

@api_router.post("/posts/{post_id}/comments")
async def add_comment(
    post_id: str,
    comment_data: dict,
    current_user: User = Depends(get_current_user)
):
    comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        content=comment_data["content"]
    )
    
    await db.comments.insert_one(comment.dict())
    await db.posts.update_one(
        {"id": post_id},
        {"$inc": {"comments_count": 1}}
    )
    
    return {"message": "Comment added successfully"}

# Search Routes
@api_router.post("/search")
async def search_posts(search_data: SearchQuery, current_user: User = Depends(get_current_user)):
    # Build search filter
    search_filter = {
        "$or": [
            {"content": {"$regex": search_data.query, "$options": "i"}},
            {"tags": {"$in": [re.compile(search_data.query, re.IGNORECASE)]}}
        ]
    }
    
    # Add department filter if specified
    if search_data.department:
        user_filter = {"department": search_data.department.upper()}
        if search_data.year:
            user_filter["year"] = search_data.year
        
        # Get user IDs matching the criteria
        matching_users = await db.users.find(user_filter, {"id": 1}).to_list(length=None)
        user_ids = [user["id"] for user in matching_users]
        search_filter["user_id"] = {"$in": user_ids}
    
    # Search posts
    pipeline = [
        {"$match": search_filter},
        {"$sort": {"created_at": -1}},
        {"$limit": 50},
        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "id",
                "as": "user"
            }
        },
        {"$unwind": "$user"},
        {
            "$addFields": {
                "user": {
                    "id": "$user.id",
                    "name": "$user.name",
                    "department": "$user.department",
                    "year": "$user.year",
                    "profile_image": "$user.profile_image"
                }
            }
        },
        {"$project": {"_id": 0}}
    ]
    
    posts = await db.posts.aggregate(pipeline).to_list(length=50)
    return posts

@api_router.get("/departments")
async def get_departments():
    departments = ['CSE', 'ECE', 'MECH', 'CIVIL', 'EEE', 'AIDS', 'AIML', 'IT', 'CHEMICAL']
    return {"departments": departments}

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

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()