#!/bin/bash
set -euo pipefail

PROJECT_DIR="/var/www/sagalhaider-com"
DB_FILE="$PROJECT_DIR/db.sqlite3"
BACKUP_DIR="$PROJECT_DIR/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=14

mkdir -p "$BACKUP_DIR"

if [ ! -f "$DB_FILE" ]; then
    echo "DB file not found: $DB_FILE" >&2
    exit 1
fi

sqlite3 "$DB_FILE" ".backup '$BACKUP_DIR/db_$TIMESTAMP.sqlite3'"

# Garde seulement les 14 derniers jours de sauvegardes
find "$BACKUP_DIR" -name "db_*.sqlite3" -mtime +$RETENTION_DAYS -delete

echo "Backup OK: $BACKUP_DIR/db_$TIMESTAMP.sqlite3"
