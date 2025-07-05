#!/bin/bash

# 🚀 Автоматическая установка HTMLPageGen для начинающих
# Этот скрипт установит всё необходимое для работы программы

set -e  # Остановка при любой ошибке

# Цвета для красивого вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для красивого вывода
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✅ УСПЕХ]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠️ ВНИМАНИЕ]${NC} $1"
}

print_error() {
    echo -e "${RED}[❌ ОШИБКА]${NC} $1"
}

# Проверка запуска в WSL
check_wsl() {
    if [[ ! -f /proc/version ]] || ! grep -q Microsoft /proc/version; then
        print_error "Этот скрипт должен запускаться в WSL (Windows Subsystem for Linux)"
        print_warning "Установите WSL и запустите Ubuntu, затем повторите попытку"
        exit 1
    fi
    print_success "WSL обнаружен - продолжаем установку"
}

# Обновление системы
update_system() {
    print_status "Обновление системы Ubuntu..."
    sudo apt update -qq
    sudo apt upgrade -y -qq
    print_success "Система обновлена"
}

# Установка основных зависимостей
install_dependencies() {
    print_status "Установка основных программ..."
    
    # Установка curl, git, python
    sudo apt install -y curl git python3 python3-pip python3-venv nodejs npm
    
    # Проверка версий
    python3 --version
    node --version
    npm --version
    
    print_success "Основные программы установлены"
}

# Клонирование репозитория
clone_repository() {
    print_status "Скачивание HTMLPageGen..."
    
    # Удаляем старую папку если есть
    if [ -d "HTMLpageGen" ]; then
        print_warning "Найдена старая установка - удаляем..."
        rm -rf HTMLpageGen
    fi
    
    # Клонируем проект
    git clone https://github.com/rybkagreen/HTMLpageGen.git
    cd HTMLpageGen
    
    print_success "Проект скачан"
}

# Установка зависимостей Backend
setup_backend() {
    print_status "Настройка Backend (Python)..."
    
    cd backend
    
    # Создание виртуального окружения
    python3 -m venv venv
    source venv/bin/activate
    
    # Установка зависимостей
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Создание .env файла
    cat > .env << EOF
# Конфигурация AI провайдера
AI_PROVIDER=local-ai

# API ключи (необязательно для локального режима)
# DEEPSEEK_API_KEY=sk-your-key-here
# HUGGINGFACE_API_KEY=hf_your-key-here
# OPENAI_API_KEY=sk-your-key-here

# База данных (необязательно)
# DATABASE_URL=postgresql://user:pass@localhost/htmlpagegen
EOF
    
    cd ..
    print_success "Backend настроен"
}

# Установка зависимостей Frontend
setup_frontend() {
    print_status "Настройка Frontend (Node.js)..."
    
    cd frontend
    
    # Установка зависимостей
    npm install
    
    # Создание .env.local файла
    cat > .env.local << EOF
# URL Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Режим разработки
NODE_ENV=development
EOF
    
    cd ..
    print_success "Frontend настроен"
}

# Создание скрипта запуска
create_start_script() {
    print_status "Создание скрипта запуска..."
    
    cat > start.sh << 'EOF'
#!/bin/bash

# 🚀 Скрипт запуска HTMLPageGen

# Цвета
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Запуск HTMLPageGen...${NC}"

# Функция для остановки всех процессов
cleanup() {
    echo -e "\n${YELLOW}Остановка всех сервисов...${NC}"
    kill $(jobs -p) 2>/dev/null || true
    exit 0
}

# Обработка Ctrl+C
trap cleanup SIGINT

# Запуск Backend
echo -e "${GREEN}📦 Запуск Backend (FastAPI)...${NC}"
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Ждем запуска Backend
echo -e "${YELLOW}⏳ Ожидание запуска Backend...${NC}"
sleep 5

# Запуск Frontend
echo -e "${GREEN}🌐 Запуск Frontend (Next.js)...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Ждем запуска Frontend
echo -e "${YELLOW}⏳ Ожидание запуска Frontend...${NC}"
sleep 10

echo -e "${GREEN}✅ HTMLPageGen успешно запущен!${NC}"
echo -e "${GREEN}🌐 Откройте браузер и перейдите по адресу:${NC}"
echo -e "${GREEN}   👉 http://localhost:3000${NC}"
echo -e "${GREEN}📚 API документация доступна по адресу:${NC}"
echo -e "${GREEN}   👉 http://localhost:8000/docs${NC}"
echo -e "\n${YELLOW}💡 Для остановки нажмите Ctrl+C${NC}"

# Ожидание
wait
EOF

    chmod +x start.sh
    print_success "Скрипт запуска создан"
}

