from app import db

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(64), index=True, unique=True)
    party = db.Column(db.String(64), index=True)
    tweets = db.relationship('Tweet', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<(%s) %s>' % (self.party, self.handle)


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweetid = db.Column(db.BigInteger)
    body = db.Column(db.String(140, convert_unicode=True))
    timestamp = db.Column(db.DateTime)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))

    def __repr__(self):
        return '<[@%s]%s:\t%s>' % (self.author.handle, self.timestamp, self.body)