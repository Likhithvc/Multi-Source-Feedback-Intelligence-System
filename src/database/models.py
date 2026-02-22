"""
Database models module.

Defines SQLAlchemy ORM models for storing feedback data.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Feedback(Base):
    """Model for storing user feedback from various sources."""
    
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    source = Column(String(50), nullable=False)
    rating = Column(Float, nullable=True)
    sentiment_label = Column(String(20), nullable=True)
    sentiment_score = Column(Float, nullable=True)
    category = Column(String(50), nullable=True)
    priority_score = Column(Float, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)


def create_tables(engine):
    """Create all tables in the database."""
    Base.metadata.create_all(engine)
