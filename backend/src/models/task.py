# [Task T014] Task model
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, Column, Text


class Task(SQLModel, table=True):
    """Task entity with title, description, completion status, priority, and categories."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    completed: bool = Field(default=False)
    priority: str = Field(default="medium", max_length=10)
    due_date: Optional[datetime] = Field(default=None)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    tags: str = Field(default="[]", max_length=1000)
    deleted_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
