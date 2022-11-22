from logging import INFO


class base_config(object):
    SERVER_NAME = 'localhost:5000'
    SITE_NAME = 'IIS'

    POSTGRES_HOST = 'localhost'
    POSTGRES_PORT = 5432
    POSTGRES_USER = 'iis'
    POSTGRES_PASS = 'chob0t3k'
    POSTGRES_DB   = 'iis'

    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % (
        POSTGRES_USER,
        POSTGRES_PASS,
        POSTGRES_HOST,
        POSTGRES_PORT,
        POSTGRES_DB
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOG_FORMAT = '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    LOG_FILEPATH = 'logfile.log'
    LOG_LEVEL = INFO


class dev_config(base_config):
    DEBUG = True
    ASSETS_DEBUG = True
