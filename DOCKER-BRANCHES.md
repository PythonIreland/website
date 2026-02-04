# Docker Multi-Branch Development

This setup allows you to run isolated Docker environments for each git branch, preventing conflicts when switching branches or working on multiple features simultaneously.

## How It Works

### Automatic Branch Detection

The system automatically:
- Detects your current git branch (`git rev-parse --abbrev-ref HEAD`)
- Normalizes the branch name (e.g., `feature/add-auth` → `feature-add-auth`)
- Uses this normalized name for:
  - Docker image tags: `python.ie/website:feature-add-auth`
  - Database names: `pythonie_feature-add-auth`
  - Container names: `pythonie-web-feature-add-auth`
  - Docker volumes: `postgres-data-feature-add-auth`

### Branch Isolation

Each branch gets:
- ✅ Its own Docker image
- ✅ Its own PostgreSQL database (isolated data)
- ✅ Its own SQLite database for local dev: `pythonie/db-{branch}.sqlite3`
- ✅ Its own Redis instance (isolated cache)
- ✅ Its own Docker volumes (persistent storage)
- ✅ Unique container names (no conflicts)

## Usage

### Basic Commands

```bash
# Check your current branch environment
task branch:info

# Build image for current branch
task docker:build

# Run development server (uses current branch)
task run

# Run tests (uses current branch database)
task tests

# Django shell for current branch
task django:shell-plus
```

### Working on Multiple Branches

**Scenario**: You want to work on `feature/auth` while keeping `main` running.

```bash
# Terminal 1: Main branch
git checkout main
task run
# → Uses: python.ie/website:main, pythonie_main database, port 8000

# Terminal 2: Feature branch (in another terminal)
git checkout feature/auth
task run
# → ERROR: Port 8000 already in use!
```

**Solution**: Use custom ports for parallel instances:

```bash
# Terminal 1: Main branch
git checkout main
task run

# Terminal 2: Feature branch with custom port
git checkout feature/auth
WEB_PORT=8001 PG_PORT=5433 task run
# → Uses: port 8001, separate database
```

### Managing Volumes

```bash
# List all volumes (all branches)
task branch:volumes

# Example output:
# pythonie-postgres-data-master
# pythonie-postgres-data-feature-add-auth
# pythonie-redis-data-master
# pythonie-redis-data-feature-add-auth

# Clean volumes for current branch (DESTRUCTIVE!)
task branch:clean
# → Deletes all data for current branch
```

### Switching Branches

When you switch branches, the system automatically uses the correct environment:

```bash
# On main branch
git checkout main
task run  # Uses main database

# Switch to feature branch
git checkout feature/add-auth
task run  # Automatically uses feature-add-auth database
```

**Important**: You must rebuild the image after switching branches if dependencies changed:

```bash
git checkout feature/new-dependencies
task docker:build  # Rebuild image with new dependencies
task run
```

## Advanced: Custom Ports for Parallel Development

Create a `.env` file (git-ignored) to override default ports:

```bash
# .env
WEB_PORT=8001
PG_PORT=5433
```

Or pass them inline:

```bash
WEB_PORT=8001 PG_PORT=5433 task run
```

## Troubleshooting

### Port Already in Use

```
Error: port 8000 already in use
```

**Solution**: Stop other instances or use custom ports:
```bash
task down  # Stop all containers for current branch
# OR
WEB_PORT=8001 PG_PORT=5433 task run
```

### Database Not Found

```
FATAL: database "pythonie_feature-xyz" does not exist
```

**Solution**: Run migrations to create the database:
```bash
task django:migrate
```

### Wrong Database Being Used

```bash
# Check which environment is active
task branch:info

# Ensure you're on the correct git branch
git branch

# Rebuild if needed
task docker:build
```

### Cleaning Up Old Branches

After deleting a git branch, clean up its Docker resources:

```bash
# Remove unused images
docker image prune -a

# Remove volumes for deleted branches
# (replace 'old-branch-name' with actual normalized branch name)
docker volume rm pythonie-postgres-data-old-branch-name
docker volume rm pythonie-redis-data-old-branch-name

# Or use the helper (must be on that branch)
git checkout old-branch-name
task branch:clean
```

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_BRANCH` | Auto-detected | Current git branch (normalized) |
| `DOCKER_IMAGE` | `python.ie/website:{branch}` | Docker image name |
| `PGDATABASE` | `pythonie_{branch}` | PostgreSQL database name |
| `WEB_PORT` | `8000` | Web server port |
| `PG_PORT` | `5432` | PostgreSQL port |

## Tips

1. **Branch Naming**: Use descriptive branch names. They'll appear in container names and logs.

2. **Disk Space**: Each branch creates separate volumes. Monitor disk usage:
   ```bash
   docker system df
   ```

3. **Production**: This system is for **development only**. Production uses fixed names and ports.

4. **Database Migrations**: Each branch has independent migrations. Remember to run `task django:migrate` after switching branches with schema changes.

5. **Shared Data**: If you need to copy data between branches:
   ```bash
   # Export from main
   git checkout main
   task run:postgres  # Start just postgres
   pg_dump -U postgres pythonie_main > /tmp/main.sql

   # Import to feature branch
   git checkout feature/xyz
   task run:postgres
   psql -U postgres pythonie_feature-xyz < /tmp/main.sql
   ```
