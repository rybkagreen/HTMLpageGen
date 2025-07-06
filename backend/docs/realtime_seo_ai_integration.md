# Real-time SEO AI Integration

## Обзор

Real-time SEO AI Integration - это система, которая обеспечивает автоматическую интеграцию между SEO Analyzer и AI генератором для мгновенной оптимизации HTML в процессе генерации.

## Основные компоненты

### 1. RealTimeSEOAIIntegrator

Главный компонент системы, который координирует взаимодействие между SEO анализатором и AI генератором.

**Местоположение:** `app/modules/seo/realtime_integration.py`

**Основные возможности:**
- Автоматический анализ HTML на предмет SEO проблем
- Применение автоматических исправлений
- Интеграция с AI для получения предложений по улучшению
- Циклическая оптимизация до достижения целевого SEO балла
- Статистика и мониторинг процесса

### 2. SEOWebSocketManager

Менеджер WebSocket соединений для real-time обмена данными.

**Местоположение:** `app/modules/seo/websocket_service.py`

**Основные возможности:**
- Управление WebSocket соединениями
- Real-time обновления прогресса оптимизации
- Обработка команд от клиентов
- Система событий для уведомлений

### 3. API Routes

REST API эндпоинты для интеграции с frontend.

**Местоположение:** `app/api/routes/seo_realtime.py`

## Архитектура системы

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway    │    │  AI Service     │
│   (React/Vue)   │◄──►│  (FastAPI)       │◄──►│  (OpenAI/Local) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         │ WebSocket              │ HTTP/REST              │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ WebSocket       │    │ RealTime         │    │ SEO Service     │
│ Manager         │◄──►│ SEO AI           │◄──►│ (Analyzer)      │
│                 │    │ Integrator       │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Использование

### 1. HTTP API

#### Запуск оптимизации

```bash
POST /api/seo-realtime/optimize
Content-Type: application/json

{
  "html": "<!DOCTYPE html>...",
  "context": {
    "title": "Заголовок страницы",
    "description": "Описание страницы",
    "url": "https://example.com/page"
  },
  "target_keywords": ["SEO", "оптимизация"],
  "auto_apply": true
}
```

#### Получение статуса сессии

```bash
GET /api/seo-realtime/session/{session_id}/status
```

#### Отмена сессии

```bash
DELETE /api/seo-realtime/session/{session_id}
```

#### Системная статистика

```bash
GET /api/seo-realtime/stats
```

### 2. WebSocket API

#### Подключение

```javascript
const ws = new WebSocket('ws://localhost:8000/api/seo-realtime/ws');

ws.onopen = function() {
  console.log('Соединение установлено');
};

ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Получено сообщение:', data);
};
```

#### Запуск оптимизации через WebSocket

```javascript
ws.send(JSON.stringify({
  type: 'start_optimization',
  html: '<!DOCTYPE html>...',
  context: {
    title: 'Заголовок страницы'
  },
  target_keywords: ['SEO', 'оптимизация']
}));
```

#### Получение системной статистики

```javascript
ws.send(JSON.stringify({
  type: 'get_system_stats'
}));
```

### 3. Программное использование

```python
from app.modules.seo.realtime_integration import realtime_integrator

async def optimize_html():
    # Callback для прогресса
    async def progress_callback(data):
        print(f"Прогресс: {data['progress']}% - {data['message']}")
    
    # Запуск оптимизации
    result = await realtime_integrator.start_realtime_optimization(
        session_id="unique-session-id",
        initial_html="<!DOCTYPE html>...",
        context={
            "title": "Заголовок страницы",
            "description": "Описание страницы"
        },
        target_keywords=["SEO", "оптимизация"],
        progress_callback=progress_callback
    )
    
    print(f"Оптимизированный HTML: {result['optimization_result']['optimized_html']}")
    print(f"SEO балл: {result['optimization_result']['final_analysis']['seo_score']}")
```

