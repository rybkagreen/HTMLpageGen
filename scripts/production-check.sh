#!/bin/bash

# Production Readiness Check for HTML Page Generator
# This script validates that the system is ready for production deployment

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
PROJECT_DIR=${PROJECT_DIR:-$(pwd)}
REQUIRED_FILES=(
    "docker-compose.prod.yml"
    "backend/Dockerfile.prod"
    "frontend/Dockerfile.prod"
    "nginx/nginx.conf"
    "backend/requirements.txt"
    "scripts/start-production.sh"
    "scripts/stop-production.sh"
    "scripts/health-check.sh"
    "scripts/backup.sh"
    "PRODUCTION_GUIDE.md"
    "DEPLOYMENT.md"
)

REQUIRED_DIRS=(
    "backend/app/core"
    "backend/app/api"
    "frontend/src"
    "scripts"
    "deployment"
    "monitoring"
)

# Check results
PASSED=0
FAILED=0
WARNINGS=0

# Logging
check_log() {
    local status=$1
    local message=$2
    local level=${3:-"INFO"}
    
    case $status in
        "PASS")
            echo -e "${GREEN}✅ PASS${NC}: $message"
            ((PASSED++))
            ;;
        "FAIL")
            echo -e "${RED}❌ FAIL${NC}: $message"
            ((FAILED++))
            ;;
        "WARN")
            echo -e "${YELLOW}⚠️  WARN${NC}: $message"
            ((WARNINGS++))
            ;;
        "INFO")
            echo -e "${BLUE}ℹ️  INFO${NC}: $message"
            ;;
    esac
}

# Check if file exists
check_file() {
    local file=$1
    local description=${2:-$file}
    
    if [ -f "$PROJECT_DIR/$file" ]; then
        check_log "PASS" "File exists: $description"
        return 0
    else
        check_log "FAIL" "Missing file: $description"
        return 1
    fi
}

# Check if directory exists
check_directory() {
    local dir=$1
    local description=${2:-$dir}
    
    if [ -d "$PROJECT_DIR/$dir" ]; then
        check_log "PASS" "Directory exists: $description"
        return 0
    else
        check_log "FAIL" "Missing directory: $description"
        return 1
    fi
}

# Check if command exists
check_command() {
    local cmd=$1
    local description=${2:-$cmd}
    
    if command -v "$cmd" &> /dev/null; then
        check_log "PASS" "Command available: $description"
        return 0
    else
        check_log "FAIL" "Missing command: $description"
        return 1
    fi
}

# Check environment configuration
check_environment() {
    check_log "INFO" "Checking environment configuration..."
    
    # Check if production env example exists
    check_file "backend/.env.production.example" "Production environment template"
    
    # Check if production env is configured (optional)
    if [ -f "$PROJECT_DIR/backend/.env.production" ]; then
        check_log "PASS" "Production environment configured"
        
        # Check for dangerous defaults
        if grep -q "your-secret-key-here" "$PROJECT_DIR/backend/.env.production" 2>/dev/null; then
            check_log "FAIL" "Default SECRET_KEY found in .env.production"
        fi
        
        if grep -q "ENVIRONMENT=development" "$PROJECT_DIR/backend/.env.production" 2>/dev/null; then
            check_log "WARN" "Development environment set in production config"
        fi
        
        if grep -q "DEBUG=true" "$PROJECT_DIR/backend/.env.production" 2>/dev/null; then
            check_log "WARN" "Debug mode enabled in production config"
        fi
    else
        check_log "WARN" "Production environment not configured (.env.production)"
    fi
}

