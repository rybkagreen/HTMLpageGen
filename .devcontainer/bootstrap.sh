#!/bin/bash

# DevContainer Bootstrap Script
# Автоматическая настройка окружения для AI Construction Ecosystem

set -e

echo "🚀 Starting DevContainer Bootstrap Process..."

# Обновление системы
echo "📦 Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Установка дополнительных системных пакетов
echo "🔧 Installing system dependencies..."
sudo apt-get install -y \
    curl \
    wget \
    vim \
    htop \
    tree \
    jq \
    unzip \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev

# Установка PostgreSQL клиента
echo "🐘 Installing PostgreSQL client..."
sudo apt-get install -y postgresql-client

# Установка Redis CLI
echo "📊 Installing Redis CLI..."
sudo apt-get install -y redis-tools

# Установка и настройка pnpm
echo "📦 Installing and configuring pnpm..."
curl -fsSL https://get.pnpm.io/install.sh | sh
export PNPM_HOME="/home/vscode/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"
echo 'export PNPM_HOME="/home/vscode/.local/share/pnpm"' >> ~/.bashrc
echo 'export PATH="$PNPM_HOME:$PATH"' >> ~/.bashrc
echo 'export PNPM_HOME="/home/vscode/.local/share/pnpm"' >> ~/.zshrc
echo 'export PATH="$PNPM_HOME:$PATH"' >> ~/.zshrc

# Глобальная установка полезных npm пакетов
echo "🛠️ Installing global npm packages..."
npm install -g \
    @nestjs/cli \
    prisma \
    nx \
    typescript \
    ts-node \
    nodemon \
    pm2 \
    eslint \
    prettier \
    @angular/cli \
    @vue/cli \
    create-react-app \
    vite

# Установка Python пакетов
echo "🐍 Installing Python packages..."
pip3 install --user \
    pipenv \
    poetry \
    black \
    pylint \
    flake8 \
    mypy \
    pytest \
    jupyter \
    pandas \
    numpy \
    requests \
    fastapi \
    uvicorn \
    pydantic \
    sqlalchemy \
    alembic \
    psycopg2-binary \
    redis

# Настройка Git (если еще не настроен)
echo "🔐 Configuring Git..."
if [ -z "$(git config --global user.name)" ]; then
    echo "⚠️  Git user.name not set. Please configure it manually:"
    echo "   git config --global user.name 'Your Name'"
fi

if [ -z "$(git config --global user.email)" ]; then
    echo "⚠️  Git user.email not set. Please configure it manually:"
    echo "   git config --global user.email 'your.email@example.com'"
fi

# Настройка Git для лучшей работы
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.autocrlf input
git config --global core.editor "code --wait"

# Создание структуры директорий для проекта
echo "📁 Creating project directory structure..."
mkdir -p \
    apps \
    libs/shared-contracts/src \
    services \
    tools \
    scripts \
    docs \
    tests \
    docker \
    config

# Создание базовых файлов окружения
echo "⚙️ Creating environment files..."

# .env.example
cat > .env.example << 'EOL'
# Database Configuration
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/ez_eco_dev"
DATABASE_HOST="localhost"
DATABASE_PORT="5432"
DATABASE_NAME="ez_eco_dev"
DATABASE_USER="postgres"
DATABASE_PASSWORD="postgres"

# Redis Configuration
REDIS_URL="redis://localhost:6379"
REDIS_HOST="localhost"
REDIS_PORT="6379"

# JWT Configuration
JWT_SECRET="your-super-secret-jwt-key-here"
JWT_EXPIRES_IN="24h"
JWT_REFRESH_EXPIRES_IN="7d"

# Application Configuration
NODE_ENV="development"
PORT="3000"
API_PREFIX="api/v1"

# Services Ports
AUTH_SERVICE_PORT="3002"
CONSTRUCTION_OBJECTS_SERVICE_PORT="3003"
USER_PROFILE_SERVICE_PORT="3004"
CONTRACTS_MANAGEMENT_SERVICE_PORT="3005"
API_GATEWAY_PORT="3001"

# External APIs
EXTERNAL_API_URL=""
EXTERNAL_API_KEY=""

# File Upload
MAX_FILE_SIZE="10485760"
UPLOAD_PATH="./uploads"

# Logging
LOG_LEVEL="debug"
LOG_FORMAT="json"

# CORS
CORS_ORIGIN="http://localhost:3000"
CORS_CREDENTIALS="true"
EOL

# .env (копия для разработки)
cp .env.example .env

