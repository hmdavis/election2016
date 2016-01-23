import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CANDIDATES = {
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