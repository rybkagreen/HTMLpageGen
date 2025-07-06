# Расширенный SEO Анализатор

## Обзор

Расширенный SEO анализатор предоставляет комплексный анализ веб-страниц с проверкой:
- **Open Graph** метатегов для социальных сетей
- **Twitter Cards** для оптимизации в Twitter
- **Метрик производительности** (размеры ресурсов, минификация, отложенная загрузка)

## Новые компоненты

### 1. OpenGraphAnalyzer

Анализирует и генерирует Open Graph метатеги для улучшения отображения в социальных сетях.

#### Функциональность:
- Проверка обязательных OG свойств (`og:title`, `og:description`, `og:type`, `og:url`, `og:image`)
- Валидация рекомендуемых свойств (`og:site_name`, `og:locale`, `og:image:alt`)
- Специальная поддержка статей (`article:author`, `article:published_time`)
- Анализ изображений (размеры, форматы, alt-тексты)
- Автоматическая генерация оптимизированных тегов

#### API:
```python
from app.modules.seo.open_graph_analyzer import OpenGraphAnalyzer

analyzer = OpenGraphAnalyzer()

# Анализ HTML
analysis = analyzer.analyze_open_graph(html)

# Генерация тегов
content_data = {
    "title": "Заголовок",
    "description": "Описание",
    "type": "article",
    "url": "https://example.com",
    "image": "https://example.com/image.jpg"
}
tags = analyzer.generate_og_tags(content_data)
```

### 2. TwitterCardsAnalyzer

Анализирует и генерирует Twitter Cards метатеги для оптимизации отображения в Twitter.

#### Поддерживаемые типы карточек:
- **summary** - стандартная карточка с изображением и текстом
- **summary_large_image** - карточка с большим изображением
- **app** - карточка для мобильного приложения
- **player** - карточка для видео/аудио контента

#### Функциональность:
- Валидация полей для каждого типа карточки
- Проверка совместимости с Open Graph
- Анализ изображений и плееров
- Генерация оптимизированных тегов

#### API:
```python
from app.modules.seo.twitter_cards_analyzer import TwitterCardsAnalyzer

analyzer = TwitterCardsAnalyzer()

# Анализ HTML
analysis = analyzer.analyze_twitter_cards(html)

# Генерация тегов
content_data = {
    "title": "Заголовок",
    "description": "Описание",
    "image": "https://example.com/image.jpg",
    "twitter_card_type": "summary_large_image"
}
tags = analyzer.generate_twitter_tags(content_data)
```

### 3. PerformanceAnalyzer

Анализирует производительность веб-страницы с проверкой размеров ресурсов, минификации и оптимизации загрузки.

#### Анализируемые аспекты:
- **Ресурсы**: CSS, JavaScript, изображения, шрифты
- **Минификация**: HTML, инлайн CSS/JS
- **Отложенная загрузка**: изображения, iframe
- **Критический CSS**: инлайн стили для выше фолда
- **DOM структура**: количество элементов, глубина
- **Блокирующие ресурсы**: CSS и JS в head

#### Пороговые значения:
- HTML: 50KB (хорошо) / 100KB (предупреждение) / 200KB (критично)
- CSS: 30KB (хорошо) / 75KB (предупреждение) / 150KB (критично)
- JavaScript: 50KB (хорошо) / 100KB (предупреждение) / 200KB (критично)
- Изображения: 100KB (хорошо) / 500KB (предупреждение) / 1MB (критично)
- HTTP запросы: 30 (хорошо) / 50 (предупреждение) / 100 (критично)
- DOM элементы: 1500 (хорошо) / 3000 (предупреждение) / 5000 (критично)

#### API:
```python
from app.modules.seo.performance_analyzer import PerformanceAnalyzer

analyzer = PerformanceAnalyzer()

# Анализ производительности
analysis = analyzer.analyze_performance(html)
```

## Обновленный SEOService

Основной сервис теперь включает все новые анализаторы и предоставляет комплексную оценку.

