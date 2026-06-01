#!/bin/bash
# ─────────────────────────────────────────────────────────────
# backup-entrypoint.sh
#
# PURPOSE:
#   Docker containers don't pass environment variables to cron
#   jobs automatically. This script solves that by:
#   1. Saving all DB-related env vars to a file (/etc/db_env)
#   2. Setting up the cron job to source that file before running
#   3. Starting crond in the foreground so the container stays alive
# ─────────────────────────────────────────────────────────────

echo "──────────────────────────────────────"
echo " CodeBoost Backup Service Starting..."
echo "──────────────────────────────────────"

# Step 1: Save environment variables to a file
# Cron runs in a clean environment so it can't see Docker env vars.
# We dump the relevant vars to /etc/db_env so the cron job can load them.
echo "📋 Saving environment variables for cron..."
printenv | grep -E "^(DB_NAME|DB_USER|DB_PASSWORD|DB_HOST|DB_PORT)" > /etc/db_env
chmod 600 /etc/db_env  # Secure the file — only root can read it
echo "✅ Environment variables saved to /etc/db_env"

# Step 2: Create the cron job
# Runs every day at 4:00 AM
# ". /etc/db_env" loads the saved environment variables before running backup
echo "⏰ Setting up cron job (runs daily at 4:00 AM)..."
echo "0 4 * * * . /etc/db_env; /backup.sh >> /backups/backup.log 2>&1" > /var/spool/cron/crontabs/root
chmod 600 /var/spool/cron/crontabs/root
echo "✅ Cron job created"

# Step 3: Ensure backups directory exists
mkdir -p /backups

echo ""
echo "──────────────────────────────────────"
echo " ✅ Backup service ready!"
echo " 📅 Automatic backup: Every day at 4:00 AM"
echo " 📁 Backup location: /backups/"
echo " 🔧 Manual backup: docker exec codeboost_backup /backup.sh"
echo "──────────────────────────────────────"
echo ""

# Step 4: Start crond in foreground
# -f = run in foreground (keeps container alive)
# -l 8 = log level (8 = only errors, keeps logs clean)
exec crond -f -l 8
