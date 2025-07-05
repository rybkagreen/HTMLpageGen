#!/bin/bash

# Backup Script for HTML Page Generator
# This script creates backups of database, uploads, and configuration

set -e

# Configuration
BACKUP_DIR=${BACKUP_DIR:-"/opt/htmlpagegen/backups"}
RETENTION_DAYS=${RETENTION_DAYS:-30}
PROJECT_DIR=${PROJECT_DIR:-"/opt/htmlpagegen"}
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="htmlpagegen_backup_$DATE"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Logging
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$BACKUP_DIR/backup.log"
}

# Create backup directory
mkdir -p "$BACKUP_DIR"

log "Starting backup: $BACKUP_NAME"

# Create temporary backup directory
TEMP_BACKUP_DIR="$BACKUP_DIR/tmp_$DATE"
mkdir -p "$TEMP_BACKUP_DIR"

# Function to backup database
backup_database() {
    log "Backing up database..."
    
    if docker-compose -f "$PROJECT_DIR/docker-compose.prod.yml" ps postgres | grep -q "Up"; then
        # PostgreSQL backup
        docker-compose -f "$PROJECT_DIR/docker-compose.prod.yml" exec -T postgres pg_dump -U postgres htmlpagegen > "$TEMP_BACKUP_DIR/database.sql"
        log "Database backup completed"
    else
        log "WARNING: PostgreSQL container not running, skipping database backup"
    fi
}

# Function to backup uploads and data
backup_files() {
    log "Backing up files..."
    
    # Backup uploads directory
    if [ -d "$PROJECT_DIR/uploads" ]; then
        cp -r "$PROJECT_DIR/uploads" "$TEMP_BACKUP_DIR/"
        log "Uploads backup completed"
    fi
    
    # Backup configuration files
    mkdir -p "$TEMP_BACKUP_DIR/config"
    cp "$PROJECT_DIR/backend/.env.production" "$TEMP_BACKUP_DIR/config/" 2>/dev/null || log "WARNING: .env.production not found"
    cp "$PROJECT_DIR/docker-compose.prod.yml" "$TEMP_BACKUP_DIR/config/"
    cp -r "$PROJECT_DIR/nginx" "$TEMP_BACKUP_DIR/config/" 2>/dev/null || true
    
    log "Configuration files backup completed"
}

