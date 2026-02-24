"""
Text cleaner module.

Cleans and preprocesses raw feedback text for analysis.
"""
import re


def clean_text(text: str) -> str:
    """
    Clean and preprocess text for analysis.
    
    Args:
        text: Raw text input
    
    Returns:
        Cleaned text (lowercase, no URLs, no special chars, emojis preserved)
    """
    if text is None:
        return ""
    
    text = str(text).lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    
    # Remove special characters but keep emojis and alphanumeric
    # Emoji ranges: various Unicode blocks
    text = re.sub(r'[^\w\s\U0001F300-\U0001F9FF\U00002600-\U000026FF\U00002700-\U000027BF]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text