## Конфигурация

### Настройки системы

```python
config = {
    "auto_optimization": True,              # Автоматическая оптимизация
    "min_score_threshold": 70,             # Минимальный SEO балл для оптимизации
    "critical_issues_auto_fix": True,      # Автоисправление критических проблем
    "optimization_cycles_limit": 3,        # Максимум циклов оптимизации
    "ai_suggestions_threshold": 60,        # Балл для запроса AI предложений
    "analysis_debounce_ms": 500           # Задержка для группировки изменений
}

# Обновление конфигурации
realtime_integrator.update_config(config)
```

### Изменение конфигурации через API

```bash
PUT /api/seo-realtime/config
Content-Type: application/json

{
  "min_score_threshold": 80,
  "optimization_cycles_limit": 5,
  "ai_suggestions_threshold": 70
}
```

## События системы

### Типы событий

1. **analysis_complete** - Анализ HTML завершен
2. **optimization_applied** - Применена оптимизация
3. **ai_suggestion_generated** - AI сгенерировал предложение
4. **error_occurred** - Произошла ошибка

### Подписка на события

```python
async def my_event_handler(data):
    print(f"Событие: {data}")

# Подписка
realtime_integrator.add_event_callback("analysis_complete", my_event_handler)

# Отписка
realtime_integrator.remove_event_callback("analysis_complete", my_event_handler)
```

## Мониторинг и статистика

### Системная статистика

```python
stats = realtime_integrator.get_system_stats()

print(f"Выполнено оптимизаций: {stats['optimizations_performed']}")
print(f"AI предложений: {stats['ai_suggestions_generated']}")
print(f"Среднее время обработки: {stats['average_processing_time']}")
print(f"Средний прирост SEO баллов: {stats['average_score_improvement']}")
```

### WebSocket статистика

```bash
GET /api/seo-realtime/ws/stats
```

## Тестирование

### Запуск тестов

```bash
# Основные тесты интеграции
python test_realtime_seo_ai.py

# Тесты WebSocket
python -m pytest tests/test_websocket_service.py

# Тесты API
python -m pytest tests/test_seo_realtime_api.py
```

### Пример теста

```python
import asyncio
from app.modules.seo.realtime_integration import realtime_integrator

async def test_optimization():
    html = "<!DOCTYPE html><html><head><title>Test</title></head><body><h2>Content</h2></body></html>"
    
    result = await realtime_integrator.start_realtime_optimization(
        session_id="test-session",
        initial_html=html,
        context={"title": "Test Page"},
        target_keywords=["test"]
    )
    
    assert result['optimization_result']['cycles_performed'] > 0
    assert 'optimized_html' in result['optimization_result']

asyncio.run(test_optimization())
```

## Принцип работы

### Алгоритм оптимизации

1. **Первичный анализ** - SEO анализ исходного HTML
2. **Проверка порога** - Если балл выше порога, минимальная оптимизация
3. **Цикл оптимизации:**
   - Выявление критических проблем
   - Применение автоматических исправлений
   - Запрос AI предложений (если балл низкий)
   - Валидация улучшений
4. **Финализация** - Финальный анализ и статистика

### Типы автоматических исправлений

- **Критические:** Добавление отсутствующих title, meta description, H1
- **Технические:** Viewport meta тег, lang атрибут, charset
- **Изображения:** Alt атрибуты, lazy loading
- **Ссылки:** rel="noopener" для внешних ссылок
- **Open Graph:** Базовые OG теги

### AI интеграция

- Запрос к AI происходит только при низком SEO балле
- AI получает контекст проблем и генерирует улучшения
- Результаты валидируются перед применением
- AI может предложить улучшения контента, структуры, мета-тегов

## Ограничения и рекомендации

### Ограничения

- Максимум 3 цикла оптимизации по умолчанию
- AI запросы ограничены размером HTML (не более 2x от оригинала)
- WebSocket соединения имеют таймаут
- Одновременно может выполняться ограниченное количество сессий

