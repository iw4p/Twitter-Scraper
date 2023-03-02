from fastapi import FastAPI
from scrape_profile_tweets import scrape_profile_tweets_since_2023

app = FastAPI()

@app.get("/tweets/{twitter_handle}")
async def tweets(twitter_handle):
    res = scrape_profile_tweets_since_2023(twitter_handle)
    return res