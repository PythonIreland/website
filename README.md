# Python Ireland Website

This is the Python Ireland (https://python.ie) website, built with Django 6.0 and Wagtail CMS 7.3. It manages content for the Python Ireland community including meetups and sponsors. The PyCon Ireland 2026 website is in a [separate repository](https://github.com/PythonIreland/2026.pycon.ie).

## Prerequisites

- Python 3.13, [uv](https://docs.astral.sh/uv/) and [prek](https://github.com/j178/prek) (git hooks), all pinned in `mise.toml`: run `mise install`, or see [Git Hooks](#git-hooks-prek) for other ways to install prek
- Docker & Docker Compose (for containerized development - recommended)
- [Task](https://taskfile.dev/) (optional but recommended)
- Redis (only for local non-Docker development)
- Environment variables file as per [the instructions here](#environment-variables)

## Quick Start (Docker - Recommended)

1. Install the git hooks (the ruff and Django hooks run on the host through `uv run`):
   ```bash
   uv sync --all-groups
   prek install
   ```

2. Build the Docker image:
   ```bash
   task docker:build
   # or: make docker-build
   ```

3. Start supporting services:
   ```bash
   docker compose up -d postgres redis
   ```

4. Run database migrations:
   ```bash
   task django:migrate
   ```

5. Generate sample data (creates pages, navigation, meetups):
   ```bash
   task django:generate-sample-data
   # or: docker compose run --rm web python pythonie/manage.py generate_sample_data --settings=pythonie.settings.dev
   ```

6. Create a superuser:
   ```bash
   docker compose run --rm web python pythonie/manage.py createsuperuser --settings=pythonie.settings.dev
   ```

7. Start the development server:
   ```bash
   task run
   # or: docker compose run --rm --service-ports web python pythonie/manage.py runserver 0.0.0.0:8000
   ```

8. Visit http://127.0.0.1:8000/ to see the site with sample content
9. Access Wagtail admin at http://127.0.0.1:8000/admin/

## Local Setup (Without Docker)

If you prefer to develop without Docker:

1. Fork the repository into your own personal GitHub account
2. Clone your fork: `git clone git@github.com:YourGitHubName/website.git`
3. Ensure you are running Python 3.13: `python -V` should output `Python 3.13.x`
4. Install dependencies: `uv sync --all-groups` (creates and populates a `.venv` automatically)
5. Install the git hooks: `prek install` (see [Git Hooks](#git-hooks-prek))
6. Set up the database: `uv run python pythonie/manage.py migrate --settings=pythonie.settings.dev`
7. Generate sample data: `task django:generate-sample-data` (or `uv run python pythonie/manage.py generate_sample_data --settings=pythonie.settings.dev`)
8. Create a superuser: `uv run python pythonie/manage.py createsuperuser --settings=pythonie.settings.dev`
9. Install and run Redis server locally: `redis-server`
10. Set Redis environment variable: `export REDISCLOUD_URL=127.0.0.1:6379`
11. Run the server: `uv run python pythonie/manage.py runserver --settings=pythonie.settings.dev`
12. Visit http://127.0.0.1:8000/ to see the site with sample content
13. Visit http://127.0.0.1:8000/admin/ to log in to Wagtail admin

## Project Structure

```
pythonie/
├── core/          # Base Wagtail pages (HomePage, SimplePage) and mixins
├── meetups/       # Meetup.com integration and event management
├── sponsors/      # Sponsor management with sponsorship levels
└── pythonie/
    ├── settings/  # Environment-specific settings (base, dev, tests, production)
    ├── urls.py    # URL configuration
    └── wsgi.py    # WSGI application
```

## Common Commands

### Using Task (Recommended)

```bash
# Development
task run                      # Run development server
task shell                    # Open bash shell in container
task django:shell-plus        # Django shell with models pre-loaded

# Database
task django:migrate           # Run migrations
task django:make-migrations   # Create new migrations
task django:collect-static    # Collect static files

# Sample Data (for development)
task django:generate-sample-data

# Testing
task tests                    # Run test suite
make docker-tests             # Alternative test command

# Code Quality
task code:format              # Format code with ruff
task code:lint                # Lint and fix issues
task code:check               # Check without changes

# Dependencies
task dependencies:compute     # Recompile dependency files
task dependencies:outdated    # List outdated packages
task dependencies:upgrade     # Upgrade all dependencies
task dependencies:upgrade:package PACKAGE=django  # Upgrade specific package
task dependencies:security    # Check for security vulnerabilities
task dependencies:tree        # Show dependencies tree

# Database Operations (Heroku)
task database:pull            # Pull production database to local
task database:push            # Push local database to production
task database:reset           # Reset local DB with production copy
task heroku:database:backups  # View Heroku backups
task heroku:database:run-backup  # Create a new backup

# Heroku Management
task heroku:logs              # View logs in real-time
task heroku:restart           # Restart the application
task heroku:shell             # Django shell on Heroku
task heroku:bash              # Bash shell on Heroku
task heroku:migrate           # Run migrations on Heroku
task heroku:config            # Show environment variables
task heroku:ps                # Show dyno status
task heroku:releases          # Show deployment history
task heroku:rollback          # Rollback to previous release
task heroku:maintenance:on    # Enable maintenance mode
task heroku:maintenance:off   # Disable maintenance mode
```

### Direct Django Commands

```bash
# Always specify --settings=pythonie.settings.dev (or tests, production, etc.)

# Run server
python pythonie/manage.py runserver --settings=pythonie.settings.dev

# Database
python pythonie/manage.py migrate --settings=pythonie.settings.dev
python pythonie/manage.py makemigrations --settings=pythonie.settings.dev

# Create superuser
python pythonie/manage.py createsuperuser --settings=pythonie.settings.dev

# Django shell
python pythonie/manage.py shell_plus --settings=pythonie.settings.dev
```

## Running Tests

```bash
# Using Task (Docker)
task tests

# Using Make (Docker)
make docker-tests

# Local (all tests)
python pythonie/manage.py test pythonie --settings=pythonie.settings.tests --verbosity=2

# Run specific test module
python pythonie/manage.py test pythonie.meetups.test_meetups --settings=pythonie.settings.tests

# Verbose output
python pythonie/manage.py test pythonie --settings=pythonie.settings.tests --verbosity=3
```

## Code Quality

```bash
# Format code with ruff
task code:format

# Lint and fix issues
task code:lint

# Check without changes
task code:check
```

### Git Hooks (prek)

The repository uses [prek](https://github.com/j178/prek), a fast drop-in replacement for pre-commit, to run ruff, django-upgrade, the Django system checks, the missing migrations check and generic file checks on every commit. Like uv, prek is not a project dependency: install it on your machine, then enable the hooks in your clone.

```bash
# 1. Install prek (once per machine), with one of:
mise install            # installs the versions pinned in mise.toml
brew install prek
uv tool install prek

# 2. Enable the git hooks (once per clone)
uv sync --all-groups    # the ruff and Django hooks run through `uv run`
prek install

# Run every hook on the whole repository (same as CI)
prek run --all-files
```

See [CONTRIBUTING.md](CONTRIBUTING.md#git-hooks-prek) for the list of hooks and how to skip one in an emergency.

## Environment Variables

For Docker development, create/edit `development.env`:

```bash
DJANGO_SETTINGS_MODULE=pythonie.settings.dev
PGDATABASE=pythonie
PGUSER=postgres
PGPASSWORD=pythonie
PGHOST=postgres
REDISCLOUD_URL=redis://redis:6379     # Optional, for Redis integration
MEETUP_KEY=your_meetup_api_key        # Optional, for Meetup.com sync
```

For local development without Docker:
```bash
export REDISCLOUD_URL=127.0.0.1:6379
export MEETUP_KEY=your_meetup_api_key  # Get from https://secure.meetup.com/meetup_api/key/
```

## Deployment

The project is deployed on Heroku using the **heroku-24** stack with PostgreSQL 17. Use Task commands for database operations:

```bash
# View backups
task heroku:database:backups

# Create a new backup
task heroku:database:run-backup

# Pull production data to local (for testing/debugging)
task database:pull

# Push local data to production (use with caution!)
task database:push
```

## Development Tools

This project uses several tools to streamline development:

- **[Task](https://taskfile.dev/)**: Task runner for common workflows. See `Taskfile.yaml` for all available tasks.
- **[Toast](https://github.com/stepchowfun/toast)**: Containerized automation for dependency management. See `toast.yml`.
- **[mise](https://mise.jdx.dev/)**: Tool version manager for consistent Python/uv/Task versions. See `mise.toml`.
- **[uv](https://github.com/astral-sh/uv)**: Fast Python package manager for dependency installation. See `pyproject.toml` and `uv.lock`.

## Troubleshooting

### Redis Connection Errors
- **Docker**: Redis should work automatically via `docker compose`
- **Local**: Ensure Redis is running (`redis-server`) and set `REDISCLOUD_URL=127.0.0.1:6379`

### Database Issues
- Reset with production data: `task database:reset`
- Check PostgreSQL is running: `docker compose ps postgres`
- Verify environment variables in `development.env`

### Permission Errors (Docker)
- Check file ownership in mounted volumes
- May need to run: `sudo chown -R $USER:$USER .`

### Migration Conflicts
- Pull latest production data: `task database:pull`
- Or create fresh migrations: `task django:make-migrations`

### Import Errors or Module Not Found
- Rebuild Docker image: `task docker:build`
- Reinstall dependencies: `uv sync --all-groups`

## Contributing

1. Fork the repository into your own GitHub account
2. Create a feature branch: `git checkout -b feature/my-new-feature`
3. Make your changes and test thoroughly
4. Format your code: `task code:format`
5. Run tests: `task tests`
6. Commit your changes with clear messages
7. Push to your fork and create a Pull Request
