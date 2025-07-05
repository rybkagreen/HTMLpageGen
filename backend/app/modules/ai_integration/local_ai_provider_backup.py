import asyncio
import json
import logging
import os
import random
from typing import Any, Dict, List

try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, set_seed

    TRANSFORMERS_AVAILABLE = True
except (ImportError, OSError) as e:
    # OSError может возникнуть при проблемах с зависимостями
    TRANSFORMERS_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning(f"Transformers недоступен: {e}")

from app.core.config import settings
from app.modules.ai_integration.base import AIProvider

logger = logging.getLogger(__name__)


class LocalAIProvider(AIProvider):
    """Локальный AI Provider с небольшими моделями"""

    def __init__(self):
        self.model_name = "microsoft/DialoGPT-small"  # Компактная модель для диалогов
        self.backup_model = "gpt2"  # Fallback модель
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        self.available = False
        self.max_length = 512  # Ограничение для небольших моделей

        if TRANSFORMERS_AVAILABLE:
            self._initialize_model()
        else:
            logger.error("Transformers не установлен")

    def _initialize_model(self):
        """Инициализация локальной модели"""
        try:
            logger.info("Загружаем локальную AI модель...")

            # Устанавливаем seed для воспроизводимости
            set_seed(42)

            # Пробуем загрузить основную модель
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_name, padding_side="left"
                )

                # Добавляем pad_token если его нет
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token

                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float32,  # Используем float32 для совместимости
                    device_map="auto" if torch.cuda.is_available() else None,
                    low_cpu_mem_usage=True,
                )

                logger.info(f"Модель {self.model_name} загружена успешно")
                self.available = True

            except Exception as e:
                logger.warning(f"Не удалось загрузить {self.model_name}: {e}")

                # Fallback к GPT-2
                try:
                    logger.info("Пробуем fallback модель GPT-2...")
                    self.model_name = self.backup_model

                    self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                    if self.tokenizer.pad_token is None:
                        self.tokenizer.pad_token = self.tokenizer.eos_token

                    self.model = AutoModelForCausalLM.from_pretrained(
                        self.model_name,
                        torch_dtype=torch.float32,
                        low_cpu_mem_usage=True,
                    )

                    logger.info(f"Fallback модель {self.model_name} загружена")
                    self.available = True

                except Exception as e2:
                    logger.error(f"Не удалось загрузить fallback модель: {e2}")
                    self.available = False

        except Exception as e:
            logger.error(f"Критическая ошибка инициализации модели: {e}")
            self.available = False

    async def _generate_text(
        self,
        prompt: str,
        max_length: int = 200,
        temperature: float = 0.7,
        do_sample: bool = True,
    ) -> str:
        """Базовая генерация текста"""

        if not self.available:
            return self._fallback_response(prompt)

        try:
            loop = asyncio.get_event_loop()

            def generate():
                inputs = self.tokenizer.encode(
                    prompt,
                    return_tensors="pt",
                    max_length=self.max_length,
                    truncation=True,
                )

                # Ограничиваем длину генерации
                max_new_tokens = min(max_length, 150)

                with torch.no_grad():
                    outputs = self.model.generate(
                        inputs,
                        max_new_tokens=max_new_tokens,
                        temperature=temperature,
                        do_sample=do_sample,
                        top_p=0.9,
                        top_k=50,
                        repetition_penalty=1.1,
                        pad_token_id=self.tokenizer.pad_token_id,
                        eos_token_id=self.tokenizer.eos_token_id,
                        early_stopping=True,
                    )

                # Декодируем только новую часть
                generated = outputs[0][inputs.shape[1] :]
                response = self.tokenizer.decode(generated, skip_special_tokens=True)

                return response.strip()

            result = await loop.run_in_executor(None, generate)

            # Постобработка результата
            if not result:
                return self._create_template_response(prompt)

            return result

        except Exception as e:
            logger.error(f"Ошибка генерации: {e}")
            return self._create_template_response(prompt)

    def _fallback_response(self, prompt: str) -> str:
        """Fallback ответ когда модель недоступна"""
        return (
            f"Локальная AI модель временно недоступна. "
            f"Создаю базовый ответ для: '{prompt[:50]}...'"
        )

    def _create_template_response(self, prompt: str) -> str:
        """Создание шаблонного ответа на основе промпта"""
        prompt_lower = prompt.lower()

        if any(word in prompt_lower for word in ["html", "страница", "сайт", "веб"]):
            return self._create_html_template()
        elif any(word in prompt_lower for word in ["css", "стиль", "дизайн"]):
            css_styles = [
                "/* Современные CSS стили */\nbody { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }",
                "/* Адаптивный дизайн */\nbody { font-family: Arial, sans-serif; margin: 0; padding: 20px; }",
                "/* Минималистичный стиль */\nbody { font-family: 'Helvetica Neue', sans-serif; line-height: 1.6; }",
            ]
            return random.choice(css_styles)
        elif any(word in prompt_lower for word in ["мета", "seo", "тег"]):
            seo_tips = [
                "Добавьте мета-теги: title, description, keywords для лучшего SEO",
                "Используйте семантические HTML теги: header, nav, main, footer",
                "Оптимизируйте заголовки H1-H6 для поисковых систем",
            ]
            return random.choice(seo_tips)
        else:
            fallback_responses = [
                "Локальная модель работает в ограниченном режиме. Попробуйте переформулировать запрос.",
                "Я понял ваш запрос, но не могу дать полный ответ. Используйте более конкретные термины.",
                "Для лучших результатов попробуйте указать конкретную задачу (HTML, CSS, SEO).",
            ]
            return random.choice(fallback_responses)

    def _create_html_template(self) -> str:
        """Создание базового HTML шаблона"""
        return """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Сгенерированная страница</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        .header {
            background: #007bff;
            color: white;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 2rem;
        }
        .content {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Добро пожаловать</h1>
    </div>
    <div class="content">
        <h2>Контент страницы</h2>
        <p>Здесь будет размещен основной контент вашей страницы.</p>
    </div>
</body>
</html>"""

    async def enhance_content(
        self, content: str, enhancement_type: str = "general"
    ) -> str:
        """Улучшить контент"""

        enhancement_prompts = {
            "general": f"Улучши этот текст: {content}",
            "seo": f"Оптимизируй для SEO: {content}",
            "accessibility": f"Сделай более доступным: {content}",
            "marketing": f"Сделай более продающим: {content}",
        }

        prompt = enhancement_prompts.get(
            enhancement_type, enhancement_prompts["general"]
        )

        if not self.available:
            return f"Улучшенная версия: {content} (добавлены базовые улучшения)"

        result = await self._generate_text(prompt, max_length=150)

        # Если результат слишком короткий, добавляем базовые улучшения
        if len(result) < 20:
            return (
                f"{content}\n\n[Добавлены улучшения: лучшая структура, SEO оптимизация]"
            )

        return result

    async def generate_meta_tags(self, content: str) -> Dict[str, str]:
        """Генерировать SEO мета-теги"""

        # Простой анализ контента для генерации тегов
        words = content.lower().split()

        # Извлекаем ключевые слова (простой алгоритм)
        common_words = {
            "и",
            "в",
            "на",
            "с",
            "по",
            "для",
            "от",
            "до",
            "из",
            "а",
            "но",
            "или",
            "что",
            "как",
            "это",
            "то",
            "не",
            "за",
            "при",
            "под",
        }
        keywords = [
            word for word in words[:20] if len(word) > 3 and word not in common_words
        ][:5]

        # Генерируем title из первых слов
        title_words = content.split()[:8]
        title = " ".join(title_words)
        if len(title) > 60:
            title = title[:57] + "..."

        # Генерируем description
        sentences = content.split(".")[:2]
        description = ". ".join(sentences).strip()
        if len(description) > 160:
            description = description[:157] + "..."

        return {
            "title": title or "AI Generated Page",
            "description": description or "Страница создана с помощью AI",
            "keywords": ", ".join(keywords) or "ai, веб, страница",
        }

    async def suggest_improvements(self, html: str) -> List[str]:
        """Предложить улучшения для HTML кода"""

        suggestions = []

        # Простые правила для анализа HTML
        if "<!DOCTYPE" not in html:
            suggestions.append("Добавьте DOCTYPE декларацию")

        if "lang=" not in html:
            suggestions.append("Добавьте атрибут lang в тег html")

        if "<title>" not in html:
            suggestions.append("Добавьте тег title")

        if "viewport" not in html:
            suggestions.append("Добавьте мета-тег viewport для адаптивности")

        if "alt=" not in html and "<img" in html:
            suggestions.append("Добавьте alt атрибуты для изображений")

        if len(suggestions) == 0:
            suggestions = [
                "Код выглядит хорошо!",
                "Рассмотрите добавление CSS для стилизации",
                "Проверьте семантическую разметку",
                "Добавьте интерактивность с JavaScript",
            ]

        return suggestions[:8]

    async def generate_html_content(
        self, prompt: str, content_type: str = "webpage"
    ) -> str:
        """Генерировать HTML контент"""

        if not self.available:
            return self._create_specialized_template(prompt, content_type)

        html_prompt = f"Создай HTML страницу типа {content_type} по описанию: {prompt}"

        result = await self._generate_text(html_prompt, max_length=300)

        # Если в результате нет HTML тегов, используем шаблон
        if "<html" not in result and "<!DOCTYPE" not in result:
            return self._create_specialized_template(prompt, content_type)

        return result

    def _create_specialized_template(self, prompt: str, content_type: str) -> str:
        """Создание специализированного шаблона по типу контента"""
        from datetime import datetime
        current_date = datetime.now().strftime("%d.%m.%Y")
        title = prompt[:50] if prompt else "Сгенерированная страница"

        # Базовые стили
        base_style = (
            "body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }"
            ".container { max-width: 800px; margin: 0 auto; }"
            "h1 { color: #333; }"
        )

        # Создаем простой HTML шаблон
        html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>{base_style}</style>
