#!/bin/bash

# 🚀 Умный скрипт запуска HTMLPageGen
# Автоматически проверяет и исправляет проблемы

# Цвета для красивого вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Функции для вывода
print_logo() {
    echo -e "${PURPLE}"
    cat << "EOF"
    ██╗  ██╗████████╗███╗   ███╗██╗     
    ██║  ██║╚══██╔══╝████╗ ████║██║     
    ███████║   ██║   ██╔████╔██║██║     
    ██╔══██║   ██║   ██║╚██╔╝██║██║     
    ██║  ██║   ██║   ██║ ╚═╝ ██║███████╗
    ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝╚══════╝
    
     PageGen - ИИ Генератор HTML Страниц
EOF
    echo -e "${NC}"
}

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

# Проверка предварительных условий
check_prerequisites() {
    print_status "Проверка системных требований..."
    
    # Проверка WSL
    if [[ ! -f /proc/version ]] || ! grep -q Microsoft /proc/version; then
        print_error "Этот скрипт должен запускаться в WSL (Ubuntu)"
        print_warning "Откройте Ubuntu и попробуйте снова"
        exit 1
    fi
    
    # Проверка директории
    if [[ ! -d "backend" ]] || [[ ! -d "frontend" ]]; then
        print_error "Не найдена структура проекта HTMLPageGen"
        print_warning "Выполните установку: curl -fsSL https://raw.githubusercontent.com/rybkagreen/HTMLpageGen/main/install.sh | bash"
        exit 1
    fi
    
    print_success "Системные требования выполнены"
}

# Проверка и установка зависимостей
check_dependencies() {
    print_status "Проверка зависимостей..."
    
    local missing_deps=0
    
    # Python
    if ! command -v python3 &> /dev/null; then
        print_warning "Python3 не установлен - устанавливаю..."
        sudo apt update -qq && sudo apt install -y python3 python3-pip python3-venv
        ((missing_deps++))
    fi
    
    # Node.js
    if ! command -v node &> /dev/null; then
        print_warning "Node.js не установлен - устанавливаю..."
        curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
        sudo apt install -y nodejs
        ((missing_deps++))
    fi
    
    if [[ $missing_deps -eq 0 ]]; then
        print_success "Все зависимости установлены"
    else
        print_success "Недостающие зависимости установлены"
    fi
}

# Настройка backend
setup_backend() {
    print_status "Настройка Backend..."
    
    cd backend
    
    # Проверка виртуального окружения
    if [[ ! -d "venv" ]]; then
        print_warning "Создание виртуального окружения..."
        python3 -m venv venv
    fi
    
    # Активация окружения
    source venv/bin/activate
    
    # Проверка зависимостей
    if [[ ! -f "venv/pyvenv.cfg" ]] || ! pip list | grep -q fastapi; then
        print_warning "Установка Python зависимостей..."
        pip install --upgrade pip -q
        pip install -r requirements.txt -q
    fi
    
    # Создание .env если отсутствует
    if [[ ! -f ".env" ]]; then
        print_warning "Создание конфигурации Backend..."
        cat > .env << EOF
AI_PROVIDER=local-ai
# Раскомментируйте для использования внешних API:
# DEEPSEEK_API_KEY=sk-your-key-here
# HUGGINGFACE_API_KEY=hf_your-key-here
# OPENAI_API_KEY=sk-your-key-here
EOF
    fi
    
    cd ..
    print_success "Backend настроен"
}

# Настройка frontend
setup_frontend() {
    print_status "Настройка Frontend..."
    
    cd frontend
    
    # Проверка зависимостей
    if [[ ! -d "node_modules" ]] || [[ ! -f "node_modules/.package-lock.json" ]]; then
        print_warning "Установка Node.js зависимостей..."
        npm install --silent
    fi
    
    # Создание .env.local если отсутствует
    if [[ ! -f ".env.local" ]]; then
        print_warning "Создание конфигурации Frontend..."
        cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development
EOF
    fi
    
    cd ..
    print_success "Frontend настроен"
}

# Проверка портов
check_ports() {
    print_status "Проверка портов..."
    
    # Проверка порта 8000 (Backend)
    if nc -z localhost 8000 2>/dev/null; then
        print_warning "Порт 8000 уже используется - останавливаю старые процессы..."
        pkill -f "uvicorn app.main:app" 2>/dev/null || true
        sleep 2
    fi
    
    # Проверка порта 3000 (Frontend)
    if nc -z localhost 3000 2>/dev/null; then
        print_warning "Порт 3000 уже используется - останавливаю старые процессы..."
        pkill -f "next-server" 2>/dev/null || true
        pkill -f "npm run dev" 2>/dev/null || true
        sleep 2
    fi
    
    print_success "Порты свободны"
}

# Запуск backend
start_backend() {
    print_status "Запуск Backend (FastAPI)..."
    
    cd backend
    source venv/bin/activate
    
    # Проверка что FastAPI может запуститься
    if ! python -c "from app.main import app; print('Backend OK')" 2>/dev/null; then
        print_error "Ошибка в коде Backend - проверьте установку"
        cd ..
        return 1
    fi
    
    # Запуск в фоне
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > ../backend.log 2>&1 &
    BACKEND_PID=$!
    
    cd ..
    
    # Ожидание запуска
    print_status "Ожидание запуска Backend..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health >/dev/null 2>&1; then
            print_success "Backend запущен (PID: $BACKEND_PID)"
            return 0
        fi
        sleep 1
        echo -n "."
    done
    
    print_error "Backend не запустился за 30 секунд"
    return 1
}

