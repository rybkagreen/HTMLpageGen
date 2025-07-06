#!/usr/bin/env python3
"""
Демонстрация real-time SEO AI интеграции (упрощенная версия)

Показывает как работает интеграция между SEO анализатором и AI генератором
без зависимости от NLTK.
"""

import asyncio
import json
from datetime import datetime
from bs4 import BeautifulSoup


class SimpleSEOAnalyzer:
    """Упрощенный SEO анализатор без NLTK"""
    
    def analyze_html(self, html):
        soup = BeautifulSoup(html, "html.parser")
        
        issues = []
        score = 100
        
        # Проверка title
        title = soup.find("title")
        if not title:
            issues.append("Отсутствует title тег")
            score -= 20
        elif len(title.get_text().strip()) < 30:
            issues.append("Title слишком короткий")
            score -= 10
        
        # Проверка meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if not meta_desc:
            issues.append("Отсутствует meta description")
            score -= 20
        
        # Проверка H1
        h1_tags = soup.find_all("h1")
        if not h1_tags:
            issues.append("Отсутствует H1 заголовок")
            score -= 15
        elif len(h1_tags) > 1:
            issues.append("Множественные H1 заголовки")
            score -= 10
        
        # Проверка изображений
        images = soup.find_all("img")
        missing_alt = len([img for img in images if not img.get("alt")])
        if missing_alt > 0:
            issues.append(f"{missing_alt} изображений без alt атрибута")
            score -= missing_alt * 5
        
        # Проверка viewport
        if not soup.find("meta", attrs={"name": "viewport"}):
            issues.append("Отсутствует viewport meta тег")
            score -= 10
        
        # Проверка lang атрибута
        html_tag = soup.find("html")
        if not html_tag or not html_tag.get("lang"):
            issues.append("Отсутствует lang атрибут")
            score -= 5
        
        return {
            "score": max(0, score),
            "issues": issues,
            "recommendations": [f"Исправить: {issue}" for issue in issues],
            "title": {
                "exists": bool(title),
                "text": title.get_text().strip() if title else "",
                "length": len(title.get_text().strip()) if title else 0
            },
            "meta_description": {
                "exists": bool(meta_desc),
                "text": meta_desc.get("content", "").strip() if meta_desc else "",
                "length": len(meta_desc.get("content", "").strip()) if meta_desc else 0
            },
            "images": {
                "total": len(images),
                "missing_alt": missing_alt
            }
        }


class SimpleAIService:
    """Упрощенный AI сервис для демонстрации"""
    
    async def suggest_improvements(self, html):
        # Имитируем AI предложения
        await asyncio.sleep(0.5)  # Имитация обработки
        
        suggestions = [
            "Добавить более описательный title",
            "Улучшить meta description",
            "Добавить alt атрибуты к изображениям",
            "Оптимизировать структуру заголовков"
        ]
        
        return suggestions
    
    async def enhance_content(self, content, enhancement_type="seo_optimization"):
        # Имитируем улучшение HTML
        await asyncio.sleep(1.0)  # Имитация AI обработки
        
        soup = BeautifulSoup(content, "html.parser")
        
        # Добавляем недостающие элементы
        if not soup.find("title"):
            head = soup.find("head")
            if head:
                title_tag = soup.new_tag("title")
                title_tag.string = "Улучшенный заголовок страницы - AI Generated"
                head.insert(0, title_tag)
        
        if not soup.find("meta", attrs={"name": "description"}):
            head = soup.find("head") 
            if head:
                meta_tag = soup.new_tag("meta", attrs={
                    "name": "description",
                    "content": "Улучшенное описание страницы, созданное с помощью AI для лучшего SEO."
                })
                head.append(meta_tag)
        
        # Добавляем H1 если отсутствует
        if not soup.find("h1"):
            body = soup.find("body")
            if body:
                h1_tag = soup.new_tag("h1")
                h1_tag.string = "Основной заголовок страницы"
                body.insert(0, h1_tag)
        
        # Добавляем alt к изображениям
        images = soup.find_all("img")
        for img in images:
            if not img.get("alt"):
                img["alt"] = "Изображение с AI-сгенерированным описанием"
        
        return str(soup)


