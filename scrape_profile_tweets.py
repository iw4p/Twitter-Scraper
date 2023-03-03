from twitter_scraper_selenium import scrape_keyword
import json
import asyncio

def scrape_profile_tweets_since_2023(username: str):
    kword = "from:" + username
    tweets = scrape_keyword(
                            headless=True,
                            keyword=kword,
                            browser="chrome",
                            tweets_count=3200,
                            filename=username,
                            output_format="csv",
                            since="2023-01-01",
                            # until="2025-03-02",
                            )
    data = json.loads(tweets)
    return data