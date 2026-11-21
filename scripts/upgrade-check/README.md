# Upgrade check

End-to-end check for dependency upgrades (Wagtail, Django, ...). It migrates
data created with the **old** dependencies, then drives the Wagtail admin and
the public site in a headless browser with the **new** ones.

The project's unit tests do not cover the admin or page rendering, so run this
before merging any Wagtail or Django upgrade.

## Usage

From the checkout of the upgrade branch (for example a worktrunk worktree):

```bash
task upgrade:check                       # compare against master
task upgrade:check BASE=v2026.10         # compare against another ref
task upgrade:check -- --docker           # also build the Docker image

# or directly
scripts/upgrade-check/run.sh [--base REF] [--docker] [--debug]
```

The script exits with status 0 when every step passes, 1 otherwise.

## What it does

1. Starts a disposable PostgreSQL 17 container (`127.0.0.1:15432`).
2. Checks out the base ref in a temporary worktree, installs its dependencies,
   runs the migrations and seeds representative content (`seed.py`):
   - a page tree: home, nested `HomePage`, `SimplePage`s and an unpublished draft
   - rich text with bold, italic, external, page and document links, lists and an embedded image
   - PNG and WebP images, a document
   - a `PageSegment`, a `Meetup`, a sponsor with a sponsorship level, a redirect
3. With the current checkout: installs the new dependencies, lists and applies
   the pending migrations, runs `check`, `makemigrations --check` and
   `collectstatic --clear`.
4. Renders the public pages before and after the upgrade and diffs the HTML
   (`snapshot.py`). A difference is reported as a warning, not a failure.
5. Starts `runserver` with `DEBUG` off (like production) and runs
   `browser_check.py` with Playwright:
   - admin login and the page explorer in the sidebar
   - page listing and search
   - editing rich text on an existing page, publishing it and checking the public page
   - creating and publishing a new page
   - preview, revision history and the unpublished draft
   - saving the `PageSegment` and `Meetup` snippets
   - images, documents, sites, users and redirects
   - the Django admin (sponsors)
   - the public pages, the redirect and the 404 page
6. Fails when a step fails, when the application returns a 4xx/5xx response
   or when the server log contains a traceback.

The container, the server and the base worktree are always removed at the end.
Logs, HTML snapshots and screenshots stay in the run directory printed at the
end (`$TMPDIR/upgrade-check.XXXXXX`).

## Requirements

- Docker, uv, git, curl.
- Playwright is fetched by `uv` on the fly; its Chromium is installed on the
  first run. To use an existing browser instead, set `CHROMIUM_PATH`
  (for example `CHROMIUM_PATH=/usr/bin/chromium-browser`).

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `UPGRADE_CHECK_PG_PORT` | `15432` | Host port of the PostgreSQL container |
| `UPGRADE_CHECK_SERVER_PORT` | `18000` | Port of the Django server |
| `UPGRADE_CHECK_ADMIN_PASSWORD` | `upgrade-check` | Password of the seeded `admin` user |
| `PLAYWRIGHT_VERSION` | `1.65.2` | Playwright version used by the browser check |
| `CHROMIUM_PATH` | unset | Chromium binary to use instead of Playwright's |

## Limits

- The data is synthetic. Before deploying, also migrate a copy of the
  production database (`task database:pull`).
- `seed.py` uses the project models: if a model changes, update the seed.
- Known noise in the browser report: the `axe.run` console messages come from
  the Wagtail userbar accessibility checker.
