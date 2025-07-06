"""
Схемы для различных типов структурированных данных schema.org
"""

import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel


class FAQItem(BaseModel):
    """Элемент FAQ"""
    question: str
    answer: str


class FAQSchema:
    """Генератор schema.org разметки для FAQ страниц"""
    
    @staticmethod
    def generate(faq_items: List[FAQItem], **kwargs) -> Dict[str, Any]:
        """
        Генерирует JSON-LD разметку для FAQ
        
        Args:
            faq_items: Список вопросов и ответов
            **kwargs: Дополнительные параметры
            
        Returns:
            Словарь с JSON-LD разметкой
        """
        main_entities = []
        
        for item in faq_items:
            main_entities.append({
                "@type": "Question",
                "name": item.question,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item.answer
                }
            })
        
        schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": main_entities
        }
        
        # Добавляем дополнительные поля если предоставлены
        if "name" in kwargs:
            schema["name"] = kwargs["name"]
        if "description" in kwargs:
            schema["description"] = kwargs["description"]
        if "url" in kwargs:
            schema["url"] = kwargs["url"]
            
        return schema


class ProductOffer(BaseModel):
    """Предложение продукта"""
    price: float
    currency: str = "RUB"
    availability: str = "InStock"  # InStock, OutOfStock, PreOrder
    url: Optional[str] = None


class ProductReview(BaseModel):
    """Отзыв о продукте"""
    rating: float  # 1-5
    review_body: str
    author: str
    date_published: Optional[str] = None


