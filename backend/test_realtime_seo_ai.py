#!/usr/bin/env python3
"""
Тестовый скрипт для демонстрации real-time SEO AI интеграции

Этот скрипт демонстрирует как работает интеграция между SEO Analyzer и AI генератором
в режиме реального времени.
"""

import asyncio
import uuid
from datetime import datetime

from app.modules.seo.realtime_integration import realtime_integrator


# Тестовый HTML с плохим SEO
BAD_SEO_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Test</title>
</head>
<body>
    <h2>Some content</h2>
    <p>This is a very short content.</p>
    <img src="test.jpg">
    <a href="http://example.com">Link</a>
</body>
</html>
"""

# HTML с неплохим SEO для сравнения
GOOD_SEO_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Качественный контент о современных технологиях - Наш Сайт</title>
    <meta name="description" content="Узнайте о последних новостях в области технологий, искусственного интеллекта и веб-разработки. Экспертные статьи и аналитика от профессионалов.">
</head>
<body>
    <h1>Современные технологии и их влияние на будущее</h1>
    <h2>Искусственный интеллект в веб-разработке</h2>
    <p>Искусственный интеллект революционизирует способы создания веб-сайтов и приложений. 
    Современные инструменты позволяют автоматизировать процессы разработки, улучшить пользовательский опыт 
    и создавать более эффективные решения для бизнеса.</p>
    
    <h2>Преимущества современных технологий</h2>
    <p>Использование передовых технологий в веб-разработке открывает новые возможности для создания 
    интерактивных и адаптивных веб-сайтов. Это включает в себя улучшенную производительность, 
    лучшую безопасность и повышенную доступность для пользователей.</p>
    
    <img src="technology.jpg" alt="Современные технологии в действии" loading="lazy">
    
    <p>Для получения дополнительной информации о наших услугах, посетите 
    <a href="/services">страницу услуг</a> или свяжитесь с нашей 
    <a href="/contact">службой поддержки</a>.</p>
</body>
</html>
"""

# Контекст для улучшения
CONTENT_CONTEXT = {
    "title": "Современные технологии и SEO оптимизация",
    "description": "Полное руководство по современным технологиям веб-разработки и SEO оптимизации",
    "url": "https://example.com/modern-tech-seo",
    "author": "Экспертная команда",
    "type": "article",
    "image": "https://example.com/images/tech-seo.jpg",
    "site_name": "Технологический Портал"
}

TARGET_KEYWORDS = [
    "технологии",
    "веб-разработка", 
    "SEO оптимизация",
    "искусственный интеллект",
    "современные решения"
]


async def progress_callback(data):
    """Callback для отображения прогресса оптимизации"""
    print(f"[{data['timestamp']}] {data['message']} - {data['progress']}%")


async def test_bad_html_optimization():
    """Тест оптимизации плохого HTML"""
    print("=" * 80)
    print("ТЕСТ: Оптимизация HTML с плохим SEO")
    print("=" * 80)
    
    session_id = str(uuid.uuid4())
    
    try:
        result = await realtime_integrator.start_realtime_optimization(
            session_id=session_id,
            initial_html=BAD_SEO_HTML,
            context=CONTENT_CONTEXT,
            target_keywords=TARGET_KEYWORDS,
            progress_callback=progress_callback
        )
        
        print("\n📊 РЕЗУЛЬТАТЫ ОПТИМИЗАЦИИ:")
        print(f"⏱️  Время обработки: {result['processing_time']:.2f} сек")
        print(f"🔄 Циклов оптимизации: {result['optimization_result']['cycles_performed']}")
        print(f"📈 Общее количество улучшений: {result['optimization_result']['total_improvements']}")
        
        initial_score = result['initial_analysis'].get('seo_score', result['initial_analysis'].get('score', 0))
        final_score = result['optimization_result']['final_analysis'].get('seo_score', 
                      result['optimization_result']['final_analysis'].get('score', 0))
        
        print(f"📊 SEO балл: {initial_score} → {final_score} (+{final_score - initial_score})")
        
        print("\n🔧 ПРИМЕНЕННЫЕ ИСПРАВЛЕНИЯ:")
        for step in result['optimization_result']['optimization_steps']:
            if step['auto_fixes']:
                print(f"  Цикл {step['cycle']}:")
                for fix in step['auto_fixes']:
                    print(f"    ✅ {fix}")
        
        print(f"\n📝 ОПТИМИЗИРОВАННЫЙ HTML ({len(result['optimization_result']['optimized_html'])} символов):")
        print("-" * 40)
        print(result['optimization_result']['optimized_html'][:500] + "..." if len(result['optimization_result']['optimized_html']) > 500 else result['optimization_result']['optimized_html'])
        
        return result
        
    except Exception as e:
        print(f"❌ Ошибка при оптимизации: {str(e)}")
        return None


