# 📚 Стандарт документации HTMLpageGen

## Общие принципы документации

1. **Ясность и простота** - документация должна быть понятна разработчикам любого уровня
2. **Актуальность** - документация обновляется вместе с кодом
3. **Структурированность** - четкая иерархия и организация материала
4. **Примеры кода** - каждое описание сопровождается рабочими примерами
5. **Двуязычность** - техническая документация на английском, бизнес-логика на русском

## Структура документации

```
docs/
├── README.md                    # Главная страница документации
├── getting-started/             # Начало работы
│   ├── installation.md         # Установка и настройка
│   ├── quick-start.md          # Быстрый старт
│   └── development-setup.md    # Настройка среды разработки
├── architecture/               # Архитектура
│   ├── overview.md            # Общий обзор
│   ├── frontend.md            # Frontend архитектура
│   ├── backend.md             # Backend архитектура
│   └── database.md            # Структура БД
├── api/                       # API документация
│   ├── authentication.md     # Аутентификация
│   ├── pages.md              # Pages API
│   ├── ai-integration.md     # AI Integration API
│   └── seo.md                # SEO API
├── modules/                   # Документация модулей
│   ├── ai-integration/       # AI интеграция
│   ├── page-generator/       # Генератор страниц
│   └── seo/                  # SEO модуль
├── guides/                   # Руководства
│   ├── contributing.md       # Гайд для контрибьюторов
│   ├── testing.md           # Тестирование
│   ├── deployment.md        # Развертывание
│   └── troubleshooting.md   # Решение проблем
└── changelog/                # История изменений
    ├── CHANGELOG.md         # Основной changelog
    └── migration-guides/    # Гайды по миграции
```

## Шаблоны документации

### 1. Главный README.md

```markdown
# HTMLpageGen

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)

> HTML-генератор страниц с интеграцией искусственного интеллекта

## 🚀 Быстрый старт

```bash
# Клонирование репозитория
git clone https://github.com/username/HTMLpageGen.git
cd HTMLpageGen

# Запуск в Docker
docker-compose up -d --build

# Приложение доступно по адресу
open http://localhost:3000
```

## ✨ Возможности

- 🤖 **AI-генерация** - Создание HTML с помощью OpenAI
- 🎨 **Современный UI** - React + Next.js + Tailwind CSS
- ⚡ **Высокая производительность** - FastAPI backend
- 🔍 **SEO оптимизация** - Автоматическая оптимизация контента
- 🐳 **Docker Ready** - Готовая контейнеризация
- 📱 **Responsive Design** - Адаптивный дизайн

## 📖 Документация

- [🛠️ Установка и настройка](docs/getting-started/installation.md)
- [🏗️ Архитектура](docs/architecture/overview.md)
- [📡 API Reference](docs/api/README.md)
- [🧪 Тестирование](docs/guides/testing.md)
- [🚀 Развертывание](docs/guides/deployment.md)

## 🏗️ Технологический стек

### Frontend
- **Framework**: Next.js 15.x
- **UI Library**: React 19.x
- **Styling**: Tailwind CSS 4.x
- **Language**: TypeScript 5.x

### Backend
- **Framework**: FastAPI 0.104.x
- **Language**: Python 3.11+
- **Database**: PostgreSQL + SQLAlchemy
- **AI Integration**: OpenAI API

### DevOps
- **Containerization**: Docker + Docker Compose
- **Development**: DevContainer
- **Testing**: Jest + pytest

## 🤝 Участие в разработке

Мы приветствуем вклад в развитие проекта! Пожалуйста, ознакомьтесь с [руководством для контрибьюторов](docs/guides/contributing.md).

## 📄 Лицензия

Этот проект лицензирован под [MIT License](LICENSE).

## 📞 Поддержка

- 📧 Email: support@htmlpagegen.com
- 💬 GitHub Issues: [Создать issue](https://github.com/username/HTMLpageGen/issues)
- 📖 Документация: [docs.htmlpagegen.com](https://docs.htmlpagegen.com)
```

### 2. Шаблон модуля

```markdown
# Название модуля

## Обзор

Краткое описание назначения и функциональности модуля.

## Установка

### Зависимости

```json
{
  "dependencies": {
    "package1": "^1.0.0",
    "package2": "^2.0.0"
  }
}
```

### Настройка

```typescript
// Пример настройки модуля
import { ModuleConfig } from './types';

