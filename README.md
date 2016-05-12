# website

# Contributing
 - Fork the repository into your own personal github account. 
 - Clone your fork of the repository. `git clone git@github.com:YourGitHubName/website.git`
 - Ensure you are running python 3.4. `python -V` or `python3 -V` should output `Python 3.4.x`
 - Create a virtualenv to isolate the project dependencies. `python3 -m venv pythonie-venv`
 - Activate the virtualenv. `source pythonie-venv/bin/activate`
 - Change into the website directory. `cd website`
 - Install the dependencies. `pip install -r requirements-dev.txt`
 - Set up the database. `python pythonie/manage.py migrate --settings=pythonie.settings.dev`
 - Run the server. `python pythonie/manage.py runserver --settings=pythonie.settings.dev`
 - Check that it works by visiting `http://localhost:8000/` in your browser. (You should see a 'welcome to Wagtail' site, as you will not see content until you've added it in your DB)
 - Create a super user on your local DB. `python pythonie/manage.py createsuperuser --settings=pythonie.settings.dev`
 - Log in to wagtail with your superuser.
 - To get rid of redis errors, install and run redis server locally and set environment variable export REDISCLOUD_URL=127.0.0.1:6379
 - To test flake8 compliance in the python source code `flake8 pythonie/`


