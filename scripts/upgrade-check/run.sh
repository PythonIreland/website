#!/usr/bin/env bash
# Upgrade check: verify that a dependency upgrade (Wagtail, Django, ...) does
# not break the site, by migrating real pre-existing data and driving the
# admin in a headless browser.
#
#   1. Start a disposable PostgreSQL 17 container.
#   2. Check out the base ref (default: master) in a temporary worktree,
#      migrate and seed representative content with the *old* dependencies.
#   3. With the current checkout (the upgrade branch): migrate, run checks,
#      collectstatic --clear.
#   4. Render the public pages before and after, and diff the HTML.
#   5. Run the server (DEBUG off) and drive the admin with Playwright.
#
# Usage: scripts/upgrade-check/run.sh [--base REF] [--docker] [--debug]
# See scripts/upgrade-check/README.md for details.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"

BASE_REF="master"
BUILD_DOCKER=0
export UPGRADE_CHECK_DEBUG=0
export UPGRADE_CHECK_PG_PORT="${UPGRADE_CHECK_PG_PORT:-15432}"
export UPGRADE_CHECK_SERVER_PORT="${UPGRADE_CHECK_SERVER_PORT:-18000}"
export UPGRADE_CHECK_ADMIN_PASSWORD="${UPGRADE_CHECK_ADMIN_PASSWORD:-upgrade-check}"
PLAYWRIGHT_VERSION="${PLAYWRIGHT_VERSION:-1.65.2}"

usage() {
    sed -n '2,15p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
    exit "${1:-0}"
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --base) BASE_REF="$2"; shift 2 ;;
        --docker) BUILD_DOCKER=1; shift ;;
        --debug) UPGRADE_CHECK_DEBUG=1; shift ;;
        -h|--help) usage 0 ;;
        *) echo "Unknown option: $1" >&2; usage 1 ;;
    esac
done

for tool in docker git uv curl; do
    command -v "$tool" >/dev/null || { echo "Missing required tool: $tool" >&2; exit 1; }
done

RUN_DIR="$(mktemp -d "${TMPDIR:-/tmp}/upgrade-check.XXXXXX")"
export UPGRADE_CHECK_DIR="$RUN_DIR"
BASE_DIR="$RUN_DIR/base"
PG_CONTAINER="upgrade-check-pg-$$"
SERVER_PID=""

section() { printf '\n\033[1m== %s\033[0m\n' "$*"; }

# Drop the noise printed by the project settings on every command.
quiet() { grep -vE "PROJECT_ROOT=|No DATABASE_URL environment variable|objects imported automatically|^$" || true; }

# Kill a process and all its descendants (the server runs as subshell -> uv -> python).
kill_tree() {
    local child
    for child in $(pgrep -P "$1" 2>/dev/null); do
        kill_tree "$child"
    done
    kill "$1" 2>/dev/null || true
}

cleanup() {
    [[ -n "$SERVER_PID" ]] && kill_tree "$SERVER_PID"
    docker rm -f "$PG_CONTAINER" >/dev/null 2>&1 || true
    git -C "$TARGET_DIR" worktree remove --force "$BASE_DIR" >/dev/null 2>&1 || true
}
trap cleanup EXIT

# manage <checkout> <args...>: run manage.py with the upgrade check settings.
manage() {
    local checkout="$1"; shift
    (
        cd "$checkout"
        env -u DATABASE_URL -u VIRTUAL_ENV PYTHONPATH="$SCRIPT_DIR" \
            uv run --frozen python pythonie/manage.py "$@" --settings=upgrade_check_settings
    )
}

wagtail_version() {
    (cd "$1" && env -u VIRTUAL_ENV uv run --frozen python -c "import wagtail, django; print(f'Wagtail {wagtail.__version__}, Django {django.__version__}')")
}

section "Run directory: $RUN_DIR"
echo "Base ref: $BASE_REF | Target: $TARGET_DIR ($(git -C "$TARGET_DIR" rev-parse --abbrev-ref HEAD))"

if [[ "$BUILD_DOCKER" == 1 ]]; then
    section "Docker build"
    docker build -t python.ie/website-dev:upgrade-check "$TARGET_DIR" > "$RUN_DIR/docker-build.log" 2>&1 \
        || { echo "Docker build failed, see $RUN_DIR/docker-build.log"; exit 1; }
    docker run --rm python.ie/website-dev:upgrade-check python -c \
        "import wagtail, django; print(f'Image OK: Wagtail {wagtail.__version__}, Django {django.__version__}')"
fi

