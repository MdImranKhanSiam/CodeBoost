#!/bin/bash

# =============================================================================
# CodeBoost — PostgreSQL Nightly Backup Script
# Stored at: /opt/codeboost/backup_db.sh   (OUTSIDE the git repo)
# Cron runs this every night at 4:00 AM.
# =============================================================================

# ── Configuration ─────────────────────────────────────────────────────────────

# Your project directory (where docker-compose.yml and .env live)
PROJECT_DIR="/var/www/codeboost"

# Where backup files are stored — OUTSIDE the repo so git pull never touches them
BACKUP_DIR="/opt/codeboost/backups"

# Log file — also outside the repo
LOG_FILE="/opt/codeboost/backup.log"

# Must match container_name in your docker-compose.yml
DB_CONTAINER="codeboost_db"

# Source of DB credentials (reads DB_NAME, DB_USER from your existing .env)
ENV_FILE="${PROJECT_DIR}/.env"

# Days of backups to keep
RETENTION_DAYS=7

# ── Ensure Docker is on PATH (cron has a minimal environment) ─────────────────

export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# ── Ensure backup directory exists ───────────────────────────────────────────

mkdir -p "$BACKUP_DIR"

# ── Load .env ────────────────────────────────────────────────────────────────

if [ ! -f "$ENV_FILE" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: .env not found at $ENV_FILE" | tee -a "$LOG_FILE"
    exit 1
fi

export $(grep -v '^\s*#' "$ENV_FILE" | grep -v '^\s*$' | xargs)

if [ -z "$DB_NAME" ] || [ -z "$DB_USER" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: DB_NAME or DB_USER missing in .env" | tee -a "$LOG_FILE"
    exit 1
fi

# ── Generate timestamped backup filename ──────────────────────────────────────

TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
BACKUP_FILE="${BACKUP_DIR}/codeboost_db_${TIMESTAMP}.sql.gz"

# ── Run pg_dump inside the live PostgreSQL container ─────────────────────────

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting backup → $BACKUP_FILE" | tee -a "$LOG_FILE"

docker exec "$DB_CONTAINER" \
    pg_dump -U "$DB_USER" "$DB_NAME" \
    | gzip > "$BACKUP_FILE"

# ── Verify the backup succeeded and is non-empty ──────────────────────────────

if [ $? -eq 0 ] && [ -s "$BACKUP_FILE" ]; then
    FILESIZE=$(du -sh "$BACKUP_FILE" | cut -f1)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS: Backup saved ($FILESIZE) → $BACKUP_FILE" | tee -a "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Backup failed or produced an empty file." | tee -a "$LOG_FILE"
    rm -f "$BACKUP_FILE"
    exit 1
fi

# ── Rotate: delete backups older than RETENTION_DAYS ─────────────────────────

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Cleaning up backups older than ${RETENTION_DAYS} days..." | tee -a "$LOG_FILE"
find "$BACKUP_DIR" -name "codeboost_db_*.sql.gz" -mtime +${RETENTION_DAYS} -exec rm -f {} \;

REMAINING=$(ls "$BACKUP_DIR" | wc -l)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Done. ${REMAINING} backup(s) retained." | tee -a "$LOG_FILE"
echo "────────────────────────────────────────────────────────────────────────────" | tee -a "$LOG_FILE"
