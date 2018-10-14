from flask import Flask
from config import config_dict
from flask_session import Session
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler
import redis
import logging


def create_app(config_name='develop'):
    app = Flask(__name__)
    config_obj = config_dict.get(config_name)
    log_file(config_obj.LEVEL)
    app.config.from_object(config_obj)
    redis_store = redis.StrictRedis(host=config_obj.REDIS_HOST, port=config_obj.REDIS_PORT, decode_responses=True)
    db = SQLAlchemy(app)
    CSRFProtect(app)
    Session(app)

    return app, db, redis_store


def log_file(log_level):
    # 设置日志的记录等级,常见等级有: DEBUG < INFO < WARING < ERROR
    logging.basicConfig(level=log_level)
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler('logs/log', maxBytes=1024*1024*100, backupCount=1)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s: %(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
