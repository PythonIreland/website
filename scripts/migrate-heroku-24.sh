#!/bin/bash

#######################################################################
# Heroku-22 to Heroku-24 Migration Script
#
# This script handles:
# - Migration from heroku-22 to heroku-24
# - Rollback to heroku-22 in case of issues
# - Pre-migration backups and verification
# - Post-migration smoke tests
#
# Usage:
#   ./scripts/migrate-heroku-24.sh migrate   # Run migration
#   ./scripts/migrate-heroku-24.sh rollback  # Rollback to heroku-22
#   ./scripts/migrate-heroku-24.sh status    # Check current stack
#
# Author: Generated for Python Ireland
# Date: 2025-12-24
#######################################################################

set -euo pipefail

# Configuration
APP_NAME="${HEROKU_APP:-pythonie}"
BACKUP_DIR="/tmp/heroku-migration-backups"
LOG_FILE=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

#######################################################################
# Logging functions
#######################################################################

log() {
    if [[ -n "$LOG_FILE" ]]; then
        echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $*" | tee -a "$LOG_FILE"
    else
        echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $*"
    fi
}

success() {
    if [[ -n "$LOG_FILE" ]]; then
        echo -e "${GREEN}✅ $*${NC}" | tee -a "$LOG_FILE"
    else
        echo -e "${GREEN}✅ $*${NC}"
    fi
}

error() {
    if [[ -n "$LOG_FILE" ]]; then
        echo -e "${RED}❌ ERROR: $*${NC}" | tee -a "$LOG_FILE"
    else
        echo -e "${RED}❌ ERROR: $*${NC}"
    fi
}

warning() {
    if [[ -n "$LOG_FILE" ]]; then
        echo -e "${YELLOW}⚠️  WARNING: $*${NC}" | tee -a "$LOG_FILE"
    else
        echo -e "${YELLOW}⚠️  WARNING: $*${NC}"
    fi
}

#######################################################################
# Setup and verification functions
#######################################################################

setup() {
    mkdir -p "$BACKUP_DIR"
    LOG_FILE="${BACKUP_DIR}/migration-$(date +%Y%m%d-%H%M%S).log"

    log "Setting up migration environment..."

    # Check if heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        error "Heroku CLI is not installed. Please install it first."
        exit 1
    fi

    # Verify authentication
    if ! heroku auth:whoami &> /dev/null; then
        error "Not authenticated with Heroku. Run 'heroku login' first."
        exit 1
    fi

    # Verify app exists
    if ! heroku apps:info -a "$APP_NAME" &> /dev/null; then
        error "App '$APP_NAME' not found. Check HEROKU_APP environment variable."
        exit 1
    fi

    success "Setup complete"
}

get_current_stack() {
    heroku stack -a "$APP_NAME" | grep '^\*' | awk '{print $2}'
}

#######################################################################
# Status check
#######################################################################

status() {
    log "Checking current Heroku stack status..."
    echo ""

    local current_stack
    current_stack=$(get_current_stack)

    log "App: $APP_NAME"
    log "Current stack: $current_stack"

    echo ""
    log "Available stacks:"
    heroku stack -a "$APP_NAME"

    echo ""
    log "PostgreSQL info:"
    heroku pg:info -a "$APP_NAME" | grep -E "Plan:|PG Version:|Status:|Data Size:"

    echo ""
    if [[ "$current_stack" == "heroku-22" ]]; then
        warning "Currently on heroku-22. Ready to migrate to heroku-24."
    elif [[ "$current_stack" == "heroku-24" ]]; then
        success "Already on heroku-24!"
    else
        warning "Currently on $current_stack"
    fi
}

#######################################################################
# Backup functions
#######################################################################

create_backup() {
    log "Creating database backup..."

    heroku pg:backups:capture -a "$APP_NAME"

    local backup_url
    backup_url=$(heroku pg:backups:url -a "$APP_NAME")

    log "Downloading backup to local storage..."
    local backup_file="${BACKUP_DIR}/backup-$(date +%Y%m%d-%H%M%S).dump"
    curl -o "$backup_file" "$backup_url"

    success "Backup created: $backup_file"
    echo "$backup_file"
}

