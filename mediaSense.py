#----Project MediaSense----#
#----Author: Abdullah Ahmad----#
#----Contact: abdullah.engg.amu@gmail.com----#

#----How to use----#
#----Running the file asks to open a csv----csv should contain 4 columns in the format: hashtag string, date since, date until, username----date format is YYYY-MM-DD----when month or day is single digit, don't prefix 0----#
#----Returns 2 csv files, one for tweets and associated sentiments for given hashtag strings, the other containing tweets from given username account----#
#----Also returns a wordcloud of terms used in tweets from accounts corresponding to the given username column----#

import twint
import tweepy
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tkinter
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

def create_wordcloud(df, imagename):
    comment_words = ' '
    stopwords = set(STOPWORDS)

    # iterate through the csv file
    for val in df.tweet:
        # typecaste each val to string
        val = str(val)

        # split the value
        tokens = val.split()

        # Converts each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()

    for words in tokens:
        comment_words = comment_words + words + ' '

    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=10).generate(comment_words)

    # plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    imagename = imagename.replace('.csv','.jpeg')
    plt.savefig(imagename, bbox_inches='tight')

def getfilenamefromhashtagstring(hashtagstring):
    filename = str(str.split(hashtagstring)[0].replace('#','')+'.csv')

    return filename

def twintScraperuser(username, since, until):
    d = twint.Config()
    d.Username = username
    d.Since = since
    d.Until = until
    d.User_full = True
    d.Stats = True
    d.Pandas = True
    d.Store_csv = True
    d.Output = getfilenamefromhashtagstring(username)
    twint.run.Search(d)
    Tweets_df_user = twint.storage.panda.Tweets_df

    return Tweets_df_user


def twintScraperhashtag(hashtagstring, username, since, until):
    c = twint.Config()
    hashtagstring_without_user = hashtagstring + '-from:' + username
    c.Search = hashtagstring_without_user
    c.Since = since
    c.Until = until
    c.User_full = True
    c.Show_hashtags = True
    c.Stats = True
    c.Pandas = True
    c.Store_csv = True
    c.Output = getfilenamefromhashtagstring(hashtagstring)
    twint.run.Search(c)
    Tweets_df = twint.storage.panda.Tweets_df
    users = Tweets_df['username']
    count = users.size

    return Tweets_df, users, count

def tweepy_follower_count(consumer_key, consumer_secret, access_token, access_token_secret, users):
    c_key = consumer_key
    c_secret = consumer_secret
    a_token = access_token
    a_token_secret = access_token_secret

    auth = tweepy.OAuthHandler(c_key, c_secret)
    auth.set_access_token(a_token, a_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    follower_count = list([])
    i = users.size
    try:
        for u in users:
            i = i-1
            print('Remaining users: '+str(i), 'Current User: '+str(u))
            usr = api.get_user(u)
            follower_count.append(usr.followers_count)
    except tweepy.TweepError:
        time.sleep(120)

    return follower_count

def vader_sentiment(dataframe):
    analyzer = SentimentIntensityAnalyzer()
    dataframe['compound'] = [analyzer.polarity_scores(x)['compound'] for x in dataframe['tweet']]
    dataframe['neg'] = [analyzer.polarity_scores(x)['neg'] for x in dataframe['tweet']]
    dataframe['neu'] = [analyzer.polarity_scores(x)['neu'] for x in dataframe['tweet']]
    dataframe['pos'] = [analyzer.polarity_scores(x)['pos'] for x in dataframe['tweet']]

    return dataframe

#counts tweets for any given date
#def tweet_count_day():

#for given df and tu, creates another column for the tu and adds that tu to this column, then adds to get
#total tweets in that tu for the whole df
#def bin_creator(dataframe, time_unit):
    #(df[column_name].groupby(df[column_name].dt.hour).count())

#counts tweets based on hour, day, month, output goes to input of visualizer
#def tweet_count_classifier():
 #   typ = input('Choose type of count - date or range:')
  #  if typ=='date':
   #     date = input('Enter the date in the format DD:MM:YYYY :')

    #elif typ=='range':
     #   tu = input('Enter the resolution of time - hour, day or month')
      #  rangestart = input('Enter the start of range in the format DD:MM:YYYY :')
       # rangeend = input('Enter the end of range in the format DD:MM:YYYY :')
        #if tu=='hour':
         #   #do hour bins on dataframe and return hourly count in the chosen range
        #elif tu=='day':
         #   # do hour bins on dataframe and return daily count in the chosen range
        #elif tu=='month':
            # do hour bins on dataframe and return monthly count in the chosen range

    #time_elements_list = dataframe['date'].tolist()
    #month = str.split(time_elements_list[0])[1]

    #return


#def visualizer(xdata, ydata, *args):
    #matplotlib based functions for
    #1. no. of tweets vs time vs sentiment with conf as origin 6 months in each direction
    #2. pie chart of before and after conf 6 months in each direction
    #3. cdf of users vs % of tweets
    #4. histogram of

def generate_data():
    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    data = pd.read_csv(file_path)
    cons_key = input('Enter the Consumer Key: ')
    cons_key_secret = input('Enter the Consumer Secret Key: ')
    acc_token = input('Enter the Access Token: ')
    acc_token_secret = input('Enter the Access Token Secret: ')
    for i, row in data.iterrows():
        print(i)
        h = row[0]
        s = row[1]
        u = row[2]
        username = row[3]
        df_user = twintScraperuser(username,s,u)
        df, us, c = twintScraperhashtag(h,username,s,u)
        print('The total number of tweets scraped is: ' + str(c))
        f_count = tweepy_follower_count(cons_key, cons_key_secret, acc_token, acc_token_secret, us)
        df['follower_count'] = np.array(f_count)
        df = vader_sentiment(df)
        df_filename = getfilenamefromhashtagstring(h)
        df_user_filename = getfilenamefromhashtagstring(username)
        create_wordcloud(df_user, df_user_filename)
        df.to_csv(df_filename)
        df_user.to_csv('user_'+df_user_filename)

def main():
    generate_data()

if __name__ == '__main__':
    main()