# Создание docker-compose для локальной разработки
echo "🐳 Creating Docker Compose configuration..."
cat > docker-compose.dev.yml << 'EOL'
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: ez_eco_postgres
    environment:
      POSTGRES_DB: ez_eco_dev
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    container_name: ez_eco_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: ez_eco_pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
      PGADMIN_CONFIG_SERVER_MODE: 'False'
    ports:
      - "8080:80"
    depends_on:
      - postgres
    volumes:
      - pgadmin_data:/var/lib/pgadmin

volumes:
  postgres_data:
  redis_data:
  pgadmin_data:
EOL

# Создание базовой инициализации БД
mkdir -p docker/postgres
cat > docker/postgres/init.sql << 'EOL'
-- Создание базы данных для разработки
CREATE DATABASE ez_eco_dev;

-- Создание базы данных для тестов
CREATE DATABASE ez_eco_test;

-- Подключение к базе разработки
\c ez_eco_dev;

-- Создание расширений
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Создание пользователя для приложения (опционально)
-- CREATE USER ez_eco_user WITH PASSWORD 'ez_eco_password';
-- GRANT ALL PRIVILEGES ON DATABASE ez_eco_dev TO ez_eco_user;
EOL

# Создание скриптов для управления проектом
echo "📜 Creating project management scripts..."
mkdir -p scripts

cat > scripts/dev-setup.sh << 'EOL'
#!/bin/bash
# Скрипт для быстрой настройки окружения разработки

echo "🚀 Setting up development environment..."

# Установка зависимостей
if [ -f "package.json" ]; then
    echo "📦 Installing npm dependencies..."
    pnpm install
fi

# Запуск базы данных
echo "🐳 Starting database services..."
docker-compose -f docker-compose.dev.yml up -d postgres redis

# Ожидание готовности базы данных
echo "⏳ Waiting for database to be ready..."
sleep 10

# Генерация Prisma клиента
if [ -f "prisma/schema.prisma" ]; then
    echo "🗄️ Generating Prisma client..."
    npx prisma generate
    
    echo "🔄 Running database migrations..."
    npx prisma db push
fi

echo "✅ Development environment is ready!"
echo "📝 Available commands:"
echo "  - pnpm dev: Start development server"
echo "  - pnpm build: Build application"
echo "  - pnpm test: Run tests"
echo "  - docker-compose -f docker-compose.dev.yml up: Start all services"
EOL

cat > scripts/cleanup.sh << 'EOL'
#!/bin/bash
# Скрипт для очистки окружения

echo "🧹 Cleaning up development environment..."

# Остановка Docker контейнеров
echo "🐳 Stopping Docker services..."
docker-compose -f docker-compose.dev.yml down

# Очистка node_modules и lock файлов
echo "📦 Cleaning node modules..."
rm -rf node_modules
rm -f package-lock.json
rm -f yarn.lock
rm -f pnpm-lock.yaml

# Очистка build артефактов
echo "🔨 Cleaning build artifacts..."
rm -rf dist
rm -rf build
rm -rf .next
rm -rf .nx

echo "✅ Cleanup completed!"
EOL

