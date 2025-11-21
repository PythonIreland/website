# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Python Ireland (python.ie / pycon.ie) website, built with Django 5.2 and Wagtail CMS 7.2. It manages content for the Python Ireland community including meetups, sponsors, speakers, and PyCon talks/sessions.

### Python Version

This project requires **Python 3.12**. All code must be compatible with Python 3.12 and should not use features from newer versions. When developing locally without Docker, ensure you are using Python 3.12.x.

## Architecture

### Django Apps Structure

The project follows a modular Django app structure within the `pythonie/` directory:

- **core**: Base Wagtail pages (HomePage, SimplePage) with StreamField content blocks. Implements PageSegment snippets and mixins (MeetupMixin, SponsorMixin) for common functionality.
- **meetups**: Manages Meetup.com integration for Python Ireland meetups. Includes a management command `updatemeetups` to sync with Meetup API.
- **sponsors**: Sponsor management with SponsorshipLevel relationships.
- **speakers**: Speaker and Session (talk/workshop) management for conferences. Includes Sessionize integration via management commands (`import-sessionize`, `update-sessionize-json-stream`).

### Settings Configuration

Multiple settings files in `pythonie/pythonie/settings/`:
- `base.py`: Shared settings, uses `dj_database_url` for database configuration
- `dev.py`: SQLite database, local Redis, DEBUG=True
- `tests.py`: Test-specific settings with SQLite and mock Redis
- `production.py`: Heroku production settings
- `pgdev.py`: PostgreSQL development settings

Always specify settings module: `--settings=pythonie.settings.dev` (or `tests`, `production`, etc.)

### Database

- Development (default): SQLite at `pythonie/db.sqlite3`
- Docker/Tests: PostgreSQL 17 in docker-compose
- Production: PostgreSQL 17 on Heroku via `DATABASE_URL` environment variable

**Important**: When using Heroku CLI tools locally (e.g., `task database:reset`), ensure you have PostgreSQL 17 installed locally. This simplifies database reset operations and ensures compatibility with production.

### Key Dependencies

- Django ~5.2.0
- Wagtail ~7.2.0 (CMS framework)
- Redis (caching, configured via `REDISCLOUD_URL`)
- WhiteNoise (static file serving)
- boto3/django-storages (S3 integration)
- Delorean/python-dateutil (date handling)

## Common Commands

### Local Development (without Docker)

```bash
# Setup
python3 -m venv pythonie-venv
source pythonie-venv/bin/activate
pip install -r requirements.txt

# Database
python pythonie/manage.py migrate --settings=pythonie.settings.dev
python pythonie/manage.py createsuperuser --settings=pythonie.settings.dev

# Run server
python pythonie/manage.py runserver --settings=pythonie.settings.dev

# Access admin at http://127.0.0.1:8000/admin/
```

### Docker Development (preferred)

Uses Task for most operations. Requires docker-compose with services: web, postgres, redis, minio.

```bash
# Build docker image
task docker:build
# or: make docker-build

# Run development server
task run
# or: docker compose run --rm --service-ports web python pythonie/manage.py runserver 0.0.0.0:8000

# Shell access
task shell
# or: docker compose run --rm web /bin/bash

# Django shell
task django:shell-plus

# Database migrations
task django:make-migrations
task django:migrate
```

### Testing

```bash
# Run all tests (local)
python pythonie/manage.py test pythonie --settings=pythonie.settings.tests --verbosity=2

# Run all tests (docker)
make docker-tests
# or: task tests

# Run single test
python pythonie/manage.py test pythonie.meetups.test_meetups --settings=pythonie.settings.tests
```

### Code Quality

```bash
# Format code with ruff
task code:format
# or: toast code:format
# or: python -m ruff format pythonie

# Lint code and fix issues
task code:lint
# or: toast code:lint
# or: python -m ruff check --fix pythonie

# Check code formatting and linting without changes
task code:check
# or: toast code:check
```

### Dependency Management

