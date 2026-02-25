"""
HuggingFace Dataset review fetcher.

Fetches user reviews from HuggingFace public datasets.
"""

import pandas as pd
from datetime import datetime, timedelta
from datasets import load_dataset


def fetch_hf_reviews(limit: int = 200) -> pd.DataFrame:
    """
    Fetch reviews from HuggingFace amazon_polarity dataset.
    
    Args:
        limit: Number of reviews to fetch (default: 200)
    
    Returns:
        DataFrame with columns: id, content, rating, date, source
    """
    try:
        # Load dataset from HuggingFace
        dataset = load_dataset("amazon_polarity", split=f"train[:{limit}]")
        
        if len(dataset) == 0:
            return pd.DataFrame(columns=['id', 'content', 'rating', 'date', 'source'])
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(dataset)
        
        # Generate sequential IDs
        df['id'] = range(1, len(df) + 1)
        
        # Map content column (amazon_polarity uses 'content' for review text)
        df['content'] = df['content']
        
        # Map label to rating scale 1-5
        # amazon_polarity: 0 = negative, 1 = positive
        # Map: 0 -> 1-2 (negative), 1 -> 4-5 (positive)
        df['rating'] = df['label'].apply(lambda x: 5 if x == 1 else 1)
        
        # Generate recent dates distributed over last 7 days
        today = datetime.now()
        df['date'] = df.index.map(lambda i: today - timedelta(days=i % 7))
        df['date'] = pd.to_datetime(df['date'])
        
        # Set source
        df['source'] = 'HuggingFace Dataset'
        
        return df[['id', 'content', 'rating', 'date', 'source']]
    
    except Exception as e:
        print(f"Error fetching HuggingFace reviews: {e}")
        return pd.DataFrame(columns=['id', 'content', 'rating', 'date', 'source'])