# Запуск frontend
start_frontend() {
    print_status "Запуск Frontend (Next.js)..."
    
    cd frontend
    
    # Проверка что Next.js может запуститься
    if ! npm run build >/dev/null 2>&1; then
        print_warning "Ошибка сборки - попробуем запустить в dev режиме..."
    fi
    
    # Запуск в фоне
    npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    
    cd ..
    
    # Ожидание запуска
    print_status "Ожидание запуска Frontend..."
    for i in {1..60}; do
        if curl -s http://localhost:3000 >/dev/null 2>&1; then
            print_success "Frontend запущен (PID: $FRONTEND_PID)"
            return 0
        fi
        sleep 1
        echo -n "."
    done
    
    print_error "Frontend не запустился за 60 секунд"
    return 1
}

# Проверка работоспособности
health_check() {
    print_status "Проверка работоспособности..."
    
    # Backend health check
    BACKEND_HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null)
    if [[ $BACKEND_HEALTH == *"healthy"* ]]; then
        print_success "Backend API работает корректно"
    else
        print_warning "Backend API отвечает с ошибками"
    fi
    
    # Frontend check
    if curl -s http://localhost:3000 >/dev/null 2>&1; then
        print_success "Frontend доступен"
    else
        print_warning "Frontend недоступен"
    fi
    
    # AI Provider check
    AI_INFO=$(curl -s http://localhost:8000/api/v1/ai/provider-info 2>/dev/null)
    if [[ $AI_INFO == *"local-ai"* ]]; then
        print_success "AI Provider работает в локальном режиме"
    else
        print_warning "Проблемы с AI Provider"
    fi
}

# Показ информации для пользователя
show_info() {
    echo -e "\n${GREEN}🎉 HTMLPageGen успешно запущен! 🎉${NC}\n"
    
    echo -e "${BLUE}📱 Веб-интерфейс:${NC}"
    echo -e "   🌐 Главная страница: ${YELLOW}http://localhost:3000${NC}"
    echo -e "   🎨 Генератор HTML: ${YELLOW}http://localhost:3000/generator${NC}"
    echo -e "   🤖 ИИ Чат: ${YELLOW}http://localhost:3000/chat${NC}"
    
    echo -e "\n${BLUE}⚙️ API документация:${NC}"
    echo -e "   📚 Swagger UI: ${YELLOW}http://localhost:8000/docs${NC}"
    echo -e "   🔍 Health Check: ${YELLOW}http://localhost:8000/health${NC}"
    
    echo -e "\n${BLUE}📋 Логи:${NC}"
    echo -e "   🔧 Backend: ${YELLOW}tail -f backend.log${NC}"
    echo -e "   🌐 Frontend: ${YELLOW}tail -f frontend.log${NC}"
    
    echo -e "\n${BLUE}🛑 Остановка:${NC}"
    echo -e "   ⌨️ Нажмите ${YELLOW}Ctrl+C${NC} в этом терминале"
    echo -e "   🔧 Или выполните: ${YELLOW}./stop.sh${NC}"
    
    echo -e "\n${PURPLE}💡 Полезные советы:${NC}"
    echo -e "   • Не закрывайте это окно терминала"
    echo -e "   • При первом открытии загрузка может занять 1-2 минуты"
    echo -e "   • Все созданные файлы автоматически скачиваются"
    echo -e "   • В локальном режиме работает без интернета"
    
    echo -e "\n${GREEN}🚀 Начните создавать веб-страницы прямо сейчас!${NC}\n"
}

# Функция очистки при завершении
cleanup() {
    echo -e "\n${YELLOW}🛑 Остановка HTMLPageGen...${NC}"
    
    # Остановка процессов
    if [[ -n $BACKEND_PID ]]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [[ -n $FRONTEND_PID ]]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    # Дополнительная очистка
    pkill -f "uvicorn app.main:app" 2>/dev/null || true
    pkill -f "next-server" 2>/dev/null || true
    pkill -f "npm run dev" 2>/dev/null || true
    
    echo -e "${GREEN}✅ Все сервисы остановлены${NC}"
    echo -e "${BLUE}👋 До свидания!${NC}"
    exit 0
}

# Обработка сигналов
trap cleanup SIGINT SIGTERM

# Основная функция
main() {
    print_logo
    
    print_status "Инициализация HTMLPageGen..."
    
    # Выполнение всех проверок и настроек
    check_prerequisites
    check_dependencies
    setup_backend
    setup_frontend
    check_ports
    
    # Запуск сервисов
    if start_backend && start_frontend; then
        sleep 3  # Даем время на стабилизацию
        health_check
        show_info
        
        # Ожидание завершения
        echo -e "${YELLOW}⏳ Ожидание... (Нажмите Ctrl+C для остановки)${NC}"
        wait
    else
        print_error "Не удалось запустить все сервисы"
        print_status "Проверьте логи: backend.log и frontend.log"
        print_status "Или выполните диагностику: ./diagnose.sh"
        exit 1
    fi
}

# Запуск главной функции
main
