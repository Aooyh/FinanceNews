from flask import Flask
from flask_script import Manager
from flask_session import Session
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import MigrateCommand, Migrate
import redis


class AppConfig(object):
    DEBUG = True
    SECRET_KEY = 'dkdjlkafj33-49$34'

    # session config
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis()

    # mysql config
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:5998381@localhost:3306/finnews_pro'
    SQLALCHEMY_TRACK_MODIFICATION = False


app = Flask(__name__)
db = SQLAlchemy(app)
CSRFProtect(app)
Session(app)
manager = Manager(app)
Migrate(app, db)
manager.add_command('dbc', MigrateCommand)


if __name__ == '__main__':
    app.run(debug=True)
