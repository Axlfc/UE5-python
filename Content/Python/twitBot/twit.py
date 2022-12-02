from datetime import datetime
import twint  # pip install --upgrade --user git+https://github.com/MarcosFP97/twint.git@origin/master#egg=twint
import json
import random
import nest_asyncio
import os

# Just replace this line in twint/user.py:

# _usr.url = ur['data']['user']['legacy']['url']

# to this:

#try:
    #_usr.url = ur['data']['user']['legacy']['url']
#except:
    #_usr.url = ''

nest_asyncio.apply()


def get_quotes():
    with open("quotes.json") as quotes_file:
        quotes = json.load(quotes_file)

    return quotes


def get_random_quote():
    return random.choice(get_quotes())


def form_tweet(quote):
    author = quote["author"].strip(",")
    tweet = f"{quote['quote']} - {author}"

    return tweet


def is_character_valid(tweet):
    return len(tweet) < 280


def get_tweet():
    while True:
        tweet = form_tweet(get_random_quote())
        if is_character_valid(tweet):
            return tweet


def get_name(user):
    c = twint.Config()
    c.Username = user
    c.Store_object = True
    c.Hide_output = True
    twint.run.Lookup(c)
    user = twint.output.users_list[0]

    return user.name


def get_user_num_tweets(user):
    c = twint.Config()
    c.Username = user
    c.Store_object = True
    c.Hide_output = True
    c.Limit = 1
    twint.run.Lookup(c)
    user = twint.output.users_list[0]
    return user.tweets


def get_user_join_date(user):
    c = twint.Config()
    c.Username = user
    c.Store_object = True
    c.Hide_output = True
    c.Limit = 1
    twint.run.Lookup(c)
    user = twint.output.users_list[0]
    return user.join_date


def twitter(user, search=None, lang=None):
    filename = user + ".csv"
    c = twint.Config()
    c.Username = user
    c.Lang = lang
    c.Since = get_user_join_date(user)
    c.Until = datetime.today().strftime('%Y-%m-%d')
    c.Limit = get_user_num_tweets(user)
    c.Store_csv = True
    c.Count = True
    if os.path.exists(filename):
        print('already present :' + user)
    else:
        c.Custom["tweet"] = ["tweet"]
        c.Output = filename
        c.Hide_output = True
        c.Store_object = True
        c.Search = search
        twint.run.Search(c)
        tweets = twint.output.tweets_list

    twits = []

    for tweet in tweets:
        twit = '{}'.format(tweet.tweet)
        twits.append(twit)
    return twits


def get_hashtags(twits):
    hashtags = []
    for tweet in twits:
        if "#" in tweet:
            tweet = tweet.split(" ")
            for word in tweet:
                if "#" in word:
                    word = word.replace(".", "").replace(",", "")
                    if word not in hashtags:
                        hashtags.append(word)
    return hashtags


def get_webpage(user):
    c = twint.Config()
    c.Username = user
    c.Store_object = True
    c.Hide_output = True
    twint.run.Lookup(c)
    usr = twint.output.users_list[0]
    return usr.url


def main():
    # accounts = ["sanchezcastejon", "katyperry"]

    '''for account in accounts:
        twits = twitter(account)    
        print(twits)
    hashtags = get_hashtags(twits)
    for hashtag in hashtags:
        print(hashtag)'''
    # print(get_tweet())


if __name__ == '__main__':
    main()