const config: ModuleConfig = {
  apiKey: process.env.API_KEY,
  timeout: 5000
};
```

## API Reference

### Классы

#### `MainClass`

Основной класс модуля для работы с функциональностью.

```typescript
class MainClass {
  constructor(config: ModuleConfig)
  
  /**
   * Основной метод модуля
   * @param input - входные данные
   * @returns Promise с результатом
   */
  async process(input: InputType): Promise<OutputType>
}
```

### Функции

#### `utilityFunction`

```typescript
/**
 * Вспомогательная функция
 * @param param1 - первый параметр
 * @param param2 - второй параметр
 * @returns результат обработки
 */
function utilityFunction(param1: string, param2: number): boolean
```

### Типы

```typescript
interface ModuleConfig {
  apiKey: string;
  timeout: number;
  retries?: number;
}

interface InputType {
  data: string;
  options?: ProcessingOptions;
}

interface OutputType {
  result: string;
  metadata: Metadata;
}
```

## Примеры использования

### Базовое использование

```typescript
import { MainClass } from './module';

const processor = new MainClass({
  apiKey: 'your-api-key',
  timeout: 3000
});

const result = await processor.process({
  data: 'input data'
});

console.log(result);
```

### Продвинутое использование

```typescript
import { MainClass, ProcessingOptions } from './module';

const processor = new MainClass({
  apiKey: process.env.API_KEY!,
  timeout: 5000,
  retries: 3
});

const options: ProcessingOptions = {
  format: 'json',
  validate: true
};

try {
  const result = await processor.process({
    data: 'complex input data',
    options
  });
  
  // Обработка результата
  handleResult(result);
} catch (error) {
  // Обработка ошибок
  handleError(error);
}
```

## Тестирование

### Запуск тестов

```bash
# Unit тесты
npm test src/modules/module-name

# Integration тесты
npm run test:integration

# Покрытие кода
npm run test:coverage
```

### Примеры тестов

```typescript
import { MainClass } from './module';

describe('MainClass', () => {
  let processor: MainClass;

  beforeEach(() => {
    processor = new MainClass({
      apiKey: 'test-key',
      timeout: 1000
    });
  });

  describe('process', () => {
    it('должен обработать входные данные корректно', async () => {
      const input = { data: 'test input' };
      const result = await processor.process(input);
      
      expect(result.result).toBeDefined();
      expect(result.metadata).toBeDefined();
    });

    it('должен выбросить ошибку при некорректных данных', async () => {
      const input = { data: '' };
      
      await expect(processor.process(input)).rejects.toThrow();
    });
  });
});
```

## Конфигурация

### Переменные окружения

| Переменная | Описание | По умолчанию | Обязательная |
|------------|----------|--------------|---------------|
| `API_KEY` | API ключ для внешнего сервиса | - | ✅ |
| `TIMEOUT` | Таймаут запросов (мс) | 5000 | ❌ |
| `RETRIES` | Количество повторных попыток | 3 | ❌ |

### Файл конфигурации

```typescript
// config.ts
export const moduleConfig = {
  api: {
    baseUrl: process.env.API_BASE_URL || 'https://api.example.com',
    timeout: parseInt(process.env.TIMEOUT || '5000'),
    retries: parseInt(process.env.RETRIES || '3')
  },
  features: {
    caching: process.env.ENABLE_CACHE === 'true',
    logging: process.env.LOG_LEVEL || 'info'
  }
};
```

## Решение проблем

### Частые ошибки

#### `API_KEY_MISSING`
```
Ошибка: API ключ не найден в переменных окружения
Решение: Установите переменную окружения API_KEY
```

#### `TIMEOUT_EXCEEDED`
```
Ошибка: Превышен таймаут запроса
Решение: Увеличьте значение TIMEOUT или проверьте сетевое соединение
```

### Отладка

```typescript
// Включение debug режима
const processor = new MainClass({
  apiKey: 'your-key',
  timeout: 5000,
  debug: true // включает подробное логирование
});
```

## Миграция

### С версии 1.x на 2.x

1. Обновите зависимости:
   ```bash
   npm install module-name@^2.0.0
   ```

2. Измените импорты:
   ```typescript
   // Было
   import { OldClass } from 'module-name';
   
   // Стало
   import { NewClass } from 'module-name';
   ```

3. Обновите конфигурацию:
   ```typescript
   // Было
   const config = { apiKey: 'key' };
   
   // Стало
   const config = { auth: { apiKey: 'key' } };
   ```

## Производительность

### Метрики

- **Время отклика**: < 100ms для базовых операций
- **Пропускная способность**: 1000 запросов/сек
- **Использование памяти**: < 50MB на процесс

### Оптимизация

```typescript
// Кэширование результатов
const processor = new MainClass({
  apiKey: 'your-key',
  cache: {
    enabled: true,
    ttl: 3600 // 1 час
  }
});

