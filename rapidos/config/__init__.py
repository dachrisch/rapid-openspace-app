# https://hackersandslackers.com/configure-flask-applications/


class DevelopmentConfig(object):
    DEBUG = True
    TESTING = True

    @property
    def config_string(self):
        return f'{self.__class__.__module__}.{self.__class__.__name__}'
