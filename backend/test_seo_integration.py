#!/usr/bin/env python3
"""
Тестовый скрипт для демонстрации автоматической интеграции SEO рекомендаций
"""

import sys
import os

# Добавляем путь к модулям приложения
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.modules.seo.integrator import SEOIntegrator
from app.modules.seo.advisor import SEOAdvisor


def test_basic_html():
    """Тестирование базового HTML без SEO оптимизации"""
    
    html_without_seo = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <div>
            <p>Это простая веб-страница о программировании. 
            Здесь мы обсуждаем различные аспекты разработки веб-приложений.</p>
            
            <p>Программирование является важной частью современного мира. 
            Веб-разработка включает в себя множество технологий и подходов.</p>
            
            <img src="code-example.jpg">
            
            <p>Изучение программирования требует времени и практики. 
            Современные инструменты значительно упрощают процесс разработки.</p>
        </div>
    </body>
    </html>
    """
    
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ SEO ИНТЕГРАЦИИ")
    print("=" * 60)
    
    # Инициализация интегратора
    integrator = SEOIntegrator()
    
    # Контекст контента
    content_context = {
        "title": "Руководство по веб-программированию",
        "description": "Полное руководство по изучению веб-программирования и разработке приложений",
        "type": "article",
        "author": "Эксперт по программированию",
        "category": "технологии",
        "site_name": "Программирование.ру"
    }
    
    # Целевые ключевые слова
    target_keywords = ["программирование", "веб-разработка", "обучение"]
    
    print("Исходный HTML:")
    print("-" * 40)
    print(html_without_seo[:200] + "...")
    print()
    
    # Интеграция SEO рекомендаций
    result = integrator.integrate_seo_recommendations(
        html=html_without_seo,
        content_context=content_context,
        target_keywords=target_keywords,
        target_audience="general",
        auto_apply=True
    )
    
    print("РЕЗУЛЬТАТЫ АНАЛИЗА:")
    print("-" * 40)
    print(f"Исходный SEO балл: {result['original_analysis']['overall_score']}")
    print(f"Итоговый SEO балл: {result['final_analysis']['overall_score']}")
    print(f"Улучшение на: {result['seo_score_improvement']} баллов")
    print()
    
    print("ПРИМЕНЁННЫЕ УЛУЧШЕНИЯ:")
    print("-" * 40)
    for improvement in result['improvements_applied']['improvements_list']:
        print(f"✓ {improvement}")
    print()
    
    print("РЕКОМЕНДАЦИИ ДЛЯ РУЧНОЙ ПРОВЕРКИ:")
    print("-" * 40)
    for rec in result['recommendations_for_manual_review']:
        print(f"• [{rec['priority'].upper()}] {rec['issue']}")
        print(f"  Рекомендация: {rec['recommendation']}")
        print()
    
    print("ОПТИМИЗИРОВАННЫЙ HTML (первые 500 символов):")
    print("-" * 40)
    print(result['optimized_html'][:500] + "...")
    print()
    
    return result


def test_seo_report():
    """Тестирование генерации SEO отчета"""
    
    print("=" * 60)
    print("ГЕНЕРАЦИЯ ПОДРОБНОГО SEO ОТЧЕТА")
    print("=" * 60)
    
    integrator = SEOIntegrator()
    
    # Тестовый HTML с некоторыми проблемами
    test_html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Короткий заголовок</title>
        <!-- Отсутствует meta description -->
    </head>
    <body>
        <!-- Отсутствует H1 -->
        <h2>Веб-разработка</h2>
        
        <p>Это статья о веб-разработке. Веб-разработка веб-разработка веб-разработка. 
        Изучение веб-разработки требует знания веб-разработки и практики веб-разработки.</p>
        
        <!-- Изображение без alt -->
        <img src="example.jpg">
        
        <h3>Технологии</h3>
        <p>HTML, CSS, JavaScript являются основными технологиями для веб-разработки.</p>
        
        <!-- Нет внутренних ссылок -->
    </body>
    </html>
    """
    
    # Генерация отчета
    report = integrator.generate_seo_report(
        html=test_html,
        target_keywords=["веб-разработка", "технологии", "HTML"]
    )
    
    print("КРАТКАЯ СВОДКА:")
    print("-" * 40)
    summary = report['summary']
    print(f"Общий SEO балл: {summary['overall_score']}/100")
    print(f"Всего рекомендаций: {summary['total_recommendations']}")
    print(f"Критические проблемы: {summary['critical_issues']}")
    print(f"Предупреждения: {summary['warnings']}")
    print(f"Предложения: {summary['suggestions']}")
    print()
    
    print("ПРИОРИТЕТНЫЕ ДЕЙСТВИЯ:")
    print("-" * 40)
    for i, action in enumerate(summary['top_priorities'], 1):
        print(f"{i}. {action}")
    print()
    
    print("РЕКОМЕНДАЦИИ ПО КАТЕГОРИЯМ:")
    print("-" * 40)
    for category, recommendations in report['recommendations_by_category'].items():
        print(f"\n{category.upper()}:")
        for rec in recommendations:
            print(f"  • {rec['issue']}")
            print(f"    → {rec['recommendation']}")
    
    return report


def main():
    """Основная функция для запуска тестов"""
    try:
        print("Запуск тестирования SEO интеграции...")
        print()
        
        # Тест 1: Базовая интеграция
        result1 = test_basic_html()
        
        print("\n" + "=" * 60)
        input("Нажмите Enter для продолжения к генерации отчета...")
        
        # Тест 2: Генерация отчета
        result2 = test_seo_report()
        
        print("\n" + "=" * 60)
        print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО!")
        print("=" * 60)
        print("Все модули SEO интеграции работают корректно.")
        print("Вы можете использовать эти функции через API или напрямую в коде.")
        
    except ImportError as e:
        print(f"Ошибка импорта: {e}")
        print("Убедитесь, что все зависимости установлены:")
        print("pip install nltk textstat beautifulsoup4")
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        print("Проверьте правильность установки модулей.")


if __name__ == "__main__":
    main()
