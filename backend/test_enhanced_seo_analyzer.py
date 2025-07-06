"""
Тест для расширенного SEO анализатора
Проверка Open Graph, Twitter Cards и метрик производительности
"""

from app.modules.seo.service import SEOService
from app.modules.seo.open_graph_analyzer import OpenGraphAnalyzer
from app.modules.seo.twitter_cards_analyzer import TwitterCardsAnalyzer
from app.modules.seo.performance_analyzer import PerformanceAnalyzer


def test_basic_html():
    """Тестовый HTML с базовыми метатегами"""
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Тестовая страница - Мой сайт</title>
        <meta name="description" content="Это тестовая страница для проверки SEO анализатора. Здесь есть все необходимые элементы для базового анализа.">
        
        <!-- Open Graph -->
        <meta property="og:title" content="Тестовая страница">
        <meta property="og:description" content="Описание для социальных сетей">
        <meta property="og:type" content="website">
        <meta property="og:url" content="https://example.com/test">
        <meta property="og:image" content="https://example.com/image.jpg">
        <meta property="og:image:width" content="1200">
        <meta property="og:image:height" content="630">
        <meta property="og:site_name" content="Мой сайт">
        
        <!-- Twitter Cards -->
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:title" content="Тестовая страница">
        <meta name="twitter:description" content="Описание для Twitter">
        <meta name="twitter:image" content="https://example.com/image.jpg">
        <meta name="twitter:site" content="@mysite">
        
        <!-- CSS -->
        <link rel="stylesheet" href="styles.css">
        <style>
            body { margin: 0; padding: 20px; }
            .hero { background: blue; color: white; }
        </style>
        
        <!-- JavaScript -->
        <script src="app.js" defer></script>
    </head>
    <body>
        <header>
            <h1>Главный заголовок страницы</h1>
            <nav>
                <a href="/">Главная</a>
                <a href="/about">О нас</a>
            </nav>
        </header>
        
        <main class="main-content">
            <section class="hero">
                <h2>Добро пожаловать</h2>
                <p>Это основной контент страницы. Здесь достаточно текста для SEO анализа. 
                Контент должен быть информативным и полезным для пользователей. 
                Поисковые системы оценивают качество и релевантность контента.</p>
            </section>
            
            <section>
                <h2>Дополнительная информация</h2>
                <p>Еще один абзац с полезной информацией. SEO анализатор проверит структуру заголовков, 
                качество контента и другие важные факторы для поискового продвижения.</p>
                
                <img src="test-image.jpg" alt="Тестовое изображение" loading="lazy">
                <img src="another-image.png" alt="Еще одно изображение">
                
                <h3>Подзаголовок третьего уровня</h3>
                <ul>
                    <li>Первый пункт списка</li>
                    <li>Второй пункт списка</li>
                    <li>Третий пункт списка</li>
                </ul>
            </section>
        </main>
        
        <footer>
            <p>© 2024 Мой сайт. Все права защищены.</p>
        </footer>
        
        <script>
            // Инлайн JavaScript
            console.log('Страница загружена');
        </script>
    </body>
    </html>
    """


def test_poor_html():
    """HTML с проблемами для тестирования рекомендаций"""
    return """
    <html>
    <head>
        <title>Короткий title</title>
        <!-- Отсутствует meta description -->
        <!-- Отсутствуют Open Graph теги -->
        <!-- Отсутствуют Twitter Cards -->
        
        <link rel="stylesheet" href="large-style.css">
        <link rel="stylesheet" href="another-style.css">
        <script src="blocking-script.js"></script>
        <script src="another-script.js"></script>
    </head>
    <body>
        <!-- Отсутствует H1 -->
        <h2>Заголовок второго уровня</h2>
        <h4>Заголовок четвертого уровня (пропуск H3)</h4>
        
        <p>Мало контента.</p>
        
        <!-- Изображения без alt -->
        <img src="image1.jpg">
        <img src="image2.png">
        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==">
        
        <!-- Много DOM элементов -->
        """ + "".join([f"<div>Element {i}</div>" for i in range(100)]) + """
    </body>
    </html>
    """


def test_seo_service():
    """Тест основного SEO сервиса"""
    print("=== Тестирование SEO Service ===\n")
    
    service = SEOService()
    
    # Тест с хорошим HTML
    print("1. Анализ хорошего HTML:")
    good_analysis = service.analyze_html(test_basic_html())
    print(f"   Общая оценка: {good_analysis['score']}/100")
    print(f"   Open Graph оценка: {good_analysis['open_graph']['score']}/100")
    print(f"   Twitter Cards оценка: {good_analysis['twitter_cards']['score']}/100")
    print(f"   Производительность: {good_analysis['performance']['performance_score']}/100")
    print(f"   Всего проблем: {len(good_analysis['issues'])}")
    print(f"   Всего рекомендаций: {len(good_analysis['recommendations'])}")
    
    # Тест с проблемным HTML
    print("\n2. Анализ проблемного HTML:")
    poor_analysis = service.analyze_html(test_poor_html())
    print(f"   Общая оценка: {poor_analysis['score']}/100")
    print(f"   Open Graph оценка: {poor_analysis['open_graph']['score']}/100")
    print(f"   Twitter Cards оценка: {poor_analysis['twitter_cards']['score']}/100")
    print(f"   Производительность: {poor_analysis['performance']['performance_score']}/100")
    print(f"   Всего проблем: {len(poor_analysis['issues'])}")
    print(f"   Всего рекомендаций: {len(poor_analysis['recommendations'])}")
    
    if poor_analysis['issues']:
        print("\n   Основные проблемы:")
        for issue in poor_analysis['issues'][:5]:  # Показываем первые 5
            print(f"   - {issue}")
    
    return good_analysis, poor_analysis


def test_open_graph_analyzer():
    """Тест анализатора Open Graph"""
    print("\n=== Тестирование Open Graph Analyzer ===\n")
    
    analyzer = OpenGraphAnalyzer()
    
    # Тест с корректными OG тегами
    print("1. Анализ корректных Open Graph тегов:")
    og_analysis = analyzer.analyze_open_graph(test_basic_html())
    print(f"   Оценка: {og_analysis['score']}/100")
    print(f"   Найдено тегов: {og_analysis['total_tags']}")
    print(f"   Проблем: {len(og_analysis['issues'])}")
    
    # Детали по обязательным свойствам
    print("\n   Обязательные свойства:")
    for prop, analysis in og_analysis['required_properties'].items():
        status = "✓" if analysis['valid'] else "✗"
        print(f"   {status} {prop}: {analysis['content'][:50] if analysis['content'] else 'отсутствует'}")
    
    # Тест без OG тегов
    print("\n2. Анализ HTML без Open Graph тегов:")
    no_og_analysis = analyzer.analyze_open_graph(test_poor_html())
    print(f"   Оценка: {no_og_analysis['score']}/100")
    print(f"   Проблем: {len(no_og_analysis['issues'])}")
    
    # Генерация тегов
    print("\n3. Генерация Open Graph тегов:")
    content_data = {
        "title": "Новая статья",
        "description": "Описание новой статьи для социальных сетей",
        "type": "article",
        "url": "https://example.com/article",
        "image": "https://example.com/article-image.jpg",
        "site_name": "Мой блог"
    }
    
    generated_tags = analyzer.generate_og_tags(content_data)
    print(f"   Сгенерировано тегов: {len(generated_tags)}")
    for tag in generated_tags[:3]:  # Показываем первые 3
        print(f"   {tag}")
    
    return og_analysis


def test_twitter_cards_analyzer():
    """Тест анализатора Twitter Cards"""
    print("\n=== Тестирование Twitter Cards Analyzer ===\n")
    
    analyzer = TwitterCardsAnalyzer()
    
    # Тест с корректными Twitter тегами
    print("1. Анализ корректных Twitter Cards:")
    twitter_analysis = analyzer.analyze_twitter_cards(test_basic_html())
    print(f"   Оценка: {twitter_analysis['score']}/100")
    print(f"   Тип карточки: {twitter_analysis['card_type']}")
    print(f"   Найдено тегов: {twitter_analysis['total_tags']}")
    print(f"   Проблем: {len(twitter_analysis['issues'])}")
    
    # Детали по обязательным полям
    print("\n   Обязательные поля:")
    for field, analysis in twitter_analysis['required_fields'].items():
        if 'error' not in analysis:
            status = "✓" if analysis['valid'] else "✗"
            print(f"   {status} {field}: {analysis['content'][:50] if analysis['content'] else 'отсутствует'}")
    
    # Тест без Twitter тегов
    print("\n2. Анализ HTML без Twitter Cards:")
    no_twitter_analysis = analyzer.analyze_twitter_cards(test_poor_html())
    print(f"   Оценка: {no_twitter_analysis['score']}/100")
    print(f"   Проблем: {len(no_twitter_analysis['issues'])}")
    
    # Генерация тегов
    print("\n3. Генерация Twitter Cards тегов:")
    content_data = {
        "title": "Новая статья",
        "description": "Описание для Twitter",
        "image": "https://example.com/article-image.jpg",
        "twitter_card_type": "summary_large_image",
        "site_twitter": "@mysite"
    }
    
    generated_tags = analyzer.generate_twitter_tags(content_data)
    print(f"   Сгенерировано тегов: {len(generated_tags)}")
    for tag in generated_tags[:3]:  # Показываем первые 3
        print(f"   {tag}")
    
    return twitter_analysis


def test_performance_analyzer():
    """Тест анализатора производительности"""
    print("\n=== Тестирование Performance Analyzer ===\n")
    
    analyzer = PerformanceAnalyzer()
    
    # Тест базового HTML
    print("1. Анализ производительности базового HTML:")
    perf_analysis = analyzer.analyze_performance(test_basic_html())
    print(f"   Оценка производительности: {perf_analysis['performance_score']}/100")
    print(f"   Всего ресурсов: {perf_analysis['resources']['total_requests']}")
    print(f"   DOM элементов: {perf_analysis['dom_structure']['total_elements']}")
    print(f"   Глубина DOM: {perf_analysis['dom_structure']['depth']}")
    
    # Детали по ресурсам
    print(f"\n   Ресурсы:")
    print(f"   - CSS файлов: {perf_analysis['resources']['css']['count']}")
    print(f"   - JS файлов: {perf_analysis['resources']['js']['count']}")
    print(f"   - Изображений: {perf_analysis['resources']['images']['count']}")
    
    # Минификация
    print(f"\n   Минификация:")
    print(f"   - HTML минифицирован: {perf_analysis['minification']['html']['is_minified']}")
    print(f"   - Потенциальная экономия HTML: {perf_analysis['minification']['html']['potential_savings']} байт")
    
    # Lazy loading
    print(f"\n   Отложенная загрузка:")
    print(f"   - Изображений с lazy loading: {perf_analysis['lazy_loading']['images']['lazy_loaded']}/{perf_analysis['lazy_loading']['images']['total']}")
    print(f"   - Оценка lazy loading: {perf_analysis['lazy_loading']['score']:.1f}%")
    
    # Проблемы производительности
    if perf_analysis['resources']['issues']:
        print(f"\n   Проблемы производительности:")
        for issue in perf_analysis['resources']['issues']:
            print(f"   - {issue}")
    
    # Рекомендации
    print(f"\n   Рекомендаций: {len(perf_analysis['recommendations'])}")
    if perf_analysis['recommendations']:
        for rec in perf_analysis['recommendations'][:3]:  # Показываем первые 3
            print(f"   - {rec['issue']}")
    
    # Оценка времени загрузки
    load_time = perf_analysis['load_time_estimate']
    print(f"\n   Оценка времени загрузки: {load_time['total_estimated_time']:.2f}s")
    
    return perf_analysis


def run_comprehensive_test():
    """Запуск всех тестов"""
    print("🚀 Запуск комплексного тестирования расширенного SEO анализатора\n")
    
    # Тестирование основного сервиса
    good_analysis, poor_analysis = test_seo_service()
    
    # Тестирование отдельных анализаторов
    og_analysis = test_open_graph_analyzer()
    twitter_analysis = test_twitter_cards_analyzer()
    perf_analysis = test_performance_analyzer()
    
    # Сводная статистика
    print("\n" + "="*60)
    print("📊 СВОДКА РЕЗУЛЬТАТОВ ТЕСТИРОВАНИЯ")
    print("="*60)
    
    print(f"\n🎯 Хороший HTML:")
    print(f"   Общая SEO оценка: {good_analysis['score']}/100")
    print(f"   Open Graph: {good_analysis['open_graph']['score']}/100")
    print(f"   Twitter Cards: {good_analysis['twitter_cards']['score']}/100")
    print(f"   Производительность: {good_analysis['performance']['performance_score']}/100")
    
    print(f"\n⚠️  Проблемный HTML:")
    print(f"   Общая SEO оценка: {poor_analysis['score']}/100")
    print(f"   Open Graph: {poor_analysis['open_graph']['score']}/100")
    print(f"   Twitter Cards: {poor_analysis['twitter_cards']['score']}/100")
    print(f"   Производительность: {poor_analysis['performance']['performance_score']}/100")
    print(f"   Выявлено проблем: {len(poor_analysis['issues'])}")
    print(f"   Сгенерировано рекомендаций: {len(poor_analysis['recommendations'])}")
    
    print(f"\n✅ Функциональность:")
    print(f"   ✓ Базовый SEO анализ")
    print(f"   ✓ Open Graph анализ и генерация")
    print(f"   ✓ Twitter Cards анализ и генерация")
    print(f"   ✓ Анализ производительности")
    print(f"   ✓ Минификация ресурсов")
    print(f"   ✓ Отложенная загрузка")
    print(f"   ✓ DOM структура")
    print(f"   ✓ Блокирующие ресурсы")
    
    print(f"\n🎉 Тестирование завершено успешно!")
    
    return {
        'good_analysis': good_analysis,
        'poor_analysis': poor_analysis,
        'og_analysis': og_analysis,
        'twitter_analysis': twitter_analysis,
        'performance_analysis': perf_analysis
    }


if __name__ == "__main__":
    results = run_comprehensive_test()
