# Contributing to Python Ireland Website

Thank you for your interest in contributing to the Python Ireland website! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Code Style](#code-style)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Review Process](#review-process)

---

## Code of Conduct

This project follows the [Python Community Code of Conduct](https://www.python.org/psf/conduct/). Please be respectful and inclusive in all interactions.

---

## Getting Started

### Prerequisites

- **Python 3.13** (required)
- **Docker** and **docker-compose** (recommended)
- **Git**
- **Task** (optional, for running predefined commands)

### Repository Structure

```
website/
├── pythonie/           # Main Django project
│   ├── core/          # Base pages and templates
│   ├── meetups/       # Meetup.com integration
│   ├── speakers/      # Conference speakers/sessions
│   ├── sponsors/      # Sponsor management
│   └── pythonie/      # Django settings
├── requirements/       # Dependency files
├── CLAUDE.md          # AI assistant instructions
├── DEVELOPMENT.md     # Detailed development guide
└── CONTRIBUTING.md    # This file
```

---

## Development Setup

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd website

# Build Docker image
task docker:build
# or: make docker-build

# Start services
docker-compose up -d postgres redis

# Run migrations
task django:migrate

# Create superuser
task django:createsuperuser

# Start development server
task run
```

### Option 2: Local Development

```bash
# Ensure Python 3.13 is installed
python3 --version  # Should show 3.13.x

# Create virtual environment
python3.13 -m venv pythonie-venv
source pythonie-venv/bin/activate

# Install dependencies
pip install uv
uv pip install -r requirements/dev.txt

# Run migrations
python pythonie/manage.py migrate --settings=pythonie.settings.dev

# Create superuser
python pythonie/manage.py createsuperuser --settings=pythonie.settings.dev

# Start server
python pythonie/manage.py runserver --settings=pythonie.settings.dev
```

### Verify Setup

1. Visit http://localhost:8000 - should show the site
2. Visit http://localhost:8000/admin/ - should show Wagtail admin
3. Log in with your superuser credentials

---

## Making Changes

### Branch Naming

Use descriptive branch names with prefixes:

```
feature/add-speaker-profile-images
bugfix/fix-meetup-sync-error
docs/update-readme
refactor/simplify-sponsor-model
```

### Workflow

1. **Create a branch** from `master`:
   ```bash
   git checkout master
   git pull origin master
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines

3. **Test your changes**:
   ```bash
   task tests
   # or: python pythonie/manage.py test pythonie --settings=pythonie.settings.tests
   ```

4. **Format your code**:
   ```bash
   task code:format
   # or: python -m ruff format pythonie
   ```

5. **Commit your changes** with clear messages:
   ```bash
   git add .
   git commit -m "Add speaker profile image upload feature"
   ```

6. **Push and create a Pull Request**:
   ```bash
   git push origin feature/your-feature-name
   ```

---

## Code Style

### Python

- **Python version**: 3.13 (strict requirement)
- **Formatter**: Ruff
- **Line length**: 88 characters (Ruff default)
- **Imports**: Sorted automatically by Ruff

### Formatting Commands

```bash
# Format all Python files
task code:format
# or: python -m ruff format pythonie

# Lint code and fix issues
task code:lint
# or: python -m ruff check --fix pythonie

# Check code formatting and linting without changes
task code:check
```

### Django/Wagtail Conventions

1. **Models**: Place in `models.py`, use explicit `Meta` classes
2. **Views**: Prefer Wagtail page models over custom views
3. **Templates**: Use template inheritance, extend `base.html`
4. **Settings**: Never hardcode secrets, use environment variables

### Documentation

- All code comments must be in **English**
- Use docstrings for functions and classes
- Update `DEVELOPMENT.md` for significant changes

### Example Code Style

```python
"""Module docstring explaining purpose."""

import logging
from django.db import models
from wagtail.models import Page

logger = logging.getLogger(__name__)


class MyModel(models.Model):
    """Model representing something.

    Attributes:
        name: The display name.
        created_at: When the record was created.
    """

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "My Model"
        verbose_name_plural = "My Models"

    def __str__(self):
        return self.name

    def some_method(self):
        """Perform some action.

        Returns:
            bool: True if successful, False otherwise.
        """
        logger.info(f"Processing {self.name}")
        return True
```

---

## Testing

### Running Tests

```bash
# All tests
task tests
# or: python pythonie/manage.py test pythonie --settings=pythonie.settings.tests -v 2

# Specific app
python pythonie/manage.py test pythonie.speakers --settings=pythonie.settings.tests

# Specific test file
python pythonie/manage.py test pythonie.meetups.test_meetups --settings=pythonie.settings.tests

# Specific test method
python pythonie/manage.py test pythonie.meetups.test_meetups.TestCase.test_method
```

### Writing Tests

Place tests in `test_*.py` files within each app:

```python
from django.test import TestCase
from model_mommy import mommy

from pythonie.speakers.models import Speaker


class SpeakerTestCase(TestCase):
    """Tests for the Speaker model."""

    def setUp(self):
        """Set up test fixtures."""
        self.speaker = mommy.make(Speaker, name="Test Speaker")

    def test_speaker_str(self):
        """Test string representation."""
        self.assertEqual(str(self.speaker), "Test Speaker")

    def test_speaker_creation(self):
        """Test speaker can be created."""
        speaker = mommy.make(Speaker)
        self.assertIsNotNone(speaker.id)
```

### Test Requirements

- All new features should include tests
- Bug fixes should include regression tests
- Maintain or improve code coverage

---

## Submitting Changes

### Pull Request Guidelines

1. **Title**: Clear, descriptive title
   - Good: "Add speaker profile image upload"
   - Bad: "Fix stuff" or "Updates"

2. **Description**: Include:
   - What changes were made
   - Why these changes were needed
   - How to test the changes
   - Screenshots (for UI changes)

3. **Size**: Keep PRs focused and reasonably sized
   - Split large changes into multiple PRs
   - One logical change per PR

### Pull Request Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (describe)

## How to Test
1. Step one
2. Step two
3. Expected result

## Checklist
- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] New tests added (if applicable)
- [ ] Documentation updated (if applicable)
```

### Commit Message Guidelines

Follow conventional commit format:

```
<type>: <short description>

<longer description if needed>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat: Add speaker bio character limit validation

fix: Resolve meetup sync timezone issue

docs: Update installation instructions for Python 3.13

refactor: Simplify sponsor level ordering logic
```

---

## Review Process

### What Reviewers Look For

1. **Functionality**: Does it work as intended?
2. **Code quality**: Is it readable and maintainable?
3. **Tests**: Are there adequate tests?
4. **Documentation**: Is it documented where needed?
5. **Security**: No vulnerabilities introduced?

### Responding to Feedback

- Address all reviewer comments
- Ask questions if feedback is unclear
- Push additional commits to address feedback
- Re-request review when ready

### Merging

- PRs require at least one approval
- All CI checks must pass
- Squash and merge is preferred for clean history

---

## Common Tasks

### Adding a New Django App

```bash
# Create app
cd pythonie
python ../pythonie/manage.py startapp myapp --settings=pythonie.settings.dev

# Add to INSTALLED_APPS in pythonie/pythonie/settings/base.py
INSTALLED_APPS = [
    # ...
    "pythonie.myapp",
]

# Create migrations
python pythonie/manage.py makemigrations myapp --settings=pythonie.settings.dev
python pythonie/manage.py migrate --settings=pythonie.settings.dev
```

### Adding a New Wagtail Page Type

```python
# In myapp/models.py
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

class MyPage(Page):
    """Description of this page type."""

    body = StreamField([...], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    # Specify allowed parent/child page types
    parent_page_types = ["core.HomePage"]
    subpage_types = []
```

### Adding a New Management Command

```python
# In myapp/management/commands/mycommand.py
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Description of what this command does."""

    help = "Does something useful"

    def add_arguments(self, parser):
        parser.add_argument("--option", type=str, help="Option description")

    def handle(self, *args, **options):
        self.stdout.write("Running command...")
        # Command logic here
        self.stdout.write(self.style.SUCCESS("Done!"))
```

---

## Getting Help

- **Documentation**: See `DEVELOPMENT.md` for detailed technical docs
- **Issues**: Check existing issues or create a new one
- **Community**: Reach out via Python Ireland channels

---

## Recognition

Contributors are recognized in release notes. Thank you for helping improve the Python Ireland website!
