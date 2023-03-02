from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from time import sleep
import time

target_tweet='https://twitter.com/BarackObama/status/1623489922438156288'

# Twitter Login 
twitter_usr="@your_twitter_username"
twitter_pass='password'

def twitter_login(driver, twitter_usr=str, twitter_pass=str):
    driver.get('https://twitter.com/i/flow/login')
    sleep(6)
    user = driver.find_element(by=By.XPATH, value='//*[@autocomplete="username"]')
    sleep(1)
    user.send_keys(twitter_usr)
    sleep(1)
    next_btn = driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[6]/div')
    next_btn.click()
    sleep(4)
    psswd_in = driver.find_element(by=By.XPATH, value='//*[@autocomplete="current-password"]')
    psswd_in.send_keys(twitter_pass)
    sleep(2)
    login_btn = driver.find_element(by=By.XPATH, value='//html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')
    login_btn.click()
    sleep(3)
    print('Login Successful')
    return driver


# driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
driver = webdriver.Chrome()

# twitter_login(driver, twitter_usr=twitter_usr, twitter_pass=twitter_pass)

tweets = []

driver.get(target_tweet)

sleep(6)

MAX_SCROLLS=5
for _ in range(MAX_SCROLLS):
    last = driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')[-1]
    driver.execute_script("arguments[0].scrollIntoView(true)", last)
    time.sleep(.2)
    all_tweets = driver.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')
    for item in all_tweets[1:]: # skip first tweet because it is BBC tweet
 
            try:
                date = item.find_element(By.XPATH, './/time').text
            except:
                date = '[empty]'

            try:
                text = item.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
            except:
                text = '[empty]'

            try:
                author_handle = item.find_element(By.XPATH, './/div[@data-testid="User-Names"]').text
                
            except:
                author_handle = '[empty]'

            try:
                replying_to = item.find_element(By.XPATH, './/div[contains(text(), "Replying to")]//a').text
            except:
                replying_to = '[empty]'
            
            tweets.append([date, author_handle, replying_to, text])
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
            for item in all_tweets: # skip first tweet because it is BBC tweet

                    try:
                        date = item.find_element(By.XPATH, './/time').text
                    except:
                        date = None

                    try:
                        text = item.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
                    except:
                        text = None

                    try:
                        replying_to = item.find_element(By.XPATH, './/div[contains(text(), "Replying to")]//a').text
                    except:
                        replying_to = None

                    tweets.append([date, replying_to, text])
                    time.sleep(.2)

        print(f'Found {len(tweets)} replies totally.')
        driver.quit()
    except:
        continue

# Example of dataframe construction
import pandas as pd

df = pd.DataFrame(tweets, columns=['Date of Tweet', 'Author', 'Replying to', 'Tweet'])

print(df)