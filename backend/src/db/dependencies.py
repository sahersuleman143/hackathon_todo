# [Task T015] Database session dependency
from typing import Generator

from sqlmodel import Session

from src.db.engine import engine


def get_db_session() -> Generator[Session, None, None]:
    """Dependency for database session per request."""
    with Session(engine) as session:
        yield session
