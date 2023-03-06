from fastapi import FastAPI
from scrape_profile_tweets import scrape_profile_tweets_since_2023
from scrape_replies import scrape_replies
from groupby import most_mentioned
from replies_sentiment import sentiment_analysis

description = """
Twitter Watch 🚀

## Accounts

You can **read accounts**.

## Tweets

You will be able to:

* **Tweets of the user** (_implemented_).
* **audience: Active users by the number of their mentions** (_implemented_).
* **sentiment: sentiment of each mention** (_implemented_).
* **replies: get the replies of each tweet** (_implemented_).
"""

app = FastAPI(
    title="Twitter Watch",
    description=description,
    version="0.0.1",
    terms_of_service="http://ehemehem.com/terms/",
    contact={
        "name": "Nima Akbarzadeh",
        "url": "http://github.com/iw4p",
        "email": "iw4p@protonmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# - /accounts: return a json list of all tracked accounts.
@app.get("/accounts/")
async def accounts():
    res = {'users': ['alikarimi_ak8', 'BarackObama', 'cathiedwood']}
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
    res = sentiment_analysis(twitter_handle)
    return res

@app.get("/replies/{twitter_handle}")
async def replies(twitter_handle):
    res = scrape_replies(twitter_handle)
    return res
    # example for test: https://twitter.com/BrianMteleSUR/status/1625111883626823681
