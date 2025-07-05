#!/bin/bash

# Health Check Monitor Script for HTML Page Generator
# This script monitors the health of all services and can be used with monitoring systems

set -e

# Configuration
BACKEND_URL=${BACKEND_URL:-"http://localhost:8000"}
FRONTEND_URL=${FRONTEND_URL:-"http://localhost:3000"}
TIMEOUT=${TIMEOUT:-10}
SLACK_WEBHOOK=${SLACK_WEBHOOK:-""}
EMAIL_ALERT=${EMAIL_ALERT:-""}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Health check results
BACKEND_HEALTHY=false
FRONTEND_HEALTHY=false
DATABASE_HEALTHY=false
REDIS_HEALTHY=false

# Function to send alert
send_alert() {
    local message=$1
    local service=$2
    local status=$3
    
    # Log to file
    echo "$(date): $service - $status - $message" >> /var/log/htmlpagegen-health.log
    
    # Send Slack notification if webhook is configured
    if [ ! -z "$SLACK_WEBHOOK" ]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"🚨 HTMLPageGen Alert: $service is $status - $message\"}" \
            "$SLACK_WEBHOOK" >/dev/null 2>&1 || true
    fi
    
    # Send email if configured
    if [ ! -z "$EMAIL_ALERT" ]; then
        echo "$message" | mail -s "HTMLPageGen: $service $status" "$EMAIL_ALERT" >/dev/null 2>&1 || true
    fi
}

# Function to check service health
check_service() {
    local service_name=$1
    local url=$2
    local expected_code=${3:-200}
    
    echo -n "Checking $service_name... "
    
    if response=$(curl -s -w "%{http_code}" -o /dev/null --connect-timeout $TIMEOUT "$url" 2>/dev/null); then
        if [ "$response" -eq "$expected_code" ]; then
            echo -e "${GREEN}✅ Healthy${NC}"
            return 0
        else
            echo -e "${RED}❌ Unhealthy (HTTP $response)${NC}"
            send_alert "HTTP $response received" "$service_name" "UNHEALTHY"
            return 1
        fi
    else
        echo -e "${RED}❌ Unreachable${NC}"
        send_alert "Service unreachable" "$service_name" "DOWN"
        return 1
    fi
}

