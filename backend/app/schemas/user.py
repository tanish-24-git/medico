"""
User Pydantic schemas for API requests and responses.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    display_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user."""
    firebase_uid: str = Field(..., min_length=1)
    photo_url: Optional[str] = None
    email_verified: bool = False


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    display_name: Optional[str] = None
    photo_url: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    firebase_uid: str
    photo_url: Optional[str] = None
    email_verified: bool
    created_at: datetime
    last_login: datetime
    
    class Config:
        from_attributes = True


class UserProfile(UserResponse):
    """Extended user profile with statistics."""
    total_reports: int = 0
    total_chat_sessions: int = 0
    
    class Config:
        from_attributes = True
