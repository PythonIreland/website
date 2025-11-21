# Development Guide - Python Ireland Website

> Complete documentation for developers working on python.ie / pycon.ie

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Environment Setup](#environment-setup)
- [Code Structure](#code-structure)
- [Data Models](#data-models)
- [External Integrations](#external-integrations)
- [Common Workflows](#common-workflows)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## Overview

### Tech Stack

- **Framework**: Django 5.2.8
- **CMS**: Wagtail 7.2
- **Python**: 3.12 (required)
- **Database**: PostgreSQL 17 (prod), SQLite (dev)
- **Cache**: Redis 6.2
- **Storage**: AWS S3 (prod), Local (dev)
- **Server**: Gunicorn (prod), Runserver (dev)
- **Containerization**: Docker + docker-compose
- **Automation**: Task (Taskfile.yaml)
- **Deployment**: Heroku

### Project Statistics

- **~2,749** lines of Python code
- **4** Django apps (core, meetups, speakers, sponsors)
- **11** models + 4 pivot tables
- **5** Wagtail page types
- **19** HTML templates
- **3** custom management commands

---

## Architecture

### Django Apps Structure

```
pythonie/
├── core/                    # Base Wagtail pages, templates, static files
│   ├── models.py           # HomePage, SimplePage, PageSegment
│   ├── templatetags/       # Template tags (meetups, sponsors)
│   ├── wagtail_hooks.py    # Wagtail admin customizations
│   └── templates/          # Base templates
├── meetups/                # Meetup.com integration
│   ├── models.py           # Meetup model
│   ├── utils.py            # Meetup.com API client
│   ├── schema.py           # Colander validation
│   └── management/         # updatemeetups command
├── speakers/               # Conference speakers/sessions management
│   ├── models.py           # Speaker, Session, Room, SpeakersPage, TalksPage
│   ├── templatetags/       # speaker_picture tag
│   └── management/         # import-sessionize, update-sessionize-json-stream
├── sponsors/               # Sponsor management
│   ├── models.py           # Sponsor, SponsorshipLevel
│   └── admin.py            # Admin customizations
└── pythonie/               # Django configuration
    ├── settings/           # Multi-environment settings
    │   ├── base.py        # Common settings
    │   ├── dev.py         # SQLite, DEBUG=True
    │   ├── production.py  # Heroku, S3, PostgreSQL
    │   ├── tests.py       # Tests with in-memory SQLite
    │   └── pgdev.py       # Local PostgreSQL
    ├── configure.py        # Helpers (configure_redis)
    └── patches.py          # Third-party patches (SlideShare OEmbed)
```

### Data Flow

```
┌─────────────────┐
│  Meetup.com API │──┐
└─────────────────┘  │
                     ├──> updatemeetups ──> Meetup model
┌─────────────────┐  │
│ Sessionize API  │──┤
└─────────────────┘  └──> import commands ──> Speaker/Session models
                                               │
                                               ├──> Wagtail Page Tree
                                               │
┌─────────────────┐                            │
│  Wagtail Admin  │──> Content editing ────────┘
└─────────────────┘                            │
                                               ▼
                                          Public Website
                                          (Templates + StreamFields)
```

---

## Environment Setup

### Prerequisites

- Python 3.12 (required)
- Docker + docker-compose
- Task (or Make)
- Git

### Initial Setup (Docker - Recommended)

```bash
# 1. Clone the repository
git clone <repo-url>
cd website

# 2. Build Docker image
task docker:build

# 3. Start PostgreSQL and Redis
docker-compose up -d postgres redis

# 4. Create/migrate the database
task django:migrate

# 5. Create a superuser
task django:createsuperuser

# 6. Create required parent pages (IMPORTANT)
task django:shell-plus
# In the Python shell:
from pythonie.core.models import HomePage
from pythonie.speakers.models import SpeakersPage, TalksPage
from wagtail.models import Site, Page

root = Page.objects.get(id=1)

# Create SpeakersPage (note the displayed ID)
speakers_page = SpeakersPage(title="Speakers", slug="speakers")
root.add_child(instance=speakers_page)
speakers_page.save_revision().publish()
print(f"SpeakersPage ID: {speakers_page.id}")  # Note this ID!

# Create TalksPage (note the displayed ID)
talks_page = TalksPage(title="Talks", slug="talks")
root.add_child(instance=talks_page)
talks_page.save_revision().publish()
print(f"TalksPage ID: {talks_page.id}")  # Note this ID!

# 7. Update hardcoded IDs in import-sessionize.py if different from 144/145
# See "Hardcoded IDs" section below

# 8. Start the server
task run

# 9. Access the admin
# http://localhost:8000/admin/
```

### Local Setup (without Docker)

```bash
# 1. Create virtualenv (ensure Python 3.12)
python3.12 -m venv pythonie-venv
source pythonie-venv/bin/activate

# 2. Install dependencies
pip install -r requirements/dev.txt

# 3. Migrate database
python pythonie/manage.py migrate --settings=pythonie.settings.dev

# 4. Create superuser
python pythonie/manage.py createsuperuser --settings=pythonie.settings.dev

# 5. Start server
python pythonie/manage.py runserver --settings=pythonie.settings.dev
```

### Environment Variables

Create `development.env` at the root (copy from `development.env.example` if it exists):

```bash
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=pythonie.settings.dev

# Database (for Docker)
PGDATABASE=pythonie
PGUSER=postgres
PGPASSWORD=postgres
PGHOST=postgres

# Redis
REDISCLOUD_URL=redis://redis:6379/0

# Meetup.com (optional)
MEETUP_KEY=your-meetup-api-key

# AWS S3 (production only)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=

# Sessionize (if different)
SESSIONIZE_API_URL=https://sessionize.com/api/v2/z66z4kb6/view/All
```

---

## Code Structure

### Key Models

#### Core App

**HomePage** (`pythonie/core/models.py:112`)
```python
class HomePage(Page, MeetupMixin, SponsorMixin):
    """Main page for conferences/events

    Features:
    - Flexible StreamField (heading, paragraph, video, image, html)
    - Conditional meetups display (via show_meetups)
    - Conditional sponsors display (via show_sponsors)
    - Reusable page segments
    """
    body = StreamField([...])

    content_panels = [
        FieldPanel("title"),
        StreamFieldPanel("body"),
        InlinePanel("page_segments", label="Page segments"),
        InlinePanel("sponsors", label="Sponsors"),
    ]
```

**SimplePage** (`pythonie/core/models.py:145`)
```python
class SimplePage(Page, MeetupMixin, SponsorMixin):
    """Standard content pages (About, Contact, etc.)"""
```

**PageSegment** (`pythonie/core/models.py:25`)
```python
@register_snippet
class PageSegment(models.Model):
    """Reusable content blocks

    Locations: main, right, left
    Usage: Reusable text across multiple pages
    """
```

#### Meetups App

**Meetup** (`pythonie/meetups/models.py:16`)
```python
class Meetup(models.Model):
    id = models.CharField(max_length=100, primary_key=True)  # Meetup.com ID
    name = models.CharField(max_length=255)
    time = models.DateTimeField()
    rsvps = models.IntegerField(default=0)
    status = models.CharField(max_length=255)

    @classmethod
    def future_events(cls):
        """Returns events for the next 3 months"""
        now = timezone.now()
        future = next_n_months(now, 3)
        return cls.objects.filter(time__gte=now, time__lte=future)
```

**WARNING**: `id` is a CharField (Meetup.com ID), not an AutoField

#### Speakers App

**Speaker** (`pythonie/speakers/models.py:27`)
```python
class Speaker(Page):
    """Speaker profile (inherits from Page for its own URL)

    Fields:
    - external_id: Sessionize UUID (unique, for idempotent import)
    - picture_url: Photo URL (Robohash fallback if empty)
    - biography: Full bio

    Required parent: SpeakersPage
    """
    external_id = models.CharField(max_length=255, unique=True)
```

**Session** (`pythonie/speakers/models.py:79`)
```python
class Session(Page):
    """Talk or workshop

    States: draft, accepted, confirmed, refused, cancelled
    Types: talk, workshop

    Fields:
    - scheduled_at: Session DateTime
    - duration: Duration in minutes (default 30)
    - room: ForeignKey to Room
    - speakers: M2M to Speaker

    Required parent: TalksPage
    """

    def is_confirmed(self):
        return self.state == Session.StateChoices.CONFIRMED
```

#### Sponsors App

**Sponsor** (`pythonie/sponsors/models.py:21`)
```python
class Sponsor(models.Model):
    """Sponsor/company

    Important method:
    - for_event(context): Returns sponsors for a page,
      sorted by level (Gold > Silver > Bronze)
    """

    @classmethod
    def for_event(cls, context):
        """Gets sponsors for current page, sorted by level"""
```

**SponsorshipLevel** (`pythonie/sponsors/models.py:9`)
```python
class SponsorshipLevel(models.Model):
    """Sponsorship levels (e.g., Gold=3, Silver=2, Bronze=1)

    Ordering: -level (descending, highest first)
    """
    level = models.IntegerField()
    name = models.CharField(max_length=255)
```

### Custom Template Tags

#### core_tags.py

```python
{% load core_tags %}

{# Display future meetups if page.show_meetups=True #}
{% meetups %}

{# Display sponsors sorted by level if page.show_sponsors=True #}
{% sponsors %}

{# Returns the site's root page #}
{% root_page as root %}

{# Returns live and in_menu children of a page #}
{% child_pages page as children %}
```

#### speaker_tags.py

```python
{% load speaker_tags %}

{# Display speaker photo or Robohash fallback #}
{% speaker_picture speaker size=100 %}
```

### Wagtail Hooks (`pythonie/core/wagtail_hooks.py`)

```python
@hooks.register("insert_editor_js")
def enable_source():
    """Enables HTML source editing in Hallo.js"""

@hooks.register("construct_whitelister_element_rules")
def allow_iframes():
    """Allows <iframe>, <tito-widget>, <tito-button> in rich text

    Usage: Embed ticketing widgets
    """

@hooks.register("insert_editor_js")
def enable_quotes():
    """Adds custom click-to-tweet button in the editor"""
```

---

## Data Models

### Relational Schema

```
┌─────────────────┐
│   HomePage      │
│  (Wagtail Page) │
└────────┬────────┘
         │
         ├──────┬─────────────────────────────┐
         │      │                             │
         │      ▼                             ▼
         │  ┌──────────────────┐      ┌────────────────┐
         │  │ HomePageSegment  │      │ HomePageSponsor│
         │  │   (Orderable)    │      │  Relationship  │
         │  └────────┬─────────┘      └───────┬────────┘
         │           │                        │
         │           ▼                        ▼
         │    ┌──────────────┐        ┌──────────────┐
         │    │ PageSegment  │        │   Sponsor    │
         │    │  (Snippet)   │        └──────┬───────┘
         │    └──────────────┘               │
         │                                   │
         │                          ┌────────┴────────┐
         │                          │                 │
         ▼                          ▼                 ▼
    ┌─────────────┐         ┌────────────┐   ┌──────────────────┐
    │ SimplePage  │         │   Meetup   │   │MeetupSponsor     │
    │(Wagtail Page│         │ (Snippet)  │   │  Relationship    │
    └─────────────┘         └────────────┘   └──────────────────┘


┌──────────────────┐          ┌──────────────────┐
│  SpeakersPage    │          │   TalksPage      │
│ (Wagtail Page)   │          │ (Wagtail Page)   │
└────────┬─────────┘          └────────┬─────────┘
         │                             │
         ▼                             ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ Speaker ├────┤ Session ├────┤  Room   │
    │ (Page)  │M2M │ (Page)  │ FK │         │
    └─────────┘    └─────────┘    └─────────┘
```

### M2M Relations with Pivot Tables

**Why explicit pivot tables?**

1. **HomePageSponsorRelationship**: Adds `level` field (SponsorshipLevel)
2. **MeetupSponsorRelationship**: Adds `note` field (TextField)
3. **HomePageSegment**: Adds `Orderable` for drag-and-drop ordering

```python
# Example: Associate sponsor with event at a specific level
HomePage.objects.get(title="PyCon 2024").sponsors.add(
    Sponsor.objects.get(name="Company"),
    through_defaults={"level": SponsorshipLevel.objects.get(name="Gold")}
)
```

---

## External Integrations

### 1. Meetup.com API

**File**: `pythonie/meetups/utils.py`

**Main function**:
```python
def update():
    """Syncs events from Meetup.com

    API Call:
    - Endpoint: https://api.meetup.com/2/events.html
    - Params: group_urlname=pythonireland, time=,3m
    - Auth: MEETUP_KEY env var

    Logic:
    1. Fetch all future events
    2. Validate with Colander schema
    3. Update or create Meetup objects
    4. Only updates if 'updated' timestamp has changed
    5. Always updates RSVP counts
    """
```

**Validation Schema** (`pythonie/meetups/schema.py`):
```python
class EventSchema(MappingSchema):
    id = SchemaNode(String())
    name = SchemaNode(String())
    time = SchemaNode(UnixTimestamp())  # Converted to UTC datetime
    description = SchemaNode(String())
    event_url = SchemaNode(String())
    # ... other fields
```

**Usage**:
```bash
# Via management command
python pythonie/manage.py updatemeetups --settings=pythonie.settings.dev

# Or via Task
task meetup:update

# Recommended cron: Every hour
0 * * * * cd /path/to/app && python pythonie/manage.py updatemeetups --settings=pythonie.settings.production
```

**Note**: Meetup.com API v2 is deprecated, migration to GraphQL API recommended

### 2. Sessionize Integration

#### Method A: Excel Import

**File**: `pythonie/speakers/management/commands/import-sessionize.py`

**Prerequisites**:
- Export Excel from Sessionize (with sheets "Accepted speakers", "Accepted sessions")
- Existing parent pages: SpeakersPage (ID 144), TalksPage (ID 145)

**Usage**:
```bash
# Download sessionize.xlsx from Sessionize
docker-compose run web python pythonie/manage.py import-sessionize --file sessionize.xlsx

# Or via Task
task pycon:import:sessionize
```

**Required Excel columns**:

Speakers:
- `Speaker Id` (Sessionize UUID)
- `Full Name`
- `Email Address`
- `Profile Picture`
- `Biography`

Sessions:
- `Session Id`
- `Session Title`
- `Session Description`
- `Session Type` (talk/workshop)
- `Speaker Ids` (comma-separated UUIDs)
- `Scheduled At`
- `Room`
- `Duration`

**Hardcoded IDs** (IMPORTANT):
```python
# Lines 50-52
parent_page = Page.objects.get(id=144).specific  # SpeakersPage
parent_page = Page.objects.get(id=145).specific  # TalksPage
```

**If your IDs differ**, update these lines or create pages with these exact IDs.

#### Method B: JSON Stream API (Recommended)

**File**: `pythonie/speakers/management/commands/update-sessionize-json-stream.py`

**Advantages**:
- Automated (no Excel file needed)
- Can be scheduled via cron
- Pydantic validation

**Usage**:
```bash
docker-compose run web python pythonie/manage.py update-sessionize-json-stream

# Or via Task
task pycon:import:sessionize:json
```

**API URL** (line 131):
```python
response = requests.get("https://sessionize.com/api/v2/z66z4kb6/view/All")
```

**To change URL** for another event:
1. Go to Sessionize > Event > API / Embed
2. Copy the "All Data (JSON)" URL
3. Update in the code OR create env variable `SESSIONIZE_API_URL`

**Pydantic Models** (validation):
```python
class SessionizeSpeaker(BaseModel):
    id: str
    firstName: str
    lastName: str
    bio: str | None = None
    profilePicture: str | None = None
    sessions: list[int]

class SessionizeSession(BaseModel):
    id: int
    title: str
    description: str | None = None
    startsAt: str | None = None
    endsAt: str | None = None
    roomId: int | None = None
    speakers: list[str]
```

**Email Fallback**:
```python
# Sessionize API doesn't provide emails
email = f"{speaker.id}@sessionize.com"
```

### 3. AWS S3 (Production)

**Configuration** (`pythonie/pythonie/settings/production.py`):

Django 5.1+ uses the `STORAGES` API instead of `DEFAULT_FILE_STORAGE`:
```python
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = "s3.python.ie"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
```

**Required env variables**:
```bash
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

**Development**: Files stored locally in `pythonie/media/`

---

## Common Workflows

### Dependency Management

**Structure**:
```
requirements/
├── main.in           # Main dependencies
├── main.txt          # Generated by uv compile
├── production.in     # Production extras (gunicorn, boto3)
├── production.txt
├── dev.in            # Dev extras (pytest, ruff)
└── dev.txt
```

**Commands**:
```bash
# Recompile all dependencies
task dependencies:compute

# Check for outdated packages
task dependencies:outdated

# Upgrade all packages
task dependencies:upgrade

# Upgrade Wagtail only
task dependencies:upgrade:wagtail

# Upgrade specific package
task dependencies:upgrade:package PACKAGE=django

# Check for security vulnerabilities
task dependencies:security

# Show dependencies tree
task dependencies:tree
```

**Manual process**:
```bash
# Edit requirements/main.in
echo "django-debug-toolbar" >> requirements/main.in

# Recompile
uv pip compile requirements/main.in -o requirements/main.txt

# Install
pip install -r requirements/dev.txt
```

### Database Migrations

**Create migrations**:
```bash
# Docker
task django:make-migrations

# Local
python pythonie/manage.py makemigrations --settings=pythonie.settings.dev
```

**Apply migrations**:
```bash
# Docker
task django:migrate

# Local
python pythonie/manage.py migrate --settings=pythonie.settings.dev
```

**Migrate specific app**:
```bash
python pythonie/manage.py migrate speakers --settings=pythonie.settings.dev
```

**Rollback migration**:
```bash
# Rollback to migration 0003
python pythonie/manage.py migrate speakers 0003 --settings=pythonie.settings.dev
```

### Heroku Database Management

**Pull production to local**:
```bash
task database:pull
# Downloads Heroku backup and restores locally
```

**Push local to production** (DANGER):
```bash
task database:push
# WARNING: Overwrites production with local DB!
```

**Reset local with fresh prod copy**:
```bash
task database:reset
# 1. Drops local DB
# 2. Creates new DB
# 3. Pulls from production
```

**List Heroku backups**:
```bash
task heroku:database:backups
```

**Create new backup**:
```bash
task heroku:database:run-backup
```

### Static Files Collection

**Development** (not needed, files served directly):
```bash
# Not needed in dev, but to test:
python pythonie/manage.py collectstatic --settings=pythonie.settings.dev
```

**Production** (via Heroku release phase):
```
# In Procfile:
release: python pythonie/manage.py migrate --settings=pythonie.settings.production
```

WhiteNoise serves static files automatically.

### Django Shell

**Interactive shell**:
```bash
# Docker (with shell_plus for auto-imports)
task django:shell-plus

# Local
python pythonie/manage.py shell_plus --settings=pythonie.settings.dev
```

**Useful examples**:
```python
# List all future meetups
from pythonie.meetups.models import Meetup
Meetup.future_events()

# Create sponsor
from pythonie.sponsors.models import Sponsor, SponsorshipLevel
gold = SponsorshipLevel.objects.create(name="Gold", level=3)
sponsor = Sponsor.objects.create(
    name="Acme Corp",
    url="https://acme.com",
    description="Great company"
)

# Associate sponsor with HomePage
from pythonie.core.models import HomePage
homepage = HomePage.objects.first()
homepage.sponsors.add(sponsor, through_defaults={"level": gold})

# Publish a page
from pythonie.speakers.models import Speaker
speaker = Speaker.objects.get(name="John Doe")
speaker.save_revision().publish()
```

---

## Testing

### Test Structure

**Existing files**:
- `pythonie/meetups/test_meetups.py`
- `pythonie/sponsors/test_sponsors.py`

**Missing**: Core and Speakers apps lack tests (high priority)

### Running Tests

**All tests**:
```bash
# Docker
task tests
# or: make docker-tests

# Local
python pythonie/manage.py test pythonie --settings=pythonie.settings.tests --verbosity=2
```

**Specific app**:
```bash
python pythonie/manage.py test pythonie.meetups --settings=pythonie.settings.tests -v 2
```

**Specific file**:
```bash
python pythonie/manage.py test pythonie.meetups.test_meetups --settings=pythonie.settings.tests
```

**Specific method**:
```bash
python pythonie/manage.py test pythonie.meetups.test_meetups.MeetupTestCase.test_future_events
```

### Test Tools

**model_mommy**: Test data generation
```python
from model_mommy import mommy

# Create Meetup with random data
meetup = mommy.make(Meetup)

# With specific values
meetup = mommy.make(Meetup, name="Test Meetup", rsvps=10)
```

**unittest.mock**: Mock external APIs
```python
from unittest.mock import patch, MagicMock

@patch("pythonie.meetups.utils.requests.get")
def test_update_meetups(self, mock_get):
    mock_get.return_value = MagicMock(
        json=lambda: {"results": [...]},
        status_code=200
    )
    update()  # Call function with mock
```

**fakeredis**: Mock Redis
```python
# Automatically configured in pythonie.settings.tests
REDIS = configure_redis(None, test=True)  # Returns FakeStrictRedis
```

### Test Configuration

**Settings** (`pythonie/pythonie/settings/tests.py`):
```python
DEBUG = True
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
REDIS = configure_redis(None, test=True)  # FakeRedis
LOGGING = {
    "loggers": {
        "pythonie": {"level": "ERROR"}  # Less verbose
    }
}
```

### Writing New Tests

**Model test example**:
```python
from django.test import TestCase
from model_mommy import mommy
from pythonie.speakers.models import Speaker, Session

class SessionTestCase(TestCase):
    def setUp(self):
        self.speaker = mommy.make(Speaker, name="Jane Doe")
        self.session = mommy.make(
            Session,
            name="Test Talk",
            state=Session.StateChoices.CONFIRMED
        )
        self.session.speakers.add(self.speaker)

    def test_is_confirmed(self):
        self.assertTrue(self.session.is_confirmed())

    def test_speaker_names(self):
        self.assertEqual(self.session.speaker_names, "Jane Doe")
```

**View test example**:
```python
from django.test import TestCase, Client

class SpeakersPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Setup page tree...

    def test_speakers_page_loads(self):
        response = self.client.get("/speakers/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Speakers")
```

---

## Deployment

### Heroku Architecture

**Heroku Apps**:
- Production: `python-ireland` (or similar name)
- Staging (if exists): `python-ireland-staging`

**Addons**:
- **Heroku Postgres**: Main database
- **RedisCloud**: Redis cache
- **AWS S3**: Media storage (external)

**Buildpacks**:
1. `heroku/python`

### Procfile

```
release: python pythonie/manage.py migrate --settings=pythonie.settings.production
web: gunicorn --chdir pythonie pythonie.wsgi --log-file -
```

**release phase**: Runs migrations automatically before deployment
**web dyno**: Gunicorn WSGI server

### Production Environment Variables

```bash
# Heroku sets these automatically:
DATABASE_URL
REDISCLOUD_URL

# Configure manually:
heroku config:set DJANGO_SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
heroku config:set DJANGO_SETTINGS_MODULE=pythonie.settings.production
heroku config:set AWS_ACCESS_KEY_ID=your-key
heroku config:set AWS_SECRET_ACCESS_KEY=your-secret
heroku config:set AWS_STORAGE_BUCKET_NAME=your-bucket
heroku config:set MEETUP_KEY=your-meetup-key
```

### Deployment Workflow

**Via Git Push**:
```bash
git push heroku master

# Or from another branch:
git push heroku my-feature-branch:master
```

**Via Heroku CLI**:
```bash
# Build + deploy
git push heroku master

# View logs
heroku logs --tail

# Restart app
heroku restart

# Run migrations manually
heroku run python pythonie/manage.py migrate --settings=pythonie.settings.production

# Django shell in production
heroku run python pythonie/manage.py shell --settings=pythonie.settings.production
```

### Monitoring

**Logs**:
```bash
heroku logs --tail --app python-ireland

# Filter by source
heroku logs --source app --tail

# Last 100 lines
heroku logs -n 100
```

**Metrics**:
```bash
heroku ps --app python-ireland
heroku pg:info --app python-ireland
```

### Rollback

```bash
# List releases
heroku releases

# Rollback to previous version
heroku rollback

# Rollback to specific version
heroku rollback v42
```

---

## Troubleshooting

### Problem: "Settings module not found"

**Error**:
```
django.core.exceptions.ImproperlyConfigured:
The SECRET_KEY setting must not be empty.
```

**Solution**:
Always specify `--settings`:
```bash
python pythonie/manage.py runserver --settings=pythonie.settings.dev
```

Or set env variable:
```bash
export DJANGO_SETTINGS_MODULE=pythonie.settings.dev
python pythonie/manage.py runserver
```

### Problem: "Page with id=144 does not exist"

**Error**:
```
DoesNotExist: Page matching query does not exist.
```

**Cause**: Sessionize import looks for SpeakersPage (id=144) and TalksPage (id=145)

**Solution A - Create pages with these IDs**:
```python
# Django shell
from pythonie.speakers.models import SpeakersPage, TalksPage
from wagtail.models import Page

root = Page.objects.get(id=1)

# Delete existing pages if present
SpeakersPage.objects.all().delete()
TalksPage.objects.all().delete()

# Creating with specific ID (tricky with Wagtail, better to recreate DB)
```

**Solution B - Modify import code**:
```python
# pythonie/speakers/management/commands/import-sessionize.py

# Lines 50-52, replace:
parent_page = Page.objects.get(id=144).specific

# With:
parent_page = SpeakersPage.objects.first()
if not parent_page:
    raise CommandError("SpeakersPage not found. Create it first.")
```

### Problem: Redis Connection Error

**Error**:
```
ConnectionError: Error 111 connecting to 127.0.0.1:6379. Connection refused.
```

**Solution Docker**:
```bash
# Check if Redis is running
docker-compose ps redis

# Start Redis
docker-compose up -d redis
```

**Solution Local**:
```bash
# Install Redis
brew install redis  # macOS

# Start Redis
redis-server

# Or disable Redis in dev:
# pythonie/pythonie/settings/dev.py
REDIS = None
```

### Problem: Sessionize import fails silently

**Cause**: Pandas doesn't parse Excel correctly

**Debug**:
```python
# Open Django shell
task django:shell-plus

import pandas as pd
df = pd.read_excel("sessionize.xlsx", sheet_name="Accepted speakers")
print(df.head())
print(df.columns)

# Check exact column names
```

**Solution**: Rename columns in Excel or modify mapping in `import-sessionize.py`

### Problem: Meetup update returns nothing

**Error**: `update()` returns 0 meetups

**Possible causes**:
1. **MEETUP_KEY missing/invalid**
   ```bash
   echo $MEETUP_KEY  # Should display key
   ```

2. **No future events** on Meetup.com

3. **Meetup API v2 deprecated**

**Solution**:
```python
# Debug in shell
from pythonie.meetups.utils import update
update()  # See output/errors

# Or manually:
import requests
url = "https://api.meetup.com/2/events.html"
params = {"group_urlname": "pythonireland", "time": ",3m", "key": "YOUR_KEY"}
response = requests.get(url, params=params)
print(response.json())
```

### Problem: StreamField blocks don't display

**Cause**: Template doesn't render `{{ page.body }}`

**Solution**:
```django
{# In template #}
{% load wagtailcore_tags %}

{% for block in page.body %}
    {% include_block block %}
{% endfor %}
```

### Problem: Static files 404 in production

**Cause**: `collectstatic` not run or WhiteNoise misconfigured

**Solution**:
```bash
# Heroku
heroku run python pythonie/manage.py collectstatic --noinput --settings=pythonie.settings.production

# Check WhiteNoise in INSTALLED_APPS
# pythonie/pythonie/settings/base.py
INSTALLED_APPS = [
    # ...
    "whitenoise.runserver_nostatic",  # Before django.contrib.staticfiles
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    # ...
    "whitenoise.middleware.WhiteNoiseMiddleware",  # After SecurityMiddleware
]
```

### Problem: Sponsors don't display on page

**Cause**: `show_sponsors=False` or no relationship

**Debug**:
```python
# Shell
from pythonie.core.models import HomePage
page = HomePage.objects.first()

print(page.show_sponsors)  # Should be True
print(page.sponsors.all())  # List sponsors
print(Sponsor.for_event({"page": page}))  # Method used by template tag
```

**Solution**:
1. Enable in admin: Page > "Show sponsors" checkbox
2. Add sponsors via inline panel
3. Verify `SponsorshipLevel` exists

---

## Best Practices

### 1. Always Specify Settings Module

```bash
# Avoid
python pythonie/manage.py migrate

# Do this
python pythonie/manage.py migrate --settings=pythonie.settings.dev
```

### 2. Use Task for Common Commands

```bash
# Less readable
docker-compose run --rm --service-ports web python pythonie/manage.py runserver 0.0.0.0:8000

# Simpler
task run
```

### 3. Test Before Commit

```bash
task tests                  # Full tests
task code:format            # Format code with ruff
task code:lint              # Lint code and fix issues
task code:check             # Check without changes
task dependencies:security  # Check for security vulnerabilities
```

### 4. Create Atomic Migrations

```bash
# Avoid large multi-app migrations
python pythonie/manage.py makemigrations

# Per app
python pythonie/manage.py makemigrations speakers
python pythonie/manage.py makemigrations sponsors
```

### 5. Backup Before Major Migrations

```bash
# Before upgrading Wagtail, Django, etc.
task heroku:database:run-backup

# Or local dump
pg_dump pythonie > backup-$(date +%Y%m%d).dump
```

### 6. Version Requirements Explicitly

```python
# requirements/main.in

# Floating version - avoid
Django>=5.0

# Precise version or restricted range - do this
Django~=5.0.14
wagtail>=6.2,<7.0
```

### 7. Use external_id for Imports

```python
# Creates duplicates - avoid
speaker = Speaker.objects.create(name=data["name"])

# Get or create with external_id - do this
speaker, created = Speaker.objects.get_or_create(
    external_id=data["id"],
    defaults={"name": data["name"], ...}
)
```

### 8. Publish Wagtail Pages After Creation

```python
# Page created but not visible - avoid
page.save()

# Publish immediately - do this
page.save_revision().publish()
```

### 9. Use Transactions for Imports

```python
from django.db import transaction

@transaction.atomic
def import_speakers(data):
    for speaker_data in data:
        # If an error occurs, everything rolls back
        speaker = create_speaker(speaker_data)
```

### 10. Log Instead of Print

```python
import logging
logger = logging.getLogger("pythonie.speakers")

# Avoid
print(f"Created speaker: {speaker.name}")

# Do this
logger.info(f"Created speaker: {speaker.name}")
```

---

## Appendices

### A. Task Commands Reference

```bash
# Docker
task docker:build              # Build image
task run                       # Dev server
task shell                     # Bash shell
task django:shell-plus         # Django shell

# Database
task django:migrate            # Apply migrations
task django:make-migrations    # Create migrations
task database:pull             # Pull Heroku DB
task database:push             # Push to Heroku (danger)
task database:reset            # Reset local DB

# Tests & Code Quality
task tests                     # Run all tests
task code:format               # Format with ruff
task code:lint                 # Lint and fix issues
task code:check                # Check without changes

# Dependencies
task dependencies:compute      # Recompile requirements
task dependencies:outdated     # Check outdated
task dependencies:upgrade      # Upgrade all
task dependencies:security     # Check for security vulnerabilities
task dependencies:tree         # Show dependencies tree

# Imports
task pycon:import:sessionize       # Import Sessionize Excel
task pycon:import:sessionize:json  # Import Sessionize JSON
task meetup:update                 # Update meetups

# Heroku
task heroku:database:backups       # List backups
task heroku:database:run-backup    # Create backup
```

### B. Admin URLs

```
http://localhost:8000/admin/              # Wagtail admin
http://localhost:8000/django-admin/       # Django admin
http://localhost:8000/documents/          # Document downloads
```

### C. Key Configuration Files

```
.env                          # Env variables (gitignored)
development.env               # Dev env template
production.env                # Prod env template (gitignored)
docker-compose.yml            # Docker services
Dockerfile                    # Python 3.12 image
Taskfile.yaml                 # Task automation
Procfile                      # Heroku processes
requirements/                 # Dependency management
pythonie/manage.py            # Django CLI entry point
pythonie/pythonie/settings/   # Multi-env settings
pythonie/pythonie/wsgi.py     # WSGI application
```

### D. Contacts and Resources

- **Repo**: (insert Git URL)
- **Production**: https://python.ie
- **Wagtail Docs**: https://docs.wagtail.org/
- **Django Docs**: https://docs.djangoproject.com/
- **Sessionize API**: https://sessionize.com/playbook/api
- **Meetup API**: https://www.meetup.com/api/ (deprecated, GraphQL recommended)

---

## Changelog

| Date | Author | Change |
|------|--------|--------|
| 2024-XX-XX | Initial | Developer documentation created |

---

**Last updated**: 2025
**Django Version**: 5.2.8
**Wagtail Version**: 7.2
**Python Version**: 3.12
