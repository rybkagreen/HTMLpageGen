# 🚀 DevContainer Quick Start Guide

## Что такое DevContainer?

DevContainer - это предварительно настроенное окружение разработки в Docker контейнере, которое включает все необходимые инструменты, зависимости и настройки для проекта AI Construction Ecosystem.

## ⚡ Быстрый запуск

### 1. GitHub Codespaces (Рекомендуется)
```bash
# Создание нового Codespace
gh codespace create --repo your-username/your-repo

# Подключение к существующему
gh codespace ssh
```

### 2. VS Code Desktop + Remote Containers
1. Установите расширение "Dev Containers"
2. Откройте проект в VS Code
3. `Ctrl+Shift+P` → "Dev Containers: Rebuild and Reopen in Container"

### 3. Docker Compose (Локально)
```bash
# Клонирование проекта
git clone https://github.com/your-username/your-repo.git
cd your-repo

# Запуск DevContainer
docker-compose -f .devcontainer/docker-compose.extended.yml up -d
```

## 🎯 Первые шаги после запуска

### 1. Проверка окружения
```bash
# Проверка версий
node --version    # Node.js LTS
python3 --version # Python 3.11
pnpm --version    # Package manager
docker --version  # Docker

# Проверка Nx workspace
npx nx --version
```

### 2. Установка зависимостей
```bash
# Автоматическая настройка
./scripts/dev-setup.sh

# Или вручную
pnpm install
db-up
npx prisma generate
npx prisma db push
```

### 3. Запуск разработки
```bash
# Простой способ
dev

# Или конкретный сервис
npx nx serve api-gateway
npx nx serve auth-service
```

## 🔧 Основные команды

### Проект:
- `dev` - запуск development режима
- `build` - сборка проекта
- `test` - запуск тестов
- `lint` - проверка кода
- `format` - форматирование кода

### База данных:
- `db-up` - запуск PostgreSQL и Redis
- `db-down` - остановка сервисов
- `db-shell` - подключение к PostgreSQL
- `prisma-studio` - веб-интерфейс БД

### Docker:
- `dps` - список контейнеров
- `dlog container-name` - логи контейнера
- `dex container-name bash` - вход в контейнер

## 📊 Доступные сервисы

| Сервис | URL | Логин | Пароль |
|--------|-----|-------|--------|
| PgAdmin | http://localhost:8080 | admin@example.com | admin |
| Redis Commander | http://localhost:8081 | admin | admin |
| Grafana | http://localhost:3001 | admin | admin123 |
| MinIO Console | http://localhost:9001 | minioadmin | minioadmin123 |

## 🆘 Помощь

### Проблемы с портами:
```bash
# Проверить занятые порты
sudo lsof -i :3000

# Остановить все сервисы
docker-compose -f docker-compose.dev.yml down
```

### Проблемы с зависимостями:
```bash
# Очистка и переустановка
./scripts/cleanup.sh
pnpm install
```

### Полная документация:
Смотрите [.devcontainer/README.md](.devcontainer/README.md) для подробной информации.

## 💡 Полезные советы

1. **Используйте алиасы** - они сэкономят время
2. **Регулярно запускайте тесты** - `test`
3. **Проверяйте логи** - `db-logs`, `dlog container-name`
4. **Используйте Prisma Studio** - `prisma-studio`
5. **Мониторьте граф зависимостей** - `npx nx graph`

## 📚 Дополнительные ресурсы

- [DevContainer README](.devcontainer/README.md) - полная документация
- [VS Code Tasks](https://code.visualstudio.com/docs/editor/tasks) - автоматизация
- [Nx Documentation](https://nx.dev/) - управление монорепозиторием
- [NestJS Docs](https://nestjs.com/) - бэкенд фреймворк

---

**Готово к разработке!** 🎉

Если возникли вопросы, проверьте [документацию](.devcontainer/README.md) или создайте issue в репозитории.
