"""
Trend service module.

Handles trend analysis operations.
"""

import pandas as pd

from intelligence.trend import analyze_sentiment_trend


def run_trend_analysis(df: pd.DataFrame) -> dict:
    """Run trend analysis on processed feedback."""
    if df.empty:
        return {}
    
    print("\nRunning trend analysis...")
    trends = analyze_sentiment_trend(df)
    
    print(f"  Overall trend: {trends['overall_trend']}")
    print(f"  Average sentiment: {trends['avg_sentiment']}")
    if trends['negative_spike_dates']:
        print(f"  Negative spike dates: {', '.join(trends['negative_spike_dates'])}")
    
    return trends
