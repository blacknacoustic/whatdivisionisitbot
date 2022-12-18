from google.colab import drive
drive.mount('/content/gdrive')

import time
from datetime import datetime
import tweepy

auth = tweepy.OAuthHandler('6KQ17czzJNfrHuMe5ozwegIyy', 'OlEhaAqfIP7XYtfqolfciiGJrBIwHXhyyDNNYrwrgFoKSMNk0P')
auth.set_access_token('1603462800889810955-iTte5qXfBZ1ccMhyfIvyOWewQ70AWl', 'zx9lMCxcX7ytWRVWQJ2nq6Cog6063Y5BWrkZ6R0C0WDHN')

api = tweepy.API(auth)

# Create the list of items
items = ["HW/LHW", "Feather and Lightweight", "All womens divs", "Fly and Bantam", "Middle and Welter"]

# Initialize the index to 0
index = 2

# Open the file for writing
file = open('/content/gdrive/My Drive/ufcdivision/currentdivision.txt', 'w')

# Write the initial item and its array location to the file
file.write("{}\n{}\n".format(items[index], index))

# Close the file
file.close()

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
        # Open the file for writing
        file = open('/content/gdrive/My Drive/ufcdivision/currentdivision.txt', 'w')

        # Write the current item and its array location to the file
        file.write("{}\n{}\n".format(items[index], index))

        # Close the file
        file.close()

        # Open the file for reading
        file = open('/content/gdrive/My Drive/ufcdivision/currentdivision.txt', 'r')

        # Read the first line of the file
        line = file.readline()

        # Close the file
        file.close()

        # Tweet the first line of the file
        try:
            tweet = api.update_status("The current division is: {}".format(line))
            print("Tweet successful! Tweet ID: {}".format(tweet.id))
        except tweepy.error.TweepError as error:
            print("Error tweeting: {}".format(error))
        
        # Increment the index, and reset to 0 if we reach the end of the list
        index = (index + 1) % len(items)

    # Sleep for 1 second
    time.sleep(1)