# [Task T012] Database engine setup
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel

# Ensure .env is loaded early
load_dotenv()

from src.config import DATABASE_URL

# Debug: Print DATABASE_URL to confirm loading
print(f"DEBUG: DATABASE_URL={DATABASE_URL}")

# Create engine for PostgreSQL (Neon)
# SQLAlchemy will automatically use psycopg2 driver for postgresql:// URLs
# Add connection pool settings to handle Neon's serverless nature
try:
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,  # Verify connections before using them
        pool_size=5,          # Number of connections to maintain
        max_overflow=10,      # Additional connections when needed
        pool_recycle=3600,    # Recycle connections after 1 hour
    )
    print("Database engine created successfully")
except Exception as e:
    print(f"Error creating database engine: {e}")
    raise

def create_db_and_tables():
    """Create all tables in the database."""
    # Import all models to ensure they're registered with SQLModel
    from src.models import User, Task, Category

    print("Creating database tables...")
    print(f"Registered tables: {list(SQLModel.metadata.tables.keys())}")

    try:
        SQLModel.metadata.create_all(engine)
        print("[OK] Database tables created successfully!")
    except Exception as e:
        print(f"[ERROR] Error creating tables: {e}")
        raise
