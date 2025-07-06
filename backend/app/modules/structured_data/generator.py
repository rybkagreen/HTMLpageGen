"""
Основной генератор структурированных данных с интеграцией AI
"""

import json
import re
from typing import Any, Dict, List, Optional, Union
from bs4 import BeautifulSoup

from .schemas import (
    FAQSchema, ProductSchema, BreadcrumbSchema, ArticleSchema, OrganizationSchema,
    FAQItem, ProductOffer, ProductReview, BreadcrumbItem
)


class StructuredDataGenerator:
    """Генератор структурированных данных schema.org с поддержкой AI"""
    
    def __init__(self, ai_service=None):
        """
        Инициализация генератора
        
        Args:
            ai_service: Сервис AI для автоматического извлечения данных
        """
        self.ai_service = ai_service
        self.schemas = {
            'faq': FAQSchema,
            'product': ProductSchema,
            'breadcrumb': BreadcrumbSchema,
            'article': ArticleSchema,
            'organization': OrganizationSchema
        }
    
    async def generate_structured_data(
        self,
        schema_type: str,
        data: Optional[Dict[str, Any]] = None,
        content: Optional[str] = None,
        auto_extract: bool = True
    ) -> Dict[str, Any]:
        """
        Генерирует структурированные данные указанного типа
        
        Args:
            schema_type: Тип схемы (faq, product, breadcrumb, article, organization)
            data: Явно переданные данные
            content: Контент для автоматического извлечения данных
            auto_extract: Использовать ли AI для автоматического извлечения
            
        Returns:
            JSON-LD структурированные данные
        """
        if schema_type not in self.schemas:
            raise ValueError(f"Неподдерживаемый тип схемы: {schema_type}")
        
        schema_class = self.schemas[schema_type]
        
        # Если данные не переданы, пытаемся извлечь автоматически
        if not data and content and auto_extract and self.ai_service:
            data = await self._extract_data_with_ai(schema_type, content)
        elif not data:
            data = {}
        
        # Генерируем схему в зависимости от типа
        if schema_type == 'faq':
            return await self._generate_faq_schema(data, content)
        elif schema_type == 'product':
            return self._generate_product_schema(data)
        elif schema_type == 'breadcrumb':
            return self._generate_breadcrumb_schema(data)
        elif schema_type == 'article':
            return self._generate_article_schema(data)
        elif schema_type == 'organization':
            return self._generate_organization_schema(data)
        
        return {}
    
    async def _extract_data_with_ai(self, schema_type: str, content: str) -> Dict[str, Any]:
        """
        Извлекает данные из контента с помощью AI
        
        Args:
            schema_type: Тип схемы
            content: Контент для анализа
            
        Returns:
            Извлеченные данные
        """
        if not self.ai_service:
            return {}
        
        prompts = {
            'faq': self._get_faq_extraction_prompt(content),
            'product': self._get_product_extraction_prompt(content),
            'breadcrumb': self._get_breadcrumb_extraction_prompt(content),
            'article': self._get_article_extraction_prompt(content),
            'organization': self._get_organization_extraction_prompt(content)
        }
        
        if schema_type not in prompts:
            return {}
        
        try:
            # Отправляем запрос AI для извлечения данных
            response = await self.ai_service.chat_completion([
                {
                    "role": "user",
                    "content": prompts[schema_type]
                }
            ])
            
            # Пытаемся парсить JSON ответ
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            return {}
        except Exception as e:
            print(f"Ошибка извлечения данных с AI: {e}")
            return {}
    
    def _get_faq_extraction_prompt(self, content: str) -> str:
        """Генерирует промпт для извлечения FAQ данных"""
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
    
    def _get_product_extraction_prompt(self, content: str) -> str:
        """Генерирует промпт для извлечения данных продукта"""
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
    
    def _get_breadcrumb_extraction_prompt(self, content: str) -> str:
        """Генерирует промпт для извлечения хлебных крошек"""
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
    
    def _get_article_extraction_prompt(self, content: str) -> str:
        """Генерирует промпт для извлечения данных статьи"""
        return f"""
Проанализируй следующий контент и извлеки информацию о статье.
Верни результат в формате JSON:

{{
    "headline": "Заголовок статьи",
    "author": "Автор статьи",
    "description": "Краткое описание статьи",
    "date_published": "2024-01-01T00:00:00Z",
    "date_modified": "2024-01-01T00:00:00Z",
    "image": "URL изображения (если есть)",
    "url": "URL статьи (если есть)",
    "publisher_name": "Название издателя (если есть)"
}}

Контент:
{content}

Если дата не указана, используй текущую дату в ISO формате.
"""
    
    def _get_organization_extraction_prompt(self, content: str) -> str:
        """Генерирует промпт для извлечения данных организации"""
        return f"""
Проанализируй следующий контент и извлеки информацию об организации.
Верни результат в формате JSON:

{{
    "name": "Название организации",
    "description": "Описание организации",
    "url": "Веб-сайт (если есть)",
    "phone": "Телефон (если есть)",
    "email": "Email (если есть)",
    "address": {{
        "street": "Улица",
        "city": "Город",
        "region": "Регион",
        "postal_code": "Индекс",
        "country": "Страна"
    }},
    "social_media": ["URL1", "URL2"]
}}

Контент:
{content}

Если какая-то информация отсутствует, используй null.
"""
    
    async def _generate_faq_schema(self, data: Dict[str, Any], content: str = None) -> Dict[str, Any]:
        """Генерирует FAQ схему"""
        faq_items = []
        
        if 'faq_items' in data:
            for item in data['faq_items']:
                faq_items.append(FAQItem(
                    question=item['question'],
                    answer=item['answer']
                ))
        elif content and self.ai_service:
            # Если нет структурированных данных, извлекаем из контента
            extracted = await self._extract_data_with_ai('faq', content)
            if 'faq_items' in extracted:
                for item in extracted['faq_items']:
                    faq_items.append(FAQItem(
                        question=item['question'],
                        answer=item['answer']
                    ))
        
        if not faq_items:
            return {}
        
        # Исключаем faq_items из kwargs, так как они передаются отдельно
        kwargs = {k: v for k, v in data.items() if k != 'faq_items'}
        return FAQSchema.generate(faq_items, **kwargs)
    
    def _generate_product_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует Product схему"""
        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in data:
                return {}
        
        # Обработка предложений
        offers = []
        if 'price' in data and data['price']:
            offers.append(ProductOffer(
                price=float(data['price']),
                currency=data.get('currency', 'RUB'),
                availability=data.get('availability', 'InStock'),
                url=data.get('url')
            ))
        
        # Обработка отзывов
        reviews = []
        if 'reviews' in data:
            for review_data in data['reviews']:
                reviews.append(ProductReview(
                    rating=review_data['rating'],
                    review_body=review_data['review_body'],
                    author=review_data['author'],
                    date_published=review_data.get('date_published')
                ))
        
        return ProductSchema.generate(
            name=data['name'],
            description=data['description'],
            image=data.get('image'),
            brand=data.get('brand'),
            sku=data.get('sku'),
            offers=offers if offers else None,
            reviews=reviews if reviews else None,
            rating=data.get('rating'),
            **{k: v for k, v in data.items() if k not in [
                'name', 'description', 'image', 'brand', 'sku', 
                'price', 'currency', 'availability', 'reviews', 'rating'
            ]}
        )
    
    def _generate_breadcrumb_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует Breadcrumb схему"""
        if 'items' not in data:
            return {}
        
        breadcrumb_items = []
        for item in data['items']:
            breadcrumb_items.append(BreadcrumbItem(
                name=item['name'],
                url=item['url'],
                position=item['position']
            ))
        
        return BreadcrumbSchema.generate(breadcrumb_items)
    
    def _generate_article_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует Article схему"""
        required_fields = ['headline', 'author', 'date_published']
        for field in required_fields:
            if field not in data:
                return {}
        
        return ArticleSchema.generate(**data)
    
    def _generate_organization_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует Organization схему"""
        if 'name' not in data:
            return {}
        
        return OrganizationSchema.generate(**data)
    
    def inject_into_html(self, html: str, structured_data: Dict[str, Any]) -> str:
        """
        Внедряет JSON-LD структурированные данные в HTML
        
        Args:
            html: Исходный HTML
            structured_data: Структурированные данные для внедрения
            
        Returns:
            HTML с внедренными структурированными данными
        """
        if not structured_data:
            return html
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Находим или создаем head секцию
        head = soup.find('head')
        if not head:
            head = soup.new_tag('head')
            if soup.html:
                soup.html.insert(0, head)
            else:
                html_tag = soup.new_tag('html')
                html_tag.append(head)
                soup.append(html_tag)
        
        # Создаем script тег с JSON-LD
        script_tag = soup.new_tag('script', type='application/ld+json')
        script_tag.string = json.dumps(structured_data, ensure_ascii=False, indent=2)
        
        # Добавляем в head
        head.append(script_tag)
        
        return str(soup)
    
    def inject_multiple_schemas(self, html: str, schemas: List[Dict[str, Any]]) -> str:
        """
        Внедряет несколько схем в HTML
        
        Args:
            html: Исходный HTML
            schemas: Список структурированных данных
            
        Returns:
            HTML с внедренными структурированными данными
        """
        result_html = html
        
        for schema in schemas:
            if schema:
                result_html = self.inject_into_html(result_html, schema)
        
        return result_html
    
    async def auto_generate_for_content(
        self,
        html: str,
        content_type: str = "auto",
        include_schemas: Optional[List[str]] = None
    ) -> str:
        """
        Автоматически генерирует и внедряет подходящие схемы для контента
        
        Args:
            html: HTML контент
            content_type: Тип контента (auto, faq, product, article, etc.)
            include_schemas: Список схем для включения
            
        Returns:
            HTML с внедренными структурированными данными
        """
        if not self.ai_service:
            return html
        
        # Извлекаем текстовый контент из HTML
        soup = BeautifulSoup(html, 'html.parser')
        text_content = soup.get_text()
        
        schemas_to_generate = include_schemas or []
        
        # Автоматическое определение подходящих схем
        if content_type == "auto":
            schemas_to_generate = await self._detect_suitable_schemas(text_content)
        elif content_type in self.schemas:
            schemas_to_generate = [content_type]
        
        # Генерируем схемы
        generated_schemas = []
        for schema_type in schemas_to_generate:
            try:
                schema = await self.generate_structured_data(
                    schema_type=schema_type,
                    content=text_content,
                    auto_extract=True
                )
                if schema:
                    generated_schemas.append(schema)
            except Exception as e:
                print(f"Ошибка генерации схемы {schema_type}: {e}")
        
        # Внедряем схемы в HTML
        return self.inject_multiple_schemas(html, generated_schemas)
    
    async def _detect_suitable_schemas(self, content: str) -> List[str]:
        """
        Определяет подходящие схемы для контента с помощью AI
        
        Args:
            content: Текстовый контент
            
        Returns:
            Список подходящих типов схем
        """
        if not self.ai_service:
            return []
        
        prompt = f"""
Проанализируй следующий контент и определи, какие типы schema.org разметки будут наиболее подходящими.

Доступные типы:
- faq: для страниц с вопросами и ответами
- product: для страниц продуктов/товаров
- article: для статей и блог-постов
- organization: для страниц компаний/организаций
- breadcrumb: для навигационных цепочек

Верни ответ в формате JSON:
{{"schemas": ["type1", "type2"]}}

Контент:
{content[:1500]}...

Выбери максимум 3 наиболее подходящих типа.
"""
        
        try:
            response = await self.ai_service.chat_completion([
                {"role": "user", "content": prompt}
            ])
            
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return result.get('schemas', [])
            
            return []
        except Exception as e:
            print(f"Ошибка определения схем: {e}")
            return []
