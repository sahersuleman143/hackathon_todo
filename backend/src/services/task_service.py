# [Task T033, T034, T044, T045, T046] Task service
from datetime import datetime
from typing import List, Optional

from sqlmodel import Session, select, or_

from src.models.task import Task


def create_task(
    db: Session,
    user_id: int,
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    due_date: Optional[datetime] = None,
    category_id: Optional[int] = None,
    tags: str = "[]"
) -> Task:
    """Create new task for user."""
    # Validate title
    if not title or len(title.strip()) == 0:
        raise ValueError("Title is required")
    if len(title) > 200:
        raise ValueError("Title must be 200 characters or less")

    # Validate description
    if description and len(description) > 1000:
        raise ValueError("Description must be 1000 characters or less")

    # Validate priority
    if priority not in ["low", "medium", "high"]:
        priority = "medium"

    # Create task
    task = Task(
        user_id=user_id,
        title=title.strip(),
        description=description,
        priority=priority,
        due_date=due_date,
        category_id=category_id,
        tags=tags
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_user_tasks(
    db: Session,
    user_id: int,
    category_id: Optional[int] = None,
    priority: Optional[str] = None,
    completed: Optional[bool] = None,
    search_query: Optional[str] = None
) -> List[Task]:
    """Get all tasks for user with optional filters."""
    statement = select(Task).where(Task.user_id == user_id, Task.deleted_at == None)

    # Apply filters
    if category_id is not None:
        statement = statement.where(Task.category_id == category_id)
    if priority is not None:
        statement = statement.where(Task.priority == priority)
    if completed is not None:
        statement = statement.where(Task.completed == completed)
    if search_query:
        search_pattern = f"%{search_query}%"
        statement = statement.where(
            or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern)
            )
        )

    # Order by due date (nulls last), then creation date
    statement = statement.order_by(Task.due_date.asc().nulls_last(), Task.created_at.desc())
    return list(db.exec(statement).all())


def get_task_by_id(db: Session, task_id: int, user_id: int) -> Optional[Task]:
    """Get specific task by ID if owned by user."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    return db.exec(statement).first()


def update_task(
    db: Session,
    task_id: int,
    user_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    due_date: Optional[datetime] = None,
    category_id: Optional[int] = None,
    tags: Optional[str] = None,
    completed: Optional[bool] = None
) -> Task:
    """Update task fields."""
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        raise ValueError("Task not found")

    # Validate and update title
    if title is not None:
        if not title or len(title.strip()) == 0:
            raise ValueError("Title is required")
        if len(title) > 200:
            raise ValueError("Title must be 200 characters or less")
        task.title = title.strip()

    # Validate and update description
    if description is not None:
        if description and len(description) > 1000:
            raise ValueError("Description must be 1000 characters or less")
        task.description = description

    # Update other fields
    if priority is not None and priority in ["low", "medium", "high"]:
        task.priority = priority
    if due_date is not None:
        task.due_date = due_date
    if category_id is not None:
        task.category_id = category_id
    if tags is not None:
        task.tags = tags
    if completed is not None:
        task.completed = completed

    task.updated_at = datetime.utcnow()
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def toggle_task_completion(db: Session, task_id: int, user_id: int) -> Task:
    """Toggle task completion status."""
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        raise ValueError("Task not found")

    task.completed = not task.completed
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, user_id: int) -> None:
    """Delete task permanently."""
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        raise ValueError("Task not found")

    db.delete(task)
    db.commit()
