release: python pythonie/manage.py migrate --settings=pythonie.settings.production
web: gunicorn --chdir pythonie pythonie.wsgi --log-file -
