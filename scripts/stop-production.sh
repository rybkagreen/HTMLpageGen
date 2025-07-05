#!/bin/bash

# Production Stop Script for HTML Page Generator
# This script safely stops all production services

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🛑 Stopping HTML Page Generator Production Services${NC}"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "docker-compose.prod.yml" ]; then
    echo -e "${RED}❌ Error: docker-compose.prod.yml not found${NC}"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Check if services are running
if ! docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo -e "${YELLOW}⚠️  No running services found${NC}"
    exit 0
fi

# Graceful shutdown with timeout
echo -e "${YELLOW}🔄 Gracefully stopping services...${NC}"
docker-compose -f docker-compose.prod.yml stop

# Remove containers but keep volumes
echo -e "${YELLOW}🗑️  Removing containers...${NC}"
docker-compose -f docker-compose.prod.yml rm -f

# Optional: Clean up unused Docker resources
read -p "Clean up unused Docker resources? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}🧹 Cleaning up unused Docker resources...${NC}"
    docker system prune -f
fi

echo -e "${GREEN}✅ All services stopped successfully${NC}"
echo ""
echo "To start again, run: ./scripts/start-production.sh"