class ProductSchema:
    """Генератор schema.org разметки для продуктов"""
    
    @staticmethod
    def generate(
        name: str,
        description: str,
        image: Optional[str] = None,
        brand: Optional[str] = None,
        sku: Optional[str] = None,
        offers: Optional[List[ProductOffer]] = None,
        reviews: Optional[List[ProductReview]] = None,
        rating: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Генерирует JSON-LD разметку для продукта
        
        Args:
            name: Название продукта
            description: Описание продукта
            image: URL изображения
            brand: Бренд
            sku: Артикул
            offers: Список предложений
            reviews: Список отзывов
            rating: Общий рейтинг
            **kwargs: Дополнительные параметры
            
        Returns:
            Словарь с JSON-LD разметкой
        """
        schema = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": name,
            "description": description
        }
        
        if image:
            schema["image"] = image
            
        if brand:
            schema["brand"] = {
                "@type": "Brand",
                "name": brand
            }
            
        if sku:
            schema["sku"] = sku
            
        if offers:
            schema_offers = []
            for offer in offers:
                offer_schema = {
                    "@type": "Offer",
                    "price": str(offer.price),
                    "priceCurrency": offer.currency,
                    "availability": f"https://schema.org/{offer.availability}"
                }
                if offer.url:
                    offer_schema["url"] = offer.url
                schema_offers.append(offer_schema)
            
            if len(schema_offers) == 1:
                schema["offers"] = schema_offers[0]
            else:
                schema["offers"] = schema_offers
                
        if reviews:
            schema_reviews = []
            for review in reviews:
                review_schema = {
                    "@type": "Review",
                    "reviewRating": {
                        "@type": "Rating",
                        "ratingValue": str(review.rating),
                        "bestRating": "5"
                    },
                    "reviewBody": review.review_body,
                    "author": {
                        "@type": "Person",
                        "name": review.author
                    }
                }
                if review.date_published:
                    review_schema["datePublished"] = review.date_published
                schema_reviews.append(review_schema)
            
            schema["review"] = schema_reviews
            
        if rating or reviews:
            # Вычисляем средний рейтинг если не предоставлен
            if not rating and reviews:
                rating = sum(r.rating for r in reviews) / len(reviews)
                
            if rating:
                schema["aggregateRating"] = {
                    "@type": "AggregateRating",
                    "ratingValue": str(round(rating, 1)),
                    "bestRating": "5",
                    "reviewCount": str(len(reviews) if reviews else 1)
                }
        
        # Добавляем дополнительные поля
        if "url" in kwargs:
            schema["url"] = kwargs["url"]
        if "category" in kwargs:
            schema["category"] = kwargs["category"]
        if "manufacturer" in kwargs:
            schema["manufacturer"] = {
                "@type": "Organization",
                "name": kwargs["manufacturer"]
            }
            
        return schema


class BreadcrumbItem(BaseModel):
    """Элемент хлебных крошек"""
    name: str
    url: str
    position: int


class BreadcrumbSchema:
    """Генератор schema.org разметки для хлебных крошек"""
    
    @staticmethod
    def generate(items: List[BreadcrumbItem], **kwargs) -> Dict[str, Any]:
        """
        Генерирует JSON-LD разметку для хлебных крошек
        
        Args:
            items: Список элементов навигации
            **kwargs: Дополнительные параметры
            
        Returns:
            Словарь с JSON-LD разметкой
        """
        # Сортируем по позиции
        sorted_items = sorted(items, key=lambda x: x.position)
        
        list_elements = []
        for item in sorted_items:
            list_elements.append({
                "@type": "ListItem",
                "position": item.position,
                "name": item.name,
                "item": item.url
            })
        
        schema = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": list_elements
        }
        
        return schema


class ArticleSchema:
    """Генератор schema.org разметки для статей"""
    
    @staticmethod
    def generate(
        headline: str,
        author: str,
        date_published: str,
        date_modified: Optional[str] = None,
        description: Optional[str] = None,
        image: Optional[str] = None,
        url: Optional[str] = None,
        publisher_name: Optional[str] = None,
        publisher_logo: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Генерирует JSON-LD разметку для статьи
        
        Args:
            headline: Заголовок статьи
            author: Автор
            date_published: Дата публикации (ISO format)
            date_modified: Дата изменения (ISO format)
            description: Описание статьи
            image: URL изображения
            url: URL статьи
            publisher_name: Название издателя
            publisher_logo: Логотип издателя
            **kwargs: Дополнительные параметры
            
        Returns:
            Словарь с JSON-LD разметкой
        """
        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": headline,
            "author": {
                "@type": "Person",
                "name": author
            },
            "datePublished": date_published
        }
        
        if date_modified:
            schema["dateModified"] = date_modified
        else:
            schema["dateModified"] = date_published
            
        if description:
            schema["description"] = description
            
        if image:
            schema["image"] = image
            
        if url:
            schema["url"] = url
            
        if publisher_name:
            publisher = {
                "@type": "Organization", 
                "name": publisher_name
            }
            if publisher_logo:
                publisher["logo"] = {
                    "@type": "ImageObject",
                    "url": publisher_logo
                }
            schema["publisher"] = publisher
            
        return schema


class OrganizationSchema:
    """Генератор schema.org разметки для организаций"""
    
    @staticmethod
    def generate(
        name: str,
        url: Optional[str] = None,
        logo: Optional[str] = None,
        description: Optional[str] = None,
        address: Optional[Dict[str, str]] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        social_media: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Генерирует JSON-LD разметку для организации
        
        Args:
            name: Название организации
            url: Веб-сайт
            logo: URL логотипа
            description: Описание
            address: Адрес (dictionary с ключами: street, city, region, postal_code, country)
            phone: Телефон
            email: Email
            social_media: Список URL социальных сетей
            **kwargs: Дополнительные параметры
            
        Returns:
            Словарь с JSON-LD разметкой
        """
        schema = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": name
        }
        
        if url:
            schema["url"] = url
            
        if logo:
            schema["logo"] = logo
            
        if description:
            schema["description"] = description
            
        if address:
            schema["address"] = {
                "@type": "PostalAddress",
                "streetAddress": address.get("street", ""),
                "addressLocality": address.get("city", ""),
                "addressRegion": address.get("region", ""),
                "postalCode": address.get("postal_code", ""),
                "addressCountry": address.get("country", "")
            }
            
        if phone:
            schema["telephone"] = phone
            
        if email:
            schema["email"] = email
            
        if social_media:
            schema["sameAs"] = social_media
            
        return schema
