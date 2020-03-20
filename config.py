import os

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_DIR = os.path.dirname(__file__)


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BaseConfig.BASE_DIR, 'dreamteam_db.sqlite3')


class ProductionConfig(BaseConfig):
    DEBUG = False

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test':TestConfig
}
