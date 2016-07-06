from pythonie.settings.configure import configure_redis
from .base import *  # flake8: noqa

DEBUG = True

SECRET_KEY = '1185a082-7e72-449e-bf43-12d2da59222b'  # Just for dev
MEETUP_KEY = ''  # Put your own key here.
# See https://secure.meetup.com/meetup_api/key/

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# SQLite (simplest install)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(PROJECT_ROOT, 'db.sqlite3'),
    }
}

LOGGING.update({
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
        'pythonie': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
        'meetups': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
        'sponsors': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
        'speakers': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
        'core': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
    }})

REDIS = configure_redis(None, test=True)