class SimpleRealtimeIntegrator:
    """Упрощенный real-time интегратор"""
    
    def __init__(self):
        self.seo_analyzer = SimpleSEOAnalyzer()
        self.ai_service = SimpleAIService()
        self.stats = {
            "optimizations_performed": 0,
            "ai_suggestions_generated": 0,
            "total_improvements": 0
        }
    
    async def start_realtime_optimization(self, html, context=None, target_keywords=None, progress_callback=None):
        """Запуск real-time оптимизации"""
        start_time = datetime.now()
        
        if progress_callback:
            await progress_callback({"message": "Начальный анализ...", "progress": 10})
        
        # Первичный анализ
        initial_analysis = self.seo_analyzer.analyze_html(html)
        print(f"📊 Первичный SEO балл: {initial_analysis['score']}")
        print(f"🔍 Найдено проблем: {len(initial_analysis['issues'])}")
        
        if progress_callback:
            await progress_callback({"message": "Применение автоматических исправлений...", "progress": 40})
        
        # Автоматические исправления
        optimized_html = await self._apply_auto_fixes(html, initial_analysis)
        
        if progress_callback:
            await progress_callback({"message": "Получение AI предложений...", "progress": 70})
        
        # AI улучшения
        if initial_analysis['score'] < 70:
            ai_suggestions = await self.ai_service.suggest_improvements(optimized_html)
            self.stats["ai_suggestions_generated"] += 1
            print(f"🤖 AI предложения: {ai_suggestions}")
            
            # Применяем AI улучшения
            optimized_html = await self.ai_service.enhance_content(optimized_html)
        
        if progress_callback:
            await progress_callback({"message": "Финальный анализ...", "progress": 90})
        
        # Финальный анализ
        final_analysis = self.seo_analyzer.analyze_html(optimized_html)
        
        if progress_callback:
            await progress_callback({"message": "Завершено!", "progress": 100})
        
        # Обновляем статистику
        self.stats["optimizations_performed"] += 1
        improvement = final_analysis['score'] - initial_analysis['score']
        if improvement > 0:
            self.stats["total_improvements"] += improvement
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "initial_analysis": initial_analysis,
            "final_analysis": final_analysis,
            "optimized_html": optimized_html,
            "improvement": improvement,
            "processing_time": processing_time,
            "stats": self.stats.copy()
        }
    
    async def _apply_auto_fixes(self, html, analysis):
        """Применение автоматических исправлений"""
        soup = BeautifulSoup(html, "html.parser")
        
        # Добавляем viewport если отсутствует
        if "viewport" in str(analysis['issues']):
            head = soup.find("head")
            if head and not soup.find("meta", attrs={"name": "viewport"}):
                viewport_tag = soup.new_tag("meta", attrs={
                    "name": "viewport",
                    "content": "width=device-width, initial-scale=1.0"
                })
                head.append(viewport_tag)
                print("✅ Добавлен viewport meta тег")
        
        # Добавляем lang атрибут
        if "lang атрибут" in str(analysis['issues']):
            html_tag = soup.find("html")
            if html_tag and not html_tag.get("lang"):
                html_tag["lang"] = "ru"
                print("✅ Добавлен lang атрибут")
        
        # Добавляем charset если отсутствует
        if not soup.find("meta", attrs={"charset": True}):
            head = soup.find("head")
            if head:
                charset_tag = soup.new_tag("meta", attrs={"charset": "UTF-8"})
                head.insert(0, charset_tag)
                print("✅ Добавлен charset")
        
        # Добавляем loading="lazy" к изображениям
        images = soup.find_all("img")
        for img in images:
            if not img.get("loading"):
                img["loading"] = "lazy"
        
        if images:
            print(f"✅ Оптимизированы изображения ({len(images)} шт.)")
        
        return str(soup)