### Новая структура ответа:
```json
{
  "score": 85,
  "title": {...},
  "meta_description": {...},
  "headings": {...},
  "images": {...},
  "links": {...},
  "content": {...},
  "open_graph": {
    "score": 90,
    "og_tags_found": {...},
    "required_properties": {...},
    "recommendations": [...]
  },
  "twitter_cards": {
    "score": 85,
    "card_type": "summary_large_image",
    "required_fields": {...},
    "recommendations": [...]
  },
  "performance": {
    "performance_score": 75,
    "resources": {...},
    "minification": {...},
    "lazy_loading": {...},
    "recommendations": [...]
  },
  "issues": [...],
  "recommendations": [...]
}
```

### Формула расчета общей оценки:
- Базовый SEO: 40%
- Open Graph: 20%
- Twitter Cards: 15%
- Производительность: 25%

## Новые API эндпоинты

### Специализированные анализы:

#### POST /seo/analyze/open-graph
Анализ только Open Graph метатегов.

#### POST /seo/analyze/twitter-cards
Анализ только Twitter Cards метатегов.

#### POST /seo/analyze/performance
Анализ только производительности.

### Генерация метатегов:

#### POST /seo/generate/meta-tags
Генерация оптимизированных метатегов.

**Запрос:**
```json
{
  "content_data": {
    "title": "Заголовок страницы",
    "description": "Описание страницы",
    "image": "https://example.com/image.jpg",
    "url": "https://example.com/page"
  },
  "include_og": true,
  "include_twitter": true
}
```

### Справочные эндпоинты:

#### GET /seo/performance/thresholds
Получение пороговых значений для анализа производительности.

#### GET /seo/social-media/best-practices
Лучшие практики для социальных сетей.

## Использование

### Базовый анализ:
```python
# Через API
POST /seo/analyze
{
  "html": "<html>...</html>"
}

# Напрямую через сервис
from app.modules.seo.service import SEOService

service = SEOService()
analysis = service.analyze_html(html)
```

### Специализированный анализ:
```python
# Open Graph
POST /seo/analyze/open-graph
{
  "html": "<html>...</html>"
}

# Twitter Cards
POST /seo/analyze/twitter-cards
{
  "html": "<html>...</html>"
}

# Производительность
POST /seo/analyze/performance
{
  "html": "<html>...</html>"
}
```

### Генерация метатегов:
```python
POST /seo/generate/meta-tags
{
  "content_data": {
    "title": "Статья о SEO",
    "description": "Подробное руководство по SEO оптимизации",
    "type": "article",
    "url": "https://example.com/seo-guide",
    "image": "https://example.com/seo-image.jpg",
    "author": "Эксперт SEO",
    "published_time": "2024-01-15T10:00:00Z"
  },
  "include_og": true,
  "include_twitter": true
}
```

## Тестирование

Запустите тесты для проверки всей функциональности:

```bash
python test_enhanced_seo_analyzer.py
```

Тесты проверяют:
- Анализ корректного HTML
- Выявление проблем в некорректном HTML
- Генерацию рекомендаций
- Создание оптимизированных метатегов
- Все новые анализаторы

## Рекомендации по использованию

### Open Graph:
1. Всегда включайте обязательные теги: `og:title`, `og:description`, `og:type`, `og:url`, `og:image`
2. Используйте изображения размером минимум 1200x630 пикселей
3. Добавляйте `og:image:alt` для доступности
4. Для статей используйте специальные теги `article:*`

### Twitter Cards:
1. Выберите подходящий тип карточки
2. Для большинства случаев используйте `summary_large_image`
3. Соблюдайте ограничения по длине текста
4. Добавляйте `@username` для связи с аккаунтом

### Производительность:
1. Минифицируйте все ресурсы
2. Используйте отложенную загрузку для изображений
3. Выделяйте критический CSS
4. Избегайте блокирующих ресурсов в `<head>`
5. Оптимизируйте размеры изображений

## Интеграция с существующим кодом

Новая функциональность полностью совместима с существующим SEO анализатором. Все существующие API остаются рабочими, но теперь возвращают расширенную информацию.

Для постепенной миграции:
1. Используйте новые эндпоинты для специализированного анализа
2. Обновите фронтенд для отображения новых метрик
3. Интегрируйте генерацию метатегов в CMS
4. Добавьте мониторинг производительности
