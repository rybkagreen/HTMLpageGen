from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AIProvider(ABC):
    """Абстрактный базовый класс для AI провайдеров"""

    @abstractmethod
    async def enhance_content(
        self, content: str, enhancement_type: str = "general"
    ) -> str:
        """Улучшить контент с помощью AI"""
        pass

    @abstractmethod
    async def generate_meta_tags(self, content: str) -> Dict[str, str]:
        """Генерировать SEO мета-теги из контента"""
        pass

    @abstractmethod
    async def suggest_improvements(self, html: str) -> List[str]:
        """Предложить улучшения для сгенерированного HTML"""
        pass

    @abstractmethod
    async def generate_html_content(
        self, prompt: str, content_type: str = "webpage"
    ) -> str:
        """Генерировать HTML контент на основе промпта"""
        pass

    @abstractmethod
    async def analyze_intention(self, message: str) -> Dict[str, str]:
        """Analyze user intention from message"""
        pass

    @abstractmethod
    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """Generate chat completion response"""
        pass

    async def get_provider_info(self) -> Dict[str, Any]:
        """Получить информацию о провайдере"""
        return {
            "provider": self.__class__.__name__,
            "configured": True,
            "ai_provider_setting": "default",
        }
