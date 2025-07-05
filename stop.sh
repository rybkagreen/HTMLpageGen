#!/bin/bash

# 🛑 Скрипт остановки HTMLPageGen
# Корректно завершает все процессы и очищает ресурсы

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✅]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠️]${NC} $1"
}

print_error() {
    echo -e "${RED}[❌]${NC} $1"
}

echo -e "${BLUE}"
echo "🛑 Остановка HTMLPageGen"
echo "======================="
echo -e "${NC}"

print_status "Поиск запущенных процессов..."

# Функция для безопасного завершения процессов
stop_process() {
    local process_name="$1"
    local search_pattern="$2"
    
    local pids=$(ps aux | grep "$search_pattern" | grep -v grep | awk '{print $2}')
    
    if [[ -n "$pids" ]]; then
        print_status "Остановка $process_name..."
        
        # Сначала пробуем мягкое завершение (SIGTERM)
        echo "$pids" | xargs kill -TERM 2>/dev/null || true
        sleep 3
        
        # Проверяем что процессы завершились
        local remaining=$(ps aux | grep "$search_pattern" | grep -v grep | awk '{print $2}')
        
        if [[ -n "$remaining" ]]; then
            print_warning "Принудительное завершение $process_name..."
            echo "$remaining" | xargs kill -KILL 2>/dev/null || true
            sleep 1
        fi
        
        # Финальная проверка
        local final_check=$(ps aux | grep "$search_pattern" | grep -v grep | awk '{print $2}')
        if [[ -z "$final_check" ]]; then
            print_success "$process_name остановлен"
        else
            print_error "Не удалось остановить $process_name"
        fi
    else
        print_warning "$process_name не запущен"
    fi
}

# Остановка Backend (FastAPI/uvicorn)
stop_process "Backend (FastAPI)" "uvicorn app.main:app"

# Остановка Frontend (Next.js)
stop_process "Frontend (Next.js)" "next-server"
stop_process "Frontend (npm)" "npm run dev"

# Дополнительная очистка Node.js процессов
stop_process "Node.js processes" "node.*next"

# Проверка портов
print_status "Проверка освобождения портов..."

# Порт 8000 (Backend)
if nc -z localhost 8000 2>/dev/null; then
    print_warning "Порт 8000 все еще занят"
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
else
    print_success "Порт 8000 освобожден"
fi

# Порт 3000 (Frontend)
if nc -z localhost 3000 2>/dev/null; then
    print_warning "Порт 3000 все еще занят"
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
else
    print_success "Порт 3000 освобожден"
fi

# Очистка временных файлов
print_status "Очистка временных файлов..."

# Удаление старых логов если они большие
if [[ -f "backend.log" ]] && [[ $(stat -f%z "backend.log" 2>/dev/null || stat -c%s "backend.log" 2>/dev/null || echo 0) -gt 10485760 ]]; then
    mv backend.log "backend.log.$(date +%Y%m%d_%H%M%S)"
    print_success "Старый backend.log архивирован"
fi

if [[ -f "frontend.log" ]] && [[ $(stat -f%z "frontend.log" 2>/dev/null || stat -c%s "frontend.log" 2>/dev/null || echo 0) -gt 10485760 ]]; then
    mv frontend.log "frontend.log.$(date +%Y%m%d_%H%M%S)"
    print_success "Старый frontend.log архивирован"
fi

# Очистка кэша Node.js если он слишком большой
if [[ -d "frontend/.next" ]]; then
    NEXT_SIZE=$(du -sm frontend/.next 2>/dev/null | cut -f1)
    if [[ $NEXT_SIZE -gt 500 ]]; then
        print_status "Очистка кэша Next.js ($NEXT_SIZE MB)..."
        rm -rf frontend/.next
        print_success "Кэш Next.js очищен"
    fi
fi

# Проверка активных процессов Python/Node
print_status "Финальная проверка активных процессов..."

PYTHON_PROCS=$(ps aux | grep -E "(python.*uvicorn|uvicorn.*python)" | grep -v grep | wc -l)
NODE_PROCS=$(ps aux | grep -E "(node.*next|next.*node|npm.*dev)" | grep -v grep | wc -l)

if [[ $PYTHON_PROCS -eq 0 ]] && [[ $NODE_PROCS -eq 0 ]]; then
    print_success "Все процессы HTMLPageGen остановлены"
else
    print_warning "Обнаружены остаточные процессы:"
    if [[ $PYTHON_PROCS -gt 0 ]]; then
        echo "  Python/uvicorn: $PYTHON_PROCS"
    fi
    if [[ $NODE_PROCS -gt 0 ]]; then
        echo "  Node.js/Next: $NODE_PROCS"
    fi
fi

# Статистика использования ресурсов
print_status "Статистика ресурсов после остановки..."

MEMORY_USAGE=$(free | awk '/^Mem:/ {printf "%.1f", $3/$2 * 100.0}')
echo -e "${BLUE}  Использование памяти: ${MEMORY_USAGE}%${NC}"

DISK_USAGE=$(df -h . | awk 'NR==2 {print $5}' | sed 's/%//')
DISK_AVAILABLE=$(df -h . | awk 'NR==2 {print $4}')
echo -e "${BLUE}  Использование диска: ${DISK_USAGE}% (свободно: ${DISK_AVAILABLE})${NC}"

# Сводка
echo -e "\n${GREEN}✅ HTMLPageGen полностью остановлен${NC}"

echo -e "\n${BLUE}📋 Полезная информация:${NC}"
echo -e "  🔄 Для запуска снова: ${YELLOW}./start.sh${NC}"
echo -e "  🔍 Для диагностики: ${YELLOW}./diagnose.sh${NC}"
echo -e "  🔧 Логи сохранены в backend.log и frontend.log"

if [[ -f "backend.log" ]] || [[ -f "frontend.log" ]]; then
    echo -e "  📊 Просмотр логов:"
    if [[ -f "backend.log" ]]; then
        echo -e "    - Backend: ${YELLOW}tail backend.log${NC}"
    fi
    if [[ -f "frontend.log" ]]; then
        echo -e "    - Frontend: ${YELLOW}tail frontend.log${NC}"
    fi
fi

# Совет по экономии ресурсов
if (( $(echo "$MEMORY_USAGE > 70" | bc -l) 2>/dev/null )); then
    echo -e "\n${YELLOW}💡 Совет: Высокое использование памяти ($MEMORY_USAGE%)${NC}"
    echo -e "   Рекомендуется перезагрузить систему для освобождения ресурсов"
fi

echo -e "\n${GREEN}👋 До свидания!${NC}\n"
