# Modified script by Victor Reyes

import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime

# Initializing variables
tweets_list = []
search_terms = ["kadamay komunista", "kadamay communist", "kadamay npa", "kadamay magnanakaw ng bahay", "kadamay skwater"]
user = "kurimaw"
research_topic = "Red-tagging of Kadamay"

years = [
    "2016",
    "2017",
    "2018",
    "2019",
    "2020",
    "2021",
    "2022"
]

months = [
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12"
]

end_of_month_days = [
    "31",
    "28",
    "31",
    "30",
    "31",
    "30",
    "31",
    "31",
    "30",
    "31",
    "30",
    "31"
]

# Initializing data frame
df = pd.DataFrame(columns=[
    "Timestamp", "Collector", "Topic", "Keywords",
    "Account Handle", "Account Name", "Account Bio", "Account Type", "Joined", "Following", "Followers", "Location",
    "Tweet", "Tweet Type", "Date Posted", "Tweet URL", "Screenshot", "Content Type", "Likes", "Replies", "Retweets",
    "Rating", "Reasoning", "Other Data"
])

# Using TwitterSearchScraper to scrape data and append tweets to list
for search_term in search_terms:
    for year in years:
        for month in range(len(months)):
            print(f"Starting with {year}-{months[month]}-01")
            for i, tweet in enumerate(
                    sntwitter.TwitterSearchScraper(f'{search_term} since:{year}-{months[month]}-01 until:{year}-{months[month]}-{end_of_month_days[month]}').get_items()):
                if i >= 300:
                    break

                # Populating fields
                df2 = {
                    "Timestamp": [datetime.date.today()],
                    "Collector": [user],
                    "Topic": [research_topic],
                    "Keywords": [search_term],
                    "Account Handle": [tweet.user.username],
                    "Account Name": [tweet.user.displayname],
                    "Account Bio": [tweet.user.rawDescription],
                    "Joined": [tweet.user.created],
                    "Following": [tweet.user.friendsCount],
                    "Followers": [tweet.user.followersCount],
                    "Location": [tweet.user.location],
                    "Tweet": [tweet.rawContent],
                    "Date Posted": [tweet.date],
                    "Tweet URL": [tweet.url],
                    "Likes": [tweet.likeCount],
                    "Replies": [tweet.replyCount],
                    "Retweets": [tweet.retweetCount],
                }

                df = pd.concat([df, pd.DataFrame.from_records(df2)])
            print(f"Done with {year}-{months[month]}-{end_of_month_days[month]}")

    df.to_csv(f'term_{search_term}.csv')

# patulong sa pagconvert
df['Date Posted'] = df['Date Posted'].dt.tz_convert('Etc/GMT+8')

print("Done.")
