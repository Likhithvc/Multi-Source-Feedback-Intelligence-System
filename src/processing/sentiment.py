"""
Sentiment analysis module.

Analyzes the sentiment of feedback text (positive, negative, neutral).
"""
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from transformers import pipeline


class SentimentAnalyzer:
    """Sentiment analyzer using VADER and HuggingFace transformers."""
    
    def __init__(self):
        """Initialize sentiment analysis models."""
        nltk.download('vader_lexicon', quiet=True)
        self.vader = SentimentIntensityAnalyzer()
        self.transformer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            truncation=True
        )
    
    def vader_sentiment(self, text: str) -> dict:
        """
        Analyze sentiment using NLTK VADER.
        
        Args:
            text: Input text
        
        Returns:
            dict with 'label' and 'score'
        """
        if not text:
            return {'label': 'neutral', 'score': 0.0}
        
        scores = self.vader.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            label = 'positive'
        elif compound <= -0.05:
            label = 'negative'
        else:
            label = 'neutral'
        
        return {'label': label, 'score': compound}
    
    def transformer_sentiment(self, text: str) -> dict:
        """
        Analyze sentiment using HuggingFace transformer.
        
        Args:
            text: Input text
        
        Returns:
            dict with 'label' and 'score'
        """
        if not text:
            return {'label': 'neutral', 'score': 0.0}
        
        try:
            result = self.transformer(text[:512])[0]
            label = result['label'].lower()
            score = result['score'] if label == 'positive' else -result['score']
            return {'label': label, 'score': score}
        except Exception as e:
            print(f"Transformer sentiment error: {e}")
            return {'label': 'neutral', 'score': 0.0}