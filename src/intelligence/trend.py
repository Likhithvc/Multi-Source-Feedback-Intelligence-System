"""
Trend analysis module.

Identifies trends and patterns in feedback over time.
"""
import pandas as pd


def analyze_sentiment_trend(df: pd.DataFrame) -> dict:
    """
    Analyze sentiment trends over time.
    
    Args:
        df: DataFrame with 'date' and 'sentiment_score' columns
    
    Returns:
        Dictionary with trend summary:
            - daily_sentiment: dict of date -> avg sentiment
            - overall_trend: 'improving', 'declining', or 'stable'
            - negative_spike_dates: list of dates with significant negative sentiment
            - avg_sentiment: overall average sentiment score
    """
    if df.empty or 'date' not in df.columns or 'sentiment_score' not in df.columns:
        return {
            'daily_sentiment': {},
            'overall_trend': 'stable',
            'negative_spike_dates': [],
            'avg_sentiment': 0.0
        }
    
    df = df.copy()
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    # Group by date and calculate average sentiment
    daily_sentiment = df.groupby('date')['sentiment_score'].mean().to_dict()
    
    # Convert dates to strings for JSON serialization
    daily_sentiment = {str(k): round(v, 3) for k, v in daily_sentiment.items()}
    
    # Calculate overall average
    avg_sentiment = df['sentiment_score'].mean()
    
    # Detect negative spikes (days with avg sentiment below -0.3)
    negative_spike_dates = [
        date for date, score in daily_sentiment.items() if score < -0.3
    ]
    
    # Determine overall trend by comparing recent vs older sentiment
    dates_sorted = sorted(daily_sentiment.keys())
    if len(dates_sorted) >= 2:
        mid = len(dates_sorted) // 2
        older_avg = sum(daily_sentiment[d] for d in dates_sorted[:mid]) / mid
        recent_avg = sum(daily_sentiment[d] for d in dates_sorted[mid:]) / (len(dates_sorted) - mid)
        
        if recent_avg - older_avg > 0.1:
            overall_trend = 'improving'
        elif older_avg - recent_avg > 0.1:
            overall_trend = 'declining'
        else:
            overall_trend = 'stable'
    else:
        overall_trend = 'stable'
    
    return {
        'daily_sentiment': daily_sentiment,
        'overall_trend': overall_trend,
        'negative_spike_dates': negative_spike_dates,
        'avg_sentiment': round(avg_sentiment, 3)
    }