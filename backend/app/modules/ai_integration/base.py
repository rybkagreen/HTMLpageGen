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

    async def generate_structured_data(
        self, content: str, schema_type: str, **kwargs
    ) -> Dict[str, Any]:
        """Generate structured data for content"""
        # Default implementation using chat completion
        prompt = self._get_structured_data_prompt(content, schema_type, **kwargs)
        
        try:
            response = await self.chat_completion([
                {"role": "user", "content": prompt}
            ])
            
            # Try to extract JSON from response
            import re
            import json
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            return {}
        except Exception:
            return {}
    
    def _get_structured_data_prompt(self, content: str, schema_type: str, **kwargs) -> str:
        """Generate prompt for structured data extraction"""
        if schema_type == 'faq':
            return f"""
Проанализируй следующий контент и извлеки из него вопросы и ответы для FAQ.
Верни результат в формате JSON:

{{
    "faq_items": [
        {{"question": "Вопрос 1", "answer": "Ответ 1"}},
        {{"question": "Вопрос 2", "answer": "Ответ 2"}}
    ],
    "name": "Название FAQ страницы (если есть)",
    "description": "Описание (если есть)"
}}

Контент:
{content}

Если в контенте нет четких вопросов-ответов, создай 3-5 логичных FAQ на основе представленной информации.
"""
        elif schema_type == 'product':
            return f"""
Проанализируй следующий контент и извлеки информацию о продукте.
Верни результат в формате JSON:

{{
    "name": "Название продукта",
    "description": "Описание продукта",
    "brand": "Бренд (если есть)",
    "sku": "Артикул (если есть)",
    "price": 0.0,
    "currency": "RUB",
    "availability": "InStock",
    "category": "Категория (если есть)",
    "image": "URL изображения (если есть)",
    "url": "URL продукта (если есть)"
}}

Контент:
{content}

Если какая-то информация отсутствует, используй null или разумные значения по умолчанию.
"""
        elif schema_type == 'breadcrumb':
            return f"""
Проанализируй следующий контент и создай логичную навигационную цепочку (хлебные крошки).
Верни результат в формате JSON:

{{
    "items": [
        {{"name": "Главная", "url": "/", "position": 1}},
        {{"name": "Категория", "url": "/category", "position": 2}},
        {{"name": "Текущая страница", "url": "/current", "position": 3}}
    ]
}}

Контент:
{content}

Создай логичную иерархию навигации, начиная с главной страницы.
"""
        else:
            return f"Extract {schema_type} structured data from: {content[:500]}..."

    async def get_provider_info(self) -> Dict[str, Any]:
        """Получить информацию о провайдере"""
        return {
            "provider": self.__class__.__name__,
            "configured": True,
            "ai_provider_setting": "default",
        }