save_config() {
    log "Saving current configuration..."

    local config_file="${BACKUP_DIR}/config-$(date +%Y%m%d-%H%M%S).env"
    heroku config -a "$APP_NAME" --shell > "$config_file"

    success "Configuration saved: $config_file"
    echo "$config_file"
}

#######################################################################
# Migration functions
#######################################################################

enable_maintenance() {
    log "Enabling maintenance mode..."
    heroku maintenance:on -a "$APP_NAME"
    success "Maintenance mode enabled"
}

disable_maintenance() {
    log "Disabling maintenance mode..."
    heroku maintenance:off -a "$APP_NAME"
    success "Maintenance mode disabled"
}

upgrade_stack() {
    local target_stack=$1

    log "Upgrading stack to $target_stack..."
    heroku stack:set "$target_stack" -a "$APP_NAME"
    success "Stack set to $target_stack"
}

redeploy() {
    log "Triggering redeploy..."

    # Get current branch
    local current_branch
    current_branch=$(git branch --show-current)

    # Check if heroku remote exists
    if git remote | grep -q "^heroku$"; then
        log "Pushing to Heroku remote..."
        git push heroku "$current_branch:master"
    else
        error "No 'heroku' git remote found. Add it with: heroku git:remote -a $APP_NAME"
        return 1
    fi

    success "Redeploy complete"
}

smoke_tests() {
    log "Running smoke tests..."

    local app_url
    app_url=$(heroku apps:info -a "$APP_NAME" | grep "Web URL:" | awk '{print $3}')

    log "Testing homepage: $app_url"
    if curl -sSf -o /dev/null "$app_url"; then
        success "Homepage is accessible"
    else
        error "Homepage is not accessible"
        return 1
    fi

    log "Testing admin: ${app_url}admin/"
    if curl -sSf -o /dev/null "${app_url}admin/"; then
        success "Admin is accessible"
    else
        warning "Admin returned error (might require login)"
    fi

    log "Checking for errors in logs..."
    local error_count
    error_count=$(heroku logs -n 100 -a "$APP_NAME" | grep -ic "error" || true)

    if [[ $error_count -gt 0 ]]; then
        warning "Found $error_count error mentions in recent logs"
        log "Recent errors:"
        heroku logs -n 100 -a "$APP_NAME" | grep -i "error" | tail -5
    else
        success "No errors in recent logs"
    fi

    success "Smoke tests complete"
}

#######################################################################
# Migration command
#######################################################################

