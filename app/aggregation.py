from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from .models import Tweet, SentimentSummary

async def aggregate_daily_sentiment(db: AsyncSession):
    result = await db.execute(
        select(
            func.date(Tweet.created_at).label('date'),
            func.count().filter(Tweet.sentiment == 'positive').label('positive'),
            func.count().filter(Tweet.sentiment == 'negative').label('negative'),
            func.count().filter(Tweet.sentiment == 'neutral').label('neutral')
        ).group_by(func.date(Tweet.created_at))
    )
    summaries = result.all()
    for summary in summaries:
        sentiment_summary = SentimentSummary(
            summary_date=summary.date,
            positive=summary.positive,
            negative=summary.negative,
            neutral=summary.neutral
        )
        db.add(sentiment_summary)
    await db.commit()