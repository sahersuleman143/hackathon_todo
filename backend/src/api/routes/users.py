# [Task T014] User profile routes
import os
import shutil
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlmodel import Session, select, func

from src.api.routes.auth import oauth2_scheme
from src.auth.dependencies import verify_token
from src.db.dependencies import get_db_session
from src.services.user_service import get_user_by_id, update_user_profile
from src.models.task import Task

router = APIRouter(prefix="/api/users", tags=["users"])


class UserProfileUpdate(BaseModel):
    """Request schema for updating user profile."""
    name: str | None = None
    theme_preference: str | None = None
    email_notifications_enabled: bool | None = None


class UserProfileResponse(BaseModel):
    """Response schema for user profile."""
    id: int
    email: str
    name: str | None
    profile_picture_url: str | None
    theme_preference: str
    email_notifications_enabled: bool
    points: int
    created_at: str

    class Config:
        from_attributes = True


class UserStatsResponse(BaseModel):
    """Response schema for user statistics."""
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    completion_rate: float
    points: int


@router.get("/me", response_model=UserProfileResponse)
def get_current_user_profile(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_session)
):
    """Get current user profile."""
    payload = verify_token(token)
    user_id = int(payload["sub"])

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserProfileResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        profile_picture_url=user.profile_picture_url,
        theme_preference=user.theme_preference,
        email_notifications_enabled=user.email_notifications_enabled,
        points=user.points,
        created_at=user.created_at.isoformat()
    )


@router.put("/me", response_model=UserProfileResponse)
def update_current_user_profile(
    request: UserProfileUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_session)
):
    """Update current user profile."""
    payload = verify_token(token)
    user_id = int(payload["sub"])

    user = update_user_profile(
        db,
        user_id,
        name=request.name,
        theme_preference=request.theme_preference,
        email_notifications_enabled=request.email_notifications_enabled
    )

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserProfileResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        profile_picture_url=user.profile_picture_url,
        theme_preference=user.theme_preference,
        email_notifications_enabled=user.email_notifications_enabled,
        points=user.points,
        created_at=user.created_at.isoformat()
    )


@router.post("/me/avatar")
def upload_avatar(
    file: UploadFile = File(...),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_session)
):
    """Upload user profile picture."""
    payload = verify_token(token)
    user_id = int(payload["sub"])

    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only JPEG, PNG, GIF, and WebP are allowed."
        )

    # Create uploads directory if it doesn't exist
    upload_dir = Path("uploads/avatars")
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Generate unique filename
    file_extension = file.filename.split(".")[-1]
    filename = f"{user_id}_{file.filename}"
    file_path = upload_dir / filename

    # Save file
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )

    # Update user profile with new avatar URL
    avatar_url = f"/uploads/avatars/{filename}"
    user = update_user_profile(db, user_id, profile_picture_url=avatar_url)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"profile_picture_url": avatar_url}


@router.get("/stats", response_model=UserStatsResponse)
def get_user_stats(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_session)
):
    """Get user task statistics."""
    payload = verify_token(token)
    user_id = int(payload["sub"])

    # Count total tasks (excluding soft-deleted)
    total_tasks = db.exec(
        select(func.count(Task.id)).where(Task.user_id == user_id, Task.deleted_at == None)
    ).one()

    # Count completed tasks
    completed_tasks = db.exec(
        select(func.count(Task.id)).where(
            Task.user_id == user_id,
            Task.completed == True,
            Task.deleted_at == None
        )
    ).one()

    # Calculate pending tasks
    pending_tasks = total_tasks - completed_tasks

    # Calculate completion rate
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0

    # Get user points
    user = get_user_by_id(db, user_id)
    points = user.points if user else 0

    return UserStatsResponse(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        completion_rate=round(completion_rate, 1),
        points=points
    )