// Пакетная обработка
const results = await processor.processBatch(inputs, {
  batchSize: 100,
  concurrency: 5
});
```

## Changelog

### v2.1.0 (2025-07-03)
- ✨ Добавлена поддержка пакетной обработки
- 🐛 Исправлена ошибка с таймаутами
- 📚 Обновлена документация

### v2.0.0 (2025-06-01)
- 💥 BREAKING: Изменен интерфейс конфигурации
- ✨ Добавлено кэширование
- ⚡ Улучшена производительность на 50%

## Contributing

Смотрите [руководство для разработчиков](../../CONTRIBUTING.md).

## Лицензия

MIT License. Подробности в файле [LICENSE](../../LICENSE).
```

### 3. Шаблон API документации

```markdown
# API Reference

## Обзор

Базовый URL: `https://api.htmlpagegen.com/v1`

Все запросы должны содержать заголовок авторизации:
```
Authorization: Bearer YOUR_API_TOKEN
```

## Аутентификация

### Получение токена

```http
POST /auth/token
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}
```

**Ответ:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

## Endpoints

### Pages

#### Создать страницу

```http
POST /pages
Content-Type: application/json
Authorization: Bearer {token}

{
  "title": "My Page",
  "description": "Create a landing page for a tech startup",
  "style": "modern",
  "seo_keywords": ["startup", "technology", "innovation"]
}
```

**Параметры:**

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `title` | string | ✅ | Название страницы |
| `description` | string | ✅ | Описание контента для AI |
| `style` | string | ❌ | Стиль дизайна (modern, classic, minimal) |
| `seo_keywords` | array | ❌ | Ключевые слова для SEO |

**Ответ (201 Created):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "My Page",
  "description": "Create a landing page for a tech startup",
  "html_content": "<!DOCTYPE html>...",
  "style": "modern",
  "seo": {
    "meta_title": "Innovative Tech Startup - My Page",
    "meta_description": "Cutting-edge technology solutions...",
    "keywords": ["startup", "technology", "innovation"]
  },
  "created_at": "2025-07-03T12:00:00Z",
  "updated_at": "2025-07-03T12:00:00Z"
}
```

**Возможные ошибки:**
- `400 Bad Request` - Некорректные входные данные
- `401 Unauthorized` - Неверный токен авторизации
- `429 Too Many Requests` - Превышен лимит запросов
- `500 Internal Server Error` - Ошибка сервера

#### Получить страницу

```http
GET /pages/{page_id}
Authorization: Bearer {token}
```

**Ответ (200 OK):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "My Page",
  "html_content": "<!DOCTYPE html>...",
  "seo": {
    "meta_title": "Innovative Tech Startup - My Page",
    "meta_description": "Cutting-edge technology solutions...",
    "keywords": ["startup", "technology", "innovation"]
  },
  "created_at": "2025-07-03T12:00:00Z",
  "updated_at": "2025-07-03T12:00:00Z"
}
```

#### Список страниц

```http
GET /pages?limit=10&offset=0&search=startup
Authorization: Bearer {token}
```

**Query параметры:**

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `limit` | integer | 10 | Количество записей |
| `offset` | integer | 0 | Смещение для пагинации |
| `search` | string | - | Поиск по названию и описанию |

**Ответ (200 OK):**
```json
{
  "items": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "My Page",
      "description": "Create a landing page for a tech startup",
      "created_at": "2025-07-03T12:00:00Z"
    }
  ],
  "total": 1,
  "limit": 10,
  "offset": 0
}
```

## Коды ошибок

| Код | Описание | Решение |
|-----|----------|---------|
| 400 | Bad Request | Проверьте корректность запроса |
| 401 | Unauthorized | Проверьте токен авторизации |
| 403 | Forbidden | Недостаточно прав доступа |
| 404 | Not Found | Ресурс не найден |
| 422 | Validation Error | Ошибка валидации данных |
| 429 | Too Many Requests | Превышен лимит запросов |
| 500 | Internal Server Error | Обратитесь в поддержку |

## Rate Limiting

- **Лимит**: 1000 запросов в час на токен
- **Заголовки ответа**:
  - `X-RateLimit-Limit`: общий лимит
  - `X-RateLimit-Remaining`: оставшиеся запросы
  - `X-RateLimit-Reset`: время сброса лимита (Unix timestamp)

