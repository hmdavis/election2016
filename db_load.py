from app import db, models
from datetime import datetime

parties = {
    "HillaryClinton": "D",
    "RandPaul": "R",
    "tedcruz": "R",
    "realDonaldTrump": "R",
    "JebBush": "R",
    "CarlyFiorina": "R",
    "BernieSanders": "D",
    "RealBenCarson": "R",
    "ChrisChristie": "R",
    "marcorubio": "R"
}

CANDIDATES = []
for line in open('./research/oldest.txt', 'r'):
    candidate, oldest = line.split(",")
    CANDIDATES.append(candidate)
    party = parties[candidate]
    u = models.Candidate(handle=candidate.lower(), party=party)
    db.session.add(u)

db.session.commit()

for candidate in CANDIDATES:
    print "Loading %s..." % candidate
    # Read the text
    fn = "./research/history/%s_tweets.csv" % (candidate)
    candidate = models.Candidate.query.filter_by(handle=candidate.lower()).first()
    for tweet in open(fn, 'r'):
        t = tweet.split(',')
        tweetid = int(t[0])
        # MAKE SURE THAT THIS TWEET DOESN'T CURRENTLY EXIST
        datetime = datetime.strptime(t[1], '%Y-%m-%d %H:%M:%S')
        body = ','.join(t[2:]).decode('utf-8').strip()
        cid = candidate.id
        x = models.Tweet(tweetid=tweetid, body=body, timestamp=datetime, candidate_id=cid)
        db.session.add(x)
    db.session.commit()
