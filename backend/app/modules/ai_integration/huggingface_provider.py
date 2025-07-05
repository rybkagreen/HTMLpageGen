import asyncio
import json
from typing import Any, Dict, List

import aiohttp

from app.core.config import settings
from app.modules.ai_integration.base import AIProvider


class HuggingFaceProvider(AIProvider):
    """Hugging Face API Provider для DeepSeek R1"""

    def __init__(self):
        self.api_key = settings.HUGGINGFACE_API_KEY
        self.base_url = settings.HUGGINGFACE_BASE_URL
        self.model = settings.HUGGINGFACE_MODEL

        # Fallback модели, если основная недоступна
        self.fallback_models = [
            "deepseek-ai/deepseek-coder-6.7b-instruct",
            "deepseek-ai/deepseek-coder-1.3b-instruct",
            "microsoft/DialoGPT-medium",
            "gpt2",
        ]

        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY is required")

    async def _make_request(
        self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7
    ) -> str:
        """Выполнить запрос к Hugging Face Inference API для DeepSeek-R1"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Формат для DeepSeek-R1 - используем messages format
        payload = {
            "inputs": {"messages": [{"role": "user", "content": prompt}]},
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "do_sample": True,
                "top_p": 0.9,
                "repetition_penalty": 1.1,
                "return_full_text": False,
            },
        }

        url = f"{self.base_url}/{self.model}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=120),
                ) as response:
                    if response.status == 503:
                        # Модель загружается, подождем и попробуем снова
                        await asyncio.sleep(20)
                        async with session.post(
                            url,
                            headers=headers,
                            json=payload,
                            timeout=aiohttp.ClientTimeout(total=120),
                        ) as retry_response:
                            if retry_response.status != 200:
                                # Fallback to simpler format
                                return await self._make_simple_request(
                                    prompt, max_tokens, temperature
                                )
                            result = await retry_response.json()
                    elif response.status != 200:
                        # Fallback to simpler format
                        return await self._make_simple_request(
                            prompt, max_tokens, temperature
                        )
                    else:
                        result = await response.json()

                # Обработка ответа DeepSeek-R1
                if isinstance(result, list) and len(result) > 0:
                    if "generated_text" in result[0]:
                        return result[0]["generated_text"].strip()
                    elif "text" in result[0]:
                        return result[0]["text"].strip()
                elif isinstance(result, dict):
                    if "generated_text" in result:
                        return result["generated_text"].strip()
                    elif "text" in result:
                        return result["text"].strip()
                    elif "choices" in result and len(result["choices"]) > 0:
                        choice = result["choices"][0]
                        return choice.get("message", {}).get("content", "").strip()

                return str(result)

            except asyncio.TimeoutError:
                # Fallback to simpler format
                return await self._make_simple_request(prompt, max_tokens, temperature)
            except Exception:
                # Fallback to simpler format
                return await self._make_simple_request(prompt, max_tokens, temperature)

    async def _make_simple_request(
        self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7
    ) -> str:
        """Простой fallback запрос для совместимости"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Простой формат для fallback
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "do_sample": True,
                "top_p": 0.9,
                "repetition_penalty": 1.1,
                "return_full_text": False,
            },
        }

        # Попробуем с основной моделью
        for model in [self.model] + self.fallback_models:
            url = f"{self.base_url}/{model}"

            async with aiohttp.ClientSession() as session:
                try:
                    async with session.post(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=60),
                    ) as response:
                        if response.status == 200:
                            result = await response.json()

                            if isinstance(result, list) and len(result) > 0:
                                if "generated_text" in result[0]:
                                    return result[0]["generated_text"].strip()
                                elif "text" in result[0]:
                                    return result[0]["text"].strip()
                            elif isinstance(result, dict):
                                if "generated_text" in result:
                                    return result["generated_text"].strip()
                                elif "text" in result:
                                    return result["text"].strip()

                        elif response.status == 503:
                            # Модель загружается, попробуем следующую
                            continue

                except Exception:
                    # Попробуем следующую модель
                    continue

        # Если все модели не работают, возвращаем заглушку
        return f"AI ответ на: {prompt[:50]}..."

    async def enhance_content(
        self, content: str, enhancement_type: str = "general"
    ) -> str:
        """Улучшить контент с помощью DeepSeek R1"""

        enhancement_prompts = {
            "general": (
                "Улучши следующий текст для веб-страницы, "
                "сделай его более привлекательным и информативным:"
            ),
            "seo": (
                "Оптимизируй следующий текст для поисковых систем, "
                "добавь ключевые слова и улучши SEO:"
            ),
            "accessibility": (
                "Улучши следующий текст с точки зрения "
                "доступности и удобства чтения:"
            ),
            "marketing": (
                "Перепиши следующий текст в маркетинговом стиле, "
                "сделай его более продающим:"
            ),
        }

        prompt = f"""
{enhancement_prompts.get(enhancement_type, enhancement_prompts["general"])}

Исходный текст:
{content}

Улучшенный текст:
"""

        return await self._make_request(prompt, max_tokens=800)

    async def generate_meta_tags(self, content: str) -> Dict[str, str]:
        """Генерировать SEO мета-теги"""

        prompt = f"""
Создай SEO мета-теги для следующего контента веб-страницы.
Верни результат в формате JSON с полями title, description, keywords.

Контент:
{content[:500]}...

Ответ в формате JSON:
"""

        response = await self._make_request(prompt, max_tokens=200)

        try:
            # Попытка извлечь JSON из ответа
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

        # Fallback: парсинг из обычного текста
        lines = response.split("\n")
        meta_tags = {"title": "", "description": "", "keywords": ""}

        for line in lines:
            line = line.strip()
            if line.startswith("title") or line.startswith("Title"):
                title = line.split(":", 1)[-1].strip().strip('"')[:60]
                meta_tags["title"] = title
            elif line.startswith("description") or line.startswith("Description"):
                desc = line.split(":", 1)[-1].strip().strip('"')[:160]
                meta_tags["description"] = desc
            elif line.startswith("keywords") or line.startswith("Keywords"):
                keywords = line.split(":", 1)[-1].strip().strip('"')
                meta_tags["keywords"] = keywords

        return meta_tags

    async def suggest_improvements(self, html: str) -> List[str]:
        """Предложить улучшения для HTML кода"""

        prompt = f"""
Проанализируй следующий HTML код и предложи конкретные улучшения.
Сосредоточься на:
1. SEO оптимизации
2. Доступности (accessibility)
3. Производительности
4. Семантической разметке
5. Лучших практиках

HTML код:
{html[:1000]}...

Список рекомендаций:
"""

        response = await self._make_request(prompt, max_tokens=600)

        # Разбиваем ответ на отдельные рекомендации
        suggestions = []
        lines = response.split("\n")

        for line in lines:
            line = line.strip()
            if line and (
                line.startswith("-")
                or line.startswith("•")
                or line.startswith("1.")
                or line.startswith("2.")
                or line.startswith("3.")
                or line.startswith("4.")
                or line.startswith("5.")
            ):
                # Очищаем префиксы
                suggestion = line.lstrip("- •123456789.").strip()
                if suggestion and len(suggestion) > 10:
                    suggestions.append(suggestion)

        # Если не удалось распарсить, возвращаем весь ответ как одну рекомендацию
        if not suggestions and response:
            suggestions = [response]

        return suggestions[:8]  # Максимум 8 рекомендаций

    async def generate_html_content(
        self, prompt: str, content_type: str = "webpage"
    ) -> str:
        """Генерировать HTML контент"""

        type_prompts = {
            "webpage": "Создай современную веб-страницу",
            "landing": "Создай продающую landing-страницу",
            "blog": "Создай страницу блога",
            "portfolio": "Создай портфолио страницу",
        }

        system_prompt = f"""
{type_prompts.get(content_type, type_prompts["webpage"])} на основе следующего описания.
Используй современный HTML5, CSS3 и при необходимости JavaScript.
Сделай дизайн адаптивным и следуй лучшим практикам веб-разработки.

Описание:
{prompt}

HTML код:
"""

        response = await self._make_request(system_prompt, max_tokens=2000)

        # Попытка извлечь HTML код из ответа
        html_start = response.find("<!DOCTYPE")
        if html_start == -1:
            html_start = response.find("<html")

        if html_start != -1:
            return response[html_start:]

        return response

    async def analyze_intention(self, message: str) -> Dict[str, Any]:
        """Анализ намерений пользователя из сообщения"""

        prompt = f"""
Проанализируй следующее сообщение пользователя и определи его намерения.
Верни результат в JSON формате с полями:
- intention: тип намерения (generate_html, improve_content, ask_question, 
  get_help)
- content_type: тип контента если applicable (webpage, landing, blog, 
  portfolio)
- confidence: уверенность в анализе (0.0-1.0)
- keywords: ключевые слова из запроса

Сообщение: {message}

JSON ответ:
"""

        response = await self._make_request(prompt, max_tokens=300)

        try:
            # Попытка извлечь JSON из ответа
            json_start = response.find("{")
            json_end = response.rfind("}") + 1

            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                analysis = json.loads(json_str)

                return {
                    "intention": analysis.get("intention", "ask_question"),
                    "content_type": analysis.get("content_type", "webpage"),
                    "confidence": float(analysis.get("confidence", 0.7)),
                    "keywords": analysis.get("keywords", []),
                }
        except (json.JSONDecodeError, ValueError):
            pass

        # Fallback анализ на основе ключевых слов
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

        content_type = "webpage"
        if "landing" in message_lower:
            content_type = "landing"
        elif "блог" in message_lower or "blog" in message_lower:
            content_type = "blog"
        elif "портфолио" in message_lower or "portfolio" in message_lower:
            content_type = "portfolio"

        return {
            "intention": intention,
            "content_type": content_type,
            "confidence": 0.6,
            "keywords": message.split()[:5],
        }

    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """Генерация ответа для чата"""

        # Формируем контекст из истории сообщений
        conversation: List[str] = []
        for msg in messages[-10:]:  # Берем последние 10 сообщений
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "user":
                conversation.append(f"Пользователь: {content}")
            elif role == "assistant":
                conversation.append(f"Ассистент: {content}")

        conversation_text = "\n".join(conversation)

        prompt = f"""
Ты - полезный AI-ассистент для создания веб-страниц и веб-разработки.
Отвечай на русском языке, будь дружелюбным и профессиональным.
Если пользователь просит создать веб-страницу, предложи конкретные варианты.

История разговора:
{conversation_text}

Ответ ассистента:
"""

        response = await self._make_request(prompt, max_tokens=800, temperature=0.8)

        return response.strip()

    async def _make_request_with_fallback(
        self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7
    ) -> str:
        """Выполнить запрос с fallback на другие модели"""

        models_to_try = [self.model] + self.fallback_models

        for model in models_to_try:
            try:
                return await self._make_request_to_model(
                    model, prompt, max_tokens, temperature
                )
            except Exception as e:
                print(f"Model {model} failed: {str(e)}")
                if model == models_to_try[-1]:  # Последняя модель
                    raise e
                continue

        raise Exception("All models failed")

    async def _make_request_to_model(
        self, model: str, prompt: str, max_tokens: int = 1000, temperature: float = 0.7
    ) -> str:
        """Выполнить запрос к конкретной модели"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "do_sample": True,
                "top_p": 0.9,
                "repetition_penalty": 1.1,
                "return_full_text": False,
            },
        }

        url = f"{self.base_url}/{model}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status == 503:
                        # Модель загружается
                        raise Exception("Model is loading")
                    elif response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API error {response.status}: {error_text}")

                    result = await response.json()

                # Обработка ответа
                if isinstance(result, list) and len(result) > 0:
                    if "generated_text" in result[0]:
                        return str(result[0]["generated_text"]).strip()
                    elif "text" in result[0]:
                        return str(result[0]["text"]).strip()
                elif isinstance(result, dict):
                    if "generated_text" in result:
                        return str(result["generated_text"]).strip()
                    elif "text" in result:
                        return str(result["text"]).strip()

                return str(result)

            except asyncio.TimeoutError:
                raise Exception("Request timeout")
            except Exception as e:
                raise Exception(f"Request failed: {str(e)}")

    def get_provider_info(self) -> Dict[str, Any]:
        """Получить информацию о провайдере"""
        return {
            "provider": "huggingface",
            "model": self.model,
            "configured": bool(self.api_key),
            "ai_provider_setting": "DeepSeek R1 via Hugging Face",
        }