async def demo_optimization():
    """Демонстрация оптимизации"""
    print("🚀 ДЕМОНСТРАЦИЯ REAL-TIME SEO AI ИНТЕГРАЦИИ")
    print("=" * 60)
    
    # Тестовый HTML с проблемами
    bad_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test</title>
    </head>
    <body>
        <h2>Some content</h2>
        <p>Very short content.</p>
        <img src="test.jpg">
    </body>
    </html>
    """
    
    integrator = SimpleRealtimeIntegrator()
    
    # Callback для прогресса
    async def progress_callback(data):
        print(f"📈 {data['progress']}% - {data['message']}")
    
    # Запускаем оптимизацию
    result = await integrator.start_realtime_optimization(
        html=bad_html,
        context={"title": "Тестовая страница"},
        target_keywords=["тест", "демонстрация"],
        progress_callback=progress_callback
    )
    
    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ ОПТИМИЗАЦИИ")
    print("=" * 60)
    
    print(f"⏱️  Время обработки: {result['processing_time']:.2f} сек")
    print(f"📊 SEO балл: {result['initial_analysis']['score']} → {result['final_analysis']['score']} (+{result['improvement']})")
    print(f"🔧 Исправлено проблем: {len(result['initial_analysis']['issues']) - len(result['final_analysis']['issues'])}")
    
    print(f"\n📝 ОПТИМИЗИРОВАННЫЙ HTML:")
    print("-" * 40)
    print(result['optimized_html'])
    
    print(f"\n📈 СТАТИСТИКА:")
    stats = result['stats']
    print(f"   Всего оптимизаций: {stats['optimizations_performed']}")
    print(f"   AI предложений: {stats['ai_suggestions_generated']}")
    print(f"   Общие улучшения: {stats['total_improvements']}")


async def demo_websocket_simulation():
    """Демонстрация WebSocket-подобного взаимодействия"""
    print("\n\n🌐 ДЕМОНСТРАЦИЯ WEBSOCKET ИНТЕГРАЦИИ")
    print("=" * 60)
    
    class MockWebSocket:
        def __init__(self):
            self.messages = []
        
        async def send_message(self, data):
            self.messages.append(data)
            print(f"📡 WebSocket отправляет: {data['type']} - {data.get('message', '')}")
    
    mock_ws = MockWebSocket()
    integrator = SimpleRealtimeIntegrator()
    
    # Имитируем обработку WebSocket сообщения
    client_message = {
        "type": "start_optimization",
        "html": "<html><head><title>WS Test</title></head><body><p>Content</p></body></html>",
        "context": {"title": "WebSocket Test"}
    }
    
    print(f"📨 Клиент отправляет: {client_message['type']}")
    
    # Обработка сообщения
    async def ws_progress_callback(data):
        await mock_ws.send_message({
            "type": "optimization_progress",
            "message": data['message'],
            "progress": data['progress']
        })
    
    result = await integrator.start_realtime_optimization(
        html=client_message['html'],
        context=client_message['context'],
        progress_callback=ws_progress_callback
    )
    
    # Отправляем финальный результат
    await mock_ws.send_message({
        "type": "optimization_completed",
        "result": {
            "seo_score": result['final_analysis']['score'],
            "improvement": result['improvement'],
            "processing_time": result['processing_time']
        }
    })
    
    print(f"\n📊 WebSocket сессия завершена. Отправлено сообщений: {len(mock_ws.messages)}")


async def main():
    """Главная демонстрация"""
    await demo_optimization()
    await demo_websocket_simulation()
    
    print("\n" + "=" * 60)
    print("✅ ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 60)
    print("\n💡 Эта демонстрация показывает как работает real-time интеграция")
    print("   между SEO анализатором и AI генератором.")
    print("\n🔗 Основные возможности:")
    print("   - Автоматический анализ HTML")
    print("   - Применение исправлений в реальном времени")
    print("   - AI предложения для улучшения")
    print("   - WebSocket интеграция для UI")
    print("   - Статистика и мониторинг")


if __name__ == "__main__":
    asyncio.run(main())
