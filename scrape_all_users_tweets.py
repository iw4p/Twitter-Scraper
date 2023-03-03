from scrape_profile_tweets import scrape_profile_tweets_since_2023
from multiprocessing import Pool

# scrape_profile_tweets_since_2023('ylecun')
# scrape_profile_tweets_since_2023('cathiedwood')
# scrape_profile_tweets_since_2023('taylorlorenz')
# scrape_profile_tweets_since_2023('BarackObama')
# scrape_profile_tweets_since_2023('alikarimi_ak8')
# scrape_profile_tweets_since_2023('elonmusk')
# print(res)

def functionToRunParallely(i):
    return i

noOfPools = 5

if __name__ == "__main__":
    with Pool(noOfPools) as p:
        p.map(scrape_profile_tweets_since_2023,['elonmusk',])
