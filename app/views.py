from flask import render_template
from app import app
from models import Candidate


@app.route('/')
@app.route('/index')
def index():
    candidate = Candidate.query.filter_by(handle='hotmdog').first()
    tweets = [
        {
            'timestamp': '2016-01-01',
            'body': 'Hanging around Iowa right now!'
        },
        {
            'timestamp': '2016-01-02',
            'body': "can't wait for the #GOPDebate"
        }
    ]
    return render_template('index.html',
                           title='Candidate Tweets',
                           candidate=candidate,
                           tweets=tweets)
