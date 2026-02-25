"""
Pipeline service module.

Orchestrates the feedback intelligence pipeline.
"""

import os
from datetime import datetime

import pandas as pd

from fetchers.google_play import fetch_google_reviews
from fetchers.csv_loader import load_feedback_from_csv
from fetchers.hf_reviews import fetch_hf_reviews
from processing.cleaner import clean_text
from processing.sentiment import SentimentAnalyzer
from processing.categorizer import categorize_feedback
from intelligence.priority import calculate_priority
from services.storage_service import store_to_database, save_to_csv
from services.trend_service import run_trend_analysis
from services.report_service import generate_pdf_report


# Configuration
GOOGLE_PLAY_APP_ID = "com.whatsapp"  # Example app
EXTERNAL_FEEDBACK_CSV = "data/external_feedback.csv"


def fetch_all_feedback() -> pd.DataFrame:
    """Fetch feedback from multiple sources: Google Play Store and CSV files."""
    all_data = []
    
    # Fetch Google Play reviews
    print("Fetching Google Play reviews...")
    gp_count = 0
    try:
        gp_reviews = fetch_google_reviews(GOOGLE_PLAY_APP_ID, count=1000)
        if not gp_reviews.empty:
            gp_reviews = gp_reviews.rename(columns={'review_id': 'id'})
            gp_count = len(gp_reviews)
            all_data.append(gp_reviews)
            print(f"  Fetched {gp_count} Google Play reviews")
    except Exception as e:
        print(f"  Error fetching Google Play reviews: {e}")
    
    # Fetch CSV feedback
    print("Fetching CSV feedback...")
    csv_count = 0
    if os.path.exists(EXTERNAL_FEEDBACK_CSV):
        try:
            csv_feedback = load_feedback_from_csv(EXTERNAL_FEEDBACK_CSV)
            if not csv_feedback.empty:
                csv_count = len(csv_feedback)
                all_data.append(csv_feedback)
                print(f"  Fetched {csv_count} CSV records")
        except Exception as e:
            print(f"  Error loading CSV feedback: {e}")
    else:
        print(f"  CSV file not found: {EXTERNAL_FEEDBACK_CSV} (skipping)")
    
    # Fetch HuggingFace reviews
    print("Fetching HuggingFace dataset reviews...")
    hf_count = 0
    try:
        hf_reviews = fetch_hf_reviews(limit=200)
        if not hf_reviews.empty:
            hf_count = len(hf_reviews)
            all_data.append(hf_reviews)
            print(f"  Fetched {hf_count} HuggingFace records")
    except Exception as e:
        print(f"  Error fetching HuggingFace reviews: {e}")
    
    # Print summary
    print(f"\nRecords fetched per source:")
    print(f"  - Google Play: {gp_count}")
    print(f"  - CSV: {csv_count}")
    print(f"  - HuggingFace: {hf_count}")
    
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
