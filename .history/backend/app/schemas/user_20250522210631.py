from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
import re

# Password validation regex
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def password_strength(cls, v):
        if not PASSWORD_REGEX.match(v):
            raise ValueError(
                'Password must be at least 8 characters long and contain: '
                'uppercase letter, lowercase letter, number, and special character'
            )
        return v

# Properties to receive via API on update
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None

# Properties to return via API
class User(UserBase):
    id: int
    uuid: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    is_totp_enabled: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_successful_login: Optional[datetime] = None
    profile_image_url: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        orm_mode = True

# Properties to return via API for current user
class UserInDB(User):
    hashed_password: str 
