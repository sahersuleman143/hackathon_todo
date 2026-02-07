# [Task T014] Category model
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    """Category entity for organizing tasks."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    name: str = Field(max_length=100)
    color: str = Field(default="#3B82F6", max_length=7)
    icon: Optional[str] = Field(default=None, max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)
