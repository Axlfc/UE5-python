import praw
from dotenv import load_dotenv
import os


# Create a function to upvote a post
def upvote_post(reddit, post_id):
    post = reddit.submission(id=post_id)
    post.upvote()


# Create a function to downvote a post
def downvote_post(reddit, post_id):
    post = reddit.submission(id=post_id)
    post.downvote()


# Create a function to submit a new post
def submit_post(reddit, title, body):
    reddit.subreddit('subreddit_name').submit(title, body)


# Create a function to post a comment
def post_comment(reddit, post_id, comment):
    post = reddit.submission(id=post_id)
    post.reply(comment)


# Create a function to scrape data from Reddit
def scrape_data(reddit, subreddit):
    subreddit = reddit.subreddit(subreddit)
    for submission in subreddit.hot(limit=1):
        post_title = submission.title
        post_author = submission.author
        post_comments = submission.comments
        post_upvotes = submission.score
        # Do something with the data
        print(post_title, post_author, post_comments, post_upvotes)


def main():
    load_dotenv()
    # Create a Reddit instance
    reddit = praw.Reddit(client_id=os.environ["REDDIT_API_KEY"],
                         client_secret=os.environ["REDDIT_API_SECRET_KEY"],
                         user_agent=os.environ["REDDIT_USER_AGENT"])

    scrape_data(reddit, "r/afaces")


if __name__ == '__main__':
    main()
