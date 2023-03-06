from fastapi import FastAPI
from scrape_profile_tweets import scrape_profile_tweets_since_2023
from scrape_replies import scrape_replies
# from sentiment import get_tweet_sentiment
from groupby import most_mentioned

app = FastAPI()

# - /accounts: return a json list of all tracked accounts.
@app.get("/accounts/")
async def accounts():
    res = {'users': ['alikarimi_ak8', 'elonmusk', 'BarackObama', 'taylorlorenz', 'cathiedwood', 'ylecun']}
    return res

# - /tweets/<twitter-handle> : return a json of the user's conversation threads since start.
@app.get("/tweets/{twitter_handle}")
async def tweets(twitter_handle):
    res = scrape_profile_tweets_since_2023(twitter_handle)
    return res

# - /audience/<twitter-handle> : return a json of information about the audience for a user's account.
@app.get("/audience/{twitter_handle}")
async def audience(twitter_handle):
    res = most_mentioned(twitter_handle)
    return res

# - /sentiment/<twitter-handle> : return a json about the sentiment information of an account (e.g. thread level, audience level)
@app.get("/sentiment/{twitter_handle}")
async def sentiment(twitter_handle):
    res = x(twitter_handle)
    return res


# - /textsentiment/<tweet> : return negative or positive
# @app.get("/textsentiment/{tweet}")
# async def text_sentiment(tweet):
#     res = get_tweet_sentiment(tweet)
#     return res

@app.get("/replies/{twitter_handle}")
async def replies(twitter_handle):
    res = scrape_replies(twitter_handle)
    return res
    # https://twitter.com/BrianMteleSUR/status/1625111883626823681
