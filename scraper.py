import tweepy
import pandas as pd

consumer_key = "fill_this"
consumer_secret = "fill_this"
access_token = "fill_this"
access_token_secret = "fill_this"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

username = ''
count = #fill_this_with_tweet_count_int
devlabel = 'fill_this'
date = 'enter_starting_date'
try:
    # Creation of query method using parameters
    tweets = tweepy.Cursor(api.search_full_archive, environment_name=devlabel, query='enter hashtags here', fromDate=date).items(count)

    # Pulling information from tweets iterable object
    tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]

    # Creation of dataframe from tweets list
    tweets_df = pd.DataFrame(tweets_list)
    tweets_df.to_csv(r'enter_path_here')

except BaseException as e:
    print('failed on_status,', str(e))