section "PostgreSQL 17 (port $UPGRADE_CHECK_PG_PORT)"
docker run -d --name "$PG_CONTAINER" -e POSTGRES_PASSWORD=pythonie -e POSTGRES_DB=pythonie \
    -p "127.0.0.1:$UPGRADE_CHECK_PG_PORT:5432" postgres:17 >/dev/null
for _ in $(seq 60); do
    docker exec "$PG_CONTAINER" pg_isready -U postgres -q 2>/dev/null && break
    sleep 1
done
docker exec "$PG_CONTAINER" pg_isready -U postgres

section "Base ($BASE_REF): install, migrate, seed"
git -C "$TARGET_DIR" worktree add --detach --quiet "$BASE_DIR" "$BASE_REF"
(cd "$BASE_DIR" && env -u VIRTUAL_ENV uv sync --frozen --all-groups --quiet)
wagtail_version "$BASE_DIR"
manage "$BASE_DIR" migrate --verbosity 0 2>&1 | quiet
manage "$BASE_DIR" shell --verbosity 0 -c "exec(open('$SCRIPT_DIR/seed.py').read())" 2>&1 | quiet
# Snapshots render with DEBUG on: static files are only collected later, and
# both sides must render with the same settings to be comparable.
UPGRADE_CHECK_DEBUG=1 UPGRADE_CHECK_SNAPSHOT="$RUN_DIR/snapshot-base" \
    manage "$BASE_DIR" shell --verbosity 0 -c "exec(open('$SCRIPT_DIR/snapshot.py').read())" 2>&1 | quiet | grep -v "Not Found"

section "Target: install, migrate, checks, collectstatic"
(cd "$TARGET_DIR" && env -u VIRTUAL_ENV uv sync --frozen --all-groups --quiet)
wagtail_version "$TARGET_DIR"
echo "Pending migrations:"
manage "$TARGET_DIR" showmigrations --plan 2>&1 | quiet | grep '\[ \]' || echo "  (none)"
manage "$TARGET_DIR" migrate 2>&1 | quiet | grep -E "Applying|No migrations" || true
manage "$TARGET_DIR" check 2>&1 | quiet
manage "$TARGET_DIR" makemigrations --check --dry-run 2>&1 | quiet
manage "$TARGET_DIR" collectstatic --clear --noinput 2>&1 | quiet | tail -1

section "Public pages: before/after HTML diff"
UPGRADE_CHECK_DEBUG=1 UPGRADE_CHECK_SNAPSHOT="$RUN_DIR/snapshot-target" \
    manage "$TARGET_DIR" shell --verbosity 0 -c "exec(open('$SCRIPT_DIR/snapshot.py').read())" 2>&1 | quiet | grep -v "Not Found"
if diff -r "$RUN_DIR/snapshot-base" "$RUN_DIR/snapshot-target" > "$RUN_DIR/snapshot.diff"; then
    echo "HTML identical before and after the upgrade."
else
    echo "WARNING: rendered HTML changed, review $RUN_DIR/snapshot.diff:"
    head -40 "$RUN_DIR/snapshot.diff"
fi

section "Browser check (server on port $UPGRADE_CHECK_SERVER_PORT, DEBUG=$UPGRADE_CHECK_DEBUG)"
manage "$TARGET_DIR" runserver "127.0.0.1:$UPGRADE_CHECK_SERVER_PORT" --noreload > "$RUN_DIR/server.log" 2>&1 &
SERVER_PID=$!
for _ in $(seq 60); do
    curl -fs -o /dev/null "http://127.0.0.1:$UPGRADE_CHECK_SERVER_PORT/" && break
    sleep 1
done
curl -fs -o /dev/null "http://127.0.0.1:$UPGRADE_CHECK_SERVER_PORT/" \
    || { echo "Server did not start, see $RUN_DIR/server.log"; exit 1; }

if [[ -z "${CHROMIUM_PATH:-}" ]]; then
    uv run --quiet --no-project --with "playwright==$PLAYWRIGHT_VERSION" playwright install chromium >/dev/null
fi
status=0
(cd "$RUN_DIR" && uv run --quiet --no-project --with "playwright==$PLAYWRIGHT_VERSION" \
    python -I "$SCRIPT_DIR/browser_check.py" "$RUN_DIR/screenshots") || status=$?

if grep -qE "Traceback|\" 5[0-9]{2} " "$RUN_DIR/server.log"; then
    echo "WARNING: server errors found in $RUN_DIR/server.log"
    status=1
fi

section "Result"
if [[ "$status" == 0 ]]; then
    echo "Upgrade check PASSED."
else
    echo "Upgrade check FAILED."
fi
echo "Artifacts (logs, HTML snapshots, screenshots): $RUN_DIR"
exit "$status"
