# [Task T017] Database initialization
from src.db.engine import create_db_and_tables

def init_database():
    """Initialize database with all tables."""
    create_db_and_tables()
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_database()
