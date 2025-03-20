from transformers import pipeline

# Load pre-trained sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(text: str) -> dict:
    """
    Analyze the sentiment of the given text.
    Returns a dictionary with label and score.
    """
    result = sentiment_analyzer(text)[0]
    return {"label": result['label'].lower(), "score": result['score']}