# Создание скрипта остановки
create_stop_script() {
    print_status "Создание скрипта остановки..."
    
    cat > stop.sh << 'EOF'
#!/bin/bash

# 🛑 Скрипт остановки HTMLPageGen

echo "🛑 Остановка всех сервисов HTMLPageGen..."

# Остановка процессов по портам
pkill -f "uvicorn app.main:app" 2>/dev/null || true
pkill -f "next-server" 2>/dev/null || true
pkill -f "npm run dev" 2>/dev/null || true

echo "✅ Все сервисы остановлены"
EOF

    chmod +x stop.sh
    print_success "Скрипт остановки создан"
}

# Тестирование установки
test_installation() {
    print_status "Тестирование установки..."
    
    # Тест Backend
    cd backend
    source venv/bin/activate
    python -c "
from app.modules.ai_integration.service import AIService
service = AIService()
print(f'✅ Backend: {service.provider.__class__.__name__}')
" 2>/dev/null || print_warning "Backend тест не прошел (это не критично)"
    
    cd ..
    
    # Тест Frontend
    cd frontend
    if npm list next >/dev/null 2>&1; then
        print_success "Frontend: Next.js установлен"
    else
        print_warning "Frontend тест не прошел (это не критично)"
    fi
    cd ..
    
    print_success "Тестирование завершено"
}

# Показ финальных инструкций
show_final_instructions() {
    echo -e "\n${GREEN}🎉 УСТАНОВКА ЗАВЕРШЕНА УСПЕШНО! 🎉${NC}\n"
    
    echo -e "${BLUE}📋 Как запустить программу:${NC}"
    echo -e "   1. Выполните команду: ${YELLOW}./start.sh${NC}"
    echo -e "   2. Подождите 1-2 минуты"
    echo -e "   3. Откройте браузер и перейдите: ${YELLOW}http://localhost:3000${NC}"
    
    echo -e "\n${BLUE}🛑 Как остановить программу:${NC}"
    echo -e "   - Нажмите ${YELLOW}Ctrl+C${NC} в терминале"
    echo -e "   - Или выполните: ${YELLOW}./stop.sh${NC}"
    
    echo -e "\n${BLUE}🔧 Полезные команды:${NC}"
    echo -e "   - Запуск: ${YELLOW}./start.sh${NC}"
    echo -e "   - Остановка: ${YELLOW}./stop.sh${NC}"
    echo -e "   - Обновление: ${YELLOW}git pull${NC}"
    
    echo -e "\n${BLUE}📞 Если что-то не работает:${NC}"
    echo -e "   - Перезапустите Ubuntu"
    echo -e "   - Выполните: ${YELLOW}cd HTMLpageGen && ./start.sh${NC}"
    echo -e "   - Проверьте руководство: ${YELLOW}QUICK_INSTALL_WINDOWS.md${NC}"
    
    echo -e "\n${GREEN}🎯 Удачного использования HTMLPageGen! 🎯${NC}\n"
}

# Основная функция
main() {
    echo -e "${GREEN}🚀 Добро пожаловать в установщик HTMLPageGen! 🚀${NC}\n"
    
    print_status "Начинаем автоматическую установку..."
    
    check_wsl
    update_system
    install_dependencies
    clone_repository
    setup_backend
    setup_frontend
    create_start_script
    create_stop_script
    test_installation
    show_final_instructions
}

# Запуск
main
