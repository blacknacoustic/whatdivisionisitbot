import base64
import time
from datetime import datetime
import tweepy
import requests
import os

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

repo_owner = 'blacknacoustic'
repo_name = 'whatdivisionisitbot'
file_path = 'currentdivision.txt'
access_token = os.environ['ACCESS_TOKEN1']


# Set the base URL of the file you want to update
base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'

# Set the headers for the request
headers = {
    'Authorization': f'token {access_token}',
    'Content-Type': 'application/json'
}

# Send a GET request to the GitHub API
response = requests.get(base_url, headers=headers)

# Check the status code of the response
if response.status_code == 200:
    # The request was successful
    print("Request successful!")
elif response.status_code == 404:
    # The file was not found
    print("File not found.")
elif response.status_code == 401:
    # You don't have sufficient permissions to access the file
    print("Permission denied.")

# Create the list of items
items = ["HW/LHW", "Feather and Lightweight", "All womens divs", "Fly and Bantam", "Middle and Welter"]

# Initialize the index to 0
index = 0

# Encode the data as a base64 string
content = f"{index}\n{items[index]}"
content_bytes = content.encode('utf-8')
encoded_content = base64.b64encode(content_bytes).decode('utf-8')

# Update the data with the encoded content
data['content'] = encoded_content

# Send a PUT request to update the file
response = requests.put(base_url, json=data, headers=headers)

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
        
        # Encode the data as a base64 string
        content = f"{index}\n{items[index]}"
        content_bytes = content.encode('utf-8')
        encoded_content = base64.b64encode(content_bytes).decode('utf-8')

        # Update the data with the encoded content
        data['content'] = encoded_content

        # Send a PUT request to update the file
        response = requests.put(base_url, json=data, headers=headers)
    
        # Open the file for writing
        file = open(file_path, 'r')

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
