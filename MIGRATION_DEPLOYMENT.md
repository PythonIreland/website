# Deployment Guide: Removing Speakers App

This guide explains how to safely deploy PR #161 which removes the speakers app from the Python Ireland website.

## Overview

PR #161 removes the entire `speakers` Django app and all associated code. A database migration has been created to cleanly drop the speakers tables from production.

## Pre-requisites

✅ All speaker/session records have been deleted from production database
✅ No Wagtail pages of type SpeakersPage or TalksPage exist in production
✅ Recent database backup exists

## Deployment Steps

### Step 1: Create a Backup

**CRITICAL**: Always backup before running destructive migrations.

```bash
# Create a fresh backup
task heroku:database:run-backup

# Verify the backup was created
task heroku:database:backups
```

### Step 2: Merge the PR

Merge PR #161 into master branch:

```bash
# Via GitHub CLI
gh pr merge 161 --squash --delete-branch

# Or via GitHub web interface
```

### Step 3: Deploy to Heroku

The deployment will happen automatically if auto-deploy is configured, or manually:

```bash
# Pull latest master
git checkout master
git pull origin master

# Push to Heroku (if manual deployment)
git push heroku master
```

### Step 4: Run the Migration

The migration will run automatically during Heroku release phase. If you need to run it manually:

```bash
# Run migrations on Heroku
task heroku:migrate

# Or directly:
heroku run python pythonie/manage.py migrate --settings=pythonie.settings.production
```

The migration `0010_remove_speakers_tables` will:
- Drop `speakers_session_speakers` (M2M table)
- Drop `speakers_session`
- Drop `speakers_speaker`
- Drop `speakers_room`
- Drop `speakers_talkspage`
- Drop `speakers_speakerspage`

### Step 5: Verify Deployment

```bash
# Check application logs
task heroku:logs

# Verify app is running
heroku ps

# Test the website
curl -I https://python.ie

# Verify migration ran
heroku run python pythonie/manage.py showmigrations core --settings=pythonie.settings.production
```

You should see `[X] 0010_remove_speakers_tables` in the output.

### Step 6: Verify Tables Were Dropped

```bash
# Connect to production database
heroku pg:psql

# Check for speakers tables (should return no rows)
\dt speakers_*

# Exit psql
\q
```

## Rollback Procedure

⚠️ **WARNING**: The migration is IRREVERSIBLE by design.

If you need to rollback:

1. **Restore from backup**:
   ```bash
   # List backups
   heroku pg:backups

   # Restore from backup (replace b001 with your backup ID)
   heroku pg:backups:restore b001 DATABASE_URL
   ```

2. **Revert the code**:
   ```bash
   # Rollback Heroku release
   task heroku:rollback

   # Or force push previous commit
   git checkout <previous-commit-sha>
   git push heroku HEAD:master --force
   ```

## Troubleshooting

### Migration fails with "table does not exist"

This is OK if the tables were already manually dropped. The migration uses `DROP TABLE IF EXISTS` so it won't error.

### Application won't start after deployment

Check logs for the specific error:
```bash
task heroku:logs
```

Common issues:
- Missing environment variable
- Database connection issue
- Code import error

### Need to verify migration status

```bash
# Show all migrations and their status
heroku run python pythonie/manage.py showmigrations --settings=pythonie.settings.production
```

## Post-Deployment Cleanup

After successful deployment, clean up your local environment:

```bash
# Remove the worktree
cd /Users/stephane/src/PythonIreland/website
git worktree remove /Users/stephane/src/PythonIreland/pythonie-remove-speakers

# Delete local branch
git branch -d remove-speakers

# Verify worktrees
git worktree list
```

## Migration Details

**File**: `pythonie/core/migrations/0010_remove_speakers_tables.py`

**What it does**:
- Uses raw SQL to drop speakers tables
- Handles CASCADE for foreign key constraints
- Drops tables in correct dependency order
- Is irreversible (raises RuntimeError on reverse)

**Why in core app**:
The speakers app has been completely removed from the codebase, so the migration must live in another app (core was chosen as it's the base app).

## Notes

- This migration does NOT delete data - data should be deleted before running the migration
- The migration is idempotent - safe to run multiple times
- All table drops use CASCADE to handle foreign keys
- The migration cannot be reversed - backup is essential

## Success Criteria

✅ Application deploys successfully
✅ No errors in Heroku logs
✅ Website loads at https://python.ie
✅ Migration 0010_remove_speakers_tables shows as applied
✅ No speakers_* tables exist in database
✅ Admin interface works correctly

## Support

If you encounter issues during deployment:

1. Check Heroku logs: `task heroku:logs`
2. Verify migration status: `heroku run python pythonie/manage.py showmigrations`
3. Restore from backup if needed
4. Contact the development team

---

**Created**: 2026-01-11
**PR**: #161
**Migration**: `core.0010_remove_speakers_tables`