async def test_good_html_analysis():
    """Тест анализа хорошего HTML"""
    print("\n" + "=" * 80)
    print("ТЕСТ: Анализ HTML с хорошим SEO")
    print("=" * 80)
    
    session_id = str(uuid.uuid4())
    
    try:
        result = await realtime_integrator.start_realtime_optimization(
            session_id=session_id,
            initial_html=GOOD_SEO_HTML,
            context=CONTENT_CONTEXT,
            target_keywords=TARGET_KEYWORDS,
            progress_callback=progress_callback
        )
        
        print("\n📊 РЕЗУЛЬТАТЫ АНАЛИЗА:")
        print(f"⏱️  Время обработки: {result['processing_time']:.2f} сек")
        
        initial_score = result['initial_analysis'].get('seo_score', result['initial_analysis'].get('score', 0))
        final_score = result['optimization_result']['final_analysis'].get('seo_score', 
                      result['optimization_result']['final_analysis'].get('score', 0))
        
        print(f"📊 SEO балл: {initial_score} → {final_score}")
        
        if result['optimization_result']['cycles_performed'] > 0:
            print(f"🔄 Применено минорных улучшений: {result['optimization_result']['total_improvements']}")
        else:
            print("✅ HTML уже хорошо оптимизирован, улучшения не требуются")
        
        return result
        
    except Exception as e:
        print(f"❌ Ошибка при анализе: {str(e)}")
        return None


async def test_system_stats():
    """Тест получения статистики системы"""
    print("\n" + "=" * 80)
    print("СТАТИСТИКА СИСТЕМЫ")
    print("=" * 80)
    
    stats = realtime_integrator.get_system_stats()
    
    print(f"🔧 Выполнено оптимизаций: {stats['optimizations_performed']}")
    print(f"🤖 Сгенерировано AI предложений: {stats['ai_suggestions_generated']}")
    print(f"🔄 Общее количество циклов: {stats['total_cycles']}")
    print(f"⏱️  Среднее время обработки: {stats['average_processing_time']:.2f} сек")
    print(f"📈 Средний прирост SEO баллов: {stats['average_score_improvement']:.1f}")
    print(f"🎛️  Активных сессий: {stats['active_sessions_count']}")
    
    print("\n⚙️  КОНФИГУРАЦИЯ:")
    config = stats['config']
    print(f"  📊 Порог автооптимизации: {config['min_score_threshold']}")
    print(f"  🔄 Лимит циклов: {config['optimization_cycles_limit']}")
    print(f"  🤖 Порог для AI: {config['ai_suggestions_threshold']}")
    print(f"  ⚡ Автооптимизация: {'Включена' if config['auto_optimization'] else 'Отключена'}")


async def test_event_system():
    """Тест системы событий"""
    print("\n" + "=" * 80)
    print("ТЕСТ: Система событий")
    print("=" * 80)
    
    events_received = []
    
    async def event_handler(data):
        events_received.append(data)
        print(f"📡 Событие получено: {data}")
    
    # Подписываемся на события
    realtime_integrator.add_event_callback("analysis_complete", event_handler)
    realtime_integrator.add_event_callback("optimization_applied", event_handler)
    
    # Запускаем короткую оптимизацию
    session_id = str(uuid.uuid4())
    short_html = "<html><head><title>Test</title></head><body><h1>Test</h1></body></html>"
    
    await realtime_integrator.start_realtime_optimization(
        session_id=session_id,
        initial_html=short_html,
        context={"title": "Test Page"},
        target_keywords=["test"],
        progress_callback=None
    )
    
    print(f"\n📊 Получено событий: {len(events_received)}")
    
    # Отписываемся от событий
    realtime_integrator.remove_event_callback("analysis_complete", event_handler)
    realtime_integrator.remove_event_callback("optimization_applied", event_handler)


async def main():
    """Главная функция тестирования"""
    print("🚀 ЗАПУСК ТЕСТОВ REAL-TIME SEO AI ИНТЕГРАЦИИ")
    print(f"🕐 Время начала: {datetime.now()}")
    
    # Тест 1: Оптимизация плохого HTML
    await test_bad_html_optimization()
    
    # Небольшая пауза между тестами
    await asyncio.sleep(1)
    
    # Тест 2: Анализ хорошего HTML
    await test_good_html_analysis()
    
    # Тест 3: Статистика системы
    await test_system_stats()
    
    # Тест 4: Система событий
    await test_event_system()
    
    print("\n" + "=" * 80)
    print("✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")
    print("=" * 80)
    
    # Финальная статистика
    final_stats = realtime_integrator.get_system_stats()
    print(f"\n📊 ФИНАЛЬНАЯ СТАТИСТИКА:")
    print(f"   Всего оптимизаций: {final_stats['optimizations_performed']}")
    print(f"   AI предложений: {final_stats['ai_suggestions_generated']}")
    print(f"   Среднее время: {final_stats['average_processing_time']:.2f} сек")


if __name__ == "__main__":
    asyncio.run(main())
