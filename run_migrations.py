# run_migrations.py
# Make sure to set the DATABASE_URL environment variable when running this script
# e.g., DATABASE_URL="postgresql://user:pass@host:port/dbname" python run_migrations.py
import os
from app.database import create_db_and_tables
from app.core.config import settings # Ensure settings are loaded for DATABASE_URL

if __name__ == "__main__":
    print(f"Attempting to create tables for DB: {settings.DATABASE_URL}")
    create_db_and_tables()
    print("Database tables created successfully (or already existed).")