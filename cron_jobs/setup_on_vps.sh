#!/bin/bash

# =============================================================================
# CodeBoost — One-Time VPS Setup Script
# Run this ONCE on your VPS after cloning the repo.
#
# What it does:
#   1. Creates /opt/codeboost/ with correct permissions
#   2. Copies backup_db.sh and restore_db.sh there from the repo
#   3. Makes scripts executable
#   4. Registers the nightly 4 AM cron job
# =============================================================================

REPO_DIR="/var/www/codeboost"
INSTALL_DIR="/opt/codeboost"
BACKUP_SCRIPT="${INSTALL_DIR}/backup_db.sh"

echo "══════════════════════════════════════════════════"
echo "  CodeBoost — Backup System Setup"
echo "══════════════════════════════════════════════════"
echo ""

# ── Step 1: Create /opt/codeboost/ ───────────────────────────────────────────

echo "📁 Creating ${INSTALL_DIR}..."
mkdir -p "${INSTALL_DIR}/backups"
echo "   ✅ ${INSTALL_DIR}/ created"
echo "   ✅ ${INSTALL_DIR}/backups/ created"
echo ""

# ── Step 2: Copy scripts out of the repo into /opt/codeboost/ ────────────────

echo "📋 Installing scripts to ${INSTALL_DIR}..."
cp "${REPO_DIR}/cron_jobs/backup_db.sh"  "${INSTALL_DIR}/backup_db.sh"
cp "${REPO_DIR}/cron_jobs/restore_db.sh" "${INSTALL_DIR}/restore_db.sh"
echo "   ✅ backup_db.sh  → ${INSTALL_DIR}/backup_db.sh"
echo "   ✅ restore_db.sh → ${INSTALL_DIR}/restore_db.sh"
echo ""

# ── Step 3: Make scripts executable ──────────────────────────────────────────

echo "🔑 Setting execute permissions..."
chmod +x "${INSTALL_DIR}/backup_db.sh"
chmod +x "${INSTALL_DIR}/restore_db.sh"
echo "   ✅ chmod +x applied"
echo ""

# ── Step 4: Test the backup script before registering cron ───────────────────

echo "🧪 Running a test backup now to verify everything works..."
echo "──────────────────────────────────────────────────────────"
"${INSTALL_DIR}/backup_db.sh"
RESULT=$?
echo "──────────────────────────────────────────────────────────"
echo ""

if [ $RESULT -ne 0 ]; then
    echo "❌ Test backup FAILED. Fix the error above before continuing."
    echo "   The cron job was NOT installed."
    exit 1
fi

echo "✅ Test backup succeeded!"
echo ""

# ── Step 5: Register the cron job ────────────────────────────────────────────

CRON_JOB="0 4 * * * ${BACKUP_SCRIPT} >> ${INSTALL_DIR}/backup.log 2>&1"

echo "⏰ Installing cron job..."

if crontab -l 2>/dev/null | grep -qF "$BACKUP_SCRIPT"; then
    echo "   ✅ Cron job already exists — no changes made."
else
    (crontab -l 2>/dev/null; echo ""; echo "# CodeBoost nightly DB backup (4 AM)"; echo "$CRON_JOB") | crontab -
    echo "   ✅ Cron job installed."
fi

echo ""
echo "══════════════════════════════════════════════════"
echo "  ✅ Setup complete!"
echo "══════════════════════════════════════════════════"
echo ""
echo "  Scripts installed : ${INSTALL_DIR}/"
echo "  Backups stored in : ${INSTALL_DIR}/backups/"
echo "  Log file          : ${INSTALL_DIR}/backup.log"
echo "  Schedule          : Every night at 4:00 AM (server time)"
echo ""
echo "  These locations are OUTSIDE your git repo."
echo "  Git pulls and deployments will NEVER affect them."
echo ""
echo "  Current crontab:"
crontab -l
echo ""
