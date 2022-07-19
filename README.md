# mediaSense
A comprehensive tool to gather sentiments and market insights from twitter.

Latest Update: Added new file mediaSense.py which implements python functions to read and store tweets based on certain hashtags, and breaks down those tweets, performs sentiment analysis on them. It can also scrape user information and stats such as follower count. Project is based on twint and tweepy libraries for scraping and nltk for natural language processing and sentiment analysis. The tweets can be scraped for a chosen time period.

The current version contains code to scrape tweets based on keywords and/or hashtags, for a given date range.
Further modifications coming including:
- GUI
- Detailed visualization using wordclouds, histograms, moving averages, heatmaps, clusters, trees, etc.
- Customized search such as date range/or specific date and time, location, exclusion of usernames and/or hashtags, etc.
