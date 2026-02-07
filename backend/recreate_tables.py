"""
Script to drop and recreate all database tables.
WARNING: This will delete all existing data!
"""
from src.db.engine import engine
from sqlmodel import SQLModel
from src.models import User, Task, Category

print("WARNING: This will drop all tables and delete all data!")
print("Press Ctrl+C to cancel...")

try:
    input("Press Enter to continue...")
except KeyboardInterrupt:
    print("\nCancelled.")
    exit(0)

print("\nDropping all tables...")
SQLModel.metadata.drop_all(engine)
print("[OK] Tables dropped")

print("\nCreating all tables with new schema...")
SQLModel.metadata.create_all(engine)
print("[OK] Tables created successfully!")

print("\nDatabase is ready with the updated schema.")
print("You can now register users and create tasks with all new fields.")
