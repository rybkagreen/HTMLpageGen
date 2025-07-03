# DevContainer Configuration

Эта конфигурация DevContainer предназначена для разработки AI Construction Ecosystem - экосистемы микросервисов на основе NestJS, TypeScript, и Nx монорепозитория.

## 🏗️ Архитектура

### Базовый образ
- **Node.js LTS** - основной рабочий контейнер
- **Пользователь**: `vscode` с правами sudo
- **Рабочая директория**: `/workspaces/${localWorkspaceFolderBasename}`

### Установленные компоненты

#### Runtime окружения:
- **Node.js LTS** с npm, yarn, и pnpm
- **Python 3.11** с pip и популярными пакетами
- **Docker-in-Docker** для контейнеризации приложений
- **Git** с GitHub CLI для работы с репозиториями

#### Инструменты разработки:
- **NestJS CLI** - для работы с NestJS фреймворком
- **Nx CLI** - для управления монорепозиторием
- **Prisma CLI** - для работы с базой данных
- **TypeScript** - компилятор и инструменты
- **ESLint & Prettier** - линтинг и форматирование кода
- **PM2** - менеджер процессов

#### Клиенты баз данных:
- **PostgreSQL Client** - для работы с PostgreSQL
- **Redis CLI** - для работы с Redis

#### Python пакеты:
- **FastAPI & Uvicorn** - для Python микросервисов
- **SQLAlchemy & Alembic** - ORM и миграции
- **Pandas & NumPy** - анализ данных
- **Pytest** - тестирование

## 🔌 Порты и сервисы

### Микросервисы (3000-3005):
| Порт | Сервис | Описание |
|------|--------|----------|
| 3000 | Frontend App | Главное веб-приложение |
| 3001 | API Gateway | Точка входа для API |
| 3002 | Auth Service | Сервис аутентификации |
| 3003 | Construction Objects | Управление строительными объектами |
| 3004 | User Profile | Профили пользователей |
| 3005 | Contracts Management | Управление контрактами |

### Базы данных и кэш:
| Порт | Сервис | Описание |
|------|--------|----------|
| 5432 | PostgreSQL | Основная база данных |
| 6379 | Redis | Кэш и сессии |

### Инструменты администрирования:
| Порт | Сервис | Описание |
|------|--------|----------|
| 8080 | PgAdmin | Веб-интерфейс для PostgreSQL |
| 8081 | Redis Commander | Веб-интерфейс для Redis |

## 📁 Структура файлов

```
.devcontainer/
├── devcontainer.json      # Основная конфигурация
├── bootstrap.sh           # Скрипт инициализации
├── tasks.json            # Задачи VS Code
├── launch.json           # Конфигурация отладки
├── docker-compose.extended.yml  # Расширенные сервисы
└── README.md             # Эта документация
```

## 🚀 Быстрый старт

### 1. Автоматическая инициализация
При создании DevContainer автоматически запускается `bootstrap.sh`, который:
- Обновляет системные пакеты
- Устанавливает дополнительные инструменты
- Настраивает окружение разработки
- Создает структуру проекта
- Настраивает алиасы командной строки

### 2. Ручная настройка проекта
```bash
# Запуск скрипта настройки
./scripts/dev-setup.sh

# Или пошагово:
pnpm install                    # Установка зависимостей
db-up                          # Запуск баз данных
npx prisma generate            # Генерация Prisma клиента
npx prisma db push             # Применение схемы БД
```

### 3. Запуск разработки
```bash
# Простой способ
dev

# Или через Nx
npx nx serve api-gateway
```

## ⚙️ Переменные окружения

Автоматически создаются файлы:
- `.env.example` - шаблон переменных
- `.env` - локальные переменные для разработки

### Основные переменные:
```env
# База данных
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/ez_eco_dev"

# Redis
REDIS_URL="redis://localhost:6379"

# JWT
JWT_SECRET="dev-jwt-secret-key"
JWT_EXPIRES_IN="24h"

# Приложение
NODE_ENV="development"
PORT="3000"
```

## 🐳 Docker сервисы

### Базовые сервисы (docker-compose.dev.yml):
- **PostgreSQL 15** с базой `ez_eco_dev`
- **Redis 7** с persistence
- **PgAdmin** для администрирования БД

### Расширенные сервисы (docker-compose.extended.yml):
- **Elasticsearch & Kibana** - логирование и поиск
- **MinIO** - S3-совместимое файловое хранилище
- **RabbitMQ** - очереди сообщений
- **Prometheus & Grafana** - мониторинг
- **Jaeger** - распределенный трейсинг
- **Nginx** - обратный прокси

```bash
# Запуск базовых сервисов
docker-compose -f docker-compose.dev.yml up -d

# Запуск всех сервисов
docker-compose -f .devcontainer/docker-compose.extended.yml up -d
```

## 🔧 VS Code интеграция

### Расширения
Автоматически устанавливаются:
- **TypeScript & JavaScript** - языковая поддержка
- **Prettier & ESLint** - форматирование и линтинг
- **Prisma** - работа с ORM
- **Docker** - управление контейнерами
- **GitHub Copilot** - ИИ-помощник
- **Thunder Client** - тестирование API
- **Markdown** - документация

