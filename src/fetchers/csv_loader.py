"""
CSV feedback loader.

Loads user feedback from uploaded CSV files.
"""

import pandas as pd


def load_feedback_from_csv(file_path: str) -> pd.DataFrame:
    """
    Load feedback from a CSV file.
    
    Args:
        file_path: Path to the CSV file
    
    Expected CSV columns:
        content: Feedback text
        rating: Numeric rating
        date: Date of feedback
    
    Returns:
        DataFrame with columns: content, rating, date, source
    """
    try:
        df = pd.read_csv(file_path)
        
        required_columns = ['content', 'rating', 'date']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        df['date'] = pd.to_datetime(df['date'])
        df['source'] = 'CSV Upload'
        
        return df[['content', 'rating', 'date', 'source']]
    
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame(columns=['content', 'rating', 'date', 'source'])
