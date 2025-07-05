#!/bin/bash

# 🔍 Скрипт диагностики HTMLPageGen
# Собирает информацию о системе и статусе установки

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# Заголовок
echo -e "${GREEN}"
echo "🔍 Диагностика HTMLPageGen"
echo "=========================="
echo -e "${NC}"

# Системная информация
print_header "Информация о системе"

# WSL проверка
if [[ -f /proc/version ]] && grep -q Microsoft /proc/version; then
    print_success "WSL обнаружен"
    cat /proc/version | head -1
else
    print_error "WSL не обнаружен - запустите в Ubuntu"
fi

# Версия Ubuntu
if [ -f /etc/os-release ]; then
    print_info "Версия ОС:"
    grep PRETTY_NAME /etc/os-release | cut -d'"' -f2
fi

# Проверка программ
print_header "Установленные программы"

# Python
if command -v python3 &> /dev/null; then
    VERSION=$(python3 --version 2>&1)
    print_success "Python: $VERSION"
else
    print_error "Python3 не установлен"
fi

# Node.js
if command -v node &> /dev/null; then
    VERSION=$(node --version 2>&1)
    print_success "Node.js: $VERSION"
else
    print_error "Node.js не установлен"
fi

# npm
if command -v npm &> /dev/null; then
    VERSION=$(npm --version 2>&1)
    print_success "npm: $VERSION"
else
    print_error "npm не установлен"
fi

# Git
if command -v git &> /dev/null; then
    VERSION=$(git --version 2>&1)
    print_success "Git: $VERSION"
else
    print_error "Git не установлен"
fi

# Проверка проекта
print_header "Статус проекта HTMLPageGen"

# Проверка папки проекта
if [ -d "backend" ] && [ -d "frontend" ]; then
    print_success "Структура проекта найдена"
    
    # Backend проверка
    if [ -f "backend/requirements.txt" ]; then
        print_success "Backend: requirements.txt найден"
    else
        print_error "Backend: requirements.txt отсутствует"
    fi
    
    if [ -d "backend/venv" ]; then
        print_success "Backend: виртуальное окружение найдено"
    else
        print_warning "Backend: виртуальное окружение не создано"
    fi
    
    if [ -f "backend/.env" ]; then
        print_success "Backend: конфигурация .env найдена"
    else
        print_warning "Backend: конфигурация .env отсутствует"
    fi
    
    # Frontend проверка
    if [ -f "frontend/package.json" ]; then
        print_success "Frontend: package.json найден"
    else
        print_error "Frontend: package.json отсутствует"
    fi
    
    if [ -d "frontend/node_modules" ]; then
        print_success "Frontend: зависимости установлены"
    else
        print_warning "Frontend: зависимости не установлены"
    fi
    
    if [ -f "frontend/.env.local" ]; then
        print_success "Frontend: конфигурация .env.local найдена"
    else
        print_warning "Frontend: конфигурация .env.local отсутствует"
    fi
    
else
    print_error "Структура проекта не найдена - выполните установку"
fi

# Проверка скриптов
print_header "Скрипты управления"

if [ -f "start.sh" ]; then
    if [ -x "start.sh" ]; then
        print_success "start.sh: найден и исполняемый"
    else
        print_warning "start.sh: найден но не исполняемый"
    fi
else
    print_error "start.sh: отсутствует"
fi

if [ -f "stop.sh" ]; then
    if [ -x "stop.sh" ]; then
        print_success "stop.sh: найден и исполняемый"
    else
        print_warning "stop.sh: найден но не исполняемый"
    fi
else
    print_warning "stop.sh: отсутствует"
fi

# Проверка портов
print_header "Статус сервисов"

# Backend (порт 8000)
if nc -z localhost 8000 2>/dev/null; then
    print_success "Backend: работает на порту 8000"
    
    # Проверка API
    if command -v curl &> /dev/null; then
        HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null)
        if [[ $HEALTH == *"healthy"* ]]; then
            print_success "Backend API: отвечает корректно"
        else
            print_warning "Backend API: отвечает с ошибками"
        fi
    fi
else
    print_warning "Backend: не запущен или не отвечает на порту 8000"
fi

# Frontend (порт 3000)
if nc -z localhost 3000 2>/dev/null; then
    print_success "Frontend: работает на порту 3000"
else
    print_warning "Frontend: не запущен или не отвечает на порту 3000"
fi

# Процессы
print_header "Запущенные процессы"

UVICORN_PROC=$(ps aux | grep -v grep | grep "uvicorn" | wc -l)
if [ $UVICORN_PROC -gt 0 ]; then
    print_success "Найдено $UVICORN_PROC процессов uvicorn (Backend)"
