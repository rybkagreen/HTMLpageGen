from typing import Any, Dict, List

from app.core.config import settings
from app.modules.ai_integration.base import AIProvider
from app.modules.ai_integration.deepseek_provider import DeepSeekProvider
from app.modules.ai_integration.huggingface_provider import HuggingFaceProvider
from app.modules.ai_integration.openai_provider import OpenAIProvider

try:
    from app.modules.ai_integration.deepseek_r1_provider import DeepSeekR1Provider

    deepseek_r1_available = True
except ImportError:
    deepseek_r1_available = False

try:
    from app.modules.ai_integration.local_ai_provider import LocalAIProvider

    local_ai_available = True
except ImportError:
    local_ai_available = False


class AIService:
    def __init__(self) -> None:
        self.provider = self._get_provider()

    def _get_provider(self) -> AIProvider:
        """Получить провайдера AI на основе конфигурации"""
        if settings.AI_PROVIDER == "local-ai" and local_ai_available:
            return LocalAIProvider()
        elif settings.AI_PROVIDER == "deepseek-r1" and deepseek_r1_available:
            return DeepSeekR1Provider()
        elif settings.AI_PROVIDER == "huggingface" and settings.HUGGINGFACE_API_KEY:
            return HuggingFaceProvider()
        elif settings.AI_PROVIDER == "deepseek" and settings.DEEPSEEK_API_KEY:
            return DeepSeekProvider()
        elif settings.AI_PROVIDER == "openai" and settings.OPENAI_API_KEY:
            return OpenAIProvider()
        elif local_ai_available:
            # Fallback к локальной модели если доступна
            return LocalAIProvider()
        elif deepseek_r1_available:
            # Попробуем DeepSeek R1 как вариант
            return DeepSeekR1Provider()
        elif settings.HUGGINGFACE_API_KEY:
            # Fallback к HuggingFace если доступен
            return HuggingFaceProvider()
        elif settings.DEEPSEEK_API_KEY:
            # Fallback к DeepSeek если доступен
            return DeepSeekProvider()
        elif settings.OPENAI_API_KEY:
            # Fallback к OpenAI если доступен
            return OpenAIProvider()
        else:
            # Возвращаем mock провайдер, если ни один не настроен
            return self._get_mock_provider()

    def _get_mock_provider(self) -> AIProvider:
        """Возвращает mock провайдер для случаев без API ключей"""
        from app.modules.ai_integration.mock_provider import MockProvider

        return MockProvider()

    async def enhance_content(
        self, content: str, enhancement_type: str = "general"
    ) -> str:
        """
        Enhance content using AI
        """
        return await self.provider.enhance_content(content, enhancement_type)

    async def generate_meta_tags(self, content: str) -> Dict[str, str]:
        """
        Generate SEO meta tags from content
        """
        return await self.provider.generate_meta_tags(content)

    async def suggest_improvements(self, html: str) -> List[str]:
        """
        Suggest improvements for generated HTML
        """
        return await self.provider.suggest_improvements(html)

    async def generate_html_content(
        self, prompt: str, content_type: str = "webpage"
    ) -> str:
        """
        Generate HTML content based on prompt
        """
        return await self.provider.generate_html_content(prompt, content_type)

    async def analyze_intention(self, message: str) -> Dict[str, Any]:
        """
        Analyze user intention from message
        """
        return await self.provider.analyze_intention(message)

    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate chat completion response
        """
        return await self.provider.chat_completion(messages)

    async def generate_structured_data(
        self, content: str, schema_type: str, **kwargs
    ) -> Dict[str, Any]:
        """
        Generate structured data for content
        """
        return await self.provider.generate_structured_data(content, schema_type, **kwargs)

    def get_provider_info(self) -> Dict[str, Any]:
        """Получить информацию о текущем провайдере"""
        provider_name = type(self.provider).__name__
        return {
            "provider": provider_name,
            "configured": provider_name != "MockProvider",
            "ai_provider_setting": settings.AI_PROVIDER,
        }
