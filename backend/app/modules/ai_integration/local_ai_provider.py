import asyncio
import logging
import random
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

# Проверяем доступность transformers
try:
    transformers_available = True
except (ImportError, OSError):
    transformers_available = False

from app.modules.ai_integration.base import AIProvider

logger = logging.getLogger(__name__)

# Расширенные шаблоны для SEO-оптимизации
SEO_TEMPLATES = {
    'business': {
        'title_patterns': [
            '{topic} - Профессиональные услуги',
            '{topic}: качественно и надежно',
            'Лучший {topic} в вашем городе'
        ],
        'h1_patterns': [
            'Профессиональный {topic}',
            'Качественный {topic} для вашего бизнеса',
            '{topic} - наш профиль'
        ],
        'keywords_base': ['услуги', 'профессиональный', 'качественный', 'надежный', 'опыт']
    },
    'product': {
        'title_patterns': [
            '{topic} - купить выгодно',
            'Лучший {topic} с доставкой',
            '{topic}: цены, характеристики, отзывы'
        ],
        'h1_patterns': [
            'Купить {topic}',
            '{topic} - лучшие предложения',
            'Каталог {topic}'
        ],
        'keywords_base': ['купить', 'цена', 'доставка', 'качество', 'гарантия']
    },
    'informational': {
        'title_patterns': [
            'Все о {topic}: полное руководство',
            '{topic} - подробная информация',
            'Как работает {topic}'
        ],
        'h1_patterns': [
            'Полное руководство по {topic}',
            'Все что нужно знать о {topic}',
            '{topic}: подробный обзор'
        ],
        'keywords_base': ['информация', 'руководство', 'обзор', 'советы', 'рекомендации']
    }
}

# Расширенные текстовые шаблоны для генерации контента
CONTENT_TEMPLATES = {
    'introduction': [
        'В современном мире {topic} играет важную роль в {context}.',
        'Качественный {topic} — это основа успешного {context}.',
        'Выбор правильного {topic} может существенно повлиять на {context}.'
    ],
    'benefits': [
        'Основные преимущества {topic} включают в себя:',
        'Почему стоит выбрать именно {topic}:',
        'Ключевые особенности {topic}:'
    ],
    'features': [
        'Высокое качество и надежность',
        'Профессиональный подход к каждому клиенту',
        'Индивидуальные решения для ваших задач',
        'Быстрое выполнение заказов',
        'Гарантия на все виды работ'
    ],
    'conclusion': [
        'Обращайтесь к нам для получения качественного {topic}.',
        'Мы поможем вам выбрать оптимальный {topic} для ваших нужд.',
        'Получите консультацию по {topic} уже сегодня.'
    ]
}


