# [Task T011] Configuration management
import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# JWT Configuration
JWT_SECRET: str = os.getenv("JWT_SECRET", "your-secret-key-change-this-in-production")
JWT_ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
