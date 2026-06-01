#!/bin/bash

# =============================================================================
# CodeBoost — Database Restore Script
# Stored at: /opt/codeboost/restore_db.sh   (OUTSIDE the git repo)
#
# Usage:
#   /opt/codeboost/restore_db.sh <path-to-backup.sql.gz>
#
# Example:
#   /opt/codeboost/restore_db.sh /opt/codeboost/backups/codeboost_db_2025-07-01_04-00-00.sql.gz
# =============================================================================

export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

PROJECT_DIR="/var/www/codeboost"
DB_CONTAINER="codeboost_db"
ENV_FILE="${PROJECT_DIR}/.env"
BACKUP_DIR="/opt/codeboost/backups"

# ── Validate argument ─────────────────────────────────────────────────────────

if [ -z "$1" ]; then
    echo "❌ ERROR: No backup file specified."
    echo ""
    echo "Usage:   /opt/codeboost/restore_db.sh <path-to-backup.sql.gz>"
    echo ""
    echo "Available backups:"
    ls -lh "$BACKUP_DIR" 2>/dev/null || echo "  (no backups found)"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ ERROR: File not found: $BACKUP_FILE"
    exit 1
fi

# ── Load .env ────────────────────────────────────────────────────────────────

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ ERROR: .env not found at $ENV_FILE"
    exit 1
fi

export $(grep -v '^\s*#' "$ENV_FILE" | grep -v '^\s*$' | xargs)

# ── Confirmation prompt ───────────────────────────────────────────────────────

echo "══════════════════════════════════════════════════════"
echo "  ⚠️  DATABASE RESTORE — THIS WILL OVERWRITE DATA ⚠️"
echo "══════════════════════════════════════════════════════"
echo ""
echo "  Database  : $DB_NAME"
echo "  Container : $DB_CONTAINER"
echo "  Backup    : $BACKUP_FILE"
echo ""
echo "  All existing data will be replaced. Irreversible."
echo ""
read -p "  Type 'yes' to continue: " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo ""
    echo "🚫 Restore cancelled."
    exit 0
fi

echo ""
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restoring from: $BACKUP_FILE"

gunzip -c "$BACKUP_FILE" | docker exec -i "$DB_CONTAINER" \
    psql -U "$DB_USER" -d "$DB_NAME"

if [ $? -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Restore completed successfully."
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Restore FAILED. Check output above."
    exit 1
fi
