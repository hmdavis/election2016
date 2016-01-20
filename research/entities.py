import nltk
import string
import operator
import timefreq

""" Identify people, places, and hashtags - eventually incoporate time? """


def format_special(word, symbol):
    return symbol + word[1:].strip().translate(string.maketrans("", ""), string.punctuation)

all_tweets = timefreq.load_tweets_by_time()

for candidate, tweets in all_tweets.iteritems():
    tweets = timefreq.get_tweets_by_time(all_tweets, candidate, 2016, 1)
    hashtags = []
    users = []
    for tweet in tweets:
        new_hashtags = [format_special(word, '#') for word in tweet.split() if word.startswith('#')]
        new_users = [format_special(word, '@') for word in tweet.split() if word.startswith('@') and word[1:].lower() != candidate]
        hashtags.extend(new_hashtags)
        users.extend(new_users)

    top_hashtags = {}
    top_users = {}

    for hashtag in hashtags:
        if hashtag not in top_hashtags: top_hashtags[hashtag] = 0
        top_hashtags[hashtag] += 1

    for user in users:
        if user not in top_users: top_users[user] = 0
        top_users[user] += 1

    print "\tHashtags:"
    for ht, cnt in sorted(top_hashtags.items(), key=operator.itemgetter(1), reverse=True)[:10]:
        print "\t\t* %s [%s]" % (ht, cnt)
    print "\tUsers:"
    for usr, cnt in sorted(top_users.items(), key=operator.itemgetter(1), reverse=True)[:10]:
        print "\t\t* %s [%s]" % (usr, cnt)


