import re
from typing import Any, Dict, List, Optional
from bs4 import BeautifulSoup


class TwitterCardsAnalyzer:
    """
    Анализатор Twitter Cards метатегов для оптимизации в Twitter
    """
    
    def __init__(self):
        # Типы Twitter карточек
        self.card_types = {
            "summary": {
                "description": "Стандартная карточка с изображением и текстом",
                "required_fields": ["twitter:card", "twitter:title", "twitter:description"],
                "optional_fields": ["twitter:image", "twitter:site", "twitter:creator"],
                "image_min_size": "120x120",
                "image_max_size": "1024x512"
            },
            "summary_large_image": {
                "description": "Карточка с большим изображением",
                "required_fields": ["twitter:card", "twitter:title", "twitter:description", "twitter:image"],
                "optional_fields": ["twitter:site", "twitter:creator", "twitter:image:alt"],
                "image_min_size": "300x157",
                "image_max_size": "4096x4096"
            },
            "app": {
                "description": "Карточка для мобильного приложения",
                "required_fields": ["twitter:card", "twitter:description", "twitter:app:id:iphone", "twitter:app:id:googleplay"],
                "optional_fields": ["twitter:app:name:iphone", "twitter:app:name:googleplay", "twitter:app:url:iphone", "twitter:app:url:googleplay"],
                "image_min_size": "120x120",
                "image_max_size": "1024x512"
            },
            "player": {
                "description": "Карточка для видео/аудио контента",
                "required_fields": ["twitter:card", "twitter:title", "twitter:description", "twitter:player", "twitter:player:width", "twitter:player:height"],
                "optional_fields": ["twitter:image", "twitter:player:stream"],
                "image_min_size": "120x120",
                "image_max_size": "1024x512"
            }
        }
        
        # Валидация полей
        self.field_validations = {
            "twitter:card": {
                "allowed_values": ["summary", "summary_large_image", "app", "player"],
                "description": "Тип Twitter карточки"
            },
            "twitter:title": {
                "max_length": 70,
                "description": "Заголовок карточки"
            },
            "twitter:description": {
                "max_length": 200,
                "description": "Описание карточки"
            },
            "twitter:image": {
                "pattern": r"^https?://[^\s]+\.(jpg|jpeg|png|gif|webp)$",
                "max_size_mb": 5,
                "description": "URL изображения"
            },
            "twitter:image:alt": {
                "max_length": 420,
                "description": "Альтернативный текст для изображения"
            },
            "twitter:site": {
                "pattern": r"^@[a-zA-Z0-9_]{1,15}$",
                "description": "Twitter аккаунт сайта (@username)"
            },
            "twitter:creator": {
                "pattern": r"^@[a-zA-Z0-9_]{1,15}$",
                "description": "Twitter аккаунт автора (@username)"
            },
            "twitter:player": {
                "pattern": r"^https://[^\s]+$",
                "description": "URL HTTPS-плеера"
            },
            "twitter:player:width": {
                "min_value": 280,
                "max_value": 1024,
                "description": "Ширина плеера в пикселях"
            },
            "twitter:player:height": {
                "min_value": 150,
                "max_value": 1024,
                "description": "Высота плеера в пикселях"
            }
        }
    
    def analyze_twitter_cards(self, html: str) -> Dict[str, Any]:
        """
        Полный анализ Twitter Cards метатегов
        """
        soup = BeautifulSoup(html, "html.parser")
        
        # Находим все Twitter метатеги
        twitter_tags = soup.find_all("meta", attrs={"name": re.compile("^twitter:")})
        twitter_data = {}
        
        for tag in twitter_tags:
            name = tag.get("name")
            content = tag.get("content", "")
            twitter_data[name] = content
        
        # Определяем тип карточки
        card_type = twitter_data.get("twitter:card", "")
        
        # Анализируем обязательные поля
        required_analysis = self._analyze_required_fields(twitter_data, card_type)
        
        # Анализируем дополнительные поля
        optional_analysis = self._analyze_optional_fields(twitter_data, card_type)
        
        # Проверяем изображения
        image_analysis = self._analyze_twitter_images(twitter_data, card_type)
        
        # Анализируем плеер (для карточки player)
        player_analysis = self._analyze_player_fields(twitter_data, card_type)
        
        # Проверяем совместимость с Open Graph
        og_compatibility = self._check_og_compatibility(soup, twitter_data)
        
        # Генерируем рекомендации
        recommendations = self._generate_twitter_recommendations(
            required_analysis, optional_analysis, image_analysis, 
            player_analysis, og_compatibility, card_type
        )
        
        # Рассчитываем оценку
        score = self._calculate_twitter_score(
            required_analysis, optional_analysis, image_analysis, 
            player_analysis, card_type
        )
        
        return {
            "twitter_tags_found": twitter_data,
            "card_type": card_type,
            "required_fields": required_analysis,
            "optional_fields": optional_analysis,
            "image_analysis": image_analysis,
            "player_analysis": player_analysis,
            "og_compatibility": og_compatibility,
            "recommendations": recommendations,
            "score": score,
            "total_tags": len(twitter_tags),
            "issues": self._collect_twitter_issues(
                required_analysis, optional_analysis, image_analysis, player_analysis
            )
        }
    
    def _analyze_required_fields(self, twitter_data: Dict[str, str], card_type: str) -> Dict[str, Any]:
        """Анализ обязательных полей для конкретного типа карточки"""
        analysis = {}
        
        if not card_type or card_type not in self.card_types:
            return {"error": "Неопределен или неверный тип карточки"}
        
        required_fields = self.card_types[card_type]["required_fields"]
        
        for field in required_fields:
            content = twitter_data.get(field, "")
            field_analysis = {
                "exists": bool(content),
                "content": content,
                "valid": True,
                "issues": []
            }
            
            if not content:
                field_analysis["valid"] = False
                field_analysis["issues"].append(f"Отсутствует обязательное поле {field}")
            else:
                # Валидируем контент
                field_analysis = self._validate_field_content(field, content, field_analysis)
            
            analysis[field] = field_analysis
        
        return analysis
    
    def _analyze_optional_fields(self, twitter_data: Dict[str, str], card_type: str) -> Dict[str, Any]:
        """Анализ дополнительных полей"""
        analysis = {}
        
        if not card_type or card_type not in self.card_types:
            return {}
        
        optional_fields = self.card_types[card_type]["optional_fields"]
        
        for field in optional_fields:
            content = twitter_data.get(field, "")
            field_analysis = {
                "exists": bool(content),
                "content": content,
                "valid": True,
                "issues": []
            }
            
            if content:
                field_analysis = self._validate_field_content(field, content, field_analysis)
            
            analysis[field] = field_analysis
        
        return analysis
    
    def _validate_field_content(self, field: str, content: str, analysis: Dict) -> Dict:
        """Валидация содержимого поля"""
        if field not in self.field_validations:
            return analysis
        
        validation = self.field_validations[field]
        
        # Проверка длины
        if "max_length" in validation and len(content) > validation["max_length"]:
            analysis["valid"] = False
            analysis["issues"].append(
                f"{field} превышает максимальную длину "
                f"({len(content)} > {validation['max_length']} символов)"
            )
        
        # Проверка паттерна
        if "pattern" in validation and not re.match(validation["pattern"], content, re.IGNORECASE):
            analysis["valid"] = False
            analysis["issues"].append(f"{field} не соответствует требуемому формату")
        
        # Проверка допустимых значений
        if "allowed_values" in validation and content not in validation["allowed_values"]:
            analysis["valid"] = False
            analysis["issues"].append(
                f"{field} должно быть одним из: {', '.join(validation['allowed_values'])}"
            )
        
        # Проверка числовых значений
        if "min_value" in validation or "max_value" in validation:
            try:
                value = int(content)
                if "min_value" in validation and value < validation["min_value"]:
                    analysis["valid"] = False
                    analysis["issues"].append(
                        f"{field} слишком маленькое ({value} < {validation['min_value']})"
                    )
                if "max_value" in validation and value > validation["max_value"]:
                    analysis["valid"] = False
                    analysis["issues"].append(
                        f"{field} слишком большое ({value} > {validation['max_value']})"
                    )
            except ValueError:
                analysis["valid"] = False
                analysis["issues"].append(f"{field} должно быть числом")
        
        return analysis
    
    def _analyze_twitter_images(self, twitter_data: Dict[str, str], card_type: str) -> Dict[str, Any]:
        """Анализ изображений для Twitter карточек"""
        image_url = twitter_data.get("twitter:image", "")
        image_alt = twitter_data.get("twitter:image:alt", "")
        
        analysis = {
            "has_image": bool(image_url),
            "has_alt": bool(image_alt),
            "valid_url": False,
            "suitable_for_card_type": False,
            "issues": []
        }
        
        if not image_url and card_type == "summary_large_image":
            analysis["issues"].append("Изображение обязательно для карточки summary_large_image")
            return analysis
        
        if image_url:
            # Проверка URL
            if re.match(r"^https?://[^\s]+\.(jpg|jpeg|png|gif|webp)$", image_url, re.IGNORECASE):
                analysis["valid_url"] = True
            else:
                analysis["issues"].append("Неверный формат URL изображения")
            
            # Проверка соответствия типу карточки
            if card_type in self.card_types:
                card_config = self.card_types[card_type]
                analysis["recommended_size"] = f"{card_config['image_min_size']} - {card_config['image_max_size']}"
                analysis["suitable_for_card_type"] = True
            
            # Проверка alt текста
            if not image_alt:
                analysis["issues"].append("Рекомендуется добавить альтернативный текст для изображения")
            elif len(image_alt) > 420:
                analysis["issues"].append(f"Alt текст слишком длинный ({len(image_alt)} > 420 символов)")
        
        return analysis
    
    def _analyze_player_fields(self, twitter_data: Dict[str, str], card_type: str) -> Dict[str, Any]:
        """Анализ полей плеера для карточки типа player"""
        analysis = {}
        
        if card_type != "player":
            return analysis
        
        player_url = twitter_data.get("twitter:player", "")
        player_width = twitter_data.get("twitter:player:width", "")
        player_height = twitter_data.get("twitter:player:height", "")
        player_stream = twitter_data.get("twitter:player:stream", "")
        
        analysis = {
            "has_player": bool(player_url),
            "has_dimensions": bool(player_width and player_height),
            "has_stream": bool(player_stream),
            "valid_player_url": False,
            "valid_dimensions": False,
            "issues": []
        }
        
        # Проверка URL плеера
        if player_url:
            if player_url.startswith("https://"):
                analysis["valid_player_url"] = True
            else:
                analysis["issues"].append("URL плеера должен использовать HTTPS")
        else:
            analysis["issues"].append("Отсутствует обязательный URL плеера")
        
        # Проверка размеров
        if player_width and player_height:
            try:
                width = int(player_width)
                height = int(player_height)
                
                if 280 <= width <= 1024 and 150 <= height <= 1024:
                    analysis["valid_dimensions"] = True
                else:
                    analysis["issues"].append(
                        f"Размеры плеера вне допустимого диапазона "
                        f"({width}x{height}, допустимо: 280-1024 x 150-1024)"
                    )
            except ValueError:
                analysis["issues"].append("Неверный формат размеров плеера")
        else:
            analysis["issues"].append("Отсутствуют обязательные размеры плеера")
        
        return analysis
    
    def _check_og_compatibility(self, soup: BeautifulSoup, twitter_data: Dict[str, str]) -> Dict[str, Any]:
        """Проверка совместимости с Open Graph тегами"""
        og_tags = soup.find_all("meta", attrs={"property": re.compile("^og:")})
        og_data = {tag.get("property"): tag.get("content", "") for tag in og_tags}
        
        compatibility = {
            "has_og_tags": len(og_tags) > 0,
            "fallback_available": {},
            "conflicts": [],
            "recommendations": []
        }
        
        # Проверяем наличие fallback значений
        fallback_mapping = {
            "twitter:title": "og:title",
            "twitter:description": "og:description",
            "twitter:image": "og:image",
            "twitter:url": "og:url"
        }
        
        for twitter_field, og_field in fallback_mapping.items():
            twitter_value = twitter_data.get(twitter_field, "")
            og_value = og_data.get(og_field, "")
            
            compatibility["fallback_available"][twitter_field] = {
                "twitter_exists": bool(twitter_value),
                "og_exists": bool(og_value),
                "can_fallback": bool(og_value) and not bool(twitter_value)
            }
            
            # Проверяем конфликты
            if twitter_value and og_value and twitter_value != og_value:
                compatibility["conflicts"].append({
                    "field": twitter_field,
                    "twitter_value": twitter_value,
                    "og_value": og_value
                })
        
        # Генерируем рекомендации
        if not compatibility["has_og_tags"]:
            compatibility["recommendations"].append(
                "Рекомендуется добавить Open Graph теги для лучшей совместимости"
            )
        
        if compatibility["conflicts"]:
            compatibility["recommendations"].append(
                "Обнаружены конфликты между Twitter Cards и Open Graph тегами"
            )
        
        return compatibility
    
    def _generate_twitter_recommendations(
        self, 
        required: Dict, 
        optional: Dict, 
        image: Dict,
        player: Dict,
        og_compatibility: Dict,
        card_type: str
    ) -> List[Dict[str, Any]]:
        """Генерация рекомендаций по Twitter Cards"""
        recommendations = []
        
        # Рекомендации по обязательным полям
        if "error" in required:
            recommendations.append({
                "type": "critical",
                "category": "twitter_cards",
                "field": "twitter:card",
                "issue": "Неопределен тип карточки",
                "recommendation": "Добавьте метатег twitter:card с одним из допустимых значений",
                "example": '<meta name="twitter:card" content="summary_large_image">',
                "impact": "high"
            })
        else:
            for field, analysis in required.items():
                if not analysis["exists"]:
                    recommendations.append({
                        "type": "critical",
                        "category": "twitter_cards",
                        "field": field,
                        "issue": f"Отсутствует обязательное поле {field}",
                        "recommendation": f"Добавьте {field}",
                        "example": self._get_field_example(field),
                        "impact": "high"
                    })
                elif not analysis["valid"]:
                    for issue in analysis["issues"]:
                        recommendations.append({
                            "type": "warning",
                            "category": "twitter_cards",
                            "field": field,
                            "issue": issue,
                            "recommendation": f"Исправьте {field}",
                            "example": self._get_field_example(field),
                            "impact": "medium"
                        })
        
        # Рекомендации по дополнительным полям
        for field, analysis in optional.items():
            if not analysis["exists"]:
                recommendations.append({
                    "type": "suggestion",
                    "category": "twitter_cards",
                    "field": field,
                    "issue": f"Рекомендуется добавить {field}",
                    "recommendation": f"Добавьте {field} для улучшения отображения",
                    "example": self._get_field_example(field),
                    "impact": "low"
                })
        
        # Рекомендации по изображениям
        for issue in image.get("issues", []):
            recommendations.append({
                "type": "warning",
                "category": "twitter_cards",
                "field": "twitter:image",
                "issue": issue,
                "recommendation": "Исправьте проблемы с изображением",
                "impact": "medium"
            })
        
        # Рекомендации по плееру
        for issue in player.get("issues", []):
            recommendations.append({
                "type": "warning",
                "category": "twitter_cards",
                "field": "twitter:player",
                "issue": issue,
                "recommendation": "Исправьте настройки плеера",
                "impact": "medium"
            })
        
        # Рекомендации по совместимости с OG
        for rec in og_compatibility.get("recommendations", []):
            recommendations.append({
                "type": "suggestion",
                "category": "twitter_cards",
                "field": "compatibility",
                "issue": rec,
                "recommendation": "Убедитесь в совместимости Twitter Cards и Open Graph",
                "impact": "low"
            })
        
        return recommendations
    
    def _get_field_example(self, field_name: str) -> str:
        """Получение примера для поля"""
        examples = {
            "twitter:card": '<meta name="twitter:card" content="summary_large_image">',
            "twitter:title": '<meta name="twitter:title" content="Заголовок страницы">',
            "twitter:description": '<meta name="twitter:description" content="Описание страницы">',
            "twitter:image": '<meta name="twitter:image" content="https://example.com/image.jpg">',
            "twitter:image:alt": '<meta name="twitter:image:alt" content="Описание изображения">',
            "twitter:site": '<meta name="twitter:site" content="@username">',
            "twitter:creator": '<meta name="twitter:creator" content="@author">',
            "twitter:player": '<meta name="twitter:player" content="https://example.com/player.html">',
            "twitter:player:width": '<meta name="twitter:player:width" content="1024">',
            "twitter:player:height": '<meta name="twitter:player:height" content="512">',
        }
        
        return examples.get(field_name, f'<meta name="{field_name}" content="...">')
    
    def _calculate_twitter_score(
        self, 
        required: Dict, 
        optional: Dict, 
        image: Dict,
        player: Dict,
        card_type: str
    ) -> int:
        """Расчет оценки Twitter Cards"""
        if "error" in required:
            return 0
        
        score = 100
        
        # Штрафы за отсутствующие обязательные поля
        for analysis in required.values():
            if not analysis["exists"]:
                score -= 25
            elif not analysis["valid"]:
                score -= 15
        
        # Штрафы за проблемы с изображением
        if card_type == "summary_large_image" and not image["has_image"]:
            score -= 20
        elif image["issues"]:
            score -= 5 * len(image["issues"])
        
        # Штрафы за проблемы с плеером
        if card_type == "player" and player["issues"]:
            score -= 10 * len(player["issues"])
        
        # Бонусы за дополнительные поля
        existing_optional = sum(1 for analysis in optional.values() if analysis["exists"])
        score += min(15, existing_optional * 3)
        
        return max(0, min(100, score))
    
    def _collect_twitter_issues(
        self, 
        required: Dict, 
        optional: Dict, 
        image: Dict,
        player: Dict
    ) -> List[str]:
        """Сбор всех найденных проблем"""
        issues = []
        
        # Проблемы с обязательными полями
        if "error" in required:
            issues.append(required["error"])
        else:
            for analysis in required.values():
                issues.extend(analysis.get("issues", []))
        
        # Проблемы с дополнительными полями
        for analysis in optional.values():
            issues.extend(analysis.get("issues", []))
        
        # Проблемы с изображениями
        issues.extend(image.get("issues", []))
        
        # Проблемы с плеером
        issues.extend(player.get("issues", []))
        
        return issues
    
    def generate_twitter_tags(self, content_data: Dict[str, Any]) -> List[str]:
        """
        Генерация Twitter Cards тегов на основе данных контента
        """
        tags = []
        
        # Определяем тип карточки
        card_type = content_data.get("twitter_card_type", "summary_large_image")
        tags.append(f'<meta name="twitter:card" content="{card_type}">')
        
        # Обязательные теги
        if content_data.get("title"):
            tags.append(f'<meta name="twitter:title" content="{content_data["title"]}">')
        
        if content_data.get("description"):
            tags.append(f'<meta name="twitter:description" content="{content_data["description"]}">')
        
        # Изображение
        if content_data.get("image"):
            tags.append(f'<meta name="twitter:image" content="{content_data["image"]}">')
            
            if content_data.get("image_alt"):
                tags.append(f'<meta name="twitter:image:alt" content="{content_data["image_alt"]}">')
        
        # Дополнительные теги
        if content_data.get("site_twitter"):
            tags.append(f'<meta name="twitter:site" content="{content_data["site_twitter"]}">')
        
        if content_data.get("creator_twitter"):
            tags.append(f'<meta name="twitter:creator" content="{content_data["creator_twitter"]}">')
        
        # Теги для плеера
        if card_type == "player":
            if content_data.get("player_url"):
                tags.append(f'<meta name="twitter:player" content="{content_data["player_url"]}">')
            
            if content_data.get("player_width"):
                tags.append(f'<meta name="twitter:player:width" content="{content_data["player_width"]}">')
            
            if content_data.get("player_height"):
                tags.append(f'<meta name="twitter:player:height" content="{content_data["player_height"]}">')
            
            if content_data.get("player_stream"):
                tags.append(f'<meta name="twitter:player:stream" content="{content_data["player_stream"]}">')
        
        # Теги для приложения
        elif card_type == "app":
            if content_data.get("app_id_iphone"):
                tags.append(f'<meta name="twitter:app:id:iphone" content="{content_data["app_id_iphone"]}">')
            
            if content_data.get("app_id_googleplay"):
                tags.append(f'<meta name="twitter:app:id:googleplay" content="{content_data["app_id_googleplay"]}">')
            
            if content_data.get("app_name_iphone"):
                tags.append(f'<meta name="twitter:app:name:iphone" content="{content_data["app_name_iphone"]}">')
            
            if content_data.get("app_name_googleplay"):
                tags.append(f'<meta name="twitter:app:name:googleplay" content="{content_data["app_name_googleplay"]}">')
        
        return tags
