#!/usr/bin/env python3
"""
Тестовый скрипт для проверки генерации структурированных данных
"""

import asyncio
import json
from app.modules.structured_data.generator import StructuredDataGenerator
from app.modules.structured_data.schemas import FAQItem, ProductOffer, BreadcrumbItem


async def test_faq_schema():
    """Тест генерации FAQ схемы"""
    print("=== Тест FAQ Schema ===")
    
    # Тестовые данные
    faq_data = {
        "faq_items": [
            {"question": "Что такое HTML генератор?", "answer": "Это инструмент для создания HTML страниц с помощью ИИ."},
            {"question": "Как использовать ИИ для создания контента?", "answer": "Просто введите описание того, что вы хотите создать."},
            {"question": "Поддерживаются ли SEO оптимизации?", "answer": "Да, генератор автоматически добавляет SEO мета-теги и структурированные данные."}
        ],
        "name": "Часто задаваемые вопросы",
        "description": "Ответы на популярные вопросы о HTML генераторе"
    }
    
    generator = StructuredDataGenerator()
    schema = await generator.generate_structured_data("faq", faq_data)
    
    print("Сгенерированная FAQ схема:")
    print(json.dumps(schema, ensure_ascii=False, indent=2))
    
    # Тест внедрения в HTML
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FAQ страница</title>
    </head>
    <body>
        <h1>Часто задаваемые вопросы</h1>
        <p>Контент страницы</p>
    </body>
    </html>
    """
    
    enhanced_html = generator.inject_into_html(test_html, schema)
    print("\nHTML с внедренной схемой:")
    print(enhanced_html)
    return schema


async def test_product_schema():
    """Тест генерации Product схемы"""
    print("\n=== Тест Product Schema ===")
    
    product_data = {
        "name": "Профессиональный HTML Генератор",
        "description": "Мощный инструмент для создания веб-страниц с помощью искусственного интеллекта",
        "brand": "WebGen Pro",
        "sku": "HTMLGEN-PRO-2024",
        "price": 2999.99,
        "currency": "RUB",
        "availability": "InStock",
        "category": "Программное обеспечение",
        "image": "https://example.com/product-image.jpg",
        "url": "https://example.com/html-generator-pro",
        "reviews": [
            {
                "rating": 5.0,
                "review_body": "Отличный инструмент! Сэкономил много времени.",
                "author": "Иван Петров",
                "date_published": "2024-01-15"
            },
            {
                "rating": 4.5,
                "review_body": "Хороший функционал, но есть место для улучшений.",
                "author": "Мария Сидорова",
                "date_published": "2024-01-10"
            }
        ]
    }
    
    generator = StructuredDataGenerator()
    schema = await generator.generate_structured_data("product", product_data)
    
    print("Сгенерированная Product схема:")
    print(json.dumps(schema, ensure_ascii=False, indent=2))
    return schema


async def test_breadcrumb_schema():
    """Тест генерации Breadcrumb схемы"""
    print("\n=== Тест Breadcrumb Schema ===")
    
    breadcrumb_data = {
        "items": [
            {"name": "Главная", "url": "https://example.com/", "position": 1},
            {"name": "Продукты", "url": "https://example.com/products", "position": 2},
            {"name": "Веб-инструменты", "url": "https://example.com/products/web-tools", "position": 3},
            {"name": "HTML Генератор", "url": "https://example.com/products/web-tools/html-generator", "position": 4}
        ]
    }
    
    generator = StructuredDataGenerator()
    schema = await generator.generate_structured_data("breadcrumb", breadcrumb_data)
    
    print("Сгенерированная Breadcrumb схема:")
    print(json.dumps(schema, ensure_ascii=False, indent=2))
    return schema


async def test_article_schema():
    """Тест генерации Article схемы"""
    print("\n=== Тест Article Schema ===")
    
    article_data = {
        "headline": "Как создать современную веб-страницу с помощью ИИ",
        "author": "Алексей Разработчик",
        "date_published": "2024-01-20T10:00:00Z",
        "date_modified": "2024-01-20T10:00:00Z",
        "description": "Подробное руководство по использованию ИИ для создания качественных веб-страниц",
        "image": "https://example.com/article-image.jpg",
        "url": "https://example.com/articles/ai-web-development",
        "publisher_name": "WebDev Blog",
        "publisher_logo": "https://example.com/logo.png"
    }
    
    generator = StructuredDataGenerator()
    schema = await generator.generate_structured_data("article", article_data)
    
    print("Сгенерированная Article схема:")
    print(json.dumps(schema, ensure_ascii=False, indent=2))
    return schema


async def test_organization_schema():
    """Тест генерации Organization схемы"""
    print("\n=== Тест Organization Schema ===")
    
    organization_data = {
        "name": "WebGen Technologies",
        "url": "https://webgen-tech.com",
        "logo": "https://webgen-tech.com/logo.png",
        "description": "Компания, специализирующаяся на разработке инструментов для веб-разработки с использованием ИИ",
        "address": {
            "street": "ул. Технологическая, 42",
            "city": "Москва",
            "region": "Московская область",
            "postal_code": "101000",
            "country": "Россия"
        },
        "phone": "+7 (495) 123-45-67",
        "email": "info@webgen-tech.com",
        "social_media": [
            "https://twitter.com/webgentech",
            "https://facebook.com/webgentech",
            "https://linkedin.com/company/webgentech"
        ]
    }
    
    generator = StructuredDataGenerator()
    schema = await generator.generate_structured_data("organization", organization_data)
    
    print("Сгенерированная Organization схема:")
    print(json.dumps(schema, ensure_ascii=False, indent=2))
    return schema


async def test_multiple_schemas_injection():
    """Тест внедрения нескольких схем в один HTML"""
    print("\n=== Тест внедрения нескольких схем ===")
    
    # Создаем несколько схем
    faq_schema = await test_faq_schema()
    breadcrumb_schema = await test_breadcrumb_schema()
    
    test_html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Тестовая страница</title>
    </head>
    <body>
        <nav>
            <a href="/">Главная</a> > 
            <a href="/products">Продукты</a> > 
            <span>HTML Генератор</span>
        </nav>
        
        <main>
            <h1>HTML Генератор с ИИ</h1>
            <p>Создавайте профессиональные веб-страницы с помощью искусственного интеллекта.</p>
            
            <section>
                <h2>Часто задаваемые вопросы</h2>
                <div>
                    <h3>Что такое HTML генератор?</h3>
                    <p>Это инструмент для создания HTML страниц с помощью ИИ.</p>
                </div>
            </section>
        </main>
    </body>
    </html>
    """
    
    generator = StructuredDataGenerator()
    
    # Внедряем несколько схем
    schemas = [faq_schema, breadcrumb_schema]
    enhanced_html = generator.inject_multiple_schemas(test_html, schemas)
    
    print("HTML с несколькими внедренными схемами:")
    print(enhanced_html)
    
    # Проверяем количество схем
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(enhanced_html, 'html.parser')
    ld_scripts = soup.find_all('script', {'type': 'application/ld+json'})
    print(f"\nВсего внедрено схем: {len(ld_scripts)}")


async def main():
    """Главная функция тестирования"""
    print("Запуск тестов генерации структурированных данных...")
    
    try:
        await test_faq_schema()
        await test_product_schema()
        await test_breadcrumb_schema()
        await test_article_schema()
        await test_organization_schema()
        await test_multiple_schemas_injection()
        
        print("\n✅ Все тесты успешно пройдены!")
        
    except Exception as e:
        print(f"\n❌ Ошибка при выполнении тестов: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
