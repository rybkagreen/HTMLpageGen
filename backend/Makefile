.PHONY: lint format type-check test test-cov install dev clean help

# Переменные
PYTHON = python3
PIP = pip3
PYTEST = pytest
BLACK = black
ISORT = isort
FLAKE8 = flake8
MYPY = mypy

# Директории
SRC_DIR = app
TEST_DIR = tests
VENV_DIR = .venv

# Цвета для вывода
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

help: ## Показать это сообщение помощи
	@echo "$(BLUE)HTMLpageGen Backend - Доступные команды:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Установить зависимости
	@echo "$(YELLOW)Установка зависимостей...$(NC)"
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

install-dev: ## Установить зависимости для разработки
	@echo "$(YELLOW)Установка dev зависимостей...$(NC)"
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .

lint: ## Проверить код линтерами
	@echo "$(YELLOW)Запуск flake8...$(NC)"
	$(FLAKE8) $(SRC_DIR) $(TEST_DIR)
	@echo "$(YELLOW)Запуск mypy...$(NC)"
	$(MYPY) $(SRC_DIR)
	@echo "$(GREEN)✅ Линтинг завершен$(NC)"

format: ## Отформатировать код
	@echo "$(YELLOW)Форматирование с black...$(NC)"
	$(BLACK) $(SRC_DIR) $(TEST_DIR)
	@echo "$(YELLOW)Сортировка импортов с isort...$(NC)"
	$(ISORT) $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✅ Форматирование завершено$(NC)"

format-check: ## Проверить форматирование без изменений
	@echo "$(YELLOW)Проверка форматирования...$(NC)"
	$(BLACK) --check $(SRC_DIR) $(TEST_DIR)
	$(ISORT) --check $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✅ Форматирование корректно$(NC)"

type-check: ## Проверить типы с mypy
	@echo "$(YELLOW)Проверка типов...$(NC)"
	$(MYPY) $(SRC_DIR)
	@echo "$(GREEN)✅ Проверка типов завершена$(NC)"

test: ## Запустить тесты
	@echo "$(YELLOW)Запуск тестов...$(NC)"
	$(PYTEST) $(TEST_DIR)/ -v
	@echo "$(GREEN)✅ Тесты завершены$(NC)"

test-unit: ## Запустить только unit тесты
	@echo "$(YELLOW)Запуск unit тестов...$(NC)"
	$(PYTEST) $(TEST_DIR)/unit/ -v -m "not integration"

test-integration: ## Запустить только integration тесты
	@echo "$(YELLOW)Запуск integration тестов...$(NC)"
	$(PYTEST) $(TEST_DIR)/integration/ -v -m "integration"

test-cov: ## Запустить тесты с покрытием
	@echo "$(YELLOW)Запуск тестов с покрытием...$(NC)"
	$(PYTEST) $(TEST_DIR)/ -v --cov=$(SRC_DIR) --cov-report=html --cov-report=term
	@echo "$(GREEN)✅ Отчет о покрытии создан в htmlcov/$(NC)"

test-watch: ## Запустить тесты в watch режиме
	@echo "$(YELLOW)Запуск тестов в watch режиме...$(NC)"
	$(PYTEST) $(TEST_DIR)/ -v --looponfail

dev: ## Запустить сервер разработки
	@echo "$(YELLOW)Запуск сервера разработки...$(NC)"
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-debug: ## Запустить сервер с отладкой
	@echo "$(YELLOW)Запуск сервера с отладкой...$(NC)"
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

db-up: ## Запустить базу данных
	@echo "$(YELLOW)Запуск PostgreSQL и Redis...$(NC)"
	docker-compose -f docker-compose.dev.yml up -d postgres redis

db-down: ## Остановить базу данных
	@echo "$(YELLOW)Остановка базы данных...$(NC)"
	docker-compose -f docker-compose.dev.yml down

db-shell: ## Подключиться к PostgreSQL
	@echo "$(YELLOW)Подключение к PostgreSQL...$(NC)"
	docker-compose -f docker-compose.dev.yml exec postgres psql -U postgres -d htmlpagegen

db-migrate: ## Создать новую миграцию
	@echo "$(YELLOW)Создание миграции...$(NC)"
	alembic revision --autogenerate -m "$(MESSAGE)"

db-upgrade: ## Применить миграции
	@echo "$(YELLOW)Применение миграций...$(NC)"
	alembic upgrade head

db-downgrade: ## Откатить миграцию
	@echo "$(YELLOW)Откат миграции...$(NC)"
	alembic downgrade -1

clean: ## Очистить временные файлы
	@echo "$(YELLOW)Очистка временных файлов...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	@echo "$(GREEN)✅ Очистка завершена$(NC)"

security: ## Проверить безопасность зависимостей
	@echo "$(YELLOW)Проверка безопасности...$(NC)"
	safety check
	bandit -r $(SRC_DIR)/

