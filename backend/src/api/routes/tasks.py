# [Task T035, T036, T047, T048, T049, T050] Task routes
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from sqlmodel import Session

from src.auth.dependencies import verify_token
from src.db.dependencies import get_db_session
from src.models.task import Task
from src.services.task_service import (
    create_task,
    delete_task,
    get_task_by_id,
    get_user_tasks,
    toggle_task_completion,
    update_task,
)

router = APIRouter(prefix="/api/tasks", tags=["tasks"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Get current user ID from JWT token."""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return int(payload.get("sub"))


class TaskCreate(BaseModel):
    """Request schema for creating a task."""
    title: str
    description: str | None = None
    priority: str = "medium"
    due_date: datetime | None = None
    category_id: int | None = None
    tags: str = "[]"


class TaskUpdate(BaseModel):
    """Request schema for updating a task."""
    title: str | None = None
    description: str | None = None
    priority: str | None = None
    due_date: datetime | None = None
    category_id: int | None = None
    tags: str | None = None
    completed: bool | None = None


@router.get("", response_model=List[Task])
def read_tasks(
    category_id: Optional[int] = Query(None),
    priority: Optional[str] = Query(None),
    completed: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db_session),
    user_id: int = Depends(get_current_user_id)
):
    """Get all tasks for current user with optional filters."""
    return get_user_tasks(db, user_id, category_id, priority, completed, search)


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task: TaskCreate,
    db: Session = Depends(get_db_session),
    user_id: int = Depends(get_current_user_id),
):
    """Create new task for current user."""
    try:
        return create_task(
            db, user_id, task.title, task.description,
            task.priority, task.due_date, task.category_id, task.tags
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db_session), user_id: int = Depends(get_current_user_id)):
    """Get specific task by ID if owned by current user."""
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=Task)
def update_existing_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db_session),
    user_id: int = Depends(get_current_user_id),
):
    """Update task fields."""
    try:
        return update_task(
            db, task_id, user_id,
            task.title, task.description, task.priority,
            task.due_date, task.category_id, task.tags, task.completed
        )
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{task_id}/toggle", response_model=Task)
def toggle_completion(task_id: int, db: Session = Depends(get_db_session), user_id: int = Depends(get_current_user_id)):
    """Toggle task completion status."""
    try:
        return toggle_task_completion(db, task_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(task_id: int, db: Session = Depends(get_db_session), user_id: int = Depends(get_current_user_id)):
    """Delete task permanently."""
    try:
        delete_task(db, task_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
