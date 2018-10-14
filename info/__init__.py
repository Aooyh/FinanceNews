from flask import Flask
from config import config_dict
from flask_session import Session
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import redis


def create_app(config_name):
    app = Flask(__name__)
    config_obj = config_dict.get(config_name)
    app.config.from_object(config_obj)
    redis_store = redis.StrictRedis(host=config_obj.REDIS_HOST, port=config_obj.REDIS_PORT, decode_responses=True)
    db = SQLAlchemy(app)
    CSRFProtect(app)
    Session(app)

    return app, db, redis_store
