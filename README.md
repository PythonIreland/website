# Python Ireland Website

Website for Python Ireland (python.ie / pycon.ie) community, built with Django 5.2 and Wagtail CMS 7.2. Manages meetups, sponsors, speakers, and conference sessions.

## Prerequisites

- Python 3.13 (see `.tool-versions`)
- Docker & Docker Compose (for containerized development - recommended)
- [Task](https://taskfile.dev/) (optional but recommended)
- Redis (only for local non-Docker development)

## Quick Start (Docker - Recommended)

1. Build the Docker image:
   ```bash
   task docker:build
   # or: make docker-build
   ```

2. Start supporting services:
   ```bash
   docker compose up -d postgres redis minio
   ```

3. Run database migrations:
   ```bash
   task django:migrate
   ```

4. Generate sample data (creates pages, navigation, meetups):
   ```bash
   docker compose run --rm web python pythonie/manage.py generate_sample_data --settings=pythonie.settings.dev
   ```

5. Create a superuser:
   ```bash
   docker compose run --rm web python pythonie/manage.py createsuperuser --settings=pythonie.settings.dev
   ```

6. Start the development server:
   ```bash
   task run
   # or: docker compose run --rm --service-ports web python pythonie/manage.py runserver 0.0.0.0:8000
   ```

7. Visit http://127.0.0.1:8000/ to see the site with sample content
8. Access Wagtail admin at http://127.0.0.1:8000/admin/

## Local Setup (Without Docker)

If you prefer to develop without Docker:

1. Fork the repository into your own personal GitHub account
2. Clone your fork: `git clone git@github.com:YourGitHubName/website.git`
3. Ensure you are running Python 3.13: `python -V` should output `Python 3.13.x`
4. Create a virtualenv: `python3 -m venv pythonie-venv`
5. Activate the virtualenv: `source pythonie-venv/bin/activate`
6. Install dependencies: `pip install -r requirements.txt` (or `uv pip install -r requirements.txt`)
7. Set up the database: `python pythonie/manage.py migrate --settings=pythonie.settings.dev`
8. Generate sample data: `python pythonie/manage.py generate_sample_data --settings=pythonie.settings.dev`
9. Create a superuser: `python pythonie/manage.py createsuperuser --settings=pythonie.settings.dev`
10. Install and run Redis server locally: `redis-server`
11. Set Redis environment variable: `export REDISCLOUD_URL=127.0.0.1:6379`
12. Run the server: `python pythonie/manage.py runserver --settings=pythonie.settings.dev`
13. Visit http://127.0.0.1:8000/ to see the site with sample content
14. Visit http://127.0.0.1:8000/admin/ to log in to Wagtail admin

## Project Structure

```
pythonie/
├── core/          # Base Wagtail pages (HomePage, SimplePage) and mixins
├── meetups/       # Meetup.com integration and event management
├── sponsors/      # Sponsor management with sponsorship levels
├── speakers/      # Conference speakers and sessions (Sessionize integration)
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
python pythonie/manage.py generate_sample_data --settings=pythonie.settings.dev

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

# Conference Management
task pycon:import:sessionize      # Import from Sessionize Excel
task pycon:import:sessionize:json # Update from Sessionize JSON stream
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

The project is deployed on Heroku. Use Task commands for database operations:

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
- **[asdf](https://asdf-vm.com/)**: Tool version manager for consistent Python versions. See `.tool-versions`.
- **[uv](https://github.com/astral-sh/uv)**: Fast Python package manager for dependency installation.

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
- Reinstall dependencies: `pip install -r requirements.txt`

## Contributing

1. Fork the repository into your own GitHub account
2. Create a feature branch: `git checkout -b feature/my-new-feature`
3. Make your changes and test thoroughly
4. Format your code: `task code:format`
5. Run tests: `task tests`
6. Commit your changes with clear messages
7. Push to your fork and create a Pull Request