### Задачи (Tasks)
Доступны через `Ctrl+Shift+P` → "Tasks: Run Task":
- **Install Dependencies** - установка пакетов
- **Start Development Server** - запуск dev сервера
- **Build Project** - сборка проекта
- **Run Tests** - запуск тестов
- **Start Database Services** - запуск БД
- **Generate Prisma Client** - генерация Prisma
- **Open Prisma Studio** - веб-интерфейс БД

### Отладка (Debug)
Конфигурации отладки:
- **Debug NestJS Application** - отладка скомпилированного приложения
- **Debug TypeScript with ts-node** - отладка TypeScript
- **Debug Jest Tests** - отладка тестов
- **Debug Current Test File** - отладка текущего теста
- **Debug Nx Serve** - отладка через Nx

## 📜 Полезные алиасы

Автоматически добавляются в `.zshrc`:

### Проект:
```bash
dev         # pnpm dev
build       # pnpm build
test        # pnpm test
lint        # pnpm lint
format      # pnpm format
```

### База данных:
```bash
db-up       # Запуск PostgreSQL и Redis
db-down     # Остановка сервисов
db-shell    # Подключение к PostgreSQL
db-logs     # Просмотр логов БД
```

### Prisma:
```bash
prisma-generate  # npx prisma generate
prisma-push      # npx prisma db push
prisma-studio    # npx prisma studio
prisma-migrate   # npx prisma migrate dev
```

### Docker:
```bash
dps         # docker ps
dimg        # docker images
dlog        # docker logs
dex         # docker exec -it
```

### Git:
```bash
gs          # git status
ga          # git add
gc          # git commit
gp          # git push
gl          # git pull
```

### Nx:
```bash
nx-build    # npx nx build
nx-serve    # npx nx serve
nx-test     # npx nx test
nx-lint     # npx nx lint
nx-graph    # npx nx graph
```

## 🔍 Мониторинг и отладка

### Доступные интерфейсы:
| URL | Сервис | Логин | Пароль |
|-----|--------|-------|--------|
| http://localhost:8080 | PgAdmin | admin@example.com | admin |
| http://localhost:8081 | Redis Commander | admin | admin |
| http://localhost:5601 | Kibana | - | - |
| http://localhost:9001 | MinIO Console | minioadmin | minioadmin123 |
| http://localhost:15672 | RabbitMQ Management | admin | admin123 |
| http://localhost:9090 | Prometheus | - | - |
| http://localhost:3001 | Grafana | admin | admin123 |
| http://localhost:16686 | Jaeger UI | - | - |

### Команды диагностики:
```bash
# Проверка состояния сервисов
docker-compose -f docker-compose.dev.yml ps

# Логи приложения
pnpm dev

# Логи базы данных
db-logs

# Состояние Nx workspace
npx nx show projects

# Граф зависимостей
npx nx graph
```

## 📋 Требования к хосту

### Минимальные:
- **CPU**: 4 ядра
- **RAM**: 8 GB
- **Диск**: 32 GB свободного места

### Рекомендуемые:
- **CPU**: 8+ ядер
- **RAM**: 16+ GB
- **Диск**: 64+ GB SSD

## 🛠️ Настройка под проект

### Добавление нового микросервиса:
1. Добавить порт в `devcontainer.json` → `forwardPorts`
2. Добавить описание в `portsAttributes`
3. Добавить переменную окружения в `.env.example`
4. Обновить документацию

### Добавление нового расширения VS Code:
```json
"customizations": {
  "vscode": {
    "extensions": [
      "publisher.extension-name"
    ]
  }
}
```

### Добавление системного пакета:
Отредактировать `bootstrap.sh`:
```bash
sudo apt-get install -y your-package
```

## 🔐 Безопасность

### Пароли по умолчанию:
⚠️ **ВАЖНО**: Измените пароли перед продакшеном!

- PostgreSQL: `postgres/postgres`
- Redis: без пароля (в расширенной конфигурации: `redispassword`)
- PgAdmin: `admin@example.com/admin`
- MinIO: `minioadmin/minioadmin123`

### Рекомендации:
- Используйте переменные окружения для секретов
- Настройте `.gitignore` для исключения `.env`
- Используйте Docker secrets в продакшене
- Регулярно обновляйте базовые образы

## 🐛 Устранение неполадок

### Контейнер не запускается:
1. Проверьте синтаксис `devcontainer.json`
2. Убедитесь в наличии Docker
3. Проверьте доступное место на диске

### Порты заняты:
```bash
# Проверить занятые порты
sudo lsof -i :3000

# Остановить конфликтующие сервисы
docker-compose -f docker-compose.dev.yml down
```

### Проблемы с БД:
```bash
# Пересоздать базу данных
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d postgres

# Проверить подключение
db-shell
```

### Проблемы с пакетами:
```bash
# Очистить кэш
pnpm store prune
rm -rf node_modules
pnpm install

# Или использовать скрипт
./scripts/cleanup.sh
```

## 📚 Дополнительные ресурсы

- [DevContainers Documentation](https://containers.dev/)
- [VS Code Remote Development](https://code.visualstudio.com/docs/remote/containers)
- [NestJS Documentation](https://nestjs.com/)
- [Nx Documentation](https://nx.dev/)
- [Prisma Documentation](https://prisma.io/docs/)

## 🤝 Вклад в проект

При внесении изменений в DevContainer конфигурацию:
1. Обновите документацию
2. Протестируйте на чистом окружении
3. Добавьте changelog запись
4. Проверьте совместимость с GitHub Codespaces
