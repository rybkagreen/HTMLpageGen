# Модуль автоматических SEO рекомендаций

Этот модуль обеспечивает автоматическую интеграцию SEO рекомендаций в процесс генерации и правки HTML. Он анализирует структуру и семантику контента, предоставляет персонализированные рекомендации и автоматически исправляет распространенные SEO проблемы.

## 🚀 Основные функции

- **Автоматический анализ SEO**: Комплексная проверка HTML на соответствие SEO стандартам
- **Интеллектуальные рекомендации**: Персонализированные советы на основе контента и целевой аудитории  
- **Автоматические исправления**: Автоматическое применение критических SEO улучшений
- **Анализ ключевых слов**: Проверка плотности, распределения и оптимизация ключевых слов
- **Анализ читаемости**: Оценка читаемости контента с рекомендациями по улучшению
- **Техническое SEO**: Проверка мета-тегов, структуры, производительности
- **Структурированные данные**: Автоматическое добавление JSON-LD разметки

## 📦 Установка зависимостей

```bash
pip install nltk==3.8.1 textstat==0.7.3 beautifulsoup4==4.12.2
```

## 🎯 Быстрый старт

### 1. Базовое использование SEOIntegrator

```python
from app.modules.seo.integrator import SEOIntegrator

# Инициализация интегратора
integrator = SEOIntegrator()

# HTML для анализа
html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body>
    <p>Ваш контент здесь...</p>
</body>
</html>
"""

# Контекст контента
content_context = {
    "title": "Заголовок страницы",
    "description": "Описание страницы",
    "type": "article",
    "author": "Автор",
    "category": "категория"
}

# Интеграция SEO рекомендаций
result = integrator.integrate_seo_recommendations(
    html=html,
    content_context=content_context,
    target_keywords=["ключевое слово", "второе слово"],
    target_audience="general",
    auto_apply=True
)

print(f"SEO балл улучшен на {result['seo_score_improvement']} пунктов")
print(f"Оптимизированный HTML: {result['optimized_html']}")
```

### 2. Использование через API

#### Интеграция SEO рекомендаций
```bash
curl -X POST "http://localhost:8000/api/seo/integrate" \
-H "Content-Type: application/json" \
-d '{
  "html": "<html><body><p>Ваш контент</p></body></html>",
  "target_keywords": ["программирование", "веб-разработка"],
  "target_audience": "general",
  "auto_apply": true,
  "content_context": {
    "title": "Руководство по программированию",
    "description": "Полное руководство для начинающих",
    "type": "article"
  }
}'
```

#### Генерация SEO отчета
```bash
curl -X POST "http://localhost:8000/api/seo/report" \
-H "Content-Type: application/json" \
-d '{
  "html": "<html><body><p>Ваш контент</p></body></html>",
  "target_keywords": ["программирование", "веб-разработка"]
}'
```

### 3. Интеграция в генератор страниц

```python
from app.services.page_generator import PageGeneratorService

generator = PageGeneratorService()

result = await generator.generate_page(
    content="Ваш контент",
    template="default",
    auto_seo=True,  # Включить автоматическую SEO оптимизацию
    target_keywords=["ключевое слово"],
    target_audience="general",
    seo_options={
        "title": "Заголовок страницы",
        "description": "Описание страницы",
        "author": "Автор",
        "category": "технологии"
    }
)

print(f"SEO балл: {result['meta']['seo_score']}")
print(f"Применённые улучшения: {result['meta']['seo_improvements']}")
```

## 🔧 Конфигурация

### Настройки автоматических исправлений

```python
integrator = SEOIntegrator()

# Настройка автоматических исправлений
integrator.auto_fix_config = {
    "title": {
        "auto_fix": True,
        "fallback_template": "{content_title} | Ваш сайт"
    },
    "meta_description": {
        "auto_fix": True,
        "fallback_template": "Узнайте больше о {main_topic}. Полезная информация."
    },
    "headings": {
        "auto_fix": True,
        "ensure_h1": True
    },
    "images": {
        "auto_fix": True,
        "default_alt": "Информативное изображение"
    },
    "internal_linking": {
        "auto_suggest": True,
        "min_links": 2
    }
}
```

## 📊 Типы анализа

### 1. Базовый SEO анализ
- ✅ Title тег (длина 30-60 символов)
- ✅ Meta description (120-160 символов)  
- ✅ Структура заголовков (H1-H6)
- ✅ Alt атрибуты изображений
- ✅ Внутренние и внешние ссылки

### 2. Анализ ключевых слов
- 🎯 Плотность ключевых слов (оптимум 1-2%)
- 🎯 Распределение по странице
- 🎯 Использование в критических местах
- 🎯 Обнаружение переспама

### 3. Анализ читаемости
- 📖 Flesch Reading Ease оценка
- 📖 Средняя длина предложений
- 📖 Структура абзацев
- 📖 Рекомендации по упрощению текста

### 4. Технический SEO
- ⚙️ Мета-теги (viewport, charset, robots)
- ⚙️ Структурированные данные (JSON-LD)
- ⚙️ Open Graph теги
- ⚙️ Атрибут lang
- ⚙️ Производительность изображений

## 🎨 Автоматические улучшения

### Что исправляется автоматически:

1. **Критические проблемы**:
   - Добавление отсутствующих title и meta description
   - Создание H1 заголовка при его отсутствии
   - Добавление alt атрибутов к изображениям
   - Добавление viewport мета-тега

2. **Технические улучшения**:
   - Добавление атрибута lang к HTML
   - Добавление структурированных данных JSON-LD
   - Создание Open Graph тегов
   - Оптимизация изображений (loading="lazy")

3. **Контентные улучшения**:
   - Предложения внутренних ссылок
   - Оптимизация заголовков для ключевых слов
   - Добавление хлебных крошек

## 📋 API Endpoints

### POST /api/seo/integrate
Интеграция SEO рекомендаций с автоматическими исправлениями

**Параметры:**
```json
{
  "html": "string",
  "target_keywords": ["string"],
  "target_audience": "general|professional|academic",
  "auto_apply": true,
  "content_context": {
    "title": "string",
    "description": "string",
    "type": "article|webpage",
    "author": "string",
    "category": "string"
  }
}
```

### POST /api/seo/report
Генерация подробного SEO отчета

### GET /api/seo/keywords/analysis
Советы по анализу ключевых слов

### GET /api/seo/technical/checklist
Технический SEO чеклист

### GET /api/seo/readability/guidelines
Рекомендации по читаемости контента

## 🧪 Тестирование

Для тестирования модуля используйте включённый тестовый скрипт:

```bash
cd backend
python test_seo_integration.py
```

Скрипт демонстрирует:
- Автоматическую интеграцию SEO рекомендаций
- Генерацию подробных отчетов
- Применение улучшений к HTML

## 🔍 Примеры результатов

### До оптимизации:
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body>
    <p>Простой текст без SEO оптимизации.</p>
    <img src="image.jpg">
</body>
</html>
```

### После оптимизации:
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Руководство по веб-программированию | Программирование.ру</title>
    <meta name="description" content="Полное руководство по изучению веб-программирования и разработке приложений">
    <meta property="og:title" content="Руководство по веб-программированию">
    <meta property="og:description" content="Полное руководство по изучению веб-программирования">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "Руководство по веб-программированию",
      "description": "Полное руководство по изучению веб-программирования"
    }
    </script>
</head>
<body>
    <h1>Руководство по веб-программированию</h1>
    <p>Простой текст без SEO оптимизации.</p>
    <img src="image.jpg" alt="Image" loading="lazy">
</body>
</html>
```

## 📈 Метрики и оценки

Модуль использует систему оценок от 0 до 100:

- **90-100**: Отличное SEO
- **70-89**: Хорошее SEO  
- **50-69**: Удовлетворительное SEO
- **30-49**: Требует улучшений
- **0-29**: Критичные проблемы

### Весовые коэффициенты:
- Title и Meta Description: 30 баллов
- Структура заголовков: 15 баллов
- Ключевые слова: 20 баллов
- Читаемость: 15 баллов
- Технические аспекты: 10 баллов
- Изображения: 10 баллов

## 🛠️ Расширение функциональности

### Добавление кастомных рекомендаций

```python
class CustomSEOAdvisor(SEOAdvisor):
    def _generate_custom_recommendations(self, analysis):
        recommendations = []
        
        # Ваша кастомная логика
        if some_condition:
            recommendations.append({
                "type": "suggestion",
                "category": "custom",
                "issue": "Кастомная проблема",
                "recommendation": "Кастомная рекомендация",
                "impact": "medium"
            })
        
        return recommendations
```

### Добавление кастомных исправлений

```python
class CustomSEOIntegrator(SEOIntegrator):
    def _apply_custom_fixes(self, soup, recommendations):
        for rec in recommendations:
            if rec["category"] == "custom":
                # Ваша логика исправлений
                pass
        return soup
```

## ⚙️ Интеграция с существующими системами

### С WordPress

```python
def optimize_wordpress_post(post_content, post_meta):
    integrator = SEOIntegrator()
    
    content_context = {
        "title": post_meta.get("title"),
        "description": post_meta.get("excerpt"),
        "type": "article",
        "author": post_meta.get("author"),
        "category": post_meta.get("category")
    }
    
    result = integrator.integrate_seo_recommendations(
        html=post_content,
        content_context=content_context,
        target_keywords=post_meta.get("keywords", [])
    )
    
    return result["optimized_html"]
```

### С CMS системами

```python
def integrate_with_cms(cms_content, cms_metadata):
    integrator = SEOIntegrator()
    
    # Преобразование метаданных CMS в формат интегратора
    content_context = convert_cms_metadata(cms_metadata)
    
    # Применение SEO оптимизации
    result = integrator.integrate_seo_recommendations(
        html=cms_content,
        content_context=content_context,
        auto_apply=True
    )
    
    return {
        "optimized_content": result["optimized_html"],
        "seo_score": result["final_analysis"]["overall_score"],
        "improvements": result["improvements_applied"]
    }
```

## 🔒 Безопасность

- ✅ Все HTML обрабатывается через BeautifulSoup для безопасности
- ✅ Валидация входных данных
- ✅ Защита от XSS через правильную обработку контента
- ✅ Ограничения на размер обрабатываемого HTML

## 📚 Дополнительные ресурсы

- [Документация API](API_DOCUMENTATION.md)
- [Примеры использования](EXAMPLES.md)
- [Лучшие практики SEO](BEST_PRACTICES.md)

## 🤝 Вклад в развитие

Если вы хотите внести вклад в развитие модуля:

1. Создайте новую ветку для ваших изменений
2. Добавьте тесты для новой функциональности
3. Обновите документацию
4. Создайте Pull Request

## 📞 Поддержка

При возникновении проблем:

1. Проверьте установку всех зависимостей
2. Запустите тестовый скрипт для диагностики
3. Проверьте логи приложения
4. Создайте issue с описанием проблемы

## 📄 Лицензия

Модуль распространяется под той же лицензией, что и основное приложение.

---

**Модуль автоматических SEO рекомендаций** - мощный инструмент для улучшения поисковой оптимизации ваших веб-страниц. Он позволяет автоматизировать большинство рутинных задач SEO и обеспечивает высокое качество оптимизации контента.
