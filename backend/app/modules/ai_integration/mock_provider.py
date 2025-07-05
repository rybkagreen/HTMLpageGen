from typing import Any, Dict, List

from app.core.config import settings
from app.modules.ai_integration.base import AIProvider


class MockProvider(AIProvider):
    """Mock провайдер для случаев без настроенного AI API"""

    async def enhance_content(
        self, content: str, enhancement_type: str = "general"
    ) -> str:
        """Возвращает оригинальный контент без изменений"""
        return content

    async def generate_meta_tags(self, content: str) -> Dict[str, str]:
        """Возвращает дефолтные мета-теги"""
        return {
            "title": settings.DEFAULT_META_TITLE,
            "description": settings.DEFAULT_META_DESCRIPTION,
            "keywords": "html, generator, web, page",
        }

    async def suggest_improvements(self, html: str) -> List[str]:
        """Возвращает базовые рекомендации"""
        return [
            "Добавьте альтернативный текст для изображений",
            "Убедитесь, что у всех ссылок есть описательный текст",
            "Проверьте контрастность цветов для доступности",
            "Оптимизируйте размеры изображений",
            "Добавьте структурированные данные для SEO",
        ]

    async def generate_html_content(
        self, prompt: str, content_type: str = "webpage"
    ) -> str:
        """Генерирует базовый HTML шаблон"""
        return f"""
        <div class="content-section">
            <h2>Сгенерированный контент</h2>
            <p>Запрос: {prompt}</p>
            <p>Тип контента: {content_type}</p>
            <p><em>Для полной функциональности AI настройте API ключ 
            в конфигурации.</em></p>
        </div>
        """

    async def analyze_intention(self, message: str) -> Dict[str, Any]:
        """Базовый анализ намерений"""
        message_lower = message.lower()

        create_words = ["создай", "генерируй", "сделай", "построй"]
        improve_words = ["улучши", "оптимизируй", "исправь"]
        help_words = ["помощь", "как", "что", "когда"]

        if any(word in message_lower for word in create_words):
            intention = "generate_html"
        elif any(word in message_lower for word in improve_words):
            intention = "improve_content"
        elif any(word in message_lower for word in help_words):
            intention = "get_help"
        else:
            intention = "ask_question"

        return {
            "intention": intention,
            "content_type": "webpage",
            "confidence": 0.5,
            "keywords": message.split()[:5],
        }

    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """Базовая реализация чата"""
        if not messages:
            return "Привет! Я могу помочь с созданием веб-страниц."

        last_message = messages[-1].get("content", "")

        return (
            f"Спасибо за ваше сообщение: '{last_message}'. "
            "Для полной функциональности AI настройте API ключ в конфигурации."
        )

    def get_provider_info(self) -> Dict[str, Any]:
        """Возвращает информацию о провайдере"""
        return {
            "provider": "mock",
            "version": "1.0",
            "description": ("Mock AI provider for development and testing purposes."),
        }
