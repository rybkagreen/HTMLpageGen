# 📚 API Документация HTMLPageGen

## 🚀 Обзор API

HTMLPageGen предоставляет простой REST API для генерации HTML-страниц с помощью ИИ. Все endpoints поддерживают JSON формат и используют современные стандарты веб-разработки.

## 🔑 Аутентификация

API использует ключи DeepSeek для аутентификации с ИИ-сервисом. Ключи настраиваются через переменные окружения и не требуют дополнительной аутентификации от пользователей.

## 📋 Endpoints

### 🎨 Генерация HTML

**POST** `/api/generate`

Генерирует HTML-страницу на основе пользовательского описания.

#### Запрос

```typescript
interface GenerateRequest {
  title: string; // Название страницы
  content: string; // Описание содержимого
  template: "basic" | "modern" | "minimal" | "business" | "blog";
  style?: "light" | "dark" | "blue" | "purple";
  features?: string[]; // Дополнительные возможности
  ai_enhance?: boolean; // Включить ИИ-улучшения
}
```

#### Ответ

```typescript
interface GenerateResponse {
  html: string; // Сгенерированный HTML код
  meta: {
    generation_time: number; // Время генерации в мс
    template_used: string; // Использованный шаблон
    ai_enhanced: boolean; // Применены ли ИИ-улучшения
    seo_score: number; // SEO оценка (0-100)
    word_count: number; // Количество слов
    meta_tags: {
      title: string;
      description: string;
      keywords: string;
    };
  };
  plugins_applied: string[]; // Примененные плагины
  generation_time: number; // Время генерации в секундах
}
```

#### Пример запроса

```bash
curl -X POST http://localhost:3000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Мой стартап",
    "content": "Лендинг для IT-стартапа с современным дизайном",
    "template": "modern",
    "style": "dark",
    "features": ["responsive", "seo"],
    "ai_enhance": true
  }'
```

### 💬 ИИ Чат

**POST** `/api/deepseek`

Отправляет сообщение в ИИ-чат для получения помощи и советов.

#### Запрос

```typescript
interface ChatRequest {
  messages: Array<{
    role: "user" | "assistant" | "system";
    content: string;
  }>;
  stream?: boolean; // Потоковый ответ
  temperature?: number; // Температура генерации (0.0-2.0)
  max_tokens?: number; // Максимум токенов в ответе
}
```

#### Ответ

```typescript
interface ChatResponse {
  success: boolean;
  message: string; // Ответ ИИ
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}
```

#### Пример запроса

```bash
curl -X POST http://localhost:3000/api/deepseek \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Как создать адаптивный дизайн?"
      }
    ],
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

## 🔧 Конфигурация

### Переменные окружения

```bash
# Обязательные
DEEPSEEK_API_KEY=sk-your-api-key-here

# Опциональные
DEEPSEEK_MODEL=deepseek-chat          # Модель ИИ
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MAX_TOKENS=3000              # Макс. токены
DEEPSEEK_TEMPERATURE=0.7              # Температура
```

### Лимиты

- **Размер запроса**: До 10MB
- **Время ожидания**: 30 секунд
- **Rate limiting**: 100 запросов/час (DeepSeek)
- **Макс. токены**: 4000 на запрос

## 🚨 Обработка ошибок

### Коды ошибок

| Код | Описание          | Решение                       |
| --- | ----------------- | ----------------------------- |
| 400 | Неверный запрос   | Проверьте формат данных       |
| 401 | Неверный API ключ | Обновите DEEPSEEK_API_KEY     |
| 429 | Превышен лимит    | Подождите или увеличьте лимит |
| 500 | Внутренняя ошибка | Попробуйте позже              |

### Примеры ошибок

```json
{
  "success": false,
  "message": "Недостаточно средств на балансе DeepSeek",
  "error": "insufficient_balance",
  "details": "Current balance: $0.00"
}
```

```json
{
  "success": false,
  "message": "Превышен лимит запросов",
  "error": "rate_limit_exceeded",
  "retry_after": 3600
}
```

## 📊 Мониторинг

### Метрики

API предоставляет метрики для мониторинга:

- Время ответа
- Количество запросов
- Ошибки по типам
- Использование токенов

### Health Check

**GET** `/api/health`

```json
{
  "status": "healthy",
  "timestamp": "2025-07-05T10:00:00Z",
  "version": "1.0.0",
  "services": {
    "deepseek": "connected",
    "database": "connected"
  }
}
```

## 🔐 Безопасность

### Защита

- CORS настроен для разрешенных доменов
- Rate limiting предотвращает злоупотребление
- Валидация всех входящих данных
- Санитизация HTML контента

### Рекомендации

1. Используйте HTTPS в продакшене
2. Ограничьте доступ к API ключам
3. Мониторьте необычную активность
4. Регулярно обновляйте зависимости

## 🧪 Тестирование

### Примеры тестов

```javascript
// Тест генерации HTML
test("генерация простой страницы", async () => {
  const response = await fetch("/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: "Тест",
      content: "Простая тестовая страница",
      template: "minimal",
    }),
  });

  const data = await response.json();
  expect(data.html).toContain("<html>");
  expect(data.meta.seo_score).toBeGreaterThan(0);
});

// Тест чата
test("ИИ отвечает на вопрос", async () => {
  const response = await fetch("/api/deepseek", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      messages: [{ role: "user", content: "Привет!" }],
    }),
  });

  const data = await response.json();
  expect(data.success).toBe(true);
  expect(data.message).toBeTruthy();
});
```

## 📈 Производительность

### Оптимизация

- Кэширование часто используемых шаблонов
- Сжатие ответов gzip
- Оптимизация промптов для ИИ
- Параллельная обработка запросов

### Рекомендации

1. Используйте короткие описания для быстрой генерации
2. Кэшируйте результаты на клиенте
3. Используйте потоковые ответы для чата
4. Мониторьте использование токенов

---

## 🔗 Дополнительные ресурсы

- [Документация DeepSeek](https://platform.deepseek.com/docs)
- [Руководство по настройке](SETUP_GUIDE.md)
- [Примеры использования](examples/)
- [Лучшие практики](BEST_PRACTICES.md)
