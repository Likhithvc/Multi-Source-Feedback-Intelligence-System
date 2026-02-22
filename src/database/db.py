"""
Database connection module.

Handles database connections and session management.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/feedback.db")

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine)


def get_db_session():
    """Create and return a new database session."""
    return SessionLocal()
