from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

async def create_tweet(db: AsyncSession, tweet: schemas.TweetCreate):
    db_tweet = models.Tweet(**tweet.dict())
    db.add(db_tweet)
    await db.commit()
    await db.refresh(db_tweet)
    return db_tweet

async def create_sentiment_summary(db: AsyncSession, summary: schemas.SentimentSummaryCreate):
    db_summary = models.SentimentSummary(**summary.dict())
    db.add(db_summary)
    await db.commit()
    await db.refresh(db_summary)
    return db_summary

async def create_trending_topic(db: AsyncSession, topic: schemas.TrendingTopicCreate):
    db_topic = models.TrendingTopic(**topic.dict())
    db.add(db_topic)
    await db.commit()
    await db.refresh(db_topic)
    return db_topic
