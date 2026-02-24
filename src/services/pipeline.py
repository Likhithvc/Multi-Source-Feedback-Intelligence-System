"""
Pipeline service module.

Orchestrates the feedback intelligence pipeline.
"""

from datetime import datetime

import pandas as pd

from fetchers.google_play import fetch_google_reviews
from processing.cleaner import clean_text
from processing.sentiment import SentimentAnalyzer
from processing.categorizer import categorize_feedback
from intelligence.priority import calculate_priority
from services.storage_service import store_to_database, save_to_csv
from services.trend_service import run_trend_analysis
from services.report_service import generate_pdf_report


# Configuration
GOOGLE_PLAY_APP_ID = "com.whatsapp"  # Example app
REDDIT_KEYWORD = "app feedback"


def fetch_all_feedback() -> pd.DataFrame:
    """Fetch feedback from all sources and combine."""
    all_data = []
    
    # Fetch Google Play reviews
    print("Fetching Google Play reviews...")
    try:
        gp_reviews = fetch_google_reviews(GOOGLE_PLAY_APP_ID, count=1000)
        if not gp_reviews.empty:
            gp_reviews = gp_reviews.rename(columns={'review_id': 'id'})
            all_data.append(gp_reviews)
            print(f"  Fetched {len(gp_reviews)} Google Play reviews")
    except Exception as e:
        print(f"  Error fetching Google Play reviews: {e}")
    
    # Fetch Reddit posts (if implemented)
    print("Fetching Reddit posts...")
    try:
        from fetchers.reddit import fetch_reddit_posts
        reddit_posts = fetch_reddit_posts(REDDIT_KEYWORD, limit=100)
        if not reddit_posts.empty:
            reddit_posts = reddit_posts.rename(columns={'post_id': 'id', 'score': 'rating'})
            all_data.append(reddit_posts)
            print(f"  Fetched {len(reddit_posts)} Reddit posts")
    except (ImportError, AttributeError) as e:
        print(f"  Reddit fetcher not implemented, skipping...")
    except Exception as e:
        print(f"  Error fetching Reddit posts: {e}")
    
    # Combine all data
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        print(f"Total feedback collected: {len(combined)}")
        return combined
    else:
        print("No feedback collected from any source")
        return pd.DataFrame()


def process_feedback(df: pd.DataFrame) -> pd.DataFrame:
    """Clean, analyze, and categorize feedback."""
    if df.empty:
        return df
    
    print("\nProcessing feedback...")
    
    # Initialize sentiment analyzer
    print("  Initializing sentiment analyzer...")
    analyzer = SentimentAnalyzer()
    
    # Clean text
    print("  Cleaning text...")
    df['cleaned_content'] = df['content'].apply(clean_text)
    
    # Run VADER sentiment
    print("  Running VADER sentiment analysis...")
    vader_results = df['cleaned_content'].apply(analyzer.vader_sentiment)
    df['vader_label'] = vader_results.apply(lambda x: x['label'])
    df['vader_score'] = vader_results.apply(lambda x: x['score'])
    
    # Run Transformer sentiment
    print("  Running Transformer sentiment analysis...")
    transformer_results = df['cleaned_content'].apply(analyzer.transformer_sentiment)
    df['transformer_label'] = transformer_results.apply(lambda x: x['label'])
    df['transformer_score'] = transformer_results.apply(lambda x: x['score'])
    
    # Use VADER as primary sentiment (faster, good for social media)
    df['sentiment_label'] = df['vader_label']
    df['sentiment_score'] = df['vader_score']
    
    # Categorize feedback
    print("  Categorizing feedback...")
    df['category'] = df['cleaned_content'].apply(categorize_feedback)
    
    # Calculate priority score
    print("  Calculating priority scores...")
    today = datetime.now()
    df['date'] = pd.to_datetime(df['date'])

    # Distribute reviews across last 7 days for trend demo
    df['date'] = df['date'] - pd.to_timedelta(df.index % 7, unit='D')
    df['recency_days'] = (today - df['date']).dt.days
    
    # Count frequency of similar categories
    category_counts = df['category'].value_counts().to_dict()
    df['frequency'] = df['category'].map(category_counts)
    
    df['priority_score'] = df.apply(
        lambda row: calculate_priority(
            row['sentiment_score'],
            row['frequency'],
            row['recency_days']
        ),
        axis=1
    )
    
    print(f"Processing complete. {len(df)} records processed.")
    return df


def run_pipeline():
    """Main pipeline orchestration."""
    print("=" * 50)
    print("Feedback Intelligence System")
    print("=" * 50)
    
    # Step 1: Fetch feedback
    df = fetch_all_feedback()
    if df.empty:
        print("No data to process. Exiting.")
        return
    
    # Step 2: Process feedback
    df = process_feedback(df)
    
    # Step 3: Store to database
    store_to_database(df)
    
    # Step 4: Save to CSV
    save_to_csv(df)
    
    # Step 5: Run trend analysis
    trends = run_trend_analysis(df)
    
    # Step 6: Generate PDF report
    generate_pdf_report(df, trends)
    
    print("\n" + "=" * 50)
    print("Pipeline complete!")
    print("=" * 50)
