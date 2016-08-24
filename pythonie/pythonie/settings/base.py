"""
Django settings for pythonie project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import os
from os.path import abspath, dirname, join

import dj_database_url

# Absolute filesystem path to the Django project directory:
PROJECT_ROOT = dirname(dirname(dirname(abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['.herokuapp.com', '.python.ie', 'next.python.ie', '127.0.0.1']

# Base URL to use when referring to full URLs within the Wagtail admin backend-
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://python.ie'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'compressor',
    'taggit',
    'modelcluster',

    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailsites',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsearch',
    'wagtail.wagtailredirects',
    'wagtail.wagtailforms',

    'wagtailnews',
    'wagtail.contrib.wagtailstyleguide',
    'core',
    'storages',
    'blog',

    'wagtailfontawesome',

    'meetups',
    'sponsors',
    'speakers',
    # 'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(levelname)s %(asctime)s %(module)s:%(lineno)s '
                       '%(funcName)s %(message)s')
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'pythonie': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'meetups': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'sponsors': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'speakers': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'core': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
    },
}

ROOT_URLCONF = 'pythonie.urls'
WSGI_APPLICATION = 'pythonie.wsgi.application'

MEETUP_KEY = os.getenv('MEETUP_KEY')

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


DATABASES = {}

DATABASES['default'] = dj_database_url.config()

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MEDIA_ROOT = join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

# Django compressor settings
# http://django-compressor.readthedocs.org/en/latest/settings/

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# # Template configuration
# TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
#     'django.core.context_processors.request',
# )
#
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# )
# TEMPLATE_DIRS = (
#     join(PROJECT_ROOT, 'templates'),
#     join(PROJECT_ROOT, 'templates/wagtailembeds'),
# )
# log.debug("Template dirs: {0}".format(TEMPLATE_DIRS))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            'templates',
            'templates/wagtailembeds'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Wagtail settings

WAGTAIL_SITE_NAME = "pythonie"

# Use Elasticsearch as the search backend for extra performance and better
# search results:
# http://wagtail.readthedocs.org/en/latest/howto/performance.html#search
# http://wagtail.readthedocs.org/en/latest/core_components/\
# search/backends.html#elasticsearch-backend
#
# WAGTAILSEARCH_BACKENDS = {
#     'default': {
#         'BACKEND': ('wagtail.wagtailsearch.backends.elasticsearch.'
#                     'ElasticSearch'),
#         'INDEX': 'pythonie',
#     },
# }


# Whether to use face/feature detection to improve image cropping -
# requires OpenCV
WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = False

MEETUPS_LAST_CHECKED = 'meetups_last_checked'
