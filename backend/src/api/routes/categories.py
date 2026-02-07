# [Task T014] Category routes
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session

from src.api.routes.auth import oauth2_scheme
from src.auth.dependencies import verify_token
from src.db.dependencies import get_db_session
from src.services.category_service import CategoryService
from src.models.category import Category

router = APIRouter(prefix="/api/categories", tags=["categories"])


class CategoryCreate(BaseModel):
    """Request schema for creating a category."""
    name: str
    color: str = "#3B82F6"
    icon: str | None = None


class CategoryUpdate(BaseModel):
    """Request schema for updating a category."""
    name: str | None = None
    color: str | None = None
    icon: str | None = None


class CategoryResponse(BaseModel):
    """Response schema for category."""
    id: int
    user_id: int
    name: str
    color: str
    icon: str | None
    created_at: str

    class Config:
        from_attributes = True


@router.get("", response_model=List[CategoryResponse])
def list_categories(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)):
    """Get all categories for the authenticated user."""
    payload = verify_token(token)
    user_id = int(payload["sub"])

    categories = CategoryService.get_user_categories(db, user_id)
    return [CategoryResponse(
        id=c.id,
        user_id=c.user_id,
        name=c.name,
        color=c.color,
        icon=c.icon,
        created_at=c.created_at.isoformat()
    ) for c in categories]


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    request: CategoryCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_session)
):
    """Create a new category."""
    payload = verify_token(token)
    user_id = int(payload["sub"])

    category = CategoryService.create_category(db, user_id, request.name, request.color, request.icon)
    return CategoryResponse(
        id=category.id,
        user_id=category.user_id,
        name=category.name,
        color=category.color,
        icon=category.icon,
        created_at=category.created_at.isoformat()
    )


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    request: CategoryUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_session)
):
    """Update a category."""
    payload = verify_token(token)
    user_id = int(payload["sub"])

    category = CategoryService.update_category(
        db, category_id, user_id, request.name, request.color, request.icon
    )
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    return CategoryResponse(
        id=category.id,
        user_id=category.user_id,
        name=category.name,
        color=category.color,
        icon=category.icon,
        created_at=category.created_at.isoformat()
    )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_session)
):
    """Delete a category."""
    payload = verify_token(token)
    user_id = int(payload["sub"])

    success = CategoryService.delete_category(db, category_id, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    return None
