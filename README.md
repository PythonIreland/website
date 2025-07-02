# Website

# Contributing
 - Fork the repository into your own personal github account. 
 - Clone your fork of the repository. `git clone git@github.com:YourGitHubName/website.git`
 - Ensure you are running python 3.12. `python -V` or `python3 -V` should output `Python 3.12.x`
 - Create a virtualenv to isolate the project dependencies. `python3 -m venv pythonie-venv` or `virtualenv -p python3 pythonie-venv` works for Ubuntu.
 - Activate the virtualenv. `source pythonie-venv/bin/activate`
 - Change into the website directory. `cd website`
 - Install the dependencies. `pip install -r requirements.txt`
 - Set up the database. `python pythonie/manage.py migrate --settings=pythonie.settings.dev`
 - Run the server. `python pythonie/manage.py runserver --settings=pythonie.settings.dev`
 - Check that it works by visiting `http://127.0.0.1:8000/` in your browser. (You should see a 'welcome to Wagtail' site, as you will not see content until you've added it in your DB)
 - Create a super user on your local DB. `python pythonie/manage.py createsuperuser --settings=pythonie.settings.dev`
 - Log in to wagtail with your superuser by navigating to `http://127.0.0.1:8000/admin/`.
 - To get rid of redis errors, install and run redis server locally and set environment variable export REDISCLOUD_URL=127.0.0.1:6379
 - To test flake8 compliance in the python source code `flake8 pythonie/`

# Running Tests
 - pythonie/manage.py test pythonie --settings=pythonie.settings.tests --verbosity=2

# Project Management Tools
We use several tools to manage and streamline development:

- [Task](https://taskfile.dev/): Task runner for automating common development workflows. See `Taskfile.yaml` for available tasks.
- [Toast](https://github.com/stepchowfun/toast): Containerized project automation. See `toast.yml` for configuration and available commands.
- [asdf](https://asdf-vm.com/): Tool version manager to ensure consistent versions of Python and other tools. Refer to `.tool-versions` if present, and see the asdf documentation for setup.
- [uv](https://github.com/astral-sh/uv): Fast Python package manager, used for installing and managing dependencies. You can use `uv pip install -r requirements.txt` as a drop-in replacement for pip.

Make sure to install these tools to ensure a smooth development experience.