else
    print_warning "Процессы uvicorn не найдены"
fi

NEXT_PROC=$(ps aux | grep -v grep | grep -E "(next-server|npm run dev)" | wc -l)
if [ $NEXT_PROC -gt 0 ]; then
    print_success "Найдено $NEXT_PROC процессов Next.js (Frontend)"
else
    print_warning "Процессы Next.js не найдены"
fi

# Использование ресурсов
print_header "Использование ресурсов"

# Память
MEMORY_TOTAL=$(free -h | awk '/^Mem:/ {print $2}')
MEMORY_USED=$(free -h | awk '/^Mem:/ {print $3}')
MEMORY_PERCENT=$(free | awk '/^Mem:/ {printf "%.1f", $3/$2 * 100.0}')

print_info "Память: $MEMORY_USED / $MEMORY_TOTAL (${MEMORY_PERCENT}%)"

if (( $(echo "$MEMORY_PERCENT > 80" | bc -l) )); then
    print_warning "Высокое использование памяти"
elif (( $(echo "$MEMORY_PERCENT > 90" | bc -l) )); then
    print_error "Критическое использование памяти"
fi

# Место на диске
DISK_USAGE=$(df -h . | awk 'NR==2 {print $5}' | sed 's/%//')
DISK_AVAILABLE=$(df -h . | awk 'NR==2 {print $4}')

print_info "Свободно на диске: $DISK_AVAILABLE"

if [ $DISK_USAGE -gt 90 ]; then
    print_error "Критически мало места на диске ($DISK_USAGE% использовано)"
elif [ $DISK_USAGE -gt 80 ]; then
    print_warning "Мало места на диске ($DISK_USAGE% использовано)"
fi

# Сетевые подключения
print_header "Сетевые соединения"

if command -v curl &> /dev/null; then
    if curl -s --connect-timeout 5 google.com > /dev/null; then
        print_success "Интернет-соединение работает"
    else
        print_warning "Нет интернет-соединения"
    fi
else
    print_warning "curl не установлен - невозможно проверить интернет"
fi

# Рекомендации
print_header "Рекомендации"

# Если программа не запущена
if ! nc -z localhost 8000 2>/dev/null || ! nc -z localhost 3000 2>/dev/null; then
    print_info "Для запуска программы выполните:"
    echo "   ./start.sh"
fi

# Если нет виртуального окружения
if [ ! -d "backend/venv" ]; then
    print_info "Для создания виртуального окружения:"
    echo "   cd backend && python3 -m venv venv"
fi

# Если не установлены зависимости frontend
if [ ! -d "frontend/node_modules" ]; then
    print_info "Для установки зависимостей frontend:"
    echo "   cd frontend && npm install"
fi

# Если высокое использование памяти
if (( $(echo "$MEMORY_PERCENT > 80" | bc -l) )); then
    print_info "Для снижения использования памяти:"
    echo "   - Закройте лишние программы"
    echo "   - Перезапустите браузер"
    echo "   - Перезагрузите компьютер"
fi

# Заключение
print_header "Итоги диагностики"

echo -e "${GREEN}📋 Результаты сохранены в файл diagnosis.log${NC}"
echo -e "${BLUE}📞 При обращении в поддержку приложите этот отчет${NC}"
echo -e "${YELLOW}💡 Для решения проблем см. INSTALLATION_GUIDE_WINDOWS.md${NC}"

echo -e "\n${GREEN}🔍 Диагностика завершена${NC}"

# Сохранение в файл
{
    echo "HTMLPageGen Diagnosis Report"
    echo "Generated: $(date)"
    echo "============================="
    echo
    
    echo "System Information:"
    uname -a
    echo
    
    echo "OS Release:"
    cat /etc/os-release 2>/dev/null || echo "Not available"
    echo
    
    echo "Installed Programs:"
    python3 --version 2>&1 || echo "Python3: Not installed"
    node --version 2>&1 || echo "Node.js: Not installed"
    npm --version 2>&1 || echo "npm: Not installed"
    git --version 2>&1 || echo "Git: Not installed"
    echo
    
    echo "Project Structure:"
    ls -la 2>/dev/null || echo "Not in project directory"
    echo
    
    echo "Running Processes:"
    ps aux | grep -E "(uvicorn|next)" | grep -v grep
    echo
    
    echo "Network Status:"
    netstat -tlnp 2>/dev/null | grep -E "(8000|3000)" || echo "Ports not active"
    echo
    
    echo "Resource Usage:"
    free -h
    df -h .
    echo
    
} > diagnosis.log