# Function to backup logs
backup_logs() {
    log "Backing up logs..."
    
    mkdir -p "$TEMP_BACKUP_DIR/logs"
    
    # Application logs
    if [ -d "$PROJECT_DIR/logs" ]; then
        cp -r "$PROJECT_DIR/logs"/* "$TEMP_BACKUP_DIR/logs/" 2>/dev/null || true
    fi
    
    # Docker logs
    if command -v docker-compose &> /dev/null; then
        cd "$PROJECT_DIR"
        docker-compose -f docker-compose.prod.yml logs --no-color > "$TEMP_BACKUP_DIR/logs/docker-logs.txt" 2>/dev/null || true
    fi
    
    log "Logs backup completed"
}

# Function to create metadata
create_metadata() {
    log "Creating backup metadata..."
    
    cat > "$TEMP_BACKUP_DIR/backup_info.txt" << EOF
HTMLPageGen Backup Information
=============================
Backup Date: $(date)
Backup Name: $BACKUP_NAME
Hostname: $(hostname)
System: $(uname -a)

Application Status:
$(docker-compose -f "$PROJECT_DIR/docker-compose.prod.yml" ps 2>/dev/null || echo "Docker Compose not available")

Git Information:
$(cd "$PROJECT_DIR" && git log -1 --oneline 2>/dev/null || echo "Git information not available")

Environment:
$(cd "$PROJECT_DIR" && grep -v "SECRET\|PASSWORD\|KEY" backend/.env.production 2>/dev/null || echo "Environment file not found")
EOF
    
    log "Metadata created"
}

# Function to compress backup
compress_backup() {
    log "Compressing backup..."
    
    cd "$BACKUP_DIR"
    tar -czf "$BACKUP_NAME.tar.gz" -C tmp_"$DATE" .
    
    # Verify archive
    if tar -tzf "$BACKUP_NAME.tar.gz" > /dev/null 2>&1; then
        log "Backup compressed successfully: $BACKUP_NAME.tar.gz"
        
        # Calculate size
        SIZE=$(du -h "$BACKUP_NAME.tar.gz" | cut -f1)
        log "Backup size: $SIZE"
        
        # Cleanup temp directory
        rm -rf "$TEMP_BACKUP_DIR"
        
        return 0
    else
        log "ERROR: Backup compression failed"
        return 1
    fi
}

# Function to cleanup old backups
cleanup_old_backups() {
    log "Cleaning up old backups (keeping last $RETENTION_DAYS days)..."
    
    find "$BACKUP_DIR" -name "htmlpagegen_backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete
    
    # Count remaining backups
    BACKUP_COUNT=$(find "$BACKUP_DIR" -name "htmlpagegen_backup_*.tar.gz" | wc -l)
    log "Cleanup completed. $BACKUP_COUNT backups retained"
}

# Function to send notification
send_notification() {
    local status=$1
    local message=$2
    
    # Send to Slack if configured
    if [ ! -z "$SLACK_WEBHOOK" ]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"📦 HTMLPageGen Backup: $status - $message\"}" \
            "$SLACK_WEBHOOK" >/dev/null 2>&1 || true
    fi
    
    # Send email if configured
    if [ ! -z "$EMAIL_ALERT" ]; then
        echo "$message" | mail -s "HTMLPageGen Backup: $status" "$EMAIL_ALERT" >/dev/null 2>&1 || true
    fi
}

# Main backup process
main() {
    echo -e "${YELLOW}🗄️  Starting HTMLPageGen Backup${NC}"
    
    # Check if project directory exists
    if [ ! -d "$PROJECT_DIR" ]; then
        log "ERROR: Project directory not found: $PROJECT_DIR"
        send_notification "FAILED" "Project directory not found"
        exit 1
    fi
    
    cd "$PROJECT_DIR"
    
    # Perform backup steps
    backup_database
    backup_files
    backup_logs
    create_metadata
    
    if compress_backup; then
        cleanup_old_backups
        
        log "Backup completed successfully: $BACKUP_NAME.tar.gz"
        echo -e "${GREEN}✅ Backup completed successfully${NC}"
        send_notification "SUCCESS" "Backup completed: $BACKUP_NAME.tar.gz"
    else
        log "ERROR: Backup failed during compression"
        echo -e "${RED}❌ Backup failed${NC}"
        send_notification "FAILED" "Backup compression failed"
        exit 1
    fi
}

# Handle command line arguments
case "${1:-backup}" in
    "backup"|"")
        main
        ;;
    "list")
        echo "Available backups:"
        ls -lh "$BACKUP_DIR"/htmlpagegen_backup_*.tar.gz 2>/dev/null || echo "No backups found"
        ;;
    "restore")
        if [ -z "$2" ]; then
            echo "Usage: $0 restore <backup_name.tar.gz>"
            echo "Available backups:"
            ls "$BACKUP_DIR"/htmlpagegen_backup_*.tar.gz 2>/dev/null || echo "No backups found"
            exit 1
        fi
        
        BACKUP_FILE="$BACKUP_DIR/$2"
        if [ ! -f "$BACKUP_FILE" ]; then
            echo "Backup file not found: $BACKUP_FILE"
            exit 1
        fi
        
        echo "WARNING: This will restore data and may overwrite current data!"
        read -p "Continue? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log "Starting restore from: $2"
            
            # Extract backup
            RESTORE_DIR="$BACKUP_DIR/restore_$(date +%s)"
            mkdir -p "$RESTORE_DIR"
            tar -xzf "$BACKUP_FILE" -C "$RESTORE_DIR"
            
            echo "Backup extracted to: $RESTORE_DIR"
            echo "Please manually restore the required files and database"
            log "Restore extraction completed: $RESTORE_DIR"
        fi
        ;;
    "cleanup")
        cleanup_old_backups
        ;;
    *)
        echo "Usage: $0 [backup|list|restore|cleanup]"
        echo "  backup   - Create new backup (default)"
        echo "  list     - List available backups"
        echo "  restore  - Restore from backup"
        echo "  cleanup  - Remove old backups"
        exit 1
        ;;
esac
