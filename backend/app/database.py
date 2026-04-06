"""
Database setup for ReBook - Simple SQLite connection
"""
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL - always in backend directory
DB_DIR = Path(__file__).parent.parent
DATABASE_URL = f"sqlite:///{DB_DIR}/rebook.db"

# Create engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Dependency to get database session
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize database (create tables)
def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
