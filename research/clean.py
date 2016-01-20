import csv

CANDIDATES = []
path = "./history/"


for line in open('./oldest.txt', 'r'):
    candidate, oldest = line.split(",")
    CANDIDATES.append(candidate)
for candidate in CANDIDATES:
    cleaned_lines = []
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
            cleaned_lines.append([l[0], l[1], tweet])
        except Exception:
            cleaned_lines[-1][2] = cleaned_lines[-1][2] + " " + line.strip()
            continue

    fw = "%s%s_tweets.csv" % (path, candidate)
    with open(fw, 'wb') as f:
        for a, b, c in cleaned_lines:
            f.write("%s,%s,%s\n" % (a.strip(),b.strip(),c.strip()))

