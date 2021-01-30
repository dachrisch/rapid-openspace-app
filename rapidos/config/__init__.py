# https://hackersandslackers.com/configure-flask-applications/
import os


class BaseConfig(object):
    RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    @classmethod
    def config_string(cls):
        return f'{cls.__module__}.{cls.__name__}'
