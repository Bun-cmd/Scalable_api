from typing import Generator
from sqlmodel import Session, SQLModel, create_engine
from app.core.config import settings

# SQLite for simplicity in local development, use PostgreSQL for production
# For PostgreSQL: "postgresql://user:password@host:port/database"
engine = create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session