Uses `uv` for fast Python package management. Dependencies are defined in `.in` files and compiled to `.txt` files:

```bash
# Recompile all dependencies
task dependencies:compute
# or: toast deps:compute

# Check outdated packages
task dependencies:outdated

# Upgrade all dependencies
task dependencies:upgrade

# Upgrade only Wagtail
task dependencies:upgrade:wagtail

# Upgrade specific package
task dependencies:upgrade:package PACKAGE=django

# Check for security vulnerabilities
task dependencies:security

# Show dependencies tree
task dependencies:tree
```

### Database Operations (Heroku)

```bash
# Pull production database to local
task database:pull

# Push local database to production
task database:push

# Reset local with fresh production copy
task database:reset

# View Heroku backups
task heroku:database:backups

# Create new backup
task heroku:database:run-backup
```

### Conference Management

```bash
# Import speakers/sessions from Sessionize
task pycon:import:sessionize
# or: docker compose run web python pythonie/manage.py import-sessionize --file sessionize.xlsx

# Update from Sessionize JSON stream
task pycon:import:sessionize:json
```

## Important Implementation Notes

### Wagtail Page Models

All page types inherit from `wagtail.models.Page`. The page tree structure:
- HomePage (root, can have child HomePage or SimplePage)
- SimplePage
- SpeakersPage → Speaker pages
- TalksPage → Session pages

Pages use StreamFields for flexible content blocks (heading, paragraph, video, image, slide, html).

### Settings Module Requirement

Django commands MUST include `--settings=pythonie.settings.<module>`. The default in `manage.py` is `pythonie.settings` which won't work without proper environment setup.

### Redis Configuration

Development expects Redis at `127.0.0.1:6379` or via `REDISCLOUD_URL` environment variable. Configure via `pythonie.settings.configure.configure_redis()`.

### Environment Variables

Key variables (see `development.env` / `production.env`):
- `DJANGO_SECRET_KEY`: Required for production
- `DJANGO_SETTINGS_MODULE`: Settings module path
- `DATABASE_URL`: PostgreSQL connection (Heroku format)
- `REDISCLOUD_URL`: Redis connection
- `MEETUP_KEY`: Meetup.com API key
- `PGDATABASE`, `PGUSER`, `PGPASSWORD`, `PGHOST`: PostgreSQL credentials for Docker

### Static Files

Static files collected via WhiteNoise with `CompressedManifestStaticFilesStorage`. SCSS compiled via django-compressor and django-libsass.

### Testing Strategy

Tests use `pythonie.settings.tests` which configures SQLite and mock Redis. Run with `--verbosity=2` or `--verbosity=3` for detailed output.

### Deployment

The project is hosted on Heroku.

### Upgrading Wagtail

After upgrading Wagtail to a new version, you must:

1. Rebuild the Docker image: `task docker:build`
2. Run migrations: `task django:migrate`
3. Clear and recollect static files: `docker compose run --rm web python pythonie/manage.py collectstatic --clear --noinput`
4. **Clear your browser cache** (Ctrl+Shift+R or Cmd+Shift+R) - this is critical as Wagtail admin JavaScript files are cached and stale cache can cause the admin sidebar menu to disappear with errors like `wagtailConfig is undefined`.

### Storage Configuration (Django 5.1+)

Django 5.1 removed `DEFAULT_FILE_STORAGE` and `STATICFILES_STORAGE` settings. The project now uses the `STORAGES` API:

- **base.py**: Defines default storage (FileSystemStorage) and staticfiles (WhiteNoise)
- **production.py**: Overrides default storage to use S3 (`storages.backends.s3boto3.S3Boto3Storage`)

If you see 404 errors for images after upgrading Django, ensure `STORAGES` is properly configured instead of the deprecated settings.

### Documentation Language

All documentation and code comments must be written in English to ensure all contributors can collaborate effectively.

### Git Commits

When creating git commits, do not include any mention of Claude, Claude Code, or AI assistance in commit messages. Commit messages should focus solely on describing the changes made, without attribution to the tool used to make them.