# Function to check detailed backend health
check_backend_detailed() {
    echo -n "Checking backend detailed health... "
    
    if response=$(curl -s --connect-timeout $TIMEOUT "$BACKEND_URL/health/detailed" 2>/dev/null); then
        # Parse JSON response
        if detailed_result=$(echo "$response" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if data.get('status') == 'healthy':
        checks = data.get('checks', {})
        db_status = checks.get('database', {}).get('status', 'unknown')
        redis_status = checks.get('redis', {}).get('status', 'unknown')
        
        print(f'Database: {db_status}, Redis: {redis_status}')
        
        if db_status == 'healthy' and redis_status == 'healthy':
            print('SUCCESS')
        else:
            print('FAILED')
    else:
        print('FAILED')
except:
    print('ERROR')
" 2>/dev/null); then
            if echo "$detailed_result" | grep -q "SUCCESS"; then
                echo -e "${GREEN}✅ All systems healthy${NC}"
                DATABASE_HEALTHY=true
                REDIS_HEALTHY=true
                return 0
            else
                echo -e "${RED}❌ Some systems unhealthy${NC}"
                echo "$detailed_result"
                return 1
            fi
        else
            echo -e "${RED}❌ Cannot parse detailed health response${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ Cannot reach detailed health endpoint${NC}"
        return 1
    fi
}

# Function to check Docker containers
check_docker_containers() {
    if command -v docker-compose &> /dev/null && [ -f "docker-compose.prod.yml" ]; then
        echo "Checking Docker containers:"
        
        # Get container status
        containers=$(docker-compose -f docker-compose.prod.yml ps --format "table {{.Name}}\t{{.State}}" 2>/dev/null || echo "")
        
        if [ ! -z "$containers" ]; then
            echo "$containers"
            
            # Check if any containers are not running
            if echo "$containers" | grep -v "Up" | grep -q "Exit\|Restarting"; then
                echo -e "${RED}⚠️  Some containers are not running properly${NC}"
                send_alert "Some Docker containers are down" "Docker" "WARNING"
            fi
        else
            echo "No Docker containers found or not using Docker Compose"
        fi
    fi
}

# Function to check system resources
check_system_resources() {
    echo "System Resources:"
    
    # Memory usage
    memory_usage=$(free | grep Mem | awk '{printf "%.1f", ($3/$2) * 100.0}')
    echo "Memory usage: ${memory_usage}%"
    
    if (( $(echo "$memory_usage > 90" | bc -l) )); then
        echo -e "${RED}⚠️  High memory usage: ${memory_usage}%${NC}"
        send_alert "High memory usage: ${memory_usage}%" "System" "WARNING"
    fi
    
    # Disk usage
    disk_usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    echo "Disk usage: ${disk_usage}%"
    
    if [ "$disk_usage" -gt 85 ]; then
        echo -e "${RED}⚠️  High disk usage: ${disk_usage}%${NC}"
        send_alert "High disk usage: ${disk_usage}%" "System" "WARNING"
    fi
    
    # Load average
    load_avg=$(uptime | awk -F'load average:' '{ print $2 }' | cut -d, -f1 | xargs)
    echo "Load average: $load_avg"
}

# Main health check routine
main() {
    echo "=== HTMLPageGen Health Check ===="
    echo "Time: $(date)"
    echo "=================================="
    
    # Check frontend
    if check_service "Frontend" "$FRONTEND_URL"; then
        FRONTEND_HEALTHY=true
    fi
    
    # Check backend basic health
    if check_service "Backend API" "$BACKEND_URL/health"; then
        BACKEND_HEALTHY=true
        
        # Check detailed backend health
        check_backend_detailed
    fi
    
    # Check Docker containers
    check_docker_containers
    
    # Check system resources
    check_system_resources
    
    echo ""
    echo "=== Health Summary ==="
    echo "Frontend: $([ "$FRONTEND_HEALTHY" = true ] && echo -e "${GREEN}Healthy${NC}" || echo -e "${RED}Unhealthy${NC}")"
    echo "Backend:  $([ "$BACKEND_HEALTHY" = true ] && echo -e "${GREEN}Healthy${NC}" || echo -e "${RED}Unhealthy${NC}")"
    echo "Database: $([ "$DATABASE_HEALTHY" = true ] && echo -e "${GREEN}Healthy${NC}" || echo -e "${RED}Unhealthy${NC}")"
    echo "Redis:    $([ "$REDIS_HEALTHY" = true ] && echo -e "${GREEN}Healthy${NC}" || echo -e "${RED}Unhealthy${NC}")"
    
    # Exit with non-zero code if any critical service is down
    if [ "$BACKEND_HEALTHY" = false ] || [ "$FRONTEND_HEALTHY" = false ]; then
        echo ""
        echo -e "${RED}❌ Critical services are down!${NC}"
        exit 1
    else
        echo ""
        echo -e "${GREEN}✅ All critical services are healthy${NC}"
        exit 0
    fi
}

# Run with different modes
case "${1:-check}" in
    "check"|"")
        main
        ;;
    "quiet")
        main >/dev/null 2>&1
        ;;
    "json")
        # Output JSON for monitoring systems
        frontend_status=$(check_service "Frontend" "$FRONTEND_URL" >/dev/null 2>&1 && echo "healthy" || echo "unhealthy")
        backend_status=$(check_service "Backend" "$BACKEND_URL/health" >/dev/null 2>&1 && echo "healthy" || echo "unhealthy")
        
        echo "{
            \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
            \"overall_status\": \"$([ "$frontend_status" = "healthy" ] && [ "$backend_status" = "healthy" ] && echo "healthy" || echo "unhealthy")\",
            \"services\": {
                \"frontend\": \"$frontend_status\",
                \"backend\": \"$backend_status\"
            }
        }"
        ;;
    *)
        echo "Usage: $0 [check|quiet|json]"
        echo "  check  - Full health check with output (default)"
        echo "  quiet  - Silent health check"
        echo "  json   - JSON output for monitoring systems"
        exit 1
        ;;
esac
