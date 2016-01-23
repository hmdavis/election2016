import operator
from collections import defaultdict

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

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

def get_entities(tweets):
    tokenizer = RegexpTokenizer(r'[\w#@\']+')
    hashtags = defaultdict(int)
    users = defaultdict(int)
    states = defaultdict(int)
    entities = {}
    tf = defaultdict(float)
    df = defaultdict(float)
    n = 0.0
    for tweet in tweets:
        twt = tweet.body
        n += 1
        twt = twt.strip().lower()
        # twt = twt.decode('utf-8').strip().lower()
        seen = set([])
        sentences = nltk.sent_tokenize(twt)
        for sentence in sentences:
            tokens = tokenizer.tokenize(sentence)
            for token in tokens:
                if token in stopwords.words('english') or token in custom_stopwords:
                    continue
                if token.startswith('@'):
                    users[token.replace("'s", "")] += 1
                if token.startswith('#'):
                    hashtags[token] += 1
                if token.upper() in abbrev_to_state or token.title() in state_to_abbrev:
                    if token.title() in state_to_abbrev:
                        name = token.title()
                    else:
                        name = abbrev_to_state[token.upper()].title()
                    states[name] += 1
                if token not in seen:
                    seen.add(token)
                    df[token] += 1
                tf[token] += 1

    top_tokens = sorted(tf.items(), key=lambda x: -x[1])[:10]
    top_hashtags = sorted(hashtags.items(), key=operator.itemgetter(1), reverse=True)[:10]
    top_users = sorted(users.items(), key=operator.itemgetter(1), reverse=True)[:10]
    top_states = sorted(states.items(), key=operator.itemgetter(1), reverse=True)[:10]

    return top_tokens, top_hashtags, top_users, top_states