docs: ## Генерировать документацию
	@echo "$(YELLOW)Генерация документации...$(NC)"
	sphinx-build -b html docs/ docs/_build/

docs-serve: ## Запустить локальный сервер документации
	@echo "$(YELLOW)Запуск сервера документации...$(NC)"
	$(PYTHON) -m http.server 8080 -d docs/_build/

pre-commit-install: ## Установить pre-commit хуки
	@echo "$(YELLOW)Установка pre-commit хуков...$(NC)"
	pre-commit install

pre-commit-run: ## Запустить pre-commit для всех файлов
	@echo "$(YELLOW)Запуск pre-commit...$(NC)"
	pre-commit run --all-files

ci: lint type-check test ## Запустить все проверки CI
	@echo "$(GREEN)✅ Все проверки CI пройдены$(NC)"

build: ## Собрать пакет
	@echo "$(YELLOW)Сборка пакета...$(NC)"
	$(PYTHON) -m build

deps-update: ## Обновить зависимости
	@echo "$(YELLOW)Обновление зависимостей...$(NC)"
	$(PIP) list --outdated
	@echo "$(BLUE)Для обновления запустите: pip install --upgrade package-name$(NC)"

performance: ## Запустить performance тесты
	@echo "$(YELLOW)Запуск performance тестов...$(NC)"
	$(PYTEST) $(TEST_DIR)/performance/ -v

load-test: ## Запустить нагрузочное тестирование
	@echo "$(YELLOW)Запуск нагрузочного тестирования...$(NC)"
	locust -f tests/load/locustfile.py --host=http://localhost:8000

profile: ## Профилирование приложения
	@echo "$(YELLOW)Профилирование приложения...$(NC)"
	$(PYTHON) -m cProfile -o profile.stats -m uvicorn app.main:app
	$(PYTHON) -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(20)"

# Алиасы для частых команд
f: format ## Алиас для format
l: lint ## Алиас для lint
t: test ## Алиас для test
d: dev ## Алиас для dev

# Docker команды
docker-build: ## Собрать Docker образ
	@echo "$(YELLOW)Сборка Docker образа...$(NC)"
	docker build -t htmlpagegen-backend .

docker-run: ## Запустить Docker контейнер
	@echo "$(YELLOW)Запуск Docker контейнера...$(NC)"
	docker run -p 8000:8000 htmlpagegen-backend

docker-logs: ## Показать логи Docker контейнера
	@echo "$(YELLOW)Логи Docker контейнера...$(NC)"
	docker-compose -f docker-compose.dev.yml logs -f backend

# Мониторинг
logs: ## Показать логи приложения
	@echo "$(YELLOW)Логи приложения...$(NC)"
	tail -f logs/app.log

logs-error: ## Показать только ошибки
	@echo "$(YELLOW)Логи ошибок...$(NC)"
	tail -f logs/app.log | grep ERROR

health: ## Проверить здоровье сервиса
	@echo "$(YELLOW)Проверка здоровья сервиса...$(NC)"
	curl -s http://localhost:8000/health | jq

metrics: ## Показать метрики приложения
	@echo "$(YELLOW)Метрики приложения...$(NC)"
	curl -s http://localhost:8000/metrics

# Утилиты
check-ports: ## Проверить используемые порты
	@echo "$(YELLOW)Проверка портов...$(NC)"
	lsof -i :8000 || echo "Порт 8000 свободен"
	lsof -i :5432 || echo "Порт 5432 свободен"
	lsof -i :6379 || echo "Порт 6379 свободен"

env-check: ## Проверить переменные окружения
	@echo "$(YELLOW)Проверка переменных окружения...$(NC)"
	@echo "PYTHONPATH: $(PYTHONPATH)"
	@echo "DATABASE_URL: $(DATABASE_URL)"
	@echo "OPENAI_API_KEY: $(if $(OPENAI_API_KEY),установлен,не установлен)"

deps-tree: ## Показать дерево зависимостей
	@echo "$(YELLOW)Дерево зависимостей...$(NC)"
	pipdeptree

backup-db: ## Создать бэкап базы данных
	@echo "$(YELLOW)Создание бэкапа базы данных...$(NC)"
	docker-compose -f docker-compose.dev.yml exec postgres pg_dump -U postgres htmlpagegen > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db: ## Восстановить базу данных (требует файл BACKUP_FILE)
	@echo "$(YELLOW)Восстановление базы данных...$(NC)"
	@if [ -z "$(BACKUP_FILE)" ]; then echo "$(RED)Укажите BACKUP_FILE=filename.sql$(NC)"; exit 1; fi
	docker-compose -f docker-compose.dev.yml exec -T postgres psql -U postgres htmlpagegen < $(BACKUP_FILE)
