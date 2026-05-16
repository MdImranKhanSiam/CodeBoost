#!/bin/sh
# ─────────────────────────────────────────────────────────────
# PostgreSQL Daily Backup Script
# Runs daily at 2:00 AM
# Keeps last 30 backups (30 days of history)
# Backups stored in /backups/ inside the container
# (mapped to Docker volume: backup_data)
# ─────────────────────────────────────────────────────────────

BACKUP_DIR="/backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_FILE="$BACKUP_DIR/codeboost_backup_$DATE.sql.gz"
KEEP_DAYS=30

echo "──────────────────────────────────────"
echo "🗄️  Starting backup at $DATE"
echo "──────────────────────────────────────"

# Create backup directory if not exists
mkdir -p $BACKUP_DIR

# Dump and compress the database
PGPASSWORD=$DB_PASSWORD pg_dump \
    -h $DB_HOST \
    -p $DB_PORT \
    -U $DB_USER \
    $DB_NAME | gzip > $BACKUP_FILE

# Check if backup was successful
if [ $? -eq 0 ]; then
    SIZE=$(du -sh $BACKUP_FILE | cut -f1)
    echo "✅ Backup successful: $BACKUP_FILE ($SIZE)"
else
    echo "❌ Backup FAILED!"
    exit 1
fi

# Delete backups older than 30 days
echo "🧹 Removing backups older than $KEEP_DAYS days..."
find $BACKUP_DIR -name "*.sql.gz" -mtime +$KEEP_DAYS -delete
echo "📋 Current backups:"
ls -lh $BACKUP_DIR

echo "──────────────────────────────────────"
echo "✅ Backup complete!"
echo "──────────────────────────────────────"

# ─────────────────────────────────────────────────────────────
# Cron schedule: runs every day at 2:00 AM
# Add this line to /var/spool/cron/crontabs/root inside container:
# 0 2 * * * /backup.sh >> /backups/backup.log 2>&1
# ─────────────────────────────────────────────────────────────
