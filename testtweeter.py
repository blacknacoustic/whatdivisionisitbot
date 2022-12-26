import base64
import time
from datetime import datetime
import tweepy

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Create the list of items
items = ["HW/LHW", "Feather and Lightweight", "All womens divs", "Fly and Bantam", "Middle and Welter"]

# Initialize the index to 0
index = 2

try:
    tweet = api.update_status("The current division is: {}".format(items[index]))
    print("Tweet successful! Tweet ID: {}".format(tweet.id))
except tweepy.error.TweepError as error:
    print("Error tweeting: {}".format(error))

# Increment the index
index += 1


while True:
    # Get the current time
    now = datetime.now()

    # Check if the current time is a whole hour
    if now.minute == 0 and now.second == 0:

        # Get the user's recent tweets
        recent_tweets = api.get_user_timeline(count=1)

        if recent_tweets:
            api.destroy_status(recent_tweets[0].id)
            print("Tweet Destroyed")

        print("Time check triggered")

        # Tweet the first line of the file
        try:
            tweet = api.update_status("The current division is: {}".format(items[index]))
            print("Tweet successful! Tweet ID: {}".format(tweet.id))
        except tweepy.error.TweepError as error:
            print("Error tweeting: {}".format(error))
        
        # Increment the index, and reset to 0 if we reach the end of the list
        index = (index + 1) % len(items)

    # Sleep for 1 second
    time.sleep(1)