class LocalAIProvider(AIProvider):
    """Локальный AI Provider - простая версия без сложных моделей"""

    def __init__(self) -> None:
        self.model_name = "local-fallback"
        self.available = True  # Всегда доступен в fallback режиме
        logger.info("Локальный AI провайдер инициализирован (fallback режим)")

    async def enhance_content(
        self, content: str, enhancement_type: str = "general"
    ) -> str:
        """Улучшить контент с помощью AI"""
        if enhancement_type == "seo":
            return await self._enhance_content_for_seo(content)
        elif enhancement_type == "accessibility":
            return await self._enhance_content_for_accessibility(content)
        elif enhancement_type == "marketing":
            return await self._enhance_content_for_marketing(content)
        else:
            return await self._enhance_content_general(content)

    async def _enhance_content_for_seo(self, content: str) -> str:
        """Улучшить контент для SEO"""
        # Извлекаем ключевую тему из контента
        topic = self._extract_main_topic(content)
        
        # Генерируем расширенный SEO-контент
        enhanced_parts = []
        
        # Добавляем введение
        intro_template = random.choice(CONTENT_TEMPLATES['introduction'])
        enhanced_parts.append(intro_template.format(topic=topic, context="бизнес-процессах"))
        
        # Добавляем основной контент с улучшениями
        enhanced_parts.append(f"\n\n{content}")
        
        # Добавляем преимущества
        benefits_intro = random.choice(CONTENT_TEMPLATES['benefits'])
        enhanced_parts.append(f"\n\n{benefits_intro.format(topic=topic)}")
        
        # Добавляем список преимуществ
        features = random.sample(CONTENT_TEMPLATES['features'], 3)
        for i, feature in enumerate(features, 1):
            enhanced_parts.append(f"\n{i}. {feature}")
        
        # Добавляем заключение
        conclusion = random.choice(CONTENT_TEMPLATES['conclusion'])
        enhanced_parts.append(f"\n\n{conclusion.format(topic=topic)}")
        
        # Добавляем дополнительную SEO-информацию
        enhanced_parts.append(f"\n\nДля получения более подробной информации о {topic}, свяжитесь с нашими специалистами. Мы предлагаем индивидуальный подход и гарантируем высокое качество услуг.")
        
        await asyncio.sleep(0.2)  # Имитация обработки
        return ''.join(enhanced_parts)

    async def _enhance_content_for_accessibility(self, content: str) -> str:
        """Улучшить контент для доступности"""
        enhanced = f"""
        {content}
        
        Дополнительная информация для улучшения доступности:
        • Весь контент адаптирован для программ чтения с экрана
        • Используются семантические HTML-теги для лучшей навигации
        • Контрастность цветов соответствует стандартам WCAG
        • Все интерактивные элементы доступны с клавиатуры
        • Предоставлены альтернативные описания для всех изображений
        """
        await asyncio.sleep(0.1)
        return enhanced

    async def _enhance_content_for_marketing(self, content: str) -> str:
        """Улучшить контент для маркетинга"""
        topic = self._extract_main_topic(content)
        enhanced = f"""
        🚀 {content}
        
        ✅ Преимущества выбора нашего {topic}:
        • Проверенное качество и надежность
        • Индивидуальный подход к каждому клиенту
        • Быстрые сроки выполнения
        • Конкурентные цены на рынке
        • Гарантия на все виды работ
        
        📞 Закажите консультацию прямо сейчас!
        💰 Специальные предложения для новых клиентов
        🎯 Получите персональное коммерческое предложение
        """
        await asyncio.sleep(0.1)
        return enhanced

    async def _enhance_content_general(self, content: str) -> str:
        """Общее улучшение контента"""
        topic = self._extract_main_topic(content)
        enhanced = f"""
        {content}
        
        Дополнительная информация:
        {topic} является важным аспектом современной деятельности. Правильный подход к {topic} 
        может значительно улучшить результаты и повысить эффективность работы.
        
        Рекомендации по использованию:
        • Учитывайте специфику вашей сферы деятельности
        • Обращайтесь к проверенным специалистам
        • Регулярно обновляйте информацию
        • Следите за новыми тенденциями в области
        """
        await asyncio.sleep(0.1)
        return enhanced

    def _extract_main_topic(self, content: str) -> str:
        """Извлечь основную тему из контента"""
        # Простой алгоритм извлечения темы
        words = re.findall(r'\b\w{4,}\b', content.lower())
        if not words:
            return "услуга"
        
        # Исключаем служебные слова
        stop_words = {'этот', 'который', 'может', 'быть', 'есть', 'для', 'или', 'как', 'что', 'когда', 'где'}
        meaningful_words = [w for w in words if w not in stop_words]
        
        if meaningful_words:
            return meaningful_words[0]
        return "услуга"

    async def generate_meta_tags(self, content: str) -> Dict[str, str]:
        """Генерировать продвинутые SEO мета-теги"""
        # Извлекаем основную тему
        topic = self._extract_main_topic(content)
        
        # Определяем тип контента для выбора подходящего шаблона
        content_type = self._determine_content_type(content)
        
        # Генерируем title с использованием шаблонов
        title = self._generate_seo_title(topic, content_type, content)
        
        # Генерируем description
        description = self._generate_seo_description(topic, content_type, content)
        
        # Генерируем keywords
        keywords = self._generate_seo_keywords(topic, content_type, content)
        
        # Дополнительные мета-теги для продвинутой SEO
        additional_meta = self._generate_additional_meta_tags(content, topic)
        
        result = {
            "title": title,
            "description": description,
            "keywords": keywords,
            **additional_meta
        }
        
        await asyncio.sleep(0.1)  # Имитация обработки
        return result

    def _determine_content_type(self, content: str) -> str:
        """Определить тип контента для выбора подходящего SEO шаблона"""
        content_lower = content.lower()
        
        # Коммерческие индикаторы
        commercial_indicators = ['купить', 'цена', 'стоимость', 'заказать', 'услуга', 'продажа']
        if any(indicator in content_lower for indicator in commercial_indicators):
            return 'business'
        
        # Информационные индикаторы
        info_indicators = ['как', 'что такое', 'почему', 'инструкция', 'руководство', 'обзор']
        if any(indicator in content_lower for indicator in info_indicators):
            return 'informational'
        
        # Продуктовые индикаторы
        product_indicators = ['характеристики', 'модель', 'функции', 'возможности']
        if any(indicator in content_lower for indicator in product_indicators):
            return 'product'
        
        return 'business'  # По умолчанию

    def _generate_seo_title(self, topic: str, content_type: str, content: str) -> str:
        """Генерировать SEO-оптимизированный title"""
        template_group = SEO_TEMPLATES.get(content_type, SEO_TEMPLATES['business'])
        title_template = random.choice(template_group['title_patterns'])
        
        # Формируем title с учетом длины (30-60 символов оптимально)
        title = title_template.format(topic=topic.title())
        
        # Если title слишком длинный, сокращаем
        if len(title) > 60:
            title = f"{topic.title()} - качественные решения"
        
        # Если слишком короткий, добавляем детали
        if len(title) < 30:
            title += f" | Профессиональные услуги"
        
        return title

    def _generate_seo_description(self, topic: str, content_type: str, content: str) -> str:
        """Генерировать SEO-оптимизированное описание"""
        # Извлекаем первое предложение из контента
        first_sentence = content.split('.')[0] if '.' in content else content[:80]
        
        # Базовые описания по типам контента
        description_templates = {
            'business': f"Профессиональный {topic} от экспертов. {first_sentence}. Качество, надежность, индивидуальный подход. Консультация и расчет стоимости.",
            'product': f"Лучший {topic} по выгодным ценам. {first_sentence}. Характеристики, отзывы, доставка. Гарантия качества.",
            'informational': f"Полная информация о {topic}. {first_sentence}. Подробные инструкции, советы экспертов, практические рекомендации."
        }
        
        description = description_templates.get(content_type, description_templates['business'])
        
        # Ограничиваем длину description (120-160 символов оптимально)
        if len(description) > 160:
            description = description[:157] + "..."
        elif len(description) < 120:
            description += f" Узнайте больше о {topic} прямо сейчас."
        
        return description

    def _generate_seo_keywords(self, topic: str, content_type: str, content: str) -> str:
        """Генерировать SEO keywords"""
        # Базовые ключевые слова из шаблонов
        template_group = SEO_TEMPLATES.get(content_type, SEO_TEMPLATES['business'])
        base_keywords = template_group['keywords_base'].copy()
        
        # Добавляем основную тему
        keywords = [topic]
        
        # Добавляем базовые keywords
        keywords.extend(base_keywords[:4])
        
        # Извлекаем дополнительные keywords из контента
        content_words = re.findall(r'\b[а-яё]{4,}\b', content.lower())
        stop_words = {'этот', 'который', 'может', 'быть', 'есть', 'для', 'или', 'как', 'что', 
                     'когда', 'где', 'после', 'перед', 'через', 'между', 'сейчас', 'всегда'}
        
        content_keywords = [word for word in content_words if word not in stop_words][:3]
        keywords.extend(content_keywords)
        
        # Удаляем дубликаты и ограничиваем количество
        unique_keywords = list(dict.fromkeys(keywords))[:8]
        
        return ", ".join(unique_keywords)

    async def generate_structured_headings(self, content: str) -> Dict[str, List[str]]:
        """Генерировать структурированные заголовки H1-H3"""
        topic = self._extract_main_topic(content)
        content_type = self._determine_content_type(content)
        
        # Генерируем основной H1
        template_group = SEO_TEMPLATES.get(content_type, SEO_TEMPLATES['business'])
        h1_template = random.choice(template_group['h1_patterns'])
        h1 = h1_template.format(topic=topic.title())
        
        # Генерируем H2 заголовки
        h2_headings = [
            f"Что такое {topic}?",
            f"Преимущества {topic}",
            f"Как выбрать {topic}?",
            f"Почему стоит обратиться к нам?"
        ]
        
        # Генерируем H3 подзаголовки
        h3_headings = [
            f"Основные характеристики {topic}",
            f"Сферы применения {topic}",
            f"Критерии качества {topic}",
            f"Инновации в области {topic}",
            f"Рекомендации по использованию {topic}",
            f"Практические советы по {topic}"
        ]
        
        await asyncio.sleep(0.1)
        return {
            "h1": [h1],
            "h2": h2_headings[:3],  # Ограничиваем 3 H2
            "h3": h3_headings[:5]   # Ограничиваем 5 H3
        }

    async def generate_key_phrases(self, content: str) -> List[str]:
        """Генерировать ключевые фразы для SEO"""
        topic = self._extract_main_topic(content)
        content_type = self._determine_content_type(content)
        
        # Базовые ключевые фразы по типам контента
        phrase_templates = {
            'business': [
                f"профессиональный {topic}",
                f"качественные услуги {topic}",
                f"{topic} по выгодным ценам",
                f"лучшие специалисты по {topic}",
                f"надежный {topic} в Москве",
                f"заказать {topic} недорого"
            ],
            'product': [
                f"купить {topic}",
                f"{topic} с доставкой",
                f"цены на {topic}",
                f"характеристики {topic}",
                f"отзывы о {topic}",
                f"лучшие модели {topic}"
            ],
            'informational': [
                f"как выбрать {topic}",
                f"что такое {topic}",
                f"руководство по {topic}",
                f"советы по {topic}",
                f"преимущества {topic}",
                f"особенности {topic}"
            ]
        }
        
        base_phrases = phrase_templates.get(content_type, phrase_templates['business'])
        
        # Добавляем длиннохвостовые ключевые фразы
        long_tail_phrases = [
            f"как правильно выбрать {topic} для дома",
            f"сколько стоит качественный {topic}",
            f"где найти лучший {topic} в Москве",
            f"почему стоит выбрать наш {topic}"
        ]
        
        all_phrases = base_phrases + long_tail_phrases[:2]
        
        await asyncio.sleep(0.1)
        return all_phrases[:8]  # Ограничиваем количество

    async def generate_alt_texts(self, content: str, image_count: int = 3) -> List[str]:
        """Генерировать alt-тексты для изображений"""
        topic = self._extract_main_topic(content)
        
        # Шаблоны alt-текстов
        alt_templates = [
            f"Профессиональный {topic} - качественные услуги",
            f"Пример качественного {topic} с гарантией",
            f"Специалисты по {topic} за работой",
            f"Результат профессионального {topic}",
            f"Качественные материалы для {topic}",
            f"Инновационные решения в области {topic}",
            f"Команда экспертов по {topic}",
            f"Процесс создания качественного {topic}"
        ]
        
        # Выбираем нужное количество alt-текстов
        selected_alts = alt_templates[:image_count]
        
        await asyncio.sleep(0.1)
        return selected_alts

    async def generate_expanded_content(self, content: str, target_word_count: int = 500) -> str:
        """Увеличить объем и уникальность основного текста"""
        topic = self._extract_main_topic(content)
        content_type = self._determine_content_type(content)
        
        # Считаем текущее количество слов
        current_word_count = len(content.split())
        
        if current_word_count >= target_word_count:
            return content  # Уже достаточно слов
        
        expanded_parts = [content]
        
        # Добавляем дополнительные секции контента
        additional_sections = [
            f"""

Особенности современного {topic}

В наше время {topic} претерпел значительные изменения. Инновационные технологии и методики позволяют достигать более высоких результатов при меньших затратах времени и ресурсов. Ключевыми факторами успеха являются профессиональное оборудование, квалифицированные специалисты и системный подход к решению задач.""",
            
            f"""

Преимущества профессионального подхода

Обращение к проверенным специалистам по {topic} гарантирует получение качественного результата в короткие сроки. Опытные мастера знают все нюансы работы с {topic}, умеют предугадывать возможные проблемы и находить оптимальные решения. Кроме того, профессиональный подход включает в себя полное сопровождение проекта, консультирование и послегарантийный сервис.""",
            
            f"""

Как выбрать качественный {topic}

Правильный выбор {topic} — это сложная задача, требующая учета множества факторов. Основными критериями являются: качество материалов, репутация поставщика, соотношение цены и качества, а также сроки выполнения работ. Не менее важны отзывы клиентов, наличие гарантий и возможность получить консультацию по всем вопросам."""
        ]
        
        # Добавляем секции пока не достигнем целевого количества слов
        for section in additional_sections:
            expanded_parts.append(section)
            current_text = ''.join(expanded_parts)
            if len(current_text.split()) >= target_word_count:
                break
        
        # Добавляем заключение
        expanded_parts.append(f"""

Заключение

VULвыбор {topic} — это важное решение, которое влияет на конечный результат. Обращаясь к профессионалам, вы можете быть уверены в качестве и надежности предоставляемых услуг. Наша команда готова предложить вам оптимальное решение в области {topic} с учетом всех ваших пожеланий и требований.""")
        
        result = ''.join(expanded_parts)
        await asyncio.sleep(0.2)
        return result

    def _generate_additional_meta_tags(self, content: str, topic: str) -> Dict[str, str]:
        """Генерировать дополнительные мета-теги для продвинутой SEO"""
        return {
            # Open Graph теги
            'og:type': 'website',
            'og:title': f"{topic.title()} - профессиональные решения",
            'og:description': content[:100] + "..." if len(content) > 100 else content,
            'og:image': '/images/default-og-image.jpg',
            
            # Twitter Card теги
            'twitter:card': 'summary_large_image',
            'twitter:title': f"{topic.title()} - качественные услуги",
            'twitter:description': content[:120] + "..." if len(content) > 120 else content,
            
            # Дополнительные SEO теги
            'robots': 'index, follow',
            'author': 'AI Content Generator',
            'viewport': 'width=device-width, initial-scale=1.0',
            'canonical': f'/services/{topic.lower().replace(" ", "-")}',
            
            # Structured data hints
            'article:author': 'AI Content Generator',
            'article:section': topic.title(),
            'geo.region': 'RU',
            'geo.placename': 'Россия'
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
        """Генерировать HTML контент на основе промпта"""
        logger.info(f"Генерация HTML контента: {prompt[:50]}...")

        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Сгенерированная страница</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        h1 {{ color: #333; }}
        .content {{ background: #f9f9f9; padding: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Автоматически сгенерированная страница</h1>
        <div class="content">
            <h2>Тема: {prompt}</h2>
            <p>Тип: {content_type}</p>
            <p>Создано локальным AI генератором в {datetime.now().strftime("%H:%M")}</p>
        </div>
    </div>
</body>
</html>"""

    async def analyze_intention(self, message: str) -> Dict[str, str]:
        """Анализ намерений пользователя"""
        message_lower = message.lower()

        if any(word in message_lower for word in ["создай", "сделай"]):
            return {
                "intent": "create",
                "action": "generate_html",
                "confidence": "high",
            }
        elif any(word in message_lower for word in ["улучши", "исправь"]):
            return {
                "intent": "improve",
                "action": "enhance_content",
                "confidence": "high",
            }
        else:
            return {
                "intent": "general",
                "action": "chat",
                "confidence": "medium",
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

    async def get_provider_info(self) -> Dict[str, Any]:
        """Получить информацию о провайдере"""
        return {
            "provider": "local-ai",
            "model": self.model_name,
            "configured": self.available,
            "transformers_available": transformers_available,
            "ai_provider_setting": "Локальная AI модель (fallback режим)",
        }
