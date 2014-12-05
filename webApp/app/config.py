import os


class Config(object):
    ''' Default Config Object '''
    DEBUG = False
    TESTING = False
    PORT = int(os.environ.get('PORT', 5000))

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    '''Production Config Object'''
    pass


class DevelopmentConfig(Config):
    '''Development Config Object'''
    DEBUG = True
    MONGODB_SETTINGS = {'DB': "flask-jumpstart"}

class TestingConfig(Config):
    '''Testing Config Object'''
    TESTING = True

config = {
        'default': DevelopmentConfig,
        'production': ProductionConfig,
        'development': DevelopmentConfig,
        'testing': TestingConfig
        }
