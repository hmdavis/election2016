import tweepy
import csv
from credentials import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


# Credit: https://gist.github.com/yanofsky/5436496
def get_all_tweets(screen_name, since_id):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    try:
        if since_id <= 0:
            new_tweets = api.user_timeline(screen_name=screen_name, count=200)
        else:
            new_tweets = api.user_timeline(screen_name=screen_name, count=200, since_id=since_id)
    except tweepy.RateLimitError:
        print "Exceeded max API limit!"
        new_tweets = []

    # save most recent tweets
    alltweets.extend(new_tweets)

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print "getting tweets before %s" % (oldest)

        # all subsiquent requests use the max_id param to prevent duplicates
        try:
            if since_id <= 0:
                new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
            else:
                new_tweets = api.user_timeline(screen_name=screen_name, count=200, since_id=since_id, max_id=oldest)
        except tweepy.RateLimitError:
            print "Exceeded max API limit!"
            new_tweets = []

        # save most recent tweets
        alltweets.extend(new_tweets)

        print "...%s tweets downloaded so far" % (len(alltweets))

    alltweets.reverse()

    if len(alltweets) > 0:
        since_id = alltweets[-1].id

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8").replace("\n", " ")] for tweet in alltweets]

    # write the csv
    with open('./history/%s_tweets.csv' % screen_name, 'ab') as f:
        writer = csv.writer(f)
        writer.writerows(outtweets)

    return since_id


CANDIDATES = {}

# get current since_id so you don't duplicate tweets
for line in open('oldest.txt', 'r'):
    candidate, oldest = line.split(",")
    CANDIDATES[candidate] = int(oldest)

print CANDIDATES

# get the tweets since the last data pull
for candidate, oldest in CANDIDATES.iteritems():
    print candidate
    new_oldest = get_all_tweets(candidate, oldest)
    CANDIDATES[candidate] = new_oldest

# write the new since_id to save for later
with open('oldest.txt', 'wb') as f:
    for candidate, oldest in CANDIDATES.iteritems():
        f.write("%s,%s\n" % (candidate, oldest))
