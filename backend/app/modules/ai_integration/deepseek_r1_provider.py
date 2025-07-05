import asyncio
import json
import os
from typing import Any, Dict, List

try:
    from huggingface_hub import InferenceClient

    HF_HUB_AVAILABLE = True
except ImportError:
    HF_HUB_AVAILABLE = False

try:
    from transformers import pipeline

    TRANSFORMERS_AVAILABLE = True
except (ImportError, OSError):
    TRANSFORMERS_AVAILABLE = False

from app.core.config import settings
from app.modules.ai_integration.base import AIProvider


class DeepSeekR1Provider(AIProvider):
    """DeepSeek R1 Provider using Hugging Face Hub InferenceClient"""

    def __init__(self):
        self.model_name = "deepseek-ai/DeepSeek-V3"
        self.client = None
        self.pipe = None
        self.available = False

        # Попробуем InferenceClient сначала
        if HF_HUB_AVAILABLE and settings.HUGGINGFACE_API_KEY:
            try:
                self.client = InferenceClient(api_key=settings.HUGGINGFACE_API_KEY)
                self.available = True
                print("DeepSeek R1 initialized with InferenceClient")
            except Exception as e:
                print(f"Failed to initialize InferenceClient: {e}")

        # Fallback к transformers pipeline
        if not self.available and TRANSFORMERS_AVAILABLE:
            try:
                self.pipe = pipeline(
                    "text-generation",
                    model="deepseek-ai/DeepSeek-R1",
                    trust_remote_code=True,
                    device_map="auto",
                    torch_dtype="auto",
                )
                self.available = True
                print("DeepSeek R1 initialized with transformers pipeline")
            except Exception as e:
                print(f"Failed to load DeepSeek-R1 with transformers: {e}")

        if not self.available:
            print("DeepSeek R1 not available, using fallback responses")

    async def _generate_response(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        """Генерация ответа через InferenceClient или transformers pipeline"""

        if not self.available:
            return self._fallback_response(messages[-1]["content"] if messages else "")

        try:
            # Используем InferenceClient если доступен
            if self.client:
                return await self._generate_with_client(
                    messages, max_tokens, temperature
                )

            # Fallback к transformers pipeline
            elif self.pipe:
                return await self._generate_with_pipeline(
                    messages, max_tokens, temperature
                )

            return self._fallback_response(messages[-1]["content"] if messages else "")

        except Exception as e:
            print(f"DeepSeek-R1 generation error: {e}")
            return self._fallback_response(messages[-1]["content"] if messages else "")

    async def _generate_with_client(
        self, messages: List[Dict[str, str]], max_tokens: int, temperature: float
    ) -> str:
        """Генерация с использованием InferenceClient"""

        try:
            # Выполняем в отдельном потоке
            loop = asyncio.get_event_loop()

            def call_client():
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                return response.choices[0].message.content

            result = await loop.run_in_executor(None, call_client)
            return result.strip() if result else ""

        except Exception as e:
            print(f"InferenceClient error: {e}")
            # Fallback к pipeline если есть
            if self.pipe:
                return await self._generate_with_pipeline(
                    messages, max_tokens, temperature
                )
            raise

    async def _generate_with_pipeline(
        self, messages: List[Dict[str, str]], max_tokens: int, temperature: float
    ) -> str:
        """Генерация с использованием transformers pipeline"""

        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.pipe(
                    messages,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    do_sample=True,
                    top_p=0.9,
                    repetition_penalty=1.1,
                    return_full_text=False,
                ),
            )

            if result and len(result) > 0:
                generated_text = result[0].get("generated_text", "")
                if isinstance(generated_text, str):
                    return generated_text.strip()

            return ""

        except Exception as e:
            print(f"Pipeline generation error: {e}")
            raise

    def _fallback_response(self, user_input: str) -> str:
        """Fallback ответ когда модель недоступна"""
        return (
            f"Извините, модель DeepSeek-R1 временно недоступна. "
            f"Ваш запрос '{user_input[:50]}...' был получен. "
            f"Пожалуйста, попробуйте позже или настройте другой AI провайдер."
        )

    async def enhance_content(
        self, content: str, enhancement_type: str = "general"
    ) -> str:
        """Улучшить контент с помощью DeepSeek R1"""

        enhancement_prompts = {
            "general": "Улучши следующий текст для веб-страницы:",
            "seo": "Оптимизируй следующий текст для SEO:",
            "accessibility": "Улучши доступность следующего текста:",
            "marketing": "Перепиши в маркетинговом стиле:",
        }

        prompt_text = enhancement_prompts.get(
            enhancement_type, enhancement_prompts["general"]
        )

        messages = [{"role": "user", "content": f"{prompt_text}\n\n{content}"}]

        return await self._generate_response(messages)

    async def generate_meta_tags(self, content: str) -> Dict[str, str]:
        """Генерировать SEO мета-теги"""

        messages = [
            {
                "role": "user",
                "content": f"""Создай SEO мета-теги для следующего контента.
Верни результат в формате JSON с полями title, description, keywords.

Контент: {content[:500]}

JSON:""",
            }
        ]

        response = await self._generate_response(messages, max_tokens=200)

        try:
            # Попытка извлечь JSON
            json_start = response.find("{")
            json_end = response.rfind("}") + 1

            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                meta_tags = json.loads(json_str)

                return {
                    "title": meta_tags.get("title", "")[:60],
                    "description": meta_tags.get("description", "")[:160],
                    "keywords": meta_tags.get("keywords", ""),
                }
        except (json.JSONDecodeError, ValueError):
            pass

        # Fallback
        return {
            "title": "AI Generated Page",
            "description": "Intelligent content created with DeepSeek-R1",
            "keywords": "ai, deepseek, html, web development",
        }

    async def suggest_improvements(self, html: str) -> List[str]:
        """Предложить улучшения для HTML кода"""

        messages = [
            {
                "role": "user",
                "content": f"""Проанализируй HTML код и предложи улучшения:

{html[:1000]}

Список рекомендаций:""",
            }
        ]

        response = await self._generate_response(messages, max_tokens=600)

        # Парсим рекомендации
        suggestions = []
        lines = response.split("\n")

        for line in lines:
            line = line.strip()
            if line and (
                line.startswith("-")
                or line.startswith("•")
                or line.startswith(("1.", "2.", "3.", "4.", "5."))
            ):
                suggestion = line.lstrip("- •123456789.").strip()
                if suggestion and len(suggestion) > 10:
                    suggestions.append(suggestion)

        if not suggestions:
            suggestions = [
                "Добавьте семантические HTML теги",
                "Оптимизируйте для доступности",
                "Улучшите SEO структуру",
                "Добавьте мета-теги",
            ]

        return suggestions[:8]

    async def generate_html_content(
        self, prompt: str, content_type: str = "webpage"
    ) -> str:
        """Генерировать HTML контент"""

        type_descriptions = {
            "webpage": "современную веб-страницу",
            "landing": "продающую landing-страницу",
            "blog": "страницу блога",
            "portfolio": "портфолио страницу",
        }

        page_description = type_descriptions.get(content_type, "веб-страницу")

        messages = [
            {
                "role": "user",
                "content": f"""Создай {page_description} по описанию:

{prompt}

Используй современный HTML5, CSS3 и JavaScript.
Сделай дизайн адаптивным и красивым.

HTML код:""",
            }
        ]

        response = await self._generate_response(messages, max_tokens=2000)

        # Попытка извлечь HTML
        html_start = response.find("<!DOCTYPE")
        if html_start == -1:
            html_start = response.find("<html")

        if html_start != -1:
            return response[html_start:]

        # Если HTML не найден, создаем базовый шаблон
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{prompt[:50]}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        h1 {{ color: #333; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Сгенерированная страница</h1>
        <p>Запрос: {prompt}</p>
        <p>Тип: {content_type}</p>
        <!-- Сгенерированный контент будет здесь -->
    </div>
</body>
</html>"""

    async def analyze_intention(self, message: str) -> Dict[str, Any]:
        """Анализ намерений пользователя"""

        messages = [
            {
                "role": "user",
                "content": f"""Проанализируй запрос пользователя и определи:
- intention: create_page, modify_page, ask_question, get_help
- content_type: webpage, landing, blog, portfolio  
- confidence: 0.0-1.0

Запрос: {message}

JSON ответ:""",
            }
        ]

        response = await self._generate_response(messages, max_tokens=200)

        try:
            json_start = response.find("{")
            json_end = response.rfind("}") + 1

            if json_start != -1 and json_end > json_start:
                analysis = json.loads(response[json_start:json_end])
                return {
                    "intention": analysis.get("intention", "ask_question"),
                    "content_type": analysis.get("content_type", "webpage"),
                    "confidence": float(analysis.get("confidence", 0.7)),
                    "keywords": message.split()[:5],
                }
        except (json.JSONDecodeError, ValueError):
            pass

        # Fallback анализ
        message_lower = message.lower()

        create_words = ["создай", "генерируй", "сделай"]
        if any(word in message_lower for word in create_words):
            intention = "create_page"
        elif any(word in message_lower for word in ["улучши", "исправь"]):
            intention = "modify_page"
        elif any(word in message_lower for word in ["помощь", "как"]):
            intention = "get_help"
        else:
            intention = "ask_question"

        return {
            "intention": intention,
            "content_type": "webpage",
            "confidence": 0.6,
            "keywords": message.split()[:5],
        }

    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """Генерация ответа для чата"""

        # Добавляем системное сообщение
        system_content = (
            "Ты полезный AI-ассистент для создания веб-страниц. "
            "Отвечай на русском языке, будь дружелюбным и профессиональным."
        )

        chat_messages = [{"role": "system", "content": system_content}] + messages[
            -10:
        ]  # Последние 10 сообщений

        return await self._generate_response(
            chat_messages, max_tokens=800, temperature=0.8
        )

    def get_provider_info(self) -> Dict[str, Any]:
        """Получить информацию о провайдере"""
        return {
            "provider": "deepseek-r1",
            "model": self.model_name,
            "configured": self.available,
            "transformers_available": TRANSFORMERS_AVAILABLE,
            "ai_provider_setting": "DeepSeek R1 (Local)",
        }
