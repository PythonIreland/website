"""Django settings for the upgrade check.

Extends the dev settings, but points to the disposable PostgreSQL container
started by run.sh and keeps media/static files inside the run directory.
"""

import os

from pythonie.settings.dev import *

RUN_DIR = os.environ["UPGRADE_CHECK_DIR"]
SERVER_PORT = os.environ.get("UPGRADE_CHECK_SERVER_PORT", "18000")

# DEBUG off by default to mimic production (WhiteNoise, compressor, manifest).
DEBUG = os.environ.get("UPGRADE_CHECK_DEBUG", "0") == "1"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "pythonie",
        "USER": "postgres",
        "PASSWORD": "pythonie",
        "HOST": "127.0.0.1",
        "PORT": os.environ.get("UPGRADE_CHECK_PG_PORT", "15432"),
    }
}
MEDIA_ROOT = os.path.join(RUN_DIR, "media")
STATIC_ROOT = os.path.join(RUN_DIR, "static")
ROOT_URLCONF = "upgrade_check_urls"
WAGTAILADMIN_BASE_URL = f"http://127.0.0.1:{SERVER_PORT}"