</head>
<body>
    <div class="container">
        <h1>{prompt}</h1>
        <p>Содержание страницы типа: {content_type}</p>
        <p>Создано с помощью локального AI генератора.</p>
    </div>
</body>
</html>"""
        
        return html_content
        <p>Мои работы и проекты</p>
    </header>
    <div class="portfolio">
        <div class="project">
            <h3>Проект 1</h3>
            <p>Описание проекта...</p>
        </div>
    </div>
</body>
</html>""",
        }

        from datetime import datetime

        template = templates.get(content_type, self._create_html_template())

        return template.format(
            prompt=prompt[:50], date=datetime.now().strftime("%d.%m.%Y")
        )

    async def analyze_intention(self, message: str) -> Dict[str, Any]:
        """Анализ намерений пользователя (простой алгоритм)"""

        message_lower = message.lower()

        # Определяем намерение по ключевым словам
        create_words = ["создай", "генерируй", "сделай", "построй", "разработай"]
        modify_words = ["улучши", "измени", "исправь", "обнови", "доработай"]
        help_words = ["помоги", "помощь", "как", "что", "объясни"]
        analyze_words = ["проанализируй", "проверь", "оцени", "анализ"]

        if any(word in message_lower for word in create_words):
            intention = "create_page"
        elif any(word in message_lower for word in modify_words):
            intention = "modify_page"
        elif any(word in message_lower for word in analyze_words):
            intention = "analyze_code"
        elif any(word in message_lower for word in help_words):
            intention = "get_help"
        else:
            intention = "ask_question"

        # Определяем тип контента
        if any(word in message_lower for word in ["лендинг", "landing"]):
            content_type = "landing"
        elif any(word in message_lower for word in ["блог", "blog", "статья"]):
            content_type = "blog"
        elif any(word in message_lower for word in ["портфолио", "portfolio"]):
            content_type = "portfolio"
        else:
            content_type = "webpage"

        return {
            "intention": intention,
            "content_type": content_type,
            "confidence": 0.8,
            "keywords": message.split()[:5],
        }

    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """Генерация ответа для чата"""

        if not messages:
            return "Привет! Я могу помочь создать веб-страницы. Что хотите создать?"

        last_message = messages[-1].get("content", "")

        # Формируем контекст
        context = "Диалог с AI помощником по веб-разработке:\n"
        for msg in messages[-3:]:  # Последние 3 сообщения для контекста
            role = "Пользователь" if msg["role"] == "user" else "Ассистент"
            context += f"{role}: {msg['content']}\n"

        context += "Ассистент:"

        if self.available:
            response = await self._generate_text(context, max_length=100)
            if len(response) > 10:
                return response

        # Fallback ответы на основе ключевых слов
        return self._generate_contextual_response(last_message)

    def _generate_contextual_response(self, message: str) -> str:
        """Генерация контекстного ответа"""
        message_lower = message.lower()

        if any(word in message_lower for word in ["создай", "сделай", "генерируй"]):
            if "лендинг" in message_lower:
                return "Отлично! Создам лендинг-страницу. Укажите тематику и целевую аудиторию."
            elif "сайт" in message_lower or "страница" in message_lower:
                return (
                    "Создам веб-страницу для вас. Опишите, что должно быть на странице."
                )
            else:
                return "Готов помочь с созданием! Уточните, что именно нужно создать."

        elif any(word in message_lower for word in ["улучши", "оптимизируй"]):
            return (
                "Помогу улучшить ваш контент. Пришлите текст или код для оптимизации."
            )

        elif any(word in message_lower for word in ["помощь", "как", "что"]):
            return "Я могу помочь создать веб-страницы, лендинги, блоги. Также умею оптимизировать контент и анализировать код."

        else:
            return "Интересный вопрос! Как я могу помочь с веб-разработкой?"

    def get_provider_info(self) -> Dict[str, Any]:
        """Получить информацию о провайдере"""
        return {
            "provider": "local-ai",
            "model": self.model_name,
            "configured": self.available,
            "transformers_available": TRANSFORMERS_AVAILABLE,
            "ai_provider_setting": "Локальная AI модель",
        }
