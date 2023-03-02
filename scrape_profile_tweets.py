from twitter_scraper_selenium import scrape_keyword
import json

def scrape_profile_tweets_since_2023(username: str):
    kword = "from:" + username
    tweets = scrape_keyword(headless=False, keyword=kword, browser="chrome", tweets_count=1, output_format="json", until="2023-03-02", since="2023-01-01")
    data = json.loads(tweets)
    # tweets = {"1630615307759894638": {"tweet_id": "1630615307759894638", "username": "BarackObama", "name": "Barack Obama", "profile_picture": "https://pbs.twimg.com/profile_images/1329647526807543809/2SGvnHYV_x96.jpg", "replies": 578, "retweets": 1234, "likes": 7004, "is_retweet": True, "posted_time": "2023-02-28T17:05:59+00:00", "content": "Real change happens one person, one community, one connection at a time. If you\u2019re an emerging leader in Chicago, Detroit, or Jackson \u2014 I hope you\u2019ll check out this new initiative to bring people from different backgrounds together to help solve local problems.", "hashtags": [], "mentions": [], "images": [], "videos": ["blob:https://twitter.com/3de71fc6-afa0-4e5b-9a90-552168cefdff"], "tweet_url": "https://twitter.com/BarackObama/status/1630615307759894638", "link": ""}}
    return data