# Сделать скрипты исполняемыми
chmod +x scripts/*.sh

# Настройка Zsh с полезными alias'ами
echo "🐚 Configuring shell aliases..."
cat >> ~/.zshrc << 'EOL'

# AI Construction Ecosystem Aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'

# Project specific aliases
alias dev='pnpm dev'
alias build='pnpm build'
alias test='pnpm test'
alias lint='pnpm lint'
alias format='pnpm format'

# Docker aliases
alias dps='docker ps'
alias dimg='docker images'
alias dlog='docker logs'
alias dex='docker exec -it'

# Database aliases
alias db-up='docker-compose -f docker-compose.dev.yml up -d postgres redis'
alias db-down='docker-compose -f docker-compose.dev.yml down'
alias db-logs='docker-compose -f docker-compose.dev.yml logs -f postgres'
alias db-shell='docker exec -it ez_eco_postgres psql -U postgres -d ez_eco_dev'

# Prisma aliases
alias prisma-generate='npx prisma generate'
alias prisma-push='npx prisma db push'
alias prisma-studio='npx prisma studio'
alias prisma-migrate='npx prisma migrate dev'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git pull'
alias gco='git checkout'
alias gb='git branch'

# Nx aliases
alias nx-build='npx nx build'
alias nx-serve='npx nx serve'
alias nx-test='npx nx test'
alias nx-lint='npx nx lint'
alias nx-graph='npx nx graph'
EOL

# Создание полезных VS Code snippets
echo "📝 Creating VS Code snippets..."
mkdir -p .vscode
cat > .vscode/snippets.json << 'EOL'
{
  "NestJS Controller": {
    "prefix": "nest-controller",
    "body": [
      "import { Controller, Get, Post, Put, Delete, Body, Param, Query } from '@nestjs/common';",
      "import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';",
      "",
      "@ApiTags('${1:resource}')",
      "@Controller('${1:resource}')",
      "export class ${2:${1/(.*)/${1:/capitalize}/}}Controller {",
      "  constructor(private readonly ${1:resource}Service: ${2:${1/(.*)/${1:/capitalize}/}}Service) {}",
      "",
      "  @Get()",
      "  @ApiOperation({ summary: 'Get all ${1:resource}' })",
      "  @ApiResponse({ status: 200, description: 'List of ${1:resource}' })",
      "  async findAll() {",
      "    return this.${1:resource}Service.findAll();",
      "  }",
      "",
      "  @Get(':id')",
      "  @ApiOperation({ summary: 'Get ${1:resource} by id' })",
      "  async findOne(@Param('id') id: string) {",
      "    return this.${1:resource}Service.findOne(id);",
      "  }",
      "",
      "  @Post()",
      "  @ApiOperation({ summary: 'Create new ${1:resource}' })",
      "  async create(@Body() createDto: Create${2:${1/(.*)/${1:/capitalize}/}}Dto) {",
      "    return this.${1:resource}Service.create(createDto);",
      "  }",
      "}"
    ],
    "description": "Create NestJS Controller"
  },
  "Prisma Service": {
    "prefix": "prisma-service",
    "body": [
      "import { Injectable, OnModuleInit } from '@nestjs/common';",
      "import { PrismaClient } from '@prisma/client';",
      "",
      "@Injectable()",
      "export class PrismaService extends PrismaClient implements OnModuleInit {",
      "  async onModuleInit() {",
      "    await this.$connect();",
      "  }",
      "",
      "  async onModuleDestroy() {",
      "    await this.$disconnect();",
      "  }",
      "}"
    ],
    "description": "Create Prisma Service"
  }
}
EOL

# Создание workspace settings для VS Code
cat > .vscode/settings.json << 'EOL'
{
  "typescript.preferences.includePackageJsonAutoImports": "auto",
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "files.associations": {
    "*.prisma": "prisma"
  },
  "emmet.includeLanguages": {
    "typescript": "html"
  }
}
EOL

# Финальная очистка и настройка прав
echo "🔧 Final cleanup and permissions setup..."
sudo chown -R vscode:vscode /home/vscode
sudo chown -R vscode:vscode /workspaces 2>/dev/null || true

# Создание информационного файла
cat > DEVCONTAINER_INFO.md << 'EOL'
# DevContainer Information

## 🚀 Что установлено

### Основное окружение:
- **Node.js LTS** с npm, yarn, pnpm
- **Python 3.11** с популярными пакетами
- **Docker** с поддержкой Docker-in-Docker
- **PostgreSQL Client** для работы с базой данных
- **Redis CLI** для работы с кэшем
- **Git** с GitHub CLI

### Глобальные пакеты:
- NestJS CLI
- Nx CLI
- Prisma CLI
- TypeScript
- ESLint & Prettier
- PM2

### Полезные алиасы:
- `dev` - запуск разработки
- `db-up` - запуск базы данных
- `db-shell` - подключение к PostgreSQL
- `prisma-studio` - открытие Prisma Studio

### Доступные порты:
- 3000-3005: Микросервисы
- 5432: PostgreSQL
- 6379: Redis
- 8080: PgAdmin

## 📝 Быстрый старт

1. **Установка зависимостей:**
   ```bash
   ./scripts/dev-setup.sh
   ```

2. **Запуск базы данных:**
   ```bash
   db-up
   ```

3. **Запуск разработки:**
   ```bash
   dev
   ```

## 🔧 Доступные команды

- `pnpm install` - установка зависимостей
- `pnpm dev` - режим разработки
- `pnpm build` - сборка проекта
- `pnpm test` - запуск тестов
- `npx nx graph` - граф зависимостей Nx

## 🗄️ База данных

Для работы с базой данных используется PostgreSQL в Docker контейнере.
Доступ: `postgresql://postgres:postgres@localhost:5432/ez_eco_dev`

PgAdmin доступен по адресу: http://localhost:8080
- Email: admin@example.com
- Password: admin

## 📊 Мониторинг

- **Prisma Studio**: `npx prisma studio`
- **Nx Graph**: `npx nx graph`
- **Docker Logs**: `docker-compose -f docker-compose.dev.yml logs -f`
EOL

echo "✅ DevContainer Bootstrap completed successfully!"
echo ""
echo "🎉 Welcome to AI Construction Ecosystem DevContainer!"
echo ""
echo "📋 Next steps:"
echo "1. Run './scripts/dev-setup.sh' to initialize the project"
echo "2. Check 'DEVCONTAINER_INFO.md' for detailed information"
echo "3. Start coding! 🚀"
echo ""
echo "💡 Tip: Use 'db-up' to start the database services"
echo ""
