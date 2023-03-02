from twitter_scraper_selenium import scrape_keyword

def scrape_profile_tweets_since_2023(username: str):
    kword = "from: " + username
    tweets = scrape_keyword(keyword=kword, browser="chrome", tweets_count=3200, output_format="json", filename="BarackObamaHead", until="2023-03-02", since="2023-01-01")
    return tweets