from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from typing import List, Dict
from dataclasses import dataclass
from time import sleep
import time
import re
import json

@dataclass
class Tweet:
    date: str
    author_name_handle: str
    author_id_handle: str
    replying_to: str
    text: str

def scrape_replies(target_tweet: str):
    # target_tweet='https://twitter.com/BrianMteleSUR/status/1625111883626823681'
    
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    # options.add_experimental_option("prefs",{"download.default_directory":"/databricks/driver"})
    driver = webdriver.Chrome(chrome_options=options)

    # driver = webdriver.Chrome()
    tweets = []

    driver.get(target_tweet)
    sleep(6)

    MAX_SCROLLS=5
    for _ in range(MAX_SCROLLS):
        time.sleep(.2)
        last = driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')[-1]
        driver.execute_script("arguments[0].scrollIntoView(true)", last)
        time.sleep(.2)
        all_tweets = driver.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')
        for item in all_tweets[1:]:
    
                try:
                    date = item.find_element(By.XPATH, './/time').text
                except:
                    date = '[empty]'

                try:
                    text = item.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
                except:
                    text = '[empty]'

                try:
                    author_name_handle = item.find_element(By.XPATH, './/div[@data-testid="User-Names"]/div[2]/div/div/a/div/span').text
                except:
                    author_name_handle = '[empty]'

                try:
                    author_id_handle = item.find_element(By.XPATH, './/div[@data-testid="User-Names"]//div//span//span').text
                except:
                    author_id_handle = '[empty]'

                try:
                    replying_to = item.find_element(By.XPATH, './/div[contains(text(), "Replying to")]//a').text
                except:
                    replying_to = '[empty]'
                
                curr_tweet = Tweet(
                    date=date,
                    author_name_handle=author_name_handle,
                    author_id_handle=author_id_handle,
                    replying_to=replying_to,
                    text=text,
                )

                if curr_tweet is not None:
                    tweets.append(curr_tweet)

                time.sleep(.2)
                
    print(f'Found {len(tweets)} replies.')

    # Scraping the replies loaded by the 'load more replies' button, if there are such. 
    #The "load more replies" XPATH changes dinamically and i cannot figure out the mechanics, so for now i'm brute-forcing it.
    # Filling the missing values with None 

    for i in range(20):
        try:
            show_more=driver.find_element(By.XPATH, value=f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[{i}]/div/div/div/div/div/span')
            show_more.click()
            print('Found more replies!')
            for _ in range(MAX_SCROLLS):
                last = driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')[-1]
                driver.execute_script("arguments[0].scrollIntoView(true)", last)
                time.sleep(.2)
                all_tweets = driver.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')
                for item in all_tweets:

                        try:
                            date = item.find_element(By.XPATH, './/time').text
                        except:
                            date = None

                        try:
                            text = item.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
                        except:
                            text = None

                        try:
                            author_name_handle = item.find_element(By.XPATH, './/div[@data-testid="User-Names"]/div[2]/div/div/a/div/span').text
                        except:
                            author_name_handle = '[empty]'

                        try:
                            author_id_handle = item.find_element(By.XPATH, './/div[@data-testid="User-Names"]//div//span//span').text
                        except:
                            author_id_handle = '[empty]'

                        try:
                            replying_to = item.find_element(By.XPATH, './/div[contains(text(), "Replying to")]//a').text
                        except:
                            replying_to = None

                        curr_tweet = Tweet(
                            date=date,
                            author_name_handle=author_name_handle,
                            author_id_handle=author_id_handle,
                            replying_to=replying_to,
                            text=text,
                        )
                        if curr_tweet is not None:
                            tweets.append(curr_tweet)

                        time.sleep(.2)

            print(f'Found {len(tweets)} replies totally.')
            driver.quit()
        except:
            continue
    try:
        outdict = [d.__dict__ for d in tweets]
        unique_tweets = list({each["text"]: each for each in outdict}.values())

        for d in unique_tweets:
            d["date"] = d["date"]
            d["author_id_handle"] = re.sub("[/@]", "", d["author_id_handle"])
            d["author_name_handle"] = d["author_name_handle"]
            d["text"] = d["text"]
            d["replying_to"] = d["replying_to"]
            # d["replying_to"] = d["replying_to"].replace("@" + d["author_name_handle"], "")

        # result = (json.dumps(unique_tweets, indent=4, ensure_ascii=False))
        # print(f"FOUND {len(unique_tweets)} TWEETS")

        output_file = 'alikarimi_ak8' + '.csv'
        # Example of dataframe construction
        import pandas as pd

        df = pd.DataFrame(tweets, columns=['date', 'author_id_handle', 'author_name_handle', 'text', 'replying_to'])
        df.drop_duplicates()
        df.to_csv(output_file, mode='a', index=False, header=False)

        print(df)
        
        # with open(output_file, "w", encoding="utf-8") as f:
        #     json.dump(unique_tweets, f, ensure_ascii=False, indent=4)
    except:
        print("no replies")