# Check Docker configuration
check_docker() {
    check_log "INFO" "Checking Docker configuration..."
    
    check_command "docker" "Docker"
    check_command "docker-compose" "Docker Compose"
    
    # Check Docker Compose syntax
    if [ -f "$PROJECT_DIR/docker-compose.prod.yml" ]; then
        if docker-compose -f "$PROJECT_DIR/docker-compose.prod.yml" config >/dev/null 2>&1; then
            check_log "PASS" "Docker Compose syntax valid"
        else
            check_log "FAIL" "Docker Compose syntax invalid"
        fi
    fi
    
    # Check Dockerfiles
    for dockerfile in "backend/Dockerfile.prod" "frontend/Dockerfile.prod"; do
        if [ -f "$PROJECT_DIR/$dockerfile" ]; then
            if grep -q "COPY\|ADD" "$PROJECT_DIR/$dockerfile"; then
                check_log "PASS" "Dockerfile has copy instructions: $dockerfile"
            else
                check_log "WARN" "Dockerfile might be incomplete: $dockerfile"
            fi
        fi
    done
}

# Check security configuration
check_security() {
    check_log "INFO" "Checking security configuration..."
    
    # Check nginx configuration
    if [ -f "$PROJECT_DIR/nginx/nginx.conf" ]; then
        if grep -q "ssl_certificate" "$PROJECT_DIR/nginx/nginx.conf"; then
            check_log "PASS" "SSL configuration found in nginx"
        else
            check_log "WARN" "No SSL configuration in nginx.conf"
        fi
        
        if grep -q "security headers" "$PROJECT_DIR/nginx/nginx.conf"; then
            check_log "PASS" "Security headers configured in nginx"
        else
            check_log "WARN" "Security headers not found in nginx.conf"
        fi
    fi
    
    # Check for hardcoded secrets in code
    if grep -r "password\|secret\|key" "$PROJECT_DIR/backend/app" --include="*.py" | grep -v "SECRET_KEY\|password_hash" | head -1 >/dev/null; then
        check_log "WARN" "Potential hardcoded secrets found in code"
    else
        check_log "PASS" "No obvious hardcoded secrets in code"
    fi
}

# Check monitoring and logging
check_monitoring() {
    check_log "INFO" "Checking monitoring and logging configuration..."
    
    # Check logging configuration
    if [ -f "$PROJECT_DIR/backend/app/core/logging.py" ]; then
        check_log "PASS" "Logging configuration exists"
    else
        check_log "FAIL" "Missing logging configuration"
    fi
    
    # Check monitoring configuration
    if [ -f "$PROJECT_DIR/backend/app/core/monitoring.py" ]; then
        check_log "PASS" "Monitoring configuration exists"
    else
        check_log "FAIL" "Missing monitoring configuration"
    fi
    
    # Check Prometheus configuration
    check_file "monitoring/prometheus.yml" "Prometheus configuration"
}

# Check backup and recovery
check_backup() {
    check_log "INFO" "Checking backup and recovery setup..."
    
    if [ -x "$PROJECT_DIR/scripts/backup.sh" ]; then
        check_log "PASS" "Backup script is executable"
    else
        check_log "FAIL" "Backup script not executable or missing"
    fi
    
    # Check if backup script has all required functions
    if [ -f "$PROJECT_DIR/scripts/backup.sh" ]; then
        if grep -q "backup_database\|backup_files\|compress_backup" "$PROJECT_DIR/scripts/backup.sh"; then
            check_log "PASS" "Backup script has required functions"
        else
            check_log "WARN" "Backup script might be incomplete"
        fi
    fi
}

# Check production scripts
check_scripts() {
    check_log "INFO" "Checking production scripts..."
    
    local scripts=(
        "scripts/start-production.sh"
        "scripts/stop-production.sh"
        "scripts/health-check.sh"
        "scripts/backup.sh"
    )
    
    for script in "${scripts[@]}"; do
        if [ -x "$PROJECT_DIR/$script" ]; then
            check_log "PASS" "Script is executable: $script"
        else
            check_log "FAIL" "Script not executable or missing: $script"
        fi
    done
}

