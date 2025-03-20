# import tweepy
# import os
# from dotenv import load_dotenv

# load_dotenv()

# # Authenticate with Twitter
# auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# api = tweepy.API(auth)

# def fetch_tweets(query: str, count: int = 10):
#     """
#     Fetch tweets based on a query.
#     """
#     tweets = api.search_tweets(q=query, count=count, tweet_mode='extended')
#     for tweet in tweets:
#         print(f"Tweet ID: {tweet.id_str}")
#         print(f"Tweet Text: {tweet.full_text}")
#         print("-" * 40)
#     return [{"id": tweet.id_str, "text": tweet.full_text} for tweet in tweets]


# if __name__ == "__main__":
#     query = input("Enter the search query: ")
#     count = int(input("Enter the number of tweets to fetch: "))
#     fetch_tweets(query, count)



import os
import tweepy
from dotenv import load_dotenv
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()


# Load environment variables
load_dotenv()


# Twitter API credentials
API_KEY = "HnAWUSaT96cMcTV4cgojXd8UC"
API_SECRET = "gQjglxJDR6KCcWaTI8bxJXi2yo5ZdULONECTLPhlAPvIY7BJGs"
ACCESS_TOKEN = "1733367972813733888-BSfbwH9x8JUPyBsNE0UtSzf44c2jiM"
ACCESS_TOKEN_SECRET = "KQZrFo0h10yoJwp2oniGTkTM9qILwtL4LSRJMwxaeIKug"


# Authenticate with Twitter API v2
client = tweepy.Client(bearer_token=os.getenv("BEARER_TOKEN"))

def fetch_tweets(query: str, count: int = 10):
    """
    Fetch tweets based on a query using Twitter API v2.
    """
    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=count,
            tweet_fields=["created_at", "author_id"]
        )
        if not response.data:
            print("No tweets found for the given query.")
            return []

        for tweet in response.data:
            print(f"Tweet ID: {tweet.id}")
            print(f"Tweet Text: {tweet.text}")
            print("-" * 40)

        return [{"id": tweet.id, "text": tweet.text} for tweet in response.data]

    except tweepy.errors.TweepyException as e:
        print(f"Error fetching tweets: {e}")
        return []

async def fetch_tweets_async(query: str, count: int = 10):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, fetch_tweets, query, count)

# if __name__ == "__main__":
#     query = input("Enter the search query: ")
#     count = int(input("Enter the number of tweets to fetch: "))
#     fetch_tweets(query, count)