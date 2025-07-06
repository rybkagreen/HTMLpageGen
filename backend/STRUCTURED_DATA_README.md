# Структурированные данные Schema.org в AI HTML Генераторе

## Обзор

AI HTML Генератор теперь поддерживает автоматическую генерацию и внедрение структурированных данных schema.org в формате JSON-LD. Эта функциональность значительно улучшает SEO и помогает поисковым системам лучше понимать контент ваших страниц.

## Поддерживаемые типы схем

### 1. FAQ Page (FAQPage)
Для страниц с часто задаваемыми вопросами.

**Пример использования:**
```python
faq_data = {
    "faq_items": [
        {"question": "Что такое HTML генератор?", "answer": "Инструмент для создания веб-страниц"},
        {"question": "Как использовать ИИ?", "answer": "Просто введите описание контента"}
    ],
    "name": "Часто задаваемые вопросы",
    "description": "Ответы на популярные вопросы"
}
```

### 2. Product (Product)
Для страниц товаров и продуктов.

**Пример использования:**
```python
product_data = {
    "name": "HTML Генератор Pro",
    "description": "Профессиональный инструмент для создания веб-страниц",
    "brand": "WebGen",
    "price": 2999.99,
    "currency": "RUB",
    "availability": "InStock",
    "reviews": [
        {
            "rating": 5.0,
            "review_body": "Отличный инструмент!",
            "author": "Иван Петров"
        }
    ]
}
```

### 3. Breadcrumb (BreadcrumbList)
Для навигационных хлебных крошек.

**Пример использования:**
```python
breadcrumb_data = {
    "items": [
        {"name": "Главная", "url": "/", "position": 1},
        {"name": "Продукты", "url": "/products", "position": 2},
        {"name": "HTML Генератор", "url": "/products/html-generator", "position": 3}
    ]
}
```

### 4. Article (Article)
Для статей и блог-постов.

**Пример использования:**
```python
article_data = {
    "headline": "Как создать веб-страницу с ИИ",
    "author": "Алексей Разработчик",
    "date_published": "2024-01-20T10:00:00Z",
    "description": "Руководство по созданию веб-страниц",
    "publisher_name": "WebDev Blog"
}
```

### 5. Organization (Organization)
Для страниц компаний и организаций.

**Пример использования:**
```python
organization_data = {
    "name": "WebGen Technologies",
    "url": "https://webgen-tech.com",
    "description": "Компания по разработке веб-инструментов",
    "address": {
        "street": "ул. Технологическая, 42",
        "city": "Москва",
        "country": "Россия"
    },
    "phone": "+7 (495) 123-45-67"
}
```

## API Эндпоинты

### 1. Генерация структурированных данных
```http
POST /api/ai/generate-structured-data
```

**Параметры запроса:**
```json
{
    "content": "Текст контента для анализа",
    "schema_type": "faq",
    "data": {
        // Дополнительные данные (опционально)
    },
    "auto_extract": true
}
```

**Ответ:**
```json
{
    "schema_data": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        // ... сгенерированная схема
    },
    "schema_type": "faq",
    "json_ld": "JSON-LD строка"
}
```

### 2. Внедрение структурированных данных в HTML
```http
POST /api/ai/inject-structured-data
```

**Параметры запроса:**
```json
{
    "html": "<html>...</html>",
    "schema_types": ["faq", "breadcrumb"],
    "auto_detect": true,
    "schema_params": {
        "faq": {
            // параметры для FAQ схемы
        }
    }
}
```

**Ответ:**
```json
{
    "html": "<html с внедренными схемами>",
    "schemas_added": 2,
    "schemas_list": ["faq", "breadcrumb"]
}
```

### 3. Генерация страницы со структурированными данными
```http
POST /api/pages/generate
```

**Параметры запроса:**
```json
{
    "content": "Контент страницы",
    "template": "default",
    "structured_data": true,
    "structured_data_types": ["faq", "article"],
    "structured_data_params": {
        "article": {
            "author": "Имя автора",
            "publisher_name": "Название издателя"
        }
    }
}
```

## Использование в коде

### Базовое использование

```python
from app.modules.structured_data.generator import StructuredDataGenerator
from app.modules.ai_integration.service import AIService

# Инициализация
ai_service = AIService()
generator = StructuredDataGenerator(ai_service)

# Генерация FAQ схемы
faq_schema = await generator.generate_structured_data(
    schema_type="faq",
    content="Ваш контент с вопросами и ответами",
    auto_extract=True
)

# Внедрение в HTML
html_with_schema = generator.inject_into_html(html, faq_schema)
```

