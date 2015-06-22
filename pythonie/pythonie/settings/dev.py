from .base import *


DEBUG = True
TEMPLATE_DEBUG = True

SECRET_KEY = '1185a082-7e72-449e-bf43-12d2da59222b'  # Just for dev
MEETUP_KEY = ''  # Put your own key here. See https://secure.meetup.com/meetup_api/key/

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# SQLite (simplest install)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(PROJECT_ROOT, 'db.sqlite3'),
    }
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }


try:
    from .local import *
except ImportError:
    pass
