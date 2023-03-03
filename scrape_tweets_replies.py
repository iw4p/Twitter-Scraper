from scrape_replies import scrape_replies
from multiprocessing import Pool
import csv

def functionToRunParallely(i):
    return i

noOfPools = 5

def read_tweets_url(csv_f):
    with open(csv_f, 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            tweet_url = dict(row)['tweet_url']
            scrape_replies(tweet_url)

if __name__ == "__main__":
    read_tweets_url('./users/alikarimi_ak8.csv')
    # with Pool(noOfPools) as p:
    #     p.map(scrape_replies,['',])
