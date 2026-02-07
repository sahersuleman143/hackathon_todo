# [Task T013] User model
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User entity with email, hashed password, and profile data."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    password_hash: str
    name: Optional[str] = Field(default=None, max_length=100)
    profile_picture_url: Optional[str] = Field(default=None, max_length=500)
    theme_preference: str = Field(default="light", max_length=10)
    email_notifications_enabled: bool = Field(default=True)
    points: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