## SDKs

### JavaScript/TypeScript

```bash
npm install htmlpagegen-sdk
```

```typescript
import { HTMLPageGenClient } from 'htmlpagegen-sdk';

const client = new HTMLPageGenClient({
  apiKey: 'your-api-key',
  baseURL: 'https://api.htmlpagegen.com/v1'
});

const page = await client.pages.create({
  title: 'My Page',
  description: 'Create a landing page',
  style: 'modern'
});
```

### Python

```bash
pip install htmlpagegen-python
```

```python
from htmlpagegen import Client

client = Client(api_key='your-api-key')

page = client.pages.create(
    title='My Page',
    description='Create a landing page',
    style='modern'
)
```

## Примеры

### Создание страницы с кастомным стилем

```javascript
const response = await fetch('https://api.htmlpagegen.com/v1/pages', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'E-commerce Store',
    description: 'Create a product catalog page with shopping cart',
    style: 'modern',
    seo_keywords: ['ecommerce', 'shopping', 'online store']
  })
});

const page = await response.json();
console.log('Generated page:', page.html_content);
```

### Обработка ошибок

```javascript
try {
  const response = await fetch('https://api.htmlpagegen.com/v1/pages', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer YOUR_TOKEN',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      title: '',  // пустое название вызовет ошибку
      description: 'Test description'
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  const page = await response.json();
} catch (error) {
  console.error('Error creating page:', error.message);
}
```
```

## Стандарт комментариев в коде

### TypeScript/JavaScript

```typescript
/**
 * Создает новый компонент кнопки с настраиваемыми свойствами
 * 
 * @param props - Свойства компонента кнопки
 * @param props.children - Содержимое кнопки
 * @param props.variant - Вариант оформления кнопки
 * @param props.size - Размер кнопки
 * @param props.disabled - Состояние блокировки кнопки
 * @param props.onClick - Обработчик клика
 * @returns React компонент кнопки
 * 
 * @example
 * ```tsx
 * <Button variant="primary" size="lg" onClick={handleClick}>
 *   Нажми меня
 * </Button>
 * ```
 * 
 * @since 1.0.0
 */
```

### Python

```python
def generate_page(description: str, style: str = "modern") -> Page:
    """
    Генерирует HTML страницу на основе описания с использованием AI
    
    Args:
        description (str): Описание желаемого контента страницы
        style (str, optional): Стиль дизайна страницы. По умолчанию "modern".
    
    Returns:
        Page: Объект сгенерированной страницы с HTML контентом и метаданными
    
    Raises:
        ValueError: Если описание пустое или некорректное
        AIServiceError: При ошибке работы с AI сервисом
        DatabaseError: При ошибке сохранения в базу данных
    
    Example:
        >>> page = generate_page("Создай лендинг для IT компании", "modern")
        >>> print(page.title)
        'IT Solutions Company'
        
    Note:
        Функция использует OpenAI API для генерации контента.
        Убедитесь, что API ключ настроен корректно.
    
    Since:
        1.0.0
    """
```

## Инструменты для документации

### Автогенерация документации

#### TypeDoc для TypeScript
```json
{
  "scripts": {
    "docs:generate": "typedoc --out docs/api src/index.ts"
  }
}
```

#### Sphinx для Python
```python
# conf.py
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]
```

### Документация API

#### OpenAPI/Swagger для FastAPI
```python
from fastapi import FastAPI

app = FastAPI(
    title="HTMLPageGen API",
    description="API для генерации HTML страниц с AI интеграцией",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
```

## Процесс обновления документации

1. **При изменении кода** - обновить соответствующие комментарии
2. **При добавлении API** - обновить API документацию
3. **При релизе** - обновить CHANGELOG.md
4. **Еженедельно** - проверка актуальности документации
5. **При onboarding** - тестирование документации новичками

## Контроль качества документации

### Checklist для review документации

- [ ] Все публичные функции/классы документированы
- [ ] Примеры кода рабочие и актуальные
- [ ] Описания понятны для целевой аудитории
- [ ] Ссылки работают корректно
- [ ] Код отформатирован и подсвечен
- [ ] Используется единый стиль написания
- [ ] Переводы на русский/английский корректны

### Метрики документации

- **Покрытие**: % документированных функций/классов
- **Качество**: % положительных отзывов от пользователей
- **Актуальность**: время с последнего обновления
- **Использование**: статистика просмотров разделов

---

**Помните**: Хорошая документация - это инвестиция в будущее проекта и команды!
