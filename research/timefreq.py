import pprint

path = "./history/"
CANDIDATES = []


def insert_tweet(d, year, month, day, tweet):
    year = int(year)
    month = int(month)
    day = int(day)
    if year not in d:
        d[year] = {}
    if month not in d[year]:
        d[year][month] = {}
    if day not in d[year][month]:
        d[year][month][day] = []
    d[year][month][day].append(tweet)


def load_tweets_by_time():
    d = {}
    for line in open('./oldest.txt', 'r'):
        candidate, oldest = line.split(",")
        CANDIDATES.append(candidate)
    for candidate in CANDIDATES:
        print "Loading %s..." % candidate
        # Read the text
        tweets_by_date = {}
        fn = "%s%s_tweets.csv" % (path, candidate)
        for line in open(fn, 'r'):
            try:
                l = line.split(',')
                tweet_id = l[0]
                date = l[1].split()[0]
                tweet = ",".join(l[2:]).strip()
                year, month, day = date.split('-')
            except IndexError:
                print line
                continue
            except ValueError:
                continue
            insert_tweet(tweets_by_date, year, month, day, tweet)
        d[candidate.lower()] = tweets_by_date
    return d


def get_tweets_by_time(tweetdict, candidate, year=None, month=None, day=None):
    if (day is not None and (month is None or year is None)) or (month is not None and year is None):
        print "Invalid date"
        return []
    if candidate.lower() not in tweetdict:
        print "Invalid candidate name"
        return []
    twts = []

    msg = "Getting %s tweets for " % (candidate)

    d = tweetdict[candidate.lower()]

    try:
        if day is not None:
            print msg + "%s-%s-%s..." % (year, month, day)
            twts.extend(d[year][month][day])
        elif month is not None:
            print msg + "%s-%s..." % (year, month)
            for day, tweets in d[year][month].iteritems():
                twts.extend(tweets)
        elif year is not None:
            print msg + "%s..." % year
            for month, day in d[year].iteritems():
                for d, tweets in day.iteritems():
                    twts.extend(tweets)
        else:
            print msg + "all time periods..."
            for year, month in d.iteritems():
                for m, day in month.iteritems():
                    for d, tweets in day.iteritems():
                        twts.extend(tweets)
        return twts
    except KeyError:
        print "Invalid date: %s-%s-%s" % (year, month, day)
        return []

