import datetime
import os

from dateutil.relativedelta import relativedelta
from flask import render_template

from app import app
from config import basedir
from entities import get_entities
from models import Candidate, Tweet


def get_tweets_by_date(handle, year, month, day):
    if day is not None:
        date = "%s/%s/%s" % (year, month, day)
        lower_bound = datetime.date(int(year), int(month), int(day))
        upper_bound = lower_bound + relativedelta(days=1)
    elif month is not None:
        date = "%s/%s" % (year, month)
        lower_bound = datetime.date(int(year), int(month), 1)
        upper_bound = lower_bound + relativedelta(months=1)
    elif year is not None:
        date = "%s" % year
        lower_bound = datetime.date(int(year), 1, 1)
        upper_bound = lower_bound + relativedelta(years=1)
    else:
        date = ""
    candidate = Candidate.query.filter_by(handle=handle).first()
    if date != "":
        tweets = candidate.tweets.filter(Tweet.timestamp >= lower_bound, Tweet.timestamp < upper_bound).all()
    else:
        tweets = candidate.tweets.all()
    return candidate, tweets, date


@app.route('/')
@app.route('/index')
def index():
    candidates = Candidate.query.all()
    return render_template('index.html',
                           title='Candidates',
                           candidates=candidates,
                           basedir=basedir)

@app.route('/candidate/<handle>')
def candidate(handle):
    candidate = Candidate.query.filter_by(handle=handle).first()
    return render_template('candidate.html',
                           title=handle,
                           candidate=candidate)

@app.route('/tweets/<handle>')
@app.route('/tweets/<handle>/<year>')
@app.route('/tweets/<handle>/<year>/<month>')
@app.route('/tweets/<handle>/<year>/<month>/<day>')
def tweets(handle, year=None, month=None, day=None):
    candidate, tweets, date = get_tweets_by_date(handle, year, month, day)
    return render_template('tweets.html',
                           title='Candidate Tweets',
                           candidate=candidate,
                           date=date,
                           tweets=tweets)


@app.route('/entities/<handle>')
@app.route('/entities/<handle>/<year>')
@app.route('/entities/<handle>/<year>/<month>')
@app.route('/entities/<handle>/<year>/<month>/<day>')
def entities(handle, year=None, month=None, day=None):
    candidate, tweets, date = get_tweets_by_date(handle, year, month, day)
    top_tokens, top_hashtags, top_users, top_states = get_entities(tweets)
    entities = {
        "Top Tokens": top_tokens,
        "Top Hashtags": top_hashtags,
        "Top Users": top_users,
        "Top States": top_states
    }
    return render_template('entities.html',
                           title='Candidate Entities',
                           candidate=candidate,
                           date=date,
                           entities=entities)