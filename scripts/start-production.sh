#!/bin/bash

# Production Start Script for HTML Page Generator
# This script starts the application in production mode

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BACKEND_PORT=${BACKEND_PORT:-8000}
FRONTEND_PORT=${FRONTEND_PORT:-3000}
ENVIRONMENT=${ENVIRONMENT:-production}

echo -e "${GREEN}🚀 Starting HTML Page Generator in Production Mode${NC}"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "docker-compose.prod.yml" ]; then
    echo -e "${RED}❌ Error: docker-compose.prod.yml not found${NC}"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Check if .env.production exists
if [ ! -f "backend/.env.production" ]; then
    echo -e "${YELLOW}⚠️  Warning: backend/.env.production not found${NC}"
    echo "Please copy backend/.env.production.example to backend/.env.production and configure it"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Function to check if a service is healthy
check_service_health() {
    local service_name=$1
    local health_url=$2
    local max_attempts=30
    local attempt=1

    echo -e "${YELLOW}🔍 Checking $service_name health...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -f "$health_url" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ $service_name is healthy${NC}"
            return 0
        fi
        
        echo "Attempt $attempt/$max_attempts: $service_name not ready yet..."
        sleep 5
        ((attempt++))
    done
    
    echo -e "${RED}❌ $service_name failed to become healthy${NC}"
    return 1
}

# Build and start services
echo -e "${YELLOW}🏗️  Building and starting services...${NC}"
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for services to be ready
echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"
sleep 10

# Check backend health
if ! check_service_health "Backend API" "http://localhost:$BACKEND_PORT/health"; then
    echo -e "${RED}❌ Backend failed to start properly${NC}"
    echo "Checking logs..."
    docker-compose -f docker-compose.prod.yml logs backend
    exit 1
fi

# Check frontend health
if ! check_service_health "Frontend" "http://localhost:$FRONTEND_PORT"; then
    echo -e "${RED}❌ Frontend failed to start properly${NC}"
    echo "Checking logs..."
    docker-compose -f docker-compose.prod.yml logs frontend
    exit 1
fi

# Check database connection
echo -e "${YELLOW}🔍 Checking database connection...${NC}"
if curl -s "http://localhost:$BACKEND_PORT/health/detailed" | grep -q '"database":{"status":"healthy"'; then
    echo -e "${GREEN}✅ Database connection is healthy${NC}"
else
    echo -e "${YELLOW}⚠️  Database connection might have issues${NC}"
fi

# Display service status
echo ""
echo -e "${GREEN}🎉 HTML Page Generator is running!${NC}"
echo "========================================="
echo -e "Frontend:     ${GREEN}http://localhost:$FRONTEND_PORT${NC}"
echo -e "Backend API:  ${GREEN}http://localhost:$BACKEND_PORT${NC}"
echo -e "API Docs:     ${GREEN}http://localhost:$BACKEND_PORT/docs${NC}"
echo -e "Health Check: ${GREEN}http://localhost:$BACKEND_PORT/health${NC}"
echo -e "Metrics:      ${GREEN}http://localhost:$BACKEND_PORT/metrics${NC}"

if command -v docker-compose &> /dev/null; then
    echo ""
    echo "🔧 Management Commands:"
    echo "  View logs:    docker-compose -f docker-compose.prod.yml logs -f"
    echo "  Stop:         docker-compose -f docker-compose.prod.yml down"
    echo "  Restart:      docker-compose -f docker-compose.prod.yml restart"
    echo "  Update:       ./scripts/deploy.sh"
fi

echo ""
echo -e "${GREEN}✨ Production deployment completed successfully!${NC}"
