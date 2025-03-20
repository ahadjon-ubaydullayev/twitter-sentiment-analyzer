from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Date, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tweet(Base):
    __tablename__ = "tweets"
    
    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, unique=True, index=True, nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    sentiment = Column(String, nullable=True)  # e.g., "positive", "negative", "neutral"
    sentiment_score = Column(Float, nullable=True)  # Optional polarity score
    embedding = Column(JSON, nullable=True)  # Storing embedding as JSON (list of floats)
    likes = Column(Integer, default=0)
    retweet_count = Column(Integer, default=0)
    impression_count = Column(Integer, default=0)
    processed_at = Column(DateTime, server_default=func.now())

class SentimentSummary(Base):
    __tablename__ = "sentiment_summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    summary_date = Column(Date, nullable=False, index=True)
    positive = Column(Integer, default=0)
    negative = Column(Integer, default=0)
    neutral = Column(Integer, default=0)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class TrendingTopic(Base):
    __tablename__ = "trending_topics"
    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False, index=True)
    tweet_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
