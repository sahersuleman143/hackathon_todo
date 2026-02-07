# [Task T020] Authentication dependencies
from typing import Optional

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from src.config import JWT_SECRET, JWT_ALGORITHM


def create_access_token(data: dict) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
