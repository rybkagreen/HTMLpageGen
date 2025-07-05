# 🚀 HTMLPageGen - ИИ Генератор HTML Страниц

> Современная full-stack платформа для создания веб-страниц с помощью искусственного интеллекта

[![Next.js](https://img.shields.io/badge/Next.js-15.3.4-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?logo=typescript)](https://www.typescriptlang.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4.0-38B2AC?logo=tailwind-css)](https://tailwindcss.com/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-R1-purple)](https://platform.deepseek.com/)
[![LocalAI](https://img.shields.io/badge/LocalAI-Fallback-orange)](https://github.com/yourusername/HTMLpageGen)

## ✨ Особенности

### 🤖 Мультипровайдерная ИИ-интеграция

- **DeepSeek R1** - Передовая модель рассуждений
- **HuggingFace** - Открытые модели через Inference API
- **OpenAI GPT** - Классические модели ChatGPT
- **Локальный AI** - Полностью автономный fallback режим

### 💻 Полнофункциональная архитектура

- � **Frontend**: Next.js 15 + React 19 + TypeScript
- ⚡ **Backend**: FastAPI + Python 3.12 + Async/Await
- 🔄 **API**: RESTful с автоматической документацией
- �️ **Типизация**: Полная поддержка TypeScript и Python typing

### 🎯 Основные возможности

- 💬 **Умный чат** - Диалог с ИИ-ассистентом
- 🎨 **Генерация HTML** - Создание страниц по описанию
- 🔍 **SEO-анализ** - Автоматическая оптимизация
- 📊 **Аналитика контента** - Проверка качества и доступности
- 🎨 **Современный UI** - Темная тема и адаптивный дизайн

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/HTMLpageGen.git
cd HTMLpageGen
```

### 2. Установка зависимостей

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 3. Настройка переменных окружения

Создайте файл `backend/.env`:

```bash
# AI Provider Configuration
AI_PROVIDER=local-ai  # local-ai, deepseek-r1, huggingface, openai

# API Keys (optional)
DEEPSEEK_API_KEY=sk-your-deepseek-key
HUGGINGFACE_API_KEY=hf_your-huggingface-key
OPENAI_API_KEY=sk-your-openai-key

# Database (optional)
DATABASE_URL=postgresql://user:pass@localhost/htmlpagegen
```

### 4. Запуск приложения

```bash
# Запуск Backend (FastAPI)
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Запуск Frontend (Next.js) - в новом терминале
cd frontend
npm run dev
```

**Доступ к приложению:**

- 🌐 **Frontend**: [http://localhost:3000](http://localhost:3000)
- ⚡ **API**: [http://localhost:8000](http://localhost:8000)
- 📚 **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🔧 Локальный режим (без внешних API)

HTMLPageGen работает полностью автономно без внешних AI сервисов:

```bash
# Backend с локальным AI
export AI_PROVIDER=local-ai
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

✅ **Локальный режим включает:**

- Генерацию HTML страниц
- Анализ контента и SEO
- Чат-бота с базовыми ответами
- Предложения по улучшению
- Все без внешних зависимостей!

## 💻 Использование

### Создание HTML страницы

1. Откройте **Генератор** в навигации
2. Введите название и описание страницы
3. Выберите шаблон и стиль
4. Нажмите **Генерировать с ИИ**
5. Скачайте готовый HTML файл

### Работа с ИИ-чатом

1. Перейдите в **ИИ Чат**
2. Опишите свою задачу или вопрос
3. Получите детальные рекомендации
4. Уточните детали в диалоге

### Примеры запросов

```
Создай лендинг для IT-стартапа с современным дизайном
Сделай страницу портфолио для веб-разработчика
Помоги оптимизировать страницу для SEO
Объясни принципы адаптивной верстки
```

## 🏗️ Архитектура

### Frontend (Next.js 15)

```
├── 🎨 components/
│   ├── generator/     # HTML генератор
│   ├── ai/           # ИИ чат интерфейс
│   ├── projects/     # Управление проектами
│   ├── knowledge/    # База знаний
│   └── ui/           # UI компоненты
├── 🧠 lib/
│   ├── ai-agent.ts      # ИИ агент логика
│   ├── project-manager.ts # Управление проектами
│   └── knowledge-base.ts  # База знаний
└── 🌐 app/
    ├── api/          # API routes
    ├── generator/    # Страница генератора
    └── chat/         # Страница чата
```

### Ключевые технологии

- **Next.js 15** - React фреймворк с App Router
- **TypeScript** - Типизированный JavaScript
- **TailwindCSS** - Утилитарный CSS фреймворк
- **Framer Motion** - Библиотека анимаций
- **Monaco Editor** - Редактор кода VS Code
- **DeepSeek API** - Интеграция с ИИ
- **Zustand** - Управление состоянием

## 📚 Документация

- 📖 [Руководство по настройке](SETUP_GUIDE.md)
- 🔧 [API Документация](API_DOCUMENTATION.md)
- ✨ [Лучшие практики](BEST_PRACTICES.md)
- 🌟 [Примеры использования](EXAMPLES.md)
- 🗺️ [Дорожная карта развития](AI_AGENT_ROADMAP.md)

## 🛠️ Разработка

### Запуск в режиме разработки

```bash
npm run dev          # Запуск frontend
npm run build        # Сборка проекта
npm run test         # Запуск тестов
npm run lint         # Проверка кода
```

## 🔧 Конфигурация

### Настройки ИИ

```bash
# Модель (по умолчанию: deepseek-chat)
DEEPSEEK_MODEL=deepseek-chat

# Максимум токенов (по умолчанию: 3000)
DEEPSEEK_MAX_TOKENS=3000

# Температура генерации (по умолчанию: 0.7)
DEEPSEEK_TEMPERATURE=0.7
```

## 🚨 Устранение неполадок

### Частые проблемы

**Ошибка "API ключ не настроен"**

- Проверьте наличие `.env.local`
- Убедитесь, что ключ начинается с `sk-`
- Перезапустите сервер

**Медленная генерация**

- Уменьшите `DEEPSEEK_MAX_TOKENS`
- Оптимизируйте промпты
- Проверьте интернет-соединение

## 📊 Дорожная карта

### ✅ v1.0 - Базовая версия (Готово)

- Единый HTML генератор
- ИИ чат интерфейс
- Интеграция DeepSeek API
- Современный UI/UX

### 🔄 v1.1 - Проекты (В разработке)

- Система управления проектами
- Версионирование
- Экспорт/импорт

### 🚀 v2.0 - ИИ Агент (Планируется)

- Векторная база знаний
- Семантический поиск
- Персонализация
- Продвинутая аналитика

## 🤝 Участие в разработке

Мы приветствуем вклад в развитие проекта!

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Создайте Pull Request

## 📄 Лицензия

Этот проект лицензирован под MIT License.

## 🙏 Благодарности

- [DeepSeek](https://deepseek.com/) за мощный ИИ
- [Next.js](https://nextjs.org/) команда за отличный фреймворк
- Сообщество разработчиков за вдохновение

---

<div align="center">
  <p><strong>Создано с ❤️ командой HTMLPageGen</strong></p>
  <p>⭐ Не забудьте поставить звезду, если проект был полезен!</p>
</div>

## ✅ Статус качества кода

### Последние исправления (2025-07-05)

После комплексного рефакторинга все критические ошибки исправлены:

**✅ Исправлены ошибки типов и наследования:**

- Добавлены полные аннотации типов Python (`-> None`, `-> Dict[str, Any]`)
- Исправлены асинхронные методы с правильными сигнатурами
- Убраны неиспользуемые импорты (`torch`, `transformers`, `Optional`)
- Обеспечена совместимость интерфейсов базового и производного классов

**✅ Качество кода:**

```bash
# Проверка типизации
✅ mypy --ignore-missing-imports → Success: no issues found

# Компиляция Python
✅ python -m py_compile *.py → All files compile successfully

# Функциональные тесты
✅ AI Service creation → OK
✅ HTML generation → 710+ characters generated
✅ Provider info → local-ai configured
```

**✅ API тестирование:**

```bash
✅ GET  /health → {"status":"healthy","version":"1.0.0"}
✅ GET  /api/v1/ai/provider-info → {"provider":"local-ai","configured":true}
✅ POST /api/v1/ai/generate-html → HTML content generated
✅ GET  /docs → OpenAPI documentation accessible
```

**✅ Архитектурная целостность:**

- Backend (FastAPI) + Frontend (Next.js) интеграция работает
- Локальный AI провайдер функционирует без внешних зависимостей
- Fallback система обеспечивает надежность
- Все абстрактные методы полностью реализованы

---
