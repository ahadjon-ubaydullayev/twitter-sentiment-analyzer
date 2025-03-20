from fastapi import FastAPI, Depends, HTTPException
from .routers import sentiment, trends
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas, crud
from sqlalchemy.future import select
from .database import engine, get_db
from .models import Tweet
from .sentiment import analyze_sentiment
from fastapi_utils.tasks import repeat_every
from typing import List
from app.twitter_client import fetch_tweets, fetch_tweets_async



app = FastAPI(title="Social Media Sentiment Analyzer")

# app.include_router(sentiment.router, prefix="/sentiment", tags=["Sentiment"])
# app.include_router(trends.router, prefix="/trends", tags=["Trends"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Social Media Sentiment Analyzer API"}


# endpoint for manual data entry
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.post("/tweets/", response_model=schemas.TweetCreate)
async def create_tweet(tweet: schemas.TweetCreate, db: AsyncSession = Depends(get_db)):
    db_tweet = await crud.create_tweet(db=db, tweet=tweet)
    return db_tweet

@app.post("/sentiment_summaries/", response_model=schemas.SentimentSummaryCreate)
async def create_sentiment_summary(summary: schemas.SentimentSummaryCreate, db: AsyncSession = Depends(get_db)):
    db_summary = await crud.create_sentiment_summary(db=db, summary=summary)
    return db_summary

@app.post("/trending_topics/", response_model=schemas.TrendingTopicCreate)
async def create_trending_topic(topic: schemas.TrendingTopicCreate, db: AsyncSession = Depends(get_db)):
    db_topic = await crud.create_trending_topic(db=db, topic=topic)
    return db_topic


# endpoint for analyze
@app.post("/analyze/")
async def analyze_tweet(tweet_id: str, text: str, db: AsyncSession = Depends(get_db)):
    # Check if tweet already exists
    result = await db.execute(select(Tweet).filter(Tweet.tweet_id == tweet_id))
    existing_tweet = result.scalars().first()
    if existing_tweet:
        raise HTTPException(status_code=400, detail="Tweet already processed.")

    # Analyze sentiment
    sentiment_result = analyze_sentiment(text)

    # Create Tweet object
    new_tweet = Tweet(
        tweet_id=tweet_id,
        text=text,
        sentiment=sentiment_result['label'],
        sentiment_score=sentiment_result['score'],
        # Add other necessary fields
    )

    # Add to database
    db.add(new_tweet)
    await db.commit()
    await db.refresh(new_tweet)

    return {"message": "Tweet analyzed and stored.", "tweet": new_tweet}



# retrieve all tweets
@app.get("/all_tweets/", response_model=List[schemas.TweetResponse])
async def read_tweets(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """
    Retrieve stored tweets from the database.
    - **skip**: Number of records to skip for pagination.
    - **limit**: Maximum number of records to return.
    """
    result = await db.execute(select(Tweet).offset(skip).limit(limit))
    tweets = result.scalars().all()
    return tweets

# function to timely fetch tweets
@app.on_event("startup")
@repeat_every(seconds=3600)  # Adjust the interval as needed
async def ingest_tweets_task():
    query = "#python"  # Define your query
    tweets = fetch_tweets_async(query)
    async with get_db() as db:
        for tweet in tweets:
            # Analyze and store each tweet
            await analyze_tweet(tweet_id=tweet['id'], text=tweet['text'], db=db)

