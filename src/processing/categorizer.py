"""
Feedback categorizer module.

Categorizes feedback into predefined topics or themes.
"""
CATEGORY_KEYWORDS = {
    'Bug': [
        'bug', 'crash', 'error', 'broken', 'fix', 'issue', 'problem',
        'not working', 'doesnt work', 'fails', 'glitch', 'freeze'
    ],
    'Feature Request': [
        'feature', 'add', 'want', 'need', 'wish', 'should have',
        'would be nice', 'suggestion', 'request', 'please add', 'missing'
    ],
    'Performance': [
        'slow', 'fast', 'speed', 'lag', 'performance', 'loading',
        'battery', 'memory', 'cpu', 'optimization', 'heavy'
    ],
    'UI/UX': [
        'ui', 'ux', 'design', 'interface', 'layout', 'look', 'ugly',
        'beautiful', 'confusing', 'intuitive', 'navigation', 'button'
    ]
}


def categorize_feedback(text: str) -> str:
    """
    Categorize feedback based on keywords.
    
    Args:
        text: Feedback text
    
    Returns:
        Category string: Bug, Feature Request, Performance, UI/UX, or Other
    """
    if not text:
        return 'Other'
    
    text_lower = text.lower()
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return category
    
    return 'Other'