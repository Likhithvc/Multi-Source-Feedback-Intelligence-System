"""
Reddit feedback fetcher.

Fetches posts and comments from specified subreddits using the Reddit API.
"""

import os
from datetime import datetime

import pandas as pd
import praw
from dotenv import load_dotenv

load_dotenv()


def fetch_reddit_posts(keyword: str, limit: int = 100) -> pd.DataFrame:
    """
    Fetch Reddit posts containing a specific keyword.
    
    Args:
        keyword: Search keyword or subreddit name
        limit: Number of posts to fetch (default: 100)
    
    Returns:
        DataFrame with columns: post_id, content, score, date, source
    """
    try:
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT")
        )
        
        posts = []
        for submission in reddit.subreddit("all").search(keyword, limit=limit):
            posts.append({
                'post_id': submission.id,
                'content': f"{submission.title} {submission.selftext}".strip(),
                'score': submission.score,
                'date': datetime.fromtimestamp(submission.created_utc),
                'source': 'reddit'
            })
        
        if not posts:
            return pd.DataFrame(columns=['post_id', 'content', 'score', 'date', 'source'])
        
        return pd.DataFrame(posts)
    
    except Exception as e:
        print(f"Error fetching Reddit posts: {e}")
        return pd.DataFrame(columns=['post_id', 'content', 'score', 'date', 'source'])
