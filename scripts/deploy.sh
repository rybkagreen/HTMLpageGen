#!/bin/bash

# Production deployment script for HTML Page Generator

set -e

echo "🚀 Starting production deployment..."

# Configuration
DOCKER_COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env.production"
BACKUP_DIR="./backups"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_requirements() {
    log_info "Checking requirements..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed!"
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed!"
        exit 1
    fi
    
    # Check if environment file exists
    if [ ! -f "$ENV_FILE" ]; then
        log_error "Environment file $ENV_FILE not found!"
        log_info "Please copy .env.production.example to $ENV_FILE and configure it"
        exit 1
    fi
    
    log_info "Requirements check passed ✅"
}

backup_database() {
    log_info "Creating database backup..."
    
    mkdir -p "$BACKUP_DIR"
    
    # Create backup with timestamp
    BACKUP_FILE="$BACKUP_DIR/db_backup_$(date +%Y%m%d_%H%M%S).sql"
    
    # Check if database container is running
    if docker-compose -f $DOCKER_COMPOSE_FILE ps postgres | grep -q "Up"; then
        docker-compose -f $DOCKER_COMPOSE_FILE exec -T postgres \
            pg_dump -U htmlpagegen htmlpagegen_prod > "$BACKUP_FILE"
        log_info "Database backup created: $BACKUP_FILE"
    else
        log_warn "Database container not running, skipping backup"
    fi
}

deploy() {
    log_info "Deploying application..."
    
    # Pull latest images
    log_info "Pulling latest images..."
    docker-compose -f $DOCKER_COMPOSE_FILE pull
    
    # Build application image
    log_info "Building application..."
    docker-compose -f $DOCKER_COMPOSE_FILE build app
    
    # Start services
    log_info "Starting services..."
    docker-compose -f $DOCKER_COMPOSE_FILE up -d
    
    # Wait for services to be healthy
    log_info "Waiting for services to be healthy..."
    sleep 30
    
    # Check health
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log_info "Application is healthy ✅"
    else
        log_error "Application health check failed!"
        log_info "Check logs with: docker-compose -f $DOCKER_COMPOSE_FILE logs app"
        exit 1
    fi
}

cleanup() {
    log_info "Cleaning up old images..."
    docker image prune -f
    log_info "Cleanup completed"
}

show_status() {
    log_info "Service status:"
    docker-compose -f $DOCKER_COMPOSE_FILE ps
    
    echo ""
    log_info "Application URLs:"
    echo "  - API: https://yourdomain.com/api/v1/docs"
    echo "  - Health: https://yourdomain.com/health"
    echo "  - Metrics: https://yourdomain.com/metrics"
    echo "  - Grafana: http://yourdomain.com:3001"
}

# Main execution
case "${1:-deploy}" in
    "check")
        check_requirements
        ;;
    "backup")
        backup_database
        ;;
    "deploy")
        check_requirements
        backup_database
        deploy
        cleanup
        show_status
        ;;
    "status")
        show_status
        ;;
    "logs")
        docker-compose -f $DOCKER_COMPOSE_FILE logs -f app
        ;;
    "stop")
        log_info "Stopping services..."
        docker-compose -f $DOCKER_COMPOSE_FILE down
        ;;
    "restart")
        log_info "Restarting services..."
        docker-compose -f $DOCKER_COMPOSE_FILE restart
        ;;
    *)
        echo "Usage: $0 {check|backup|deploy|status|logs|stop|restart}"
        echo ""
        echo "Commands:"
        echo "  check   - Check deployment requirements"
        echo "  backup  - Create database backup"
        echo "  deploy  - Full deployment (default)"
        echo "  status  - Show service status"
        echo "  logs    - Show application logs"
        echo "  stop    - Stop all services"
        echo "  restart - Restart all services"
        exit 1
        ;;
esac

log_info "Operation completed successfully! 🎉"
