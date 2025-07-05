import asyncio
import logging
import random
from datetime import datetime
from typing import Any, Dict, List

# Проверяем доступность transformers
try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    transformers_available = True
except (ImportError, OSError):
    transformers_available = False

from app.modules.ai_integration.base import AIProvider

logger = logging.getLogger(__name__)


class LocalAIProvider(AIProvider):
    """Локальный AI Provider - простая версия без сложных моделей"""

    def __init__(self):
        self.model_name = "local-fallback"
        self.available = True  # Всегда доступен в fallback режиме
        logger.info("Локальный AI провайдер инициализирован (fallback режим)")

    async def enhance_content(
        self, content: str, enhancement_type: str = "general"
    ) -> str:
        """Улучшить контент"""
        improvements = {
            "general": f"Улучшенная версия: {content} (добавлена структура и читабельность)",
            "seo": f"SEO-оптимизированный контент: {content} (добавлены ключевые слова и мета-теги)",
            "accessibility": f"Доступный контент: {content} (улучшена семантика и навигация)",
            "marketing": f"Маркетинговая версия: {content} (добавлен призыв к действию)",
        }

        result = improvements.get(enhancement_type, improvements["general"])
        await asyncio.sleep(0.1)  # Имитация обработки
        return result

    async def generate_meta_tags(self, content: str) -> Dict[str, str]:
        """Генерировать SEO мета-теги"""
        # Простой анализ контента для извлечения ключевых слов
        words = content.lower().split()
        common_words = {"и", "в", "на", "с", "по", "для", "как", "что", "это", "или"}
        keywords = [
            word for word in words[:10] if len(word) > 3 and word not in common_words
        ]

        # Генерируем мета-теги на основе контента
        title = content[:50] + "..." if len(content) > 50 else content
        description = content[:150] + "..." if len(content) > 150 else content

        return {
            "title": title,
            "description": description,
            "keywords": ", ".join(keywords[:5]),
        }

    async def suggest_improvements(self, html: str) -> List[str]:
        """Предложить улучшения для HTML кода"""
        suggestions: List[str] = []

        # Базовые проверки HTML
        if "<!DOCTYPE" not in html:
            suggestions.append("Добавьте DOCTYPE для стандартного HTML5")

        if "lang=" not in html:
            suggestions.append("Укажите язык страницы в теге <html>")

        if "<meta charset=" not in html:
            suggestions.append("Добавьте кодировку UTF-8 в мета-теги")

        if "<title>" not in html:
            suggestions.append("Добавьте заголовок страницы в теге <title>")

        if "viewport" not in html:
            suggestions.append("Добавьте мета-тег viewport для адаптивности")

        # Если нет предложений, добавляем общие
        if not suggestions:
            suggestions = [
                "Добавьте семантические HTML5 теги (header, nav, main, footer)",
                "Оптимизируйте изображения с атрибутами alt",
                "Используйте заголовки H1-H6 для структуры контента",
                "Добавьте мета-описание для поисковых систем",
            ]

        return suggestions[:5]

    async def generate_html_content(
        self, prompt: str, content_type: str = "webpage"
    ) -> str:
        """Генерировать HTML контент"""
        await asyncio.sleep(0.2)  # Имитация генерации
        return self._create_template(prompt, content_type)

    def _create_template(self, prompt: str, content_type: str) -> str:
        """Создание HTML шаблона"""
        title = prompt[:50] if prompt else "Сгенерированная страница"

        # Определяем стили по типу контента
        if content_type == "landing":
            bg_color = "#007bff"
            theme = "лендинг"
        elif content_type == "blog":
            bg_color = "#28a745"
            theme = "блог"
        elif content_type == "portfolio":
            bg_color = "#6f42c1"
            theme = "портфолио"
        else:
            bg_color = "#17a2b8"
            theme = "веб-страница"

        html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            background: {bg_color};
            color: white;
            padding: 2rem;
            text-align: center;
            border-radius: 8px 8px 0 0;
        }}
        .content {{
            padding: 2rem;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 1rem;
            text-align: center;
            border-radius: 0 0 8px 8px;
            color: #666;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>{prompt}</h1>
            <p>Тип: {theme}</p>
        </header>
        <main class="content">
            <h2>Добро пожаловать!</h2>
            <p>Это автоматически сгенерированная страница по вашему запросу: <strong>"{prompt}"</strong></p>
            <p>Тип контента: <em>{content_type}</em></p>
            <p>Здесь может быть размещен ваш основной контент, изображения, формы или другие элементы.</p>
        </main>
        <footer class="footer">
            Создано с помощью локального AI генератора • {datetime.now().strftime("%d.%m.%Y")}
        </footer>
    </div>
</body>
</html>"""

        return html

    async def analyze_intention(self, message: str) -> Dict[str, Any]:
        """Анализ намерений пользователя"""
        message_lower = message.lower()

        # Определяем намерение
        if any(word in message_lower for word in ["создай", "сделай", "генерируй"]):
            intention = "create_page"
        elif any(
            word in message_lower for word in ["улучши", "исправь", "оптимизируй"]
        ):
            intention = "modify_page"
        elif any(word in message_lower for word in ["помощь", "как", "что"]):
            intention = "get_help"
        else:
            intention = "ask_question"

        # Определяем тип контента
        if any(word in message_lower for word in ["лендинг", "landing"]):
            content_type = "landing"
        elif any(word in message_lower for word in ["блог", "blog"]):
            content_type = "blog"
        elif any(word in message_lower for word in ["портфолио", "portfolio"]):
            content_type = "portfolio"
        else:
            content_type = "webpage"

        return {
            "intention": intention,
            "content_type": content_type,
            "confidence": 0.7,
            "keywords": message.split()[:5],
        }

    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """Генерация ответа для чата"""
        if not messages:
            return "Привет! Я могу помочь создать веб-страницы. Что хотите создать?"

        last_message = messages[-1].get("content", "").lower()

        # Контекстные ответы
        responses = {
            "создай": "Отлично! Опишите, какую страницу нужно создать - лендинг, блог или обычную веб-страницу?",
            "помощь": "Я могу создавать HTML страницы, анализировать код и давать рекомендации по улучшению.",
            "html": "Создам HTML код по вашему описанию. Укажите тематику и тип страницы.",
            "css": "Помогу со стилями CSS. Опишите желаемый дизайн.",
            "seo": "Проанализирую контент для SEO и предложу оптимизации.",
        }

        # Ищем подходящий ответ
        for keyword, response in responses.items():
            if keyword in last_message:
                return response

        # Общие ответы
        general_responses = [
            "Интересный вопрос! Как я могу помочь с веб-разработкой?",
            "Готов помочь с созданием веб-страниц. Что именно нужно сделать?",
            "Давайте разберем вашу задачу. Опишите подробнее, что хотите создать.",
        ]

        return random.choice(general_responses)

    def get_provider_info(self) -> Dict[str, Any]:
        """Получить информацию о провайдере"""
        return {
            "provider": "local-ai",
            "model": self.model_name,
            "configured": self.available,
            "transformers_available": transformers_available,
            "ai_provider_setting": "Локальная AI модель (fallback режим)",
        }
