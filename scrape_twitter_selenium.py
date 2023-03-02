import json
import re
from dataclasses import dataclass
from pathlib import Path
from time import sleep, time
from typing import List, Dict

from bs4 import BeautifulSoup
from selenium import webdriver
import argparse


@dataclass
class Tweet:
    text: str
    time: str
    time_tag: str
    author: str
    author_handle: str


def parse(page_source, tweets: List):
    soup = BeautifulSoup(page_source, "html.parser")
    for article in soup.find_all("article"):
        curr_tweet = None
        author_tag = article.find(
            "a",
            class_="css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l",
        )

        text_tag = article.find(
            "div",
            class_="css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0",
        )

        # print('author_tag')
        # print(author_tag)
        # print('text_tag')
        # print(text_tag)

        time_tag = article.find("time")

        if (
            author_tag is not None
            and time_tag is not None
            and text_tag is not None
        ):
            author = author_tag["href"].split("@")[0]
            time_text = time_tag.get_text()
            timestamp = time_tag["datetime"]
            tweet_text = text_tag.get_text()
            author_text = author_tag.get_text()

            # quickfix for fixing scandinavian unicode letters
            author_text = author_text.encode("utf-8")
            tweet_text = tweet_text.encode("utf-8")

            curr_tweet = Tweet(
                author=author_text,
                author_handle=author,
                text=tweet_text,
                time_tag=timestamp,
                time=time_text,
            )

        if curr_tweet is not None:
            tweets.append(curr_tweet)

def main(args:Dict):
    output_file = args["output"]
    url = args["url"]
    print("Starting - loading URL")
    # create a new Firefox session
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    driver.get(url)
    print("Now waiting for some time....")
    # try:
    #     replies_present = EC.presence_of_element_located((By.TAG_NAME, 'article'))
    #     WebDriverWait(driver, 10).until(replies_present)
    # except TimeoutException:
    #     print("Timeoot!")
    #     exit()

    sleep(3)
    tweets = []

    print("Starting scroll")
    # Scroll to bottom to make sure we get all tweets
    pre_scroll_height = driver.execute_script("return document.body.scrollHeight;")
    run_time, max_run_time = 0, 2
    while True:
        iteration_start = time()
        # Scroll webpage, the 100 allows for a more 'aggressive' scroll
        driver.execute_script("window.scrollTo(0, 100*document.body.scrollHeight);")

        post_scroll_height = driver.execute_script(
            "return document.body.scrollHeight;"
        )
        
        scrolled = post_scroll_height != pre_scroll_height
        print(post_scroll_height)
        print(pre_scroll_height)
        print(scrolled)
        timed_out = run_time >= max_run_time
        sleep(7)
        if scrolled:
            run_time = 0
            pre_scroll_height = post_scroll_height
            parse(driver.page_source, tweets)
        elif not scrolled and not timed_out:
            run_time += time() - iteration_start
        elif not scrolled and timed_out:
            break

    parse(driver.page_source, tweets)

    # end the Selenium browser session
    driver.quit()

    # Data cleanup - remove duplicates and clean author names
    outdict = [d.__dict__ for d in tweets]
    unique_tweets = list({each["text"]: each for each in outdict}.values())
    f = open("test.txt", "a")
    # for d in unique_tweets:
    #     f.write(d)

    # remove / from authornames
    for d in unique_tweets:
        d["author"] = d["author"].decode("utf-8")
        d["text"] = d["text"].decode("utf-8")
        d["author_handle"] = re.sub("[/@]", "", d["author_handle"])
        d["author"] = d["author"].replace("@" + d["author_handle"], "")

    print(json.dumps(unique_tweets, indent=4, ensure_ascii=False))
    print(f"FOUND {len(unique_tweets)} TWEETS")

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(unique_tweets, f, ensure_ascii=False, indent=4)


def parse_args():
    parser = argparse.ArgumentParser(description='Scrape all replies from a tweet.')
    parser.add_argument('--url', type=str, default="http://twitter.com/francesarnold/status/1260227823580491776",
                        help='URL to scrape')
    parser.add_argument('--output',
                        default="./output/test.json",
                        type=str,
                        help='File to output JSON to.')

    args = parser.parse_args()
    argdict = vars(args)

    argdict["output"] = Path(argdict["output"])
    argdict["output"].parent.mkdir(exist_ok=True)

    return argdict


if __name__ == '__main__':
    args = parse_args()
    main(args)