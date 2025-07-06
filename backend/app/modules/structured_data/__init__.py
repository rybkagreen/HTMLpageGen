"""
Модуль для работы со структурированными данными schema.org
"""

from .generator import StructuredDataGenerator
from .schemas import FAQSchema, ProductSchema, BreadcrumbSchema

__all__ = [
    "StructuredDataGenerator",
    "FAQSchema", 
    "ProductSchema",
    "BreadcrumbSchema"
]