# Check dependencies
check_dependencies() {
    check_log "INFO" "Checking dependencies..."
    
    # Check Python dependencies
    if [ -f "$PROJECT_DIR/backend/requirements.txt" ]; then
        if grep -q "fastapi\|uvicorn\|gunicorn" "$PROJECT_DIR/backend/requirements.txt"; then
            check_log "PASS" "Core Python dependencies found"
        else
            check_log "FAIL" "Missing core Python dependencies"
        fi
        
        if grep -q "sentry-sdk\|prometheus-client" "$PROJECT_DIR/backend/requirements.txt"; then
            check_log "PASS" "Production dependencies found"
        else
            check_log "WARN" "Missing production dependencies (sentry, prometheus)"
        fi
    fi
    
    # Check Node.js dependencies
    if [ -f "$PROJECT_DIR/frontend/package.json" ]; then
        if grep -q "next\|react" "$PROJECT_DIR/frontend/package.json"; then
            check_log "PASS" "Core Node.js dependencies found"
        else
            check_log "FAIL" "Missing core Node.js dependencies"
        fi
    fi
}

# Check documentation
check_documentation() {
    check_log "INFO" "Checking documentation..."
    
    local docs=(
        "README.md"
        "PRODUCTION_GUIDE.md"
        "DEPLOYMENT.md"
    )
    
    for doc in "${docs[@]}"; do
        check_file "$doc" "Documentation: $doc"
    done
    
    # Check if CI/CD is configured
    if [ -f "$PROJECT_DIR/.github/workflows/deploy.yml" ]; then
        check_log "PASS" "CI/CD workflow configured"
    else
        check_log "WARN" "No CI/CD workflow found"
    fi
}

# Main check routine
main() {
    echo -e "${BLUE}🔍 Production Readiness Check for HTML Page Generator${NC}"
    echo "========================================================="
    echo "Project Directory: $PROJECT_DIR"
    echo "Date: $(date)"
    echo ""
    
    # Change to project directory
    cd "$PROJECT_DIR"
    
    # Run all checks
    check_log "INFO" "Starting production readiness validation..."
    echo ""
    
    # Check required files
    check_log "INFO" "Checking required files..."
    for file in "${REQUIRED_FILES[@]}"; do
        check_file "$file"
    done
    echo ""
    
    # Check required directories
    check_log "INFO" "Checking required directories..."
    for dir in "${REQUIRED_DIRS[@]}"; do
        check_directory "$dir"
    done
    echo ""
    
    # Run specific checks
    check_environment
    echo ""
    
    check_docker
    echo ""
    
    check_security
    echo ""
    
    check_monitoring
    echo ""
    
    check_backup
    echo ""
    
    check_scripts
    echo ""
    
    check_dependencies
    echo ""
    
    check_documentation
    echo ""
    
    # Summary
    echo "========================================================="
    echo -e "${BLUE}📊 Production Readiness Summary${NC}"
    echo "========================================================="
    echo -e "Passed:   ${GREEN}$PASSED${NC}"
    echo -e "Failed:   ${RED}$FAILED${NC}"
    echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
    echo ""
    
    if [ $FAILED -eq 0 ]; then
        if [ $WARNINGS -eq 0 ]; then
            echo -e "${GREEN}🎉 Production Ready! All checks passed.${NC}"
            echo "The system is ready for production deployment."
        else
            echo -e "${YELLOW}⚠️  Production Ready with Warnings${NC}"
            echo "The system is ready for production but please review the warnings."
        fi
        exit 0
    else
        echo -e "${RED}❌ Not Production Ready${NC}"
        echo "Please fix the failed checks before deploying to production."
        exit 1
    fi
}

# Run with different modes
case "${1:-check}" in
    "check"|"")
        main
        ;;
    "quick")
        # Quick check - only critical files
        echo "Quick production readiness check..."
        failed=0
        for file in "${REQUIRED_FILES[@]}"; do
            if [ ! -f "$PROJECT_DIR/$file" ]; then
                echo "❌ Missing: $file"
                ((failed++))
            fi
        done
        
        if [ $failed -eq 0 ]; then
            echo "✅ Quick check passed"
            exit 0
        else
            echo "❌ Quick check failed ($failed missing files)"
            exit 1
        fi
        ;;
    *)
        echo "Usage: $0 [check|quick]"
        echo "  check - Full production readiness check (default)"
        echo "  quick - Quick check of critical files only"
        exit 1
        ;;
esac
