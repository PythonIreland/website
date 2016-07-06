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

# assumes no DEV:REDISCLOUD_URL available but that redis-server running locally
REDIS_URL = os.environ.get('REDISCLOUD_URL', '//127.0.0.1:6379')
REDIS = configure_redis(REDIS_URL)

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }


try:
    from .local import *  # noqa
except ImportError:
    pass
