"""
Priority scoring module.

Assigns priority scores to feedback based on urgency and impact.
"""


def calculate_priority(sentiment_score: float, frequency: int, recency_days: int) -> float:
    """
    Calculate priority score for feedback.
    
    Args:
        sentiment_score: Sentiment score (-1 to 1, negative = bad)
        frequency: Number of similar feedback occurrences
        recency_days: Days since the feedback was posted
    
    Returns:
        Priority score (higher = more urgent)
        Returns 0 for positive/neutral sentiment.
    
    Formula:
        priority = (negativity * recency_weight * 80) + (frequency * 3)
    """
    # Positive or neutral sentiment = no priority
    # Only negative feedback needs attention
    if sentiment_score >= 0:
        return 0.0
    
    # Negativity: how negative is the sentiment (0 to 1)
    negativity = abs(sentiment_score)
    
    # Recency weight: linear decay over 30 days
    # 0 days = 1.0, 15 days = 0.5, 30+ days = 0
    recency_weight = max(0, 30 - recency_days) / 30
    
    # Multiplicative decay: negativity * recency_weight
    # Why multiply? A very negative review from 30+ days ago is no longer urgent.
    # Recency acts as a decay factor - even strong negativity fades over time.
    # This ensures old issues don't stay high priority forever.
    # Example: -1.0 sentiment, 0 days old = 80 points
    # Example: -1.0 sentiment, 30 days old = 0 points (decayed)
    negativity_recency = negativity * recency_weight * 80
    
    # Frequency bonus: adds priority if issue is widespread
    frequency_bonus = frequency * 3
    
    priority = negativity_recency + frequency_bonus
    
    return round(priority, 2)