### Рекомендации

- Используйте содержательный контекст для лучших результатов AI
- Устанавливайте разумные целевые ключевые слова
- Мониторьте системную статистику для оптимизации производительности
- Используйте WebSocket для real-time обновлений в UI
- Кэшируйте результаты для похожих HTML

## Примеры использования

### Интеграция в редактор

```javascript
// Подключение WebSocket
const seoWS = new WebSocket('ws://localhost:8000/api/seo-realtime/ws');

// Автоматическая оптимизация при изменении HTML
let debounceTimer;
editor.onchange = function(html) {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    seoWS.send(JSON.stringify({
      type: 'start_optimization',
      html: html,
      context: getPageContext(),
      target_keywords: getKeywords()
    }));
  }, 500);
};

// Обработка результатов
seoWS.onmessage = function(event) {
  const data = JSON.parse(event.data);
  
  if (data.type === 'optimization_completed') {
    updateSEOScore(data.result.optimization_result.final_analysis.seo_score);
    showOptimizedHTML(data.result.optimization_result.optimized_html);
  }
  
  if (data.type === 'optimization_progress') {
    updateProgressBar(data.progress);
  }
};
```

### Batch обработка

```python
async def optimize_multiple_pages(pages):
    results = []
    
    for page in pages:
        try:
            result = await realtime_integrator.start_realtime_optimization(
                session_id=f"batch-{page['id']}",
                initial_html=page['html'],
                context=page['context'],
                target_keywords=page['keywords']
            )
            results.append(result)
        except Exception as e:
            print(f"Ошибка оптимизации страницы {page['id']}: {e}")
    
    return results
```

## Troubleshooting

### Частые проблемы

1. **AI не генерирует предложения**
   - Проверьте настройки AI провайдера
   - Убедитесь что SEO балл ниже порога ai_suggestions_threshold

2. **WebSocket соединение разрывается**
   - Реализуйте переподключение
   - Используйте ping-pong для поддержания соединения

3. **Медленная оптимизация**
   - Уменьшите optimization_cycles_limit
   - Оптимизируйте HTML перед отправкой

4. **Высокое потребление ресурсов**
   - Ограничьте количество одновременных сессий
   - Используйте кэширование результатов

### Логирование

```python
import logging

# Включение подробного логирования
logging.getLogger('app.modules.seo.realtime_integration').setLevel(logging.DEBUG)
logging.getLogger('app.modules.seo.websocket_service').setLevel(logging.DEBUG)
```

## Безопасность

### Рекомендации по безопасности

- Валидируйте HTML перед обработкой
- Ограничивайте размер входящих данных
- Используйте HTTPS для WebSocket соединений
- Реализуйте аутентификацию для WebSocket
- Мониторьте использование ресурсов

### Ограничения доступа

```python
# Ограничение количества активных сессий на пользователя
user_sessions = {}

async def check_user_limit(user_id):
    if user_id in user_sessions and len(user_sessions[user_id]) >= 3:
        raise HTTPException(status_code=429, detail="Превышен лимит активных сессий")
```

## Расширение функциональности

### Добавление нового типа анализа

```python
class CustomSEOAnalyzer:
    def analyze(self, html):
        # Ваша логика анализа
        return {"custom_score": 85, "issues": []}

# Интеграция в систему
realtime_integrator.add_analyzer("custom", CustomSEOAnalyzer())
```

### Кастомные AI провайдеры

```python
class CustomAIProvider(AIProvider):
    async def suggest_improvements(self, html):
        # Ваша логика AI предложений
        return ["Улучшение 1", "Улучшение 2"]

# Использование
ai_service.set_provider(CustomAIProvider())
```

Эта документация покрывает все основные аспекты использования real-time SEO AI интеграции. Система готова к использованию и может быть расширена под конкретные потребности проекта.
