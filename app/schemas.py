from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TweetCreate(BaseModel):
    tweet_id: str
    text: str
    created_at: datetime
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    embedding: Optional[list[float]] = None
    likes: Optional[int] = 0
    retweet_count: Optional[int] = 0
    impression_count: Optional[int] = 0


class SentimentSummaryCreate(BaseModel):
    summary_date: datetime
    positive: int
    negative: int
    neutral: int


class TrendingTopicCreate(BaseModel):
    topic: str
    tweet_count: int


class TweetResponse(BaseModel):
    tweet_id: str
    text: str
    sentiment: str
    sentiment_score: float
    created_at: datetime

    class Config:
        from_attributes = True
