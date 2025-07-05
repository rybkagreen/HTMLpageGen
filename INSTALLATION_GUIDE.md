# Руководство по установке HTMLpageGen

## Системные требования

### Минимальные требования

- **Node.js**: версия 18.0 или выше
- **Python**: версия 3.9 или выше
- **RAM**: минимум 4 GB
- **Свободное место**: 2 GB

### Рекомендуемые требования

- **Node.js**: версия 20.0 или выше
- **Python**: версия 3.11 или выше
- **RAM**: 8 GB или больше
- **Свободное место**: 5 GB

## Предварительная настройка

### 1. Установка Docker (рекомендуется)

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
```

#### macOS

```bash
brew install docker docker-compose
```

#### Windows

Скачайте и установите Docker Desktop с официального сайта.

### 2. Клонирование репозитория

```bash
git clone https://github.com/your-username/HTMLpageGen.git
cd HTMLpageGen
```

## Методы установки

### Метод 1: Docker (Рекомендуется)

#### Быстрый запуск

```bash
# Скопируйте файл конфигурации
cp .env.local.example .env.local

# Запустите все сервисы
docker-compose up -d
```

#### Production деплой

```bash
# Скопируйте production конфигурацию
cp backend/.env.production.example backend/.env.production

# Соберите и запустите production версию
docker-compose -f docker-compose.prod.yml up -d --build
```

### Метод 2: Локальная установка

#### 1. Backend (FastAPI)

```bash
cd backend

# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate     # Windows

# Установите зависимости
pip install -r requirements.txt

# Скопируйте конфигурацию
cp .env.example .env

# Запустите сервер
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Frontend (Next.js)

```bash
cd frontend

# Установите зависимости
npm install

# Скопируйте конфигурацию
cp .env.local.example .env.local

# Запустите в режиме разработки
npm run dev

# Или соберите для production
npm run build
npm start
```

## Настройка переменных окружения

### Backend (.env)

```env
# API настройки
API_V1_STR=/api/v1
PROJECT_NAME=HTMLpageGen

# DeepSeek API
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com

# База данных
DATABASE_URL=postgresql://user:password@localhost:5432/htmlpagegen

# Redis (для кэширования)
REDIS_URL=redis://localhost:6379

# Безопасность
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","https://yourdomain.com"]

# Логирование
LOG_LEVEL=INFO
SENTRY_DSN=your_sentry_dsn_here

# Мониторинг
PROMETHEUS_ENABLED=true
HEALTH_CHECK_ENABLED=true
```

### Frontend (.env.local)

```env
# API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_FRONTEND_URL=http://localhost:3000

# DeepSeek API (для клиентской части)
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Аналитика (опционально)
NEXT_PUBLIC_GA_ID=your_google_analytics_id
NEXT_PUBLIC_SENTRY_DSN=your_sentry_dsn_here

# Режим отладки
NEXT_PUBLIC_DEBUG=false
```

## Получение API ключей

### DeepSeek API

1. Зарегистрируйтесь на [DeepSeek Platform](https://platform.deepseek.com/)
2. Перейдите в раздел API Keys
3. Создайте новый API ключ
4. Скопируйте ключ в переменные окружения

### Дополнительные сервисы (опционально)

- **Sentry**: [sentry.io](https://sentry.io) - для отслеживания ошибок
- **Google Analytics**: [analytics.google.com](https://analytics.google.com) - для аналитики

## Проверка установки

### 1. Проверка backend

```bash
curl http://localhost:8000/health
# Ожидаемый ответ: {"status": "healthy"}
```

### 2. Проверка frontend

Откройте в браузере: http://localhost:3000

### 3. Проверка интеграции

1. Перейдите на страницу генератора
2. Введите простой промпт: "Создай простую страницу с заголовком"
3. Проверьте, что генерация работает

## Решение проблем

### Ошибки установки

#### "Node.js version not supported"

```bash
# Обновите Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### "Python module not found"

```bash
# Убедитесь, что виртуальное окружение активировано
source venv/bin/activate
pip install -r requirements.txt
```

#### "Port already in use"

```bash
# Найдите процесс, использующий порт
lsof -i :3000  # для frontend
lsof -i :8000  # для backend

# Остановите процесс
kill -9 <PID>
```

### Ошибки конфигурации

#### "DeepSeek API key not found"

1. Проверьте, что API ключ правильно указан в .env файлах
2. Убедитесь, что ключ активен на платформе DeepSeek
3. Проверьте лимиты API

#### "Database connection failed"

```bash
# Проверьте, что PostgreSQL запущен
sudo systemctl status postgresql

# Или используйте Docker
docker run -d \
  --name postgres \
  -e POSTGRES_DB=htmlpagegen \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:15
```

### Проблемы производительности

#### Медленная генерация

1. Проверьте интернет-соединение
2. Убедитесь, что DeepSeek API доступен
3. Проверьте лимиты API

#### Высокое использование памяти

1. Уменьшите размер контекста в настройках
2. Очистите кэш браузера
3. Перезапустите сервисы

## Обновление

### Обновление через Git

```bash
git pull origin main

# Backend
cd backend
pip install -r requirements.txt
alembic upgrade head  # если используете миграции

# Frontend
cd frontend
npm install
npm run build
```

### Обновление Docker образов

```bash
docker-compose pull
docker-compose up -d --build
```

## Следующие шаги

После успешной установки:

1. Прочитайте [USER_GUIDE.md](./USER_GUIDE.md) для изучения возможностей
2. Ознакомьтесь с [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) для разработки
3. Изучите [BEST_PRACTICES.md](./BEST_PRACTICES.md) для оптимального использования
4. Посмотрите [EXAMPLES.md](./EXAMPLES.md) для примеров использования

## Поддержка

Если у вас возникли проблемы:

1. Проверьте [FAQ](./FAQ.md)
2. Создайте issue в GitHub репозитории
3. Обратитесь к [документации по разработке](./DEVELOPMENT_STANDARDS.md)

---

_Последнее обновление: Январь 2025_
