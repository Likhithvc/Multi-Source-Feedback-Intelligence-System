"""
Storage service module.

Handles data persistence to database and CSV files.
"""

import os
from datetime import datetime

import pandas as pd

from database.db import engine, get_db_session
from database.models import Feedback, create_tables


# Configuration
DATA_DIR = "data"


def store_to_database(df: pd.DataFrame):
    """Store processed feedback to SQLite database."""
    if df.empty:
        return
    
    print("\nStoring to database...")
    
    # Create tables if not exist
    create_tables(engine)
    
    session = get_db_session()
    try:
        records_added = 0
        for _, row in df.iterrows():
            feedback = Feedback(
                content=row['content'],
                source=row['source'],
                rating=row.get('rating'),
                sentiment_label=row['sentiment_label'],
                sentiment_score=row['sentiment_score'],
                category=row['category'],
                priority_score=row['priority_score'],
                date=row['date']
            )
            session.add(feedback)
            records_added += 1
        
        session.commit()
        print(f"  Stored {records_added} records to database")
    except Exception as e:
        session.rollback()
        print(f"  Error storing to database: {e}")
    finally:
        session.close()


def save_to_csv(df: pd.DataFrame):
    """Save processed data to CSV file."""
    if df.empty:
        return
    
    os.makedirs(DATA_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(DATA_DIR, f"processed_feedback_{timestamp}.csv")
    
    # Select columns to save
    columns_to_save = [
        'content', 'source', 'rating', 'date',
        'sentiment_label', 'sentiment_score',
        'category', 'priority_score'
    ]
    df[columns_to_save].to_csv(filepath, index=False)
    print(f"\nSaved processed data to {filepath}")
