# 🚀 DevContainer Quick Start Guide

## Что такое DevContainer?

DevContainer - это предварительно настроенное окружение разработки в Docker контейнере, которое включает все необходимые инструменты, зависимости и настройки для проекта HTMLpageGen.

## ⚡ Быстрый запуск

### 1. GitHub Codespaces (Рекомендуется)
- Откройте репозиторий на GitHub.
- Нажмите на кнопку `Code` и выберите `Create a new codespace`.

### 2. VS Code + Dev Containers (Локально)
1. Установите расширение [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
2. Откройте проект в VS Code.
3. Нажмите `Ctrl+Shift+P` и выберите команду `Dev Containers: Rebuild and Reopen in Container`.

## 🎯 Первые шаги после запуска

После того как DevContainer будет готов, используйте встроенные задачи VS Code для управления проектом.

Откройте палитру команд (`Ctrl+Shift+P`) и выберите `Tasks: Run Task`.

### 1. Установка зависимостей
- Выполните задачу **`Install Frontend Dependencies`** для установки пакетов `pnpm`.
- Выполните задачу **`Install Backend Dependencies`** для установки пакетов `pip`.

### 2. Запуск Docker-сервисов
- Выполните задачу **`Start Docker Services`** для запуска PostgreSQL и Redis.

### 3. Запуск серверов разработки
- Выполните задачу **`Start Frontend (Next.js)`** для запуска клиентского приложения.
- Выполните задачу **`Start Backend (FastAPI)`** для запуска серверного приложения.

## ✅ Проверка доступности

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🔧 Основные задачи (Tasks)

Вы можете найти все доступные команды в меню `Terminal > Run Task...`.

- `Install Frontend Dependencies`: Установка зависимостей фронтенда.
- `Install Backend Dependencies`: Установка зависимостей бэкенда.
- `Start Frontend (Next.js)`: Запуск сервера разработки Next.js.
- `Start Backend (FastAPI)`: Запуск сервера разработки FastAPI.
- `Start Docker Services`: Запуск контейнеров `postgres` и `redis`.
- `Stop Docker Services`: Остановка контейнеров.

## 🆘 Помощь

Если у вас возникли проблемы с запуском или работой в DevContainer, убедитесь, что Docker Desktop запущен и работает корректно. Проверьте логи контейнеров на наличие ошибок.
