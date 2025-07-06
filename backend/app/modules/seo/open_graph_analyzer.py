import re
from typing import Any, Dict, List, Optional
from bs4 import BeautifulSoup


class OpenGraphAnalyzer:
    """
    Анализатор Open Graph метатегов для социальных сетей
    """
    
    def __init__(self):
        # Обязательные Open Graph свойства
        self.required_og_properties = {
            "og:title": {
                "min_length": 30,
                "max_length": 60,
                "description": "Заголовок для социальных сетей"
            },
            "og:description": {
                "min_length": 120,
                "max_length": 300,
                "description": "Описание для социальных сетей"
            },
            "og:type": {
                "allowed_values": ["website", "article", "book", "profile", "music", "video"],
                "description": "Тип контента"
            },
            "og:url": {
                "pattern": r"^https?://[^\s]+$",
                "description": "Канонический URL страницы"
            },
            "og:image": {
                "pattern": r"^https?://[^\s]+\.(jpg|jpeg|png|gif|webp)$",
                "min_width": 1200,
                "min_height": 630,
                "description": "Изображение для превью"
            }
        }
        
        # Рекомендуемые Open Graph свойства
        self.recommended_og_properties = {
            "og:site_name": {
                "max_length": 40,
                "description": "Название сайта"
            },
            "og:locale": {
                "pattern": r"^[a-z]{2}_[A-Z]{2}$",
                "description": "Локаль контента"
            },
            "og:image:alt": {
                "max_length": 100,
                "description": "Alt текст для изображения"
            },
            "og:image:width": {
                "min_value": 1200,
                "description": "Ширина изображения"
            },
            "og:image:height": {
                "min_value": 630,
                "description": "Высота изображения"
            }
        }
        
        # Дополнительные свойства для статей
        self.article_properties = {
            "article:author": {"description": "Автор статьи"},
            "article:published_time": {
                "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z?$",
                "description": "Дата публикации"
            },
            "article:modified_time": {
                "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z?$",
                "description": "Дата изменения"
            },
            "article:section": {"description": "Раздел/категория статьи"},
            "article:tag": {"description": "Теги статьи"}
        }
    
    def analyze_open_graph(self, html: str) -> Dict[str, Any]:
        """
        Полный анализ Open Graph метатегов
        """
        soup = BeautifulSoup(html, "html.parser")
        
        # Находим все OG теги
        og_tags = soup.find_all("meta", attrs={"property": re.compile("^og:")})
        og_data = {}
        
        for tag in og_tags:
            property_name = tag.get("property")
            content = tag.get("content", "")
            og_data[property_name] = content
        
        # Анализируем обязательные свойства
        required_analysis = self._analyze_required_properties(og_data)
        
        # Анализируем рекомендуемые свойства
        recommended_analysis = self._analyze_recommended_properties(og_data)
        
        # Анализируем специфичные для статей свойства
        article_analysis = self._analyze_article_properties(og_data)
        
        # Проверяем изображения
        image_analysis = self._analyze_og_images(og_data)
        
        # Генерируем рекомендации
        recommendations = self._generate_og_recommendations(
            required_analysis, recommended_analysis, article_analysis, image_analysis
        )
        
        # Рассчитываем оценку
        score = self._calculate_og_score(
            required_analysis, recommended_analysis, article_analysis, image_analysis
        )
        
        return {
            "og_tags_found": og_data,
            "required_properties": required_analysis,
            "recommended_properties": recommended_analysis,
            "article_properties": article_analysis,
            "image_analysis": image_analysis,
            "recommendations": recommendations,
            "score": score,
            "total_tags": len(og_tags),
            "issues": self._collect_issues(
                required_analysis, recommended_analysis, article_analysis, image_analysis
            )
        }
    
    def _analyze_required_properties(self, og_data: Dict[str, str]) -> Dict[str, Any]:
        """Анализ обязательных Open Graph свойств"""
        analysis = {}
        
        for prop, config in self.required_og_properties.items():
            content = og_data.get(prop, "")
            prop_analysis = {
                "exists": bool(content),
                "content": content,
                "valid": True,
                "issues": []
            }
            
            if not content:
                prop_analysis["valid"] = False
                prop_analysis["issues"].append(f"Отсутствует обязательное свойство {prop}")
            else:
                # Проверяем длину
                if "min_length" in config and len(content) < config["min_length"]:
                    prop_analysis["valid"] = False
                    prop_analysis["issues"].append(
                        f"{prop} слишком короткое ({len(content)} символов, "
                        f"минимум {config['min_length']})"
                    )
                
                if "max_length" in config and len(content) > config["max_length"]:
                    prop_analysis["valid"] = False
                    prop_analysis["issues"].append(
                        f"{prop} слишком длинное ({len(content)} символов, "
                        f"максимум {config['max_length']})"
                    )
                
                # Проверяем паттерн
                if "pattern" in config and not re.match(config["pattern"], content):
                    prop_analysis["valid"] = False
                    prop_analysis["issues"].append(f"{prop} не соответствует формату")
                
                # Проверяем допустимые значения
                if "allowed_values" in config and content not in config["allowed_values"]:
                    prop_analysis["valid"] = False
                    prop_analysis["issues"].append(
                        f"{prop} должно быть одним из: {', '.join(config['allowed_values'])}"
                    )
            
            analysis[prop] = prop_analysis
        
        return analysis
    
    def _analyze_recommended_properties(self, og_data: Dict[str, str]) -> Dict[str, Any]:
        """Анализ рекомендуемых Open Graph свойств"""
        analysis = {}
        
        for prop, config in self.recommended_og_properties.items():
            content = og_data.get(prop, "")
            prop_analysis = {
                "exists": bool(content),
                "content": content,
                "valid": True,
                "issues": []
            }
            
            if content:
                # Проверяем длину
                if "max_length" in config and len(content) > config["max_length"]:
                    prop_analysis["valid"] = False
                    prop_analysis["issues"].append(
                        f"{prop} слишком длинное ({len(content)} символов, "
                        f"максимум {config['max_length']})"
                    )
                
                # Проверяем паттерн
                if "pattern" in config and not re.match(config["pattern"], content):
                    prop_analysis["valid"] = False
                    prop_analysis["issues"].append(f"{prop} не соответствует формату")
                
                # Проверяем минимальные значения
                if "min_value" in config:
                    try:
                        value = int(content)
                        if value < config["min_value"]:
                            prop_analysis["valid"] = False
                            prop_analysis["issues"].append(
                                f"{prop} слишком маленькое ({value}, "
                                f"минимум {config['min_value']})"
                            )
                    except ValueError:
                        prop_analysis["valid"] = False
                        prop_analysis["issues"].append(f"{prop} должно быть числом")
            
            analysis[prop] = prop_analysis
        
        return analysis
    
    def _analyze_article_properties(self, og_data: Dict[str, str]) -> Dict[str, Any]:
        """Анализ свойств для статей"""
        analysis = {}
        og_type = og_data.get("og:type", "")
        
        # Проверяем только если тип контента - article
        if og_type == "article":
            for prop, config in self.article_properties.items():
                content = og_data.get(prop, "")
                prop_analysis = {
                    "exists": bool(content),
                    "content": content,
                    "valid": True,
                    "issues": []
                }
                
                if content and "pattern" in config:
                    if not re.match(config["pattern"], content):
                        prop_analysis["valid"] = False
                        prop_analysis["issues"].append(f"{prop} не соответствует формату")
                
                analysis[prop] = prop_analysis
        
        return analysis
    
    def _analyze_og_images(self, og_data: Dict[str, str]) -> Dict[str, Any]:
        """Анализ Open Graph изображений"""
        image_url = og_data.get("og:image", "")
        image_alt = og_data.get("og:image:alt", "")
        image_width = og_data.get("og:image:width", "")
        image_height = og_data.get("og:image:height", "")
        
        analysis = {
            "has_image": bool(image_url),
            "has_alt": bool(image_alt),
            "has_dimensions": bool(image_width and image_height),
            "valid_url": False,
            "valid_dimensions": False,
            "issues": []
        }
        
        if image_url:
            # Проверяем URL изображения
            if re.match(r"^https?://[^\s]+\.(jpg|jpeg|png|gif|webp)$", image_url, re.IGNORECASE):
                analysis["valid_url"] = True
            else:
                analysis["issues"].append("Неверный формат URL изображения")
            
            # Проверяем размеры
            if image_width and image_height:
                try:
                    width = int(image_width)
                    height = int(image_height)
                    
                    if width >= 1200 and height >= 630:
                        analysis["valid_dimensions"] = True
                    else:
                        analysis["issues"].append(
                            f"Размеры изображения слишком малы ({width}x{height}, "
                            "рекомендуется минимум 1200x630)"
                        )
                except ValueError:
                    analysis["issues"].append("Неверный формат размеров изображения")
            else:
                analysis["issues"].append("Не указаны размеры изображения")
            
            # Проверяем alt текст
            if not image_alt:
                analysis["issues"].append("Отсутствует альтернативный текст для изображения")
        else:
            analysis["issues"].append("Отсутствует изображение для Open Graph")
        
        return analysis
    
    def _generate_og_recommendations(
        self, 
        required: Dict, 
        recommended: Dict, 
        article: Dict,
        image: Dict
    ) -> List[Dict[str, Any]]:
        """Генерация рекомендаций по Open Graph"""
        recommendations = []
        
        # Рекомендации по обязательным свойствам
        for prop, analysis in required.items():
            if not analysis["exists"]:
                recommendations.append({
                    "type": "critical",
                    "category": "open_graph",
                    "property": prop,
                    "issue": f"Отсутствует обязательное свойство {prop}",
                    "recommendation": f"Добавьте {prop} с {self.required_og_properties[prop]['description'].lower()}",
                    "example": self._get_property_example(prop),
                    "impact": "high"
                })
            elif not analysis["valid"]:
                for issue in analysis["issues"]:
                    recommendations.append({
                        "type": "warning",
                        "category": "open_graph",
                        "property": prop,
                        "issue": issue,
                        "recommendation": f"Исправьте {prop}",
                        "example": self._get_property_example(prop),
                        "impact": "medium"
                    })
        
        # Рекомендации по рекомендуемым свойствам
        for prop, analysis in recommended.items():
            if not analysis["exists"]:
                recommendations.append({
                    "type": "suggestion",
                    "category": "open_graph",
                    "property": prop,
                    "issue": f"Рекомендуется добавить {prop}",
                    "recommendation": f"Добавьте {prop} для улучшения отображения в социальных сетях",
                    "example": self._get_property_example(prop),
                    "impact": "low"
                })
        
        # Рекомендации по изображению
        if not image["has_image"]:
            recommendations.append({
                "type": "critical",
                "category": "open_graph",
                "property": "og:image",
                "issue": "Отсутствует изображение для Open Graph",
                "recommendation": "Добавьте привлекательное изображение размером минимум 1200x630px",
                "example": '<meta property="og:image" content="https://example.com/image.jpg">',
                "impact": "high"
            })
        
        return recommendations
    
    def _get_property_example(self, property_name: str) -> str:
        """Получение примера для свойства"""
        examples = {
            "og:title": '<meta property="og:title" content="Заголовок страницы">',
            "og:description": '<meta property="og:description" content="Описание страницы для социальных сетей">',
            "og:type": '<meta property="og:type" content="website">',
            "og:url": '<meta property="og:url" content="https://example.com/page">',
            "og:image": '<meta property="og:image" content="https://example.com/image.jpg">',
            "og:site_name": '<meta property="og:site_name" content="Название сайта">',
            "og:locale": '<meta property="og:locale" content="ru_RU">',
            "og:image:alt": '<meta property="og:image:alt" content="Описание изображения">',
            "og:image:width": '<meta property="og:image:width" content="1200">',
            "og:image:height": '<meta property="og:image:height" content="630">',
        }
        
        return examples.get(property_name, f'<meta property="{property_name}" content="...">')
    
    def _calculate_og_score(
        self, 
        required: Dict, 
        recommended: Dict, 
        article: Dict,
        image: Dict
    ) -> int:
        """Расчет оценки Open Graph"""
        score = 100
        
        # Штрафы за отсутствующие обязательные свойства
        for prop, analysis in required.items():
            if not analysis["exists"]:
                score -= 20
            elif not analysis["valid"]:
                score -= 10
        
        # Штрафы за проблемы с изображением
        if not image["has_image"]:
            score -= 15
        elif not image["valid_url"]:
            score -= 10
        elif not image["valid_dimensions"]:
            score -= 5
        
        # Бонусы за рекомендуемые свойства
        existing_recommended = sum(1 for analysis in recommended.values() if analysis["exists"])
        score += min(10, existing_recommended * 2)
        
        return max(0, min(100, score))
    
    def _collect_issues(
        self, 
        required: Dict, 
        recommended: Dict, 
        article: Dict,
        image: Dict
    ) -> List[str]:
        """Сбор всех найденных проблем"""
        issues = []
        
        # Проблемы с обязательными свойствами
        for analysis in required.values():
            issues.extend(analysis["issues"])
        
        # Проблемы с рекомендуемыми свойствами
        for analysis in recommended.values():
            issues.extend(analysis["issues"])
        
        # Проблемы со статьями
        for analysis in article.values():
            issues.extend(analysis["issues"])
        
        # Проблемы с изображениями
        issues.extend(image["issues"])
        
        return issues
    
    def generate_og_tags(self, content_data: Dict[str, Any]) -> List[str]:
        """
        Генерация Open Graph тегов на основе данных контента
        """
        tags = []
        
        # Обязательные теги
        if content_data.get("title"):
            tags.append(f'<meta property="og:title" content="{content_data["title"]}">')
        
        if content_data.get("description"):
            tags.append(f'<meta property="og:description" content="{content_data["description"]}">')
        
        og_type = content_data.get("type", "website")
        tags.append(f'<meta property="og:type" content="{og_type}">')
        
        if content_data.get("url"):
            tags.append(f'<meta property="og:url" content="{content_data["url"]}">')
        
        if content_data.get("image"):
            tags.append(f'<meta property="og:image" content="{content_data["image"]}">')
            
            # Дополнительные теги для изображения
            if content_data.get("image_alt"):
                tags.append(f'<meta property="og:image:alt" content="{content_data["image_alt"]}">')
            
            if content_data.get("image_width"):
                tags.append(f'<meta property="og:image:width" content="{content_data["image_width"]}">')
            
            if content_data.get("image_height"):
                tags.append(f'<meta property="og:image:height" content="{content_data["image_height"]}">')
        
        # Рекомендуемые теги
        if content_data.get("site_name"):
            tags.append(f'<meta property="og:site_name" content="{content_data["site_name"]}">')
        
        if content_data.get("locale"):
            tags.append(f'<meta property="og:locale" content="{content_data["locale"]}">')
        
        # Теги для статей
        if og_type == "article":
            if content_data.get("author"):
                tags.append(f'<meta property="article:author" content="{content_data["author"]}">')
            
            if content_data.get("published_time"):
                tags.append(f'<meta property="article:published_time" content="{content_data["published_time"]}">')
            
            if content_data.get("modified_time"):
                tags.append(f'<meta property="article:modified_time" content="{content_data["modified_time"]}">')
            
            if content_data.get("section"):
                tags.append(f'<meta property="article:section" content="{content_data["section"]}">')
            
            if content_data.get("tags"):
                for tag in content_data["tags"]:
                    tags.append(f'<meta property="article:tag" content="{tag}">')
        
        return tags
