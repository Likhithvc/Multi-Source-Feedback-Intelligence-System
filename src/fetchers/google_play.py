"""
Google Play Store review fetcher.

Fetches user reviews from Google Play Store for specified apps.
"""

import pandas as pd
from google_play_scraper import reviews, Sort


def fetch_google_reviews(app_id: str, count: int = 200) -> pd.DataFrame:
    """
    Fetch reviews from Google Play Store for a given app.
    
    Args:
        app_id: The Google Play app ID (e.g., 'com.example.app')
        count: Number of reviews to fetch (default: 200)
    
    Returns:
        DataFrame with columns: review_id, content, rating, date, source
    """
    try:
        result, _ = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=count
        )
        
        if not result:
            return pd.DataFrame(columns=['review_id', 'content', 'rating', 'date', 'source'])
        
        df = pd.DataFrame(result)
        df = df.rename(columns={
            'reviewId': 'review_id',
            'content': 'content',
            'score': 'rating',
            'at': 'date'
        })
        df['source'] = 'google_play'
        
        return df[['review_id', 'content', 'rating', 'date', 'source']]
    
    except Exception as e:
        print(f"Error fetching Google Play reviews: {e}")
        return pd.DataFrame(columns=['review_id', 'content', 'rating', 'date', 'source'])
