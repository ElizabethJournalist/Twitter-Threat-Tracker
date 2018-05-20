import tweepy
import re
import csv
import sys

from pathlib import Path

consumer_key = ""
consumer_secret = ""
token_key = ""
token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(token_key, token_secret)
api = tweepy.API(auth)

tweets_file_name = 'CVE_tweets.csv'
twitter_data_filename = 'raw_twitter_data.txt'

def process_status(status):
    p = re.compile(r'CVE-\d{4}-\d{4,7}')
    cve_matches = p.findall(status.text)

    for cve in cve_matches:
        if hasattr(status, 'retweeted_status'):
            retweeted_text = status.retweeted_status.text.encode('utf-8')
        else:
            retweeted_text = ""

        print(cve)
        print(cve, status.text.encode('utf-8'), status.user.screen_name, status.created_at, status.user.friends_count,
              status.user.followers_count, retweeted_text)

        with open(tweets_file_name, 'a', encoding="utf8") as f:
            writer = csv.writer(f)
            writer.writerow([cve, status.text.encode('utf-8'), status.user.screen_name, status.created_at,
                             status.user.friends_count, status.user.followers_count, retweeted_text])

def write_data(data):
    with open(twitter_data_filename, 'a', encoding="utf8") as twitter_data_file:
        twitter_data_file.write(data)

#override tweepy.StreamListener to add logic to on_status
class CustomStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        print("DATA: " + data)
        write_data(data)
        return True

    def on_status(self, status):
        print("STATUS: " + status)
        process_status(status)
        return True

    def on_error(self, status_code):
        print(sys.stderr, "Encountered error with status code:", status_code)
        return True  # Don't kill the stream

    def on_timeout(self):
        print(sys.stderr, 'Timeout...')
        return True  # Don't kill the stream


# Writing csv titles, if the tweet file does not already exist
my_file = Path(tweets_file_name)
if my_file.is_file() == False:
    with open(tweets_file_name, 'a', encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerow(['cve','text','user', 'tweet_time', 'friends_count', 'followers_count', 'in_reply_to_status_id'])


# Read CSV Values

# Get previous CVE Tweets
for status in tweepy.Cursor(api.search,
                           q="cve",
                           rpp=100,
                           #result_type="recent",
                           include_entities=True,
                           lang="en").items():

    process_status(status)

# Get new CVE Tweets
myStreamListener = CustomStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['CVE'])
