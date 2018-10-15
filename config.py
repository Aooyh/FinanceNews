import redis
import logging


class AppConfig(object):
    DEBUG = True
    SECRET_KEY = 'dkdjlkafj33-49$34'
    LEVEL = logging.DEBUG

    # redis config
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # session config
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 2

    # mysql config
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:5998381@localhost:3306/finnews_pro'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopConfig(AppConfig):     # config on develop scheme
    pass


class ProductConfig(AppConfig):     # config on product scheme
    LEVEL = logging.ERROR
    DEBUG = False


class TestingConfig(AppConfig):     # config on testing scheme  
    TESTING = True


# Entrance for other files
config_dict = {
    'develop': DevelopConfig,
    'product': ProductConfig,
    'testing': TestingConfig
}
