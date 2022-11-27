from datetime import datetime
import twint  # pip install twint
# pip3 install --user --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint

# TODO: Do some web scrape to get some twitter handles
url = "https://www.ign.com/wikis/game-companies-on-twitter/Longpages"


def get_user_num_tweets(user):
    c = twint.Config()
    c.Username = user
    c.Store_object = True
    twint.run.Lookup(c)
    user = twint.output.users_list[0]
    return user.tweets


def get_user_join_date(user):
    c = twint.Config()
    c.Username = user
    c.Store_object = True
    twint.run.Lookup(c)
    user = twint.output.users_list[0]
    return user.join_date


def twitter(user, search=None, lang=None):
    c = twint.Config()
    c.Username = user
    c.Search = search
    c.Lang = lang
    c.Since = get_user_join_date(user)
    c.Until = datetime.today().strftime('%Y-%m-%d')
    c.Limit = get_user_num_tweets(user)
    c.Store_object = True
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


def main():
    twits = twitter("katyperry")

    hashtags = get_hashtags(twits)
    for hashtag in hashtags:
        print(hashtag)


if __name__ == '__main__':
    main()
