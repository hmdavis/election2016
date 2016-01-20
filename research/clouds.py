from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import string
import re
from PIL import Image
import numpy as np
import os


def normalize(s):
    return word.strip().lower().translate(string.maketrans("", ""), string.punctuation)


def get_candidate_image(candidate):
    f = "./images/%s.jpg" % candidate
    if os.path.isfile(f):
        return f
    else:
        return ""


path = "./history/"
CANDIDATES = []
FILTER_WORDS = ['rt', 'co', 'tco', 't', 'c', 'amp']

for line in open('./oldest.txt', 'r'):
    candidate, oldest = line.split(",")
    CANDIDATES.append(candidate)

print "Candidates:", CANDIDATES

for candidate in CANDIDATES:
    print candidate

    # Read the text
    fn = "%s%s_tweets.csv" % (path, candidate)
    tweets = []
    for line in open(fn, 'r'):
        l = line.split(',')
        tweet = ",".join(l[2:]).strip()
        tweets.append(tweet)

    text = " ".join(tweets)

    no_urls_no_tags = " ".join([re.sub('ies$', 'y', word) for word in text.split()
                                if 'http' not in word
                                and not word.startswith('@')
                                and normalize(word) not in FILTER_WORDS
                                and len(normalize(word)) > 1
                                ])

    img_path = get_candidate_image(candidate)
    if img_path is "":
        continue
    else:
        coloring = np.array(Image.open(img_path))

        # take relative word frequencies into account, lower max_font_size
        wordcloud = WordCloud(
                font_path='./fonts/HighVoltageRough.ttf',
                # max_font_size=40,
                relative_scaling=.5,
                stopwords=STOPWORDS,
                background_color='white',
                mask=coloring
        )

        wordcloud.generate(no_urls_no_tags)
        image_colors = ImageColorGenerator(coloring)
        plt.figure()
        plt.imshow(wordcloud.recolor(color_func=image_colors))
        plt.axis("off")
        plt.title("@" + candidate)
        plt.show()

        break
