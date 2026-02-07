# [Task T018] Authentication schemas
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Request model for user login."""
    email: EmailStr
    password: str = Field(min_length=8)


class RegisterRequest(BaseModel):
    """Request model for user registration."""
    email: EmailStr
    password: str = Field(min_length=8)


class TokenResponse(BaseModel):
    """Response model for authentication token."""
    access_token: str
    token_type: str = "bearer"
