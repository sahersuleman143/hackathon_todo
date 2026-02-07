# [Task T019] User service for authentication
import bcrypt
from typing import Optional

from sqlmodel import Session, select

from src.models.user import User


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    statement = select(User).where(User.email == email)
    return db.exec(statement).first()


def create_user(db: Session, email: str, password: str) -> User:
    """Create new user with hashed password."""
    # Check if user already exists
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise ValueError("Email already registered")

    # Hash password
    password_hash = hash_password(password)

    # Create user
    user = User(email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID."""
    statement = select(User).where(User.id == user_id)
    return db.exec(statement).first()


def update_user_profile(
    db: Session,
    user_id: int,
    name: Optional[str] = None,
    theme_preference: Optional[str] = None,
    email_notifications_enabled: Optional[bool] = None,
    profile_picture_url: Optional[str] = None,
) -> Optional[User]:
    """Update user profile information."""
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    if name is not None:
        user.name = name
    if theme_preference is not None:
        user.theme_preference = theme_preference
    if email_notifications_enabled is not None:
        user.email_notifications_enabled = email_notifications_enabled
    if profile_picture_url is not None:
        user.profile_picture_url = profile_picture_url

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
