from os import environ

import datetime
import random
import tweepy

import OEISEntry

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

# Load all of the numbers from our raw list
numbers = [ ];

f = open("rawlist.txt", "r")
for line in f:
    number  = line.split(" ", 1)[0]
    numbers.append(number.strip())
f.close()

# Shuffle the numbers deterministically
random.Random(7).shuffle(numbers)

# Find our slot in the list of shuffled numbers
start = datetime.datetime(2020, 11, 26, hour=10)
now   = datetime.datetime.now()
delta = now - start
hours = int(delta.seconds / 60 / 60 / 6)

# Generate a tweet for the number we picked
tweet = OEISEntry.OEISEntry(numbers[hours]).tweetify()

# Set up our twitter account
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# Tweet the tweet
api.update_status(status=tweet)

print(tweet)
print(len(tweet))
