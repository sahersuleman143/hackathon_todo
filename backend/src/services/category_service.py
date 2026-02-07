# [Task T014] Category service
from typing import List, Optional
from sqlmodel import Session, select
from src.models.category import Category


class CategoryService:
    """Business logic for category operations."""

    @staticmethod
    def create_category(
        session: Session, user_id: int, name: str, color: str = "#3B82F6", icon: Optional[str] = None
    ) -> Category:
        """Create a new category for a user."""
        category = Category(user_id=user_id, name=name, color=color, icon=icon)
        session.add(category)
        session.commit()
        session.refresh(category)
        return category

    @staticmethod
    def get_user_categories(session: Session, user_id: int) -> List[Category]:
        """Get all categories for a user."""
        statement = select(Category).where(Category.user_id == user_id).order_by(Category.created_at)
        return list(session.exec(statement).all())

    @staticmethod
    def get_category_by_id(session: Session, category_id: int, user_id: int) -> Optional[Category]:
        """Get a category by ID, ensuring it belongs to the user."""
        statement = select(Category).where(Category.id == category_id, Category.user_id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def update_category(
        session: Session,
        category_id: int,
        user_id: int,
        name: Optional[str] = None,
        color: Optional[str] = None,
        icon: Optional[str] = None,
    ) -> Optional[Category]:
        """Update a category."""
        category = CategoryService.get_category_by_id(session, category_id, user_id)
        if not category:
            return None

        if name is not None:
            category.name = name
        if color is not None:
            category.color = color
        if icon is not None:
            category.icon = icon

        session.add(category)
        session.commit()
        session.refresh(category)
        return category

    @staticmethod
    def delete_category(session: Session, category_id: int, user_id: int) -> bool:
        """Delete a category."""
        category = CategoryService.get_category_by_id(session, category_id, user_id)
        if not category:
            return False

        session.delete(category)
        session.commit()
        return True