### Автоматическое определение схем

```python
# Автоматически определяет подходящие схемы и внедряет их
enhanced_html = await generator.auto_generate_for_content(
    html=original_html,
    content_type="auto"
)
```

### Множественные схемы

```python
# Генерация нескольких схем
schemas = []
for schema_type in ["faq", "breadcrumb", "organization"]:
    schema = await generator.generate_structured_data(
        schema_type=schema_type,
        content=content,
        auto_extract=True
    )
    if schema:
        schemas.append(schema)

# Внедрение всех схем
final_html = generator.inject_multiple_schemas(html, schemas)
```

## Интеграция с PageGeneratorService

Структурированные данные автоматически интегрированы в основной процесс генерации страниц:

```python
result = await page_service.generate_page(
    content="Ваш контент",
    structured_data=True,  # Включить генерацию структурированных данных
    structured_data_types=["faq", "article"],  # Конкретные типы схем
    structured_data_params={
        "article": {
            "author": "Автор статьи",
            "publisher_name": "Издатель"
        }
    }
)

# Информация о добавленных схемах в result["meta"]["structured_data"]
```

## AI-Поддержка

### Автоматическое извлечение данных

ИИ может автоматически анализировать контент и извлекать данные для схем:

- **FAQ**: Определяет вопросы и ответы в тексте или создает логичные FAQ
- **Product**: Извлекает название, описание, цену и характеристики продукта
- **Breadcrumb**: Создает логичную навигационную цепочку
- **Article**: Определяет заголовок, автора и метаданные статьи
- **Organization**: Извлекает информацию о компании

### Автоматическое определение типов схем

ИИ может автоматически определить, какие типы схем лучше всего подходят для конкретного контента.

## Валидация Schema.org

Сгенерированные схемы соответствуют стандартам schema.org и могут быть проверены с помощью:

- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)
- [Structured Data Testing Tool](https://search.google.com/structured-data/testing-tool)

## SEO Преимущества

Структурированные данные помогают:

1. **Улучшить отображение в поисковой выдаче** - Rich Snippets, Featured Snippets
2. **Повысить CTR** - более привлекательные результаты поиска
3. **Улучшить понимание контента** поисковыми системами
4. **Получить дополнительные возможности** - голосовой поиск, Knowledge Graph

## Примеры результатов

### FAQ Schema в поисковой выдаче
- Отображение вопросов прямо в результатах поиска
- Возможность раскрытия ответов без перехода на сайт

### Product Schema
- Отображение цены, рейтинга и наличия
- Rich snippets с изображением продукта

### Breadcrumb Schema
- Навигационная цепочка в результатах поиска
- Лучшее понимание структуры сайта

## Настройка и конфигурация

### Включение/отключение функциональности

```python
# В настройках генерации страницы
result = await page_service.generate_page(
    content=content,
    structured_data=True,  # True/False - включить/отключить
    # ...
)
```

### Кастомизация промптов для ИИ

Промпты для извлечения данных можно кастомизировать в `generator.py`:

```python
def _get_faq_extraction_prompt(self, content: str) -> str:
    # Кастомизированный промпт для FAQ
    return f"Анализируй контент и извлеки FAQ: {content}"
```

## Тестирование

Запустите тесты для проверки функциональности:

```bash
cd backend
python test_structured_data.py
```

Тесты покрывают:
- Генерацию всех типов схем
- Внедрение в HTML
- Множественные схемы
- Валидацию JSON-LD

## Ограничения и рекомендации

1. **Размер контента**: Для больших текстов ИИ анализирует первые 1500 символов
2. **Качество данных**: Результат зависит от качества входного контента
3. **Производительность**: Генерация схем добавляет время к процессу создания страницы
4. **API лимиты**: При использовании внешних ИИ провайдеров учитывайте лимиты запросов

## Будущие улучшения

- Поддержка дополнительных типов схем (Event, Recipe, LocalBusiness)
- Визуальный редактор структурированных данных
- Кэширование сгенерированных схем
- Аналитика эффективности структурированных данных

## Поддержка

При возникновении проблем:

1. Проверьте логи сервиса
2. Убедитесь, что ИИ провайдер настроен корректно
3. Проверьте формат входных данных
4. Используйте валидаторы schema.org для проверки результатов