migrate() {
    log "========================================="
    log "Starting migration to Heroku-24"
    log "========================================="
    echo ""

    setup

    # Check current stack
    local current_stack
    current_stack=$(get_current_stack)

    if [[ "$current_stack" == "heroku-24" ]]; then
        success "Already on heroku-24. No migration needed."
        exit 0
    fi

    if [[ "$current_stack" != "heroku-22" ]]; then
        error "Unexpected stack: $current_stack. This script is for heroku-22 to heroku-24 migration."
        exit 1
    fi

    # Confirmation prompt
    echo ""
    warning "This will migrate $APP_NAME from heroku-22 to heroku-24"
    warning "The app will be in maintenance mode during the migration (~5-10 minutes)"
    echo ""
    read -p "Do you want to proceed? (yes/no): " -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        log "Migration cancelled by user"
        exit 0
    fi

    # Create backups
    log "Step 1/7: Creating backups..."
    local backup_file
    local config_file
    backup_file=$(create_backup)
    config_file=$(save_config)
    echo ""

    # Enable maintenance mode
    log "Step 2/7: Enabling maintenance mode..."
    enable_maintenance
    echo ""

    # Create final backup
    log "Step 3/7: Creating final backup before migration..."
    heroku pg:backups:capture -a "$APP_NAME"
    echo ""

    # Upgrade stack
    log "Step 4/7: Upgrading to heroku-24..."
    upgrade_stack "heroku-24"
    echo ""

    # Redeploy
    log "Step 5/7: Redeploying application..."
    if ! redeploy; then
        error "Redeploy failed! Check logs with: heroku logs --tail -a $APP_NAME"
        warning "App is still in maintenance mode. Fix issues or run rollback."
        exit 1
    fi
    echo ""

    # Wait for deployment
    log "Step 6/7: Waiting for deployment to stabilize..."
    sleep 10
    echo ""

    # Smoke tests
    log "Step 7/7: Running smoke tests..."
    if ! smoke_tests; then
        error "Smoke tests failed!"
        warning "App is still in maintenance mode."
        echo ""
        read -p "Do you want to rollback to heroku-22? (yes/no): " -r
        echo ""

        if [[ $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
            rollback
        else
            warning "Please fix issues manually. App remains in maintenance mode."
            exit 1
        fi
    fi
    echo ""

    # Disable maintenance mode
    log "Disabling maintenance mode..."
    disable_maintenance
    echo ""

    # Success
    log "========================================="
    success "Migration to Heroku-24 completed successfully!"
    log "========================================="
    echo ""
    log "Backups saved to:"
    log "  Database: $backup_file"
    log "  Config: $config_file"
    echo ""
    log "Next steps:"
    log "  1. Monitor logs: heroku logs --tail -a $APP_NAME"
    log "  2. Check metrics: heroku metrics -a $APP_NAME"
    log "  3. Test critical features"
    log "  4. Monitor for 24-48 hours"
    echo ""
    log "Current stack:"
    heroku stack -a "$APP_NAME" | grep '^\*'
}

#######################################################################
# Rollback command
#######################################################################

rollback() {
    log "========================================="
    log "Starting rollback to Heroku-22"
    log "========================================="
    echo ""

    setup

    # Check current stack
    local current_stack
    current_stack=$(get_current_stack)

    if [[ "$current_stack" == "heroku-22" ]]; then
        success "Already on heroku-22. No rollback needed."
        exit 0
    fi

    # Confirmation prompt
    echo ""
    warning "This will rollback $APP_NAME to heroku-22"
    echo ""
    read -p "Do you want to proceed with rollback? (yes/no): " -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        log "Rollback cancelled by user"
        exit 0
    fi

    # Enable maintenance mode (if not already enabled)
    log "Step 1/4: Enabling maintenance mode..."
    enable_maintenance
    echo ""

    # Rollback release
    log "Step 2/4: Rolling back to previous release..."
    heroku rollback -a "$APP_NAME"
    success "Rolled back to previous release"
    echo ""

    # Revert stack
    log "Step 3/4: Reverting stack to heroku-22..."
    upgrade_stack "heroku-22"
    echo ""

    # Redeploy
    log "Step 4/4: Redeploying on heroku-22..."
    if ! redeploy; then
        error "Redeploy failed! Check logs with: heroku logs --tail -a $APP_NAME"
        exit 1
    fi
    echo ""

    # Wait for deployment
    log "Waiting for deployment to stabilize..."
    sleep 10
    echo ""

    # Disable maintenance mode
    log "Disabling maintenance mode..."
    disable_maintenance
    echo ""

    # Success
    log "========================================="
    success "Rollback to Heroku-22 completed successfully!"
    log "========================================="
    echo ""
    log "Current stack:"
    heroku stack -a "$APP_NAME" | grep '^\*'
    echo ""
    log "Please verify the application is working correctly:"
    log "  heroku logs --tail -a $APP_NAME"
}

#######################################################################
# Main entry point
#######################################################################

main() {
    case "${1:-}" in
        migrate)
            migrate
            ;;
        rollback)
            rollback
            ;;
        status)
            setup
            status
            ;;
        *)
            echo "Usage: $0 {migrate|rollback|status}"
            echo ""
            echo "Commands:"
            echo "  migrate   - Migrate from heroku-22 to heroku-24"
            echo "  rollback  - Rollback to heroku-22"
            echo "  status    - Check current stack status"
            echo ""
            echo "Environment variables:"
            echo "  HEROKU_APP - Heroku app name (default: pythonie)"
            echo ""
            echo "Examples:"
            echo "  $0 status"
            echo "  $0 migrate"
            echo "  HEROKU_APP=my-app $0 migrate"
            exit 1
            ;;
    esac
}

main "$@"
