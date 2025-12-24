# Heroku-24 Migration Script

Automated script to migrate the Python Ireland website from Heroku-22 to Heroku-24 stack, with built-in rollback capabilities.

## Prerequisites

- Heroku CLI installed and authenticated (`heroku login`)
- Git repository with `heroku` remote configured
- Access to the `pythonie` Heroku app
- HEROKU_APP environment variable set (or defaults to `pythonie`)

## Quick Start

### 1. Check Current Status

```bash
./scripts/migrate-heroku-24.sh status
```

This shows:
- Current stack (heroku-22 or heroku-24)
- Available stacks
- PostgreSQL version and status
- Migration readiness

### 2. Run Migration

```bash
./scripts/migrate-heroku-24.sh migrate
```

**What happens:**
1. Creates database and config backups
2. Enables maintenance mode (~5-10 min downtime)
3. Upgrades stack to heroku-24
4. Redeploys the application
5. Runs smoke tests (homepage, admin, logs)
6. Disables maintenance mode
7. Reports success or offers rollback

### 3. Rollback (if needed)

```bash
./scripts/migrate-heroku-24.sh rollback
```

**What happens:**
1. Enables maintenance mode
2. Rolls back to previous Heroku release
3. Reverts stack to heroku-22
4. Redeploys the application
5. Disables maintenance mode

## Features

### ✅ Safety Features

- **Automatic backups**: Database and config saved before migration
- **Confirmation prompts**: Requires explicit confirmation before proceeding
- **Maintenance mode**: App goes into maintenance during migration
- **Smoke tests**: Automatic verification after migration
- **Error handling**: Stops on errors, offers rollback option
- **Detailed logging**: All actions logged to timestamped file

### 📋 Migration Steps

The script performs these steps automatically:

1. **Setup & Verification**
   - Checks Heroku CLI is installed
   - Verifies authentication
   - Confirms app exists

2. **Backup Phase**
   - Creates PostgreSQL backup
   - Saves configuration to file
   - Downloads backup locally

3. **Migration Phase**
   - Enables maintenance mode
   - Creates final backup
   - Upgrades stack to heroku-24
   - Redeploys application

4. **Verification Phase**
   - Waits for deployment stabilization
   - Tests homepage accessibility
   - Tests admin accessibility
   - Checks logs for errors

5. **Completion**
   - Disables maintenance mode
   - Reports success
   - Provides monitoring instructions

## Usage Examples

### Basic migration (uses default app: pythonie)

```bash
./scripts/migrate-heroku-24.sh migrate
```

### Migration for different app

```bash
HEROKU_APP=my-other-app ./scripts/migrate-heroku-24.sh migrate
```

### Check status before migration

```bash
./scripts/migrate-heroku-24.sh status
```

### Emergency rollback

```bash
./scripts/migrate-heroku-24.sh rollback
```

## Output & Logging

All actions are logged to:
```
/tmp/heroku-migration-backups/migration-YYYYMMDD-HHMMSS.log
```

Backups are saved to:
```
/tmp/heroku-migration-backups/backup-YYYYMMDD-HHMMSS.dump
/tmp/heroku-migration-backups/config-YYYYMMDD-HHMMSS.env
```

## What to Monitor After Migration

### Immediate (0-1 hour)

```bash
# Watch logs in real-time
heroku logs --tail -a pythonie

# Check dyno status
heroku ps -a pythonie

# Verify stack
heroku stack -a pythonie
```

### Short-term (1-24 hours)

```bash
# Check metrics
heroku metrics -a pythonie

# Review error rates
heroku logs -a pythonie | grep -i error

# Test critical features
# - Homepage: https://python.ie
# - Admin: https://python.ie/admin/
# - Content pages
```

### Medium-term (24-48 hours)

- Monitor error logs daily
- Check performance metrics
- Verify all business features
- Review CPU/memory usage

## Troubleshooting

### Migration fails during redeploy

The script will automatically offer to rollback. Accept the rollback prompt.

### Smoke tests fail

The script will ask if you want to rollback. You can:
- Accept rollback (recommended)
- Decline and debug manually (app stays in maintenance mode)

### Manual rollback needed

```bash
# Enable maintenance
heroku maintenance:on -a pythonie

# Rollback release
heroku rollback -a pythonie

# Revert stack
heroku stack:set heroku-22 -a pythonie
git push heroku master

# Disable maintenance
heroku maintenance:off -a pythonie
```

### App won't start after migration

1. Check build logs:
   ```bash
   heroku logs --tail -a pythonie
   ```

2. Check for migration errors:
   ```bash
   heroku run python pythonie/manage.py showmigrations -a pythonie
   ```

3. Rollback if needed:
   ```bash
   ./scripts/migrate-heroku-24.sh rollback
   ```

## Exit Codes

- `0` - Success
- `1` - Error occurred (check logs)

## Environment Variables

- `HEROKU_APP` - Heroku application name (default: `pythonie`)

## Security Notes

- Backups contain sensitive data - stored in `/tmp` (auto-cleaned on reboot)
- Config files contain secrets - handle with care
- Clean up old backups regularly

## Support

For issues or questions:
- See full test documentation: `docs/heroku-24-migration-tests.md`
- GitHub issue: #180
- Heroku support: https://help.heroku.com/

## Related Documentation

- [Heroku-24 Stack](https://devcenter.heroku.com/articles/heroku-24-stack)
- [Stack Upgrades](https://devcenter.heroku.com/articles/upgrading-to-the-latest-stack)
- [Python 3.13 on Heroku](https://devcenter.heroku.com/articles/python-support)
