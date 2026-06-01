#!/bin/bash
# ─────────────────────────────────────────────────────────────
# backup.sh
#
# PURPOSE:
#   Dumps the PostgreSQL database, compresses it, saves it
#   to /backups/ with a timestamp filename, and deletes
#   backups older than 30 days to save disk space.
#
# USAGE:
#   Automatic: Runs daily at 4:00 AM via cron
#   Manual:    docker exec codeboost_backup /backup.sh
# ─────────────────────────────────────────────────────────────

BACKUP_DIR="/backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_FILE="$BACKUP_DIR/codeboost_$DATE.sql.gz"
KEEP_DAYS=30

echo "══════════════════════════════════════"
echo " 🗄️  CodeBoost Database Backup"
echo " 📅 $(date '+%Y-%m-%d %H:%M:%S')"
echo "══════════════════════════════════════"

# Step 1: Check that required environment variables exist
if [ -z "$DB_NAME" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ] || [ -z "$DB_HOST" ]; then
    echo "❌ ERROR: Missing required environment variables!"
    echo "   DB_NAME=$DB_NAME"
    echo "   DB_USER=$DB_USER"
    echo "   DB_HOST=$DB_HOST"
    echo "   DB_PORT=$DB_PORT"
    exit 1
fi

echo "📦 Database : $DB_NAME"
echo "👤 User     : $DB_USER"
echo "🖥️  Host     : $DB_HOST:$DB_PORT"
echo "📁 Output   : $BACKUP_FILE"
echo ""

# Step 2: Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Step 3: Run pg_dump and pipe output through gzip for compression
# PGPASSWORD env var is read automatically by pg_dump — no password prompt
echo "⏳ Starting database dump..."
PGPASSWORD="$DB_PASSWORD" pg_dump \
    -h "$DB_HOST" \
    -p "${DB_PORT:-5432}" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    --no-password \
    --verbose \
    2>/tmp/pg_dump_log.txt | gzip > "$BACKUP_FILE"

# Step 4: Check if backup succeeded
# pg_dump returns exit code 0 on success, non-zero on failure
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    SIZE=$(du -sh "$BACKUP_FILE" | cut -f1)
    echo "✅ Backup successful!"
    echo "   File : $BACKUP_FILE"
    echo "   Size : $SIZE"
else
    echo "❌ Backup FAILED!"
    echo "   Error log:"
    cat /tmp/pg_dump_log.txt
    # Remove the failed/empty backup file
    rm -f "$BACKUP_FILE"
    exit 1
fi

# Step 5: Delete backups older than 30 days to save disk space
echo ""
echo "🧹 Cleaning up backups older than $KEEP_DAYS days..."
DELETED=$(find "$BACKUP_DIR" -name "codeboost_*.sql.gz" -mtime +$KEEP_DAYS -delete -print | wc -l)
echo "   Deleted $DELETED old backup(s)"

# Step 6: Show all current backups
echo ""
echo "📋 Current backups in $BACKUP_DIR:"
ls -lh "$BACKUP_DIR"/*.sql.gz 2>/dev/null || echo "   (no backups found)"

echo ""
echo "══════════════════════════════════════"
echo " ✅ Backup complete!"
echo "══════════════════════════════════════"
