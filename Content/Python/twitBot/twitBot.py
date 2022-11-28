import os
from dotenv import load_dotenv
import time
import tweepy
import twit as services
import sys
load_dotenv()

API_KEY = os.environ["TWITTER_API_KEY"]
SECRET_KEY = os.environ["TWITTER_API_SECRET_KEY"]
ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

def get_twitter_api():
    auth = tweepy.OAuthHandler(API_KEY, SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth, wait_on_rate_limit=True)


def write_tweet(tweet=None):
    if not tweet:
        tweet = services.get_tweet()

    twitter_api = get_twitter_api()
    twitter_api.update_status(tweet)


def main():
    if not sys.stdin.isatty():
        print("ERROR: twitBot needs at least one argument (twit)")
        exit(1)

    write_tweet(sys.argv[1])


if __name__ == '__main__':
    main()
