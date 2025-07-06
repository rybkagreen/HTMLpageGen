# База данных - Настройка и инициализация

## Обзор

Проект использует SQLite в качестве базы данных для разработки. Для производственной среды можно переключиться на PostgreSQL, изменив `DATABASE_URL` в конфигурации.

## Конфигурация

### Файл .env

Убедитесь, что в файле `.env` указан правильный путь к базе данных:

```env
# Database
DATABASE_URL=sqlite:///./htmlpagegen.db
```

Для PostgreSQL:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/htmlpagegen_db
```

### Структура базы данных

Текущая схема включает следующие таблицы:

- **html_pages** - Хранение сгенерированных HTML страниц
  - `id` - Первичный ключ
  - `title` - Заголовок страницы
  - `content` - HTML контент
  - `prompt` - Исходный запрос для AI
  - `ai_provider` - Используемый AI провайдер
  - `created_at` - Дата создания
  - `updated_at` - Дата обновления
  - `is_active` - Статус активности

- **users** - Пользователи системы (для будущего использования)
  - `id` - Первичный ключ
  - `email` - Email пользователя
  - `hashed_password` - Хешированный пароль
  - `is_active` - Статус активности
  - `created_at` - Дата создания
  - `updated_at` - Дата обновления

## Инициализация базы данных

### Автоматическая инициализация

Используйте скрипт инициализации:

```bash
cd backend
python scripts/init_db.py
```

Скрипт автоматически:
- Проверяет существование базы данных
- Создает базу данных если её нет
- Применяет все необходимые миграции
- Выводит статус операции

### Ручная инициализация

#### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

#### 2. Инициализация Alembic (уже выполнено)

```bash
alembic init alembic
```

#### 3. Создание первой миграции (уже выполнено)

```bash
alembic revision --autogenerate -m "Initial migration"
```

#### 4. Применение миграций

```bash
alembic upgrade head
```

## Управление миграциями

### Создание новой миграции

После изменения моделей в `app/db/models.py`:

```bash
alembic revision --autogenerate -m "Описание изменений"
```

### Применение миграций

```bash
alembic upgrade head
```

### Откат миграций

```bash
# Откат на одну миграцию назад
alembic downgrade -1

# Откат к конкретной ревизии
alembic downgrade <revision_id>
```

### Просмотр истории миграций

```bash
alembic history
```

### Просмотр текущей ревизии

```bash
alembic current
```

## Проверка состояния базы данных

### Health Check API

Проверить состояние базы данных можно через API:

```bash
# Базовая проверка
curl http://localhost:8000/health

# Детальная проверка
curl http://localhost:8000/health/detailed
```

### Прямое подключение к SQLite

```bash
sqlite3 htmlpagegen.db

# Просмотр таблиц
.tables

# Просмотр схемы таблицы
.schema html_pages

# Выход
.quit
```

## Структура файлов

```
backend/
├── app/
│   └── db/
│       ├── __init__.py          # Экспорты модуля
│       ├── database.py          # Подключение к БД
│       └── models.py            # Модели SQLAlchemy
├── alembic/                     # Конфигурация Alembic
│   ├── versions/                # Файлы миграций
│   ├── env.py                   # Настройка окружения
│   └── script.py.mako          # Шаблон миграций
├── scripts/
│   └── init_db.py              # Скрипт инициализации БД
├── alembic.ini                 # Конфигурация Alembic
├── htmlpagegen.db             # Файл базы данных SQLite
└── .env                       # Переменные окружения
```

## Часто задаваемые вопросы

### Q: Как переключиться с SQLite на PostgreSQL?

A: 
1. Установите psycopg2: `pip install psycopg2-binary`
2. Обновите DATABASE_URL в .env: `DATABASE_URL=postgresql://user:pass@host:port/dbname`
3. Примените миграции: `alembic upgrade head`

### Q: Что делать при ошибке миграции?

A:
1. Проверьте подключение к базе данных
2. Убедитесь, что база данных существует
3. Проверьте права доступа к файлу базы данных (для SQLite)
4. Просмотрите логи ошибок в выводе alembic

### Q: Как сбросить базу данных?

A:
```bash
# Для SQLite - удалите файл
rm htmlpagegen.db

# Затем примените миграции заново
alembic upgrade head
```

### Q: Как создать резервную копию?

A:
```bash
# SQLite
cp htmlpagegen.db htmlpagegen_backup.db

# PostgreSQL
pg_dump dbname > backup.sql
```

## Безопасность

- **Никогда не коммитьте файлы базы данных в Git**
- **Используйте переменные окружения для чувствительных данных**
- **Регулярно создавайте резервные копии**
- **Используйте сильные пароли для производственных баз данных**

## Мониторинг

Приложение автоматически собирает метрики о состоянии базы данных:

- Время ответа подключения
- Статус здоровья
- Количество ошибок подключения

Метрики доступны через endpoint: `GET /health/detailed`
