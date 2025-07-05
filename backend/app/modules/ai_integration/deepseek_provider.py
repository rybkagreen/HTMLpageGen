import json
from typing import Any, Dict, List

import httpx

from app.core.config import settings
from app.modules.ai_integration.base import AIProvider


class DeepSeekProvider(AIProvider):
    """Провайдер для DeepSeek API"""

    def __init__(self) -> None:
        self.api_key = settings.DEEPSEEK_API_KEY
        self.base_url = settings.DEEPSEEK_BASE_URL
        self.model = settings.DEEPSEEK_MODEL

    async def _make_request(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        """Выполнить запрос к DeepSeek API"""
        if not self.api_key:
            raise Exception("DeepSeek API key не настроен")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30.0,
            )

            if response.status_code != 200:
                raise Exception(
                    f"DeepSeek API error: {response.status_code} - {response.text}"
                )

            result = response.json()
            return result["choices"][0]["message"]["content"]

    async def enhance_content(
        self, content: str, enhancement_type: str = "general"
    ) -> str:
        """Улучшить контент с помощью DeepSeek"""
        prompts = {
            "general": f"Улучши и дополни следующий контент для веб-презентации. Сделай его более привлекательным и информативным:\n\n{content}",
            "seo": f"Оптимизируй следующий контент для SEO, сохраняя читабельность. Добавь ключевые слова и улучши структуру:\n\n{content}",
            "accessibility": f"Улучши следующий контент для доступности и читабельности. Сделай его понятным для всех пользователей:\n\n{content}",
            "marketing": f"Перепиши следующий контент с маркетинговым фокусом. Сделай его более убедительным и продающим:\n\n{content}",
        }

        try:
            messages = [
                {
                    "role": "system",
                    "content": "Ты помощник по улучшению контента. Отвечай на русском языке, если контент на русском, иначе на том же языке, что и исходный контент.",
                },
                {
                    "role": "user",
                    "content": prompts.get(enhancement_type, prompts["general"]),
                },
            ]

            return await self._make_request(messages, max_tokens=1500, temperature=0.7)
        except Exception as e:
            print(f"DeepSeek content enhancement failed: {e}")
            return content

    async def generate_meta_tags(self, content: str) -> Dict[str, str]:
        """Генерировать SEO мета-теги из контента"""
        prompt = f"""
        На основе следующего контента создай SEO-оптимизированные мета-теги:
        
        Контент:
        {content}
        
        Предоставь:
        1. Привлекательный заголовок (максимум 60 символов)
        2. Мета-описание (максимум 160 символов) 
        3. Релевантные ключевые слова (через запятую)
        
        Ответь строго в формате JSON с ключами: title, description, keywords
        """

        try:
            messages = [
                {
                    "role": "system",
                    "content": "Ты SEO-специалист. Всегда отвечай валидным JSON.",
                },
                {"role": "user", "content": prompt},
            ]

            response = await self._make_request(
                messages, max_tokens=300, temperature=0.5
            )
            result = json.loads(response)
            return result
        except Exception as e:
            print(f"DeepSeek meta tag generation failed: {e}")
            return {
                "title": settings.DEFAULT_META_TITLE,
                "description": settings.DEFAULT_META_DESCRIPTION,
                "keywords": "",
            }

    async def suggest_improvements(self, html: str) -> List[str]:
        """Предложить улучшения для сгенерированного HTML"""
        prompt = f"""
        Проанализируй следующий HTML и предложи улучшения для:
        1. SEO оптимизации
        2. Доступности (accessibility)
        3. Производительности
        4. Пользовательского опыта
        
        HTML:
        {html}
        
        Предоставь предложения в виде маркированного списка.
        """

        try:
            messages = [
                {
                    "role": "system",
                    "content": "Ты эксперт по веб-разработке, предоставляющий рекомендации по улучшению.",
                },
                {"role": "user", "content": prompt},
            ]

            response = await self._make_request(
                messages, max_tokens=800, temperature=0.6
            )
            suggestions = response.strip().split("\n")
            return [s.strip("- ").strip() for s in suggestions if s.strip()]
        except Exception as e:
            print(f"DeepSeek suggestion generation failed: {e}")
            return []

    async def generate_html_content(
        self, prompt: str, content_type: str = "webpage"
    ) -> str:
        """Генерировать HTML контент на основе промпта"""
        system_prompts = {
            "webpage": "Ты эксперт по созданию веб-страниц. Создавай качественный, семантический HTML с хорошей структурой.",
            "landing": "Ты специалист по созданию landing страниц. Создавай убедительные и конверсионные страницы.",
            "blog": "Ты эксперт по созданию блогов. Создавай читабельные и SEO-оптимизированные статьи.",
            "portfolio": "Ты специалист по созданию портфолио. Создавай профессиональные и впечатляющие страницы.",
        }

        try:
            messages = [
                {
                    "role": "system",
                    "content": system_prompts.get(
                        content_type, system_prompts["webpage"]
                    ),
                },
                {
                    "role": "user",
                    "content": f"Создай HTML контент на основе следующего описания: {prompt}",
                },
            ]

            return await self._make_request(messages, max_tokens=2000, temperature=0.7)
        except Exception as e:
            print(f"DeepSeek HTML generation failed: {e}")
            return f"<p>Ошибка генерации контента: {e}</p>"

    async def analyze_intention(self, message: str) -> Dict[str, str]:
        """Analyze user intention from message"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": """Проанализируй намерение пользователя и верни JSON:
{
  "type": "code_generation|code_improvement|question|consultation",
  "confidence": "0.0-1.0",
  "details": "краткое описание намерения"
}

Типы намерений:
- code_generation: пользователь хочет создать новый код
- code_improvement: пользователь хочет улучшить существующий код  
- question: общий вопрос о веб-разработке
- consultation: нужна консультация/совет""",
                },
                {"role": "user", "content": message},
            ]

            response = await self._make_request(
                messages, max_tokens=200, temperature=0.3
            )

            try:
                import json

                return json.loads(response)
            except json.JSONDecodeError:
                # Fallback если AI не ответил в JSON
                if any(
                    word in message.lower()
                    for word in ["создай", "сделай", "сгенерируй", "построй"]
                ):
                    return {
                        "type": "code_generation",
                        "confidence": "0.8",
                        "details": "Запрос на создание кода",
                    }
                elif any(
                    word in message.lower()
                    for word in ["улучши", "оптимизируй", "исправь"]
                ):
                    return {
                        "type": "code_improvement",
                        "confidence": "0.7",
                        "details": "Запрос на улучшение",
                    }
                else:
                    return {
                        "type": "question",
                        "confidence": "0.6",
                        "details": "Общий вопрос",
                    }

        except Exception as e:
            print(f"DeepSeek intention analysis failed: {e}")
            return {
                "type": "question",
                "confidence": "0.5",
                "details": "Анализ не удался",
            }

    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """Generate chat completion response"""
        try:
            return await self._make_request(messages, max_tokens=1500, temperature=0.7)
        except Exception as e:
            print(f"DeepSeek chat completion failed: {e}")
            return f"Извините, произошла ошибка при генерации ответа: {e}"
