# DeepSeek R1 Integration for HTMLpageGen

## Обзор

Проект HTMLpageGen теперь поддерживает интеграцию с DeepSeek R1 API для мощных возможностей генерации контента с помощью ИИ.

## Настройка DeepSeek API

### Шаг 1: Получение API ключа

1. Зарегистрируйтесь на [DeepSeek Platform](https://platform.deepseek.com)
2. Получите ваш API ключ
3. В проекте уже настроен ключ: `sk-aeaf60f610ee429892a113b1f4e20960`

### Шаг 2: Конфигурация

Обновите файл `.env` в папке `backend`:

```env
# AI Configuration
AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-aeaf60f610ee429892a113b1f4e20960
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
```

## Возможности DeepSeek R1

### 1. Улучшение контента 📝

- **Общее улучшение**: Автоматическое улучшение текста для веб-презентации
- **SEO оптимизация**: Оптимизация контента для поисковых систем
- **Доступность**: Улучшение читабельности и доступности
- **Маркетинг**: Переписывание с маркетинговым фокусом

### 2. Генерация HTML 🏗️

- **Веб-страницы**: Создание семантически правильного HTML
- **Лендинги**: Убедительные конверсионные страницы
- **Блог статьи**: Читабельные и SEO-оптимизированные статьи
- **Портфолио**: Профессиональные страницы портфолио

### 3. SEO Мета-теги 🏷️

- Автоматическая генерация title (до 60 символов)
- Создание meta description (до 160 символов)
- Подбор релевантных ключевых слов
- SEO-оптимизированные теги на основе контента

### 4. Анализ HTML 🔍

- Проверка SEO оптимизации
- Рекомендации по доступности
- Советы по производительности
- Улучшение пользовательского опыта

## API Endpoints

### Улучшение контента

```http
POST /api/v1/ai/enhance-content
Content-Type: application/json

{
  "content": "Ваш исходный контент",
  "enhancement_type": "general" // general, seo, accessibility, marketing
}
```

### Генерация HTML

```http
POST /api/v1/ai/generate-html
Content-Type: application/json

{
  "prompt": "Описание того, что нужно создать",
  "content_type": "webpage" // webpage, landing, blog, portfolio
}
```

### Генерация мета-тегов

```http
POST /api/v1/ai/generate-meta-tags
Content-Type: application/json

{
  "content": "Контент для анализа"
}
```

### Анализ HTML

```http
POST /api/v1/ai/suggest-improvements
Content-Type: application/json

{
  "html": "<html>...</html>"
}
```

### Информация о провайдере

```http
GET /api/v1/ai/provider-info
```

## Использование в интерфейсе

1. Откройте `/ai` в браузере после запуска приложения
2. Выберите нужную вкладку:
   - **Улучшение контента** - для улучшения существующего текста
   - **Генерация HTML** - для создания нового HTML
   - **Мета-теги** - для генерации SEO тегов
   - **Анализ HTML** - для получения рекомендаций

## Запуск проекта

### Бэкенд

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Фронтенд

```bash
cd frontend
npm run dev
```

## Архитектура AI Integration

Проект использует паттерн Provider для поддержки множественных AI провайдеров:

- `AIProvider` - базовый интерфейс
- `DeepSeekProvider` - реализация для DeepSeek API
- `OpenAIProvider` - реализация для OpenAI API (опционально)
- `MockProvider` - заглушка без API ключей

## Переключение провайдеров

Измените `AI_PROVIDER` в `.env` файле:

- `deepseek` - для DeepSeek R1
- `openai` - для OpenAI (требует OPENAI_API_KEY)

## Отладка

Проверить статус интеграции:

```bash
cd backend
source venv/bin/activate
python -c "from app.modules.ai_integration.service import AIService; ai = AIService(); print(type(ai.provider).__name__)"
```

## Примеры использования

### Python (бэкенд)

```python
from app.modules.ai_integration.service import AIService

ai_service = AIService()

# Улучшение контента
enhanced = await ai_service.enhance_content(
    "Ваш текст",
    enhancement_type="seo"
)

# Генерация HTML
html = await ai_service.generate_html_content(
    "Создай страницу о компании",
    content_type="webpage"
)
```

### TypeScript (фронтенд)

```typescript
import { generateHTMLContent } from "@/lib/api";

const response = await generateHTMLContent({
  prompt: "Создай лендинг для IT компании",
  content_type: "landing",
});

console.log(response.html_content);
```

## Ограничения и рекомендации

- DeepSeek R1 поддерживает русский и английский языки
- Максимальная длина запроса: ~4000 токенов
- Рекомендуется кэшировать результаты для оптимизации
- Используйте разные `content_type` для лучших результатов

## Поддержка

При возникновении проблем:

1. Проверьте правильность API ключа
2. Убедитесь в доступности DeepSeek API
3. Проверите логи бэкенда для диагностики
4. Используйте `/ai/provider-info` для проверки статуса

---

**Powered by DeepSeek R1** 🚀
