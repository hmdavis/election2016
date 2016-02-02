import operator
from collections import defaultdict

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

import timefreq

abbrev_to_state = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "Washington D.C.",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VI": "Virgin Islands",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}

state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Puerto Rico": "PR",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virgin Islands": "VI",
    "Virginia": "VA",
    "Washington D.C.": "DC",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}

custom_stopwords = ['co', 't', 'http', 'https', 'amp', 'rt', 'tco']
all_tweets = timefreq.load_tweets_by_time()

tokenizer = RegexpTokenizer(r'[\w#@\']+')
for candidate, tweets in all_tweets.iteritems():
    tweets = timefreq.get_tweets_by_time(all_tweets, candidate, 2016, 01)
    hashtags = defaultdict(int)
    users = defaultdict(int)
    states = defaultdict(int)
    entities = {}
    tf = defaultdict(float)
    df = defaultdict(float)
    n = 0.0
    for tweet in tweets:
        n += 1
        tweet = tweet.decode('utf-8').strip().lower()
        seen = set([])
        sentences = nltk.sent_tokenize(tweet)
        for sentence in sentences:
            tokens = tokenizer.tokenize(sentence)
            for token in tokens:
                if token in stopwords.words('english') or token in custom_stopwords:
                    continue
                if token.startswith('@'):
                    users[token.replace("'s", "")] += 1
                elif token.startswith('#'):
                    hashtags[token] += 1
                elif token.upper() in abbrev_to_state or token.title() in state_to_abbrev:
                    if token.title() in state_to_abbrev:
                        name = token.title()
                    else:
                        name = abbrev_to_state[token.upper()].title()
                    states[name] += 1
                else:
                    if token not in seen:
                        seen.add(token)
                        df[token] += 1
                    tf[token] += 1

    print "\tFound %s tweets..." % n
    print "\tTokens:"
    for t, score in sorted(tf.items(), key=lambda x: -x[1])[:10]:
        print "\t\t* %s [%s]" % (t, score)
    print "\tHashtags:"
    for ht, cnt in sorted(hashtags.items(), key=operator.itemgetter(1), reverse=True)[:10]:
        print "\t\t* %s [%s]" % (ht, cnt)
    print "\tUsers:"
    for usr, cnt in sorted(users.items(), key=operator.itemgetter(1), reverse=True)[:10]:
        print "\t\t* %s [%s]" % (usr, cnt)
    print "\tStates:"
    for st, cnt in sorted(states.items(), key=operator.itemgetter(1), reverse=True)[:10]:
        print "\t\t* %s [%s]" % (st, cnt)


