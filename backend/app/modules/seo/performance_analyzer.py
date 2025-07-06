import re
import gzip
from typing import Any, Dict, List, Optional, Tuple
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import base64


class PerformanceAnalyzer:
    """
    Анализатор производительности для SEO
    Проверяет размеры ресурсов, минификацию, отложенную загрузку
    """
    
    def __init__(self):
        # Пороговые значения для производительности
        self.thresholds = {
            "html_size": {
                "good": 50 * 1024,      # 50KB
                "warning": 100 * 1024,   # 100KB
                "critical": 200 * 1024   # 200KB
            },
            "css_size": {
                "good": 30 * 1024,      # 30KB per file
                "warning": 75 * 1024,    # 75KB per file
                "critical": 150 * 1024   # 150KB per file
            },
            "js_size": {
                "good": 50 * 1024,      # 50KB per file
                "warning": 100 * 1024,   # 100KB per file
                "critical": 200 * 1024   # 200KB per file
            },
            "image_size": {
                "good": 100 * 1024,     # 100KB per image
                "warning": 500 * 1024,   # 500KB per image
                "critical": 1024 * 1024  # 1MB per image
            },
            "total_requests": {
                "good": 30,
                "warning": 50,
                "critical": 100
            },
            "dom_elements": {
                "good": 1500,
                "warning": 3000,
                "critical": 5000
            }
        }
        
        # Критические CSS селекторы для выше фолда
        self.critical_css_selectors = [
            "header", "nav", ".hero", ".banner", ".above-fold",
            "h1", "h2", ".title", ".main-content", ".sidebar"
        ]
        
        # Типы ресурсов для анализа
        self.resource_types = {
            "css": {
                "extensions": [".css"],
                "inline_tag": "style",
                "external_attribute": "href"
            },
            "js": {
                "extensions": [".js"],
                "inline_tag": "script",
                "external_attribute": "src"
            },
            "images": {
                "extensions": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
                "inline_tag": "img",
                "external_attribute": "src"
            },
            "fonts": {
                "extensions": [".woff", ".woff2", ".ttf", ".otf", ".eot"],
                "inline_tag": None,
                "external_attribute": "href"
            }
        }
    
    def analyze_performance(self, html: str, base_url: str = "") -> Dict[str, Any]:
        """
        Полный анализ производительности HTML страницы
        """
        soup = BeautifulSoup(html, "html.parser")
        
        # Анализ размеров ресурсов
        resource_analysis = self._analyze_resources(soup, base_url)
        
        # Анализ минификации
        minification_analysis = self._analyze_minification(html, soup)
        
        # Анализ отложенной загрузки
        lazy_loading_analysis = self._analyze_lazy_loading(soup)
        
        # Анализ критического CSS
        critical_css_analysis = self._analyze_critical_css(soup)
        
        # Анализ DOM структуры
        dom_analysis = self._analyze_dom_structure(soup)
        
        # Анализ сжатия
        compression_analysis = self._analyze_compression(html, resource_analysis)
        
        # Анализ кэширования
        caching_analysis = self._analyze_caching_headers(soup)
        
        # Анализ блокирующих ресурсов
        blocking_analysis = self._analyze_blocking_resources(soup)
        
        # Генерация рекомендаций
        recommendations = self._generate_performance_recommendations(
            resource_analysis, minification_analysis, lazy_loading_analysis,
            critical_css_analysis, dom_analysis, compression_analysis,
            caching_analysis, blocking_analysis
        )
        
        # Расчет общей оценки производительности
        performance_score = self._calculate_performance_score(
            resource_analysis, minification_analysis, lazy_loading_analysis,
            critical_css_analysis, dom_analysis, blocking_analysis
        )
        
        return {
            "performance_score": performance_score,
            "resources": resource_analysis,
            "minification": minification_analysis,
            "lazy_loading": lazy_loading_analysis,
            "critical_css": critical_css_analysis,
            "dom_structure": dom_analysis,
            "compression": compression_analysis,
            "caching": caching_analysis,
            "blocking_resources": blocking_analysis,
            "recommendations": recommendations,
            "total_size_estimate": self._calculate_total_size(resource_analysis),
            "load_time_estimate": self._estimate_load_time(resource_analysis, dom_analysis)
        }
    
    def _analyze_resources(self, soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
        """Анализ размеров и количества ресурсов"""
        analysis = {
            "css": {"external": [], "inline": [], "total_size": 0, "count": 0},
            "js": {"external": [], "inline": [], "total_size": 0, "count": 0},
            "images": {"external": [], "inline": [], "total_size": 0, "count": 0},
            "fonts": {"external": [], "inline": [], "total_size": 0, "count": 0},
            "total_requests": 0,
            "issues": []
        }
        
        # Анализ CSS
        css_links = soup.find_all("link", rel="stylesheet")
        for link in css_links:
            href = link.get("href", "")
            if href:
                size_estimate = self._estimate_resource_size(href, "css")
                analysis["css"]["external"].append({
                    "url": href,
                    "size_estimate": size_estimate,
                    "is_blocking": not link.get("media") or link.get("media") == "all"
                })
                analysis["css"]["total_size"] += size_estimate
                analysis["css"]["count"] += 1
                analysis["total_requests"] += 1
        
        # Инлайн CSS
        style_tags = soup.find_all("style")
        for style in style_tags:
            content = style.get_text()
            size = len(content.encode('utf-8'))
            analysis["css"]["inline"].append({
                "size": size,
                "minified": self._is_css_minified(content)
            })
            analysis["css"]["total_size"] += size
            analysis["css"]["count"] += 1
        
        # Анализ JavaScript
        js_scripts = soup.find_all("script", src=True)
        for script in js_scripts:
            src = script.get("src", "")
            if src:
                size_estimate = self._estimate_resource_size(src, "js")
                analysis["js"]["external"].append({
                    "url": src,
                    "size_estimate": size_estimate,
                    "async": script.has_attr("async"),
                    "defer": script.has_attr("defer"),
                    "is_blocking": not (script.has_attr("async") or script.has_attr("defer"))
                })
                analysis["js"]["total_size"] += size_estimate
                analysis["js"]["count"] += 1
                analysis["total_requests"] += 1
        
        # Инлайн JavaScript
        inline_scripts = soup.find_all("script", src=False)
        for script in inline_scripts:
            content = script.get_text()
            if content.strip():
                size = len(content.encode('utf-8'))
                analysis["js"]["inline"].append({
                    "size": size,
                    "minified": self._is_js_minified(content)
                })
                analysis["js"]["total_size"] += size
                analysis["js"]["count"] += 1
        
        # Анализ изображений
        images = soup.find_all("img")
        for img in images:
            src = img.get("src", "")
            if src:
                if src.startswith("data:"):
                    # Инлайн изображение (base64)
                    size = self._calculate_base64_size(src)
                    analysis["images"]["inline"].append({
                        "type": "base64",
                        "size": size
                    })
                    analysis["images"]["total_size"] += size
                else:
                    # Внешнее изображение
                    size_estimate = self._estimate_image_size(src, img)
                    analysis["images"]["external"].append({
                        "url": src,
                        "size_estimate": size_estimate,
                        "lazy_loading": img.get("loading") == "lazy",
                        "has_alt": bool(img.get("alt")),
                        "format": self._get_image_format(src)
                    })
                    analysis["images"]["total_size"] += size_estimate
                    analysis["total_requests"] += 1
                analysis["images"]["count"] += 1
        
        # Анализ шрифтов
        font_links = soup.find_all("link", href=re.compile(r"\.(woff2?|ttf|otf|eot)"))
        for link in font_links:
            href = link.get("href", "")
            size_estimate = self._estimate_resource_size(href, "font")
            analysis["fonts"]["external"].append({
                "url": href,
                "size_estimate": size_estimate,
                "preload": link.get("rel") == "preload"
            })
            analysis["fonts"]["total_size"] += size_estimate
            analysis["fonts"]["count"] += 1
            analysis["total_requests"] += 1
        
        # Проверка превышения пороговых значений
        self._check_resource_thresholds(analysis)
        
        return analysis
    
    def _analyze_minification(self, html: str, soup: BeautifulSoup) -> Dict[str, Any]:
        """Анализ минификации ресурсов"""
        analysis = {
            "html": {
                "is_minified": self._is_html_minified(html),
                "original_size": len(html.encode('utf-8')),
                "potential_savings": 0
            },
            "css": {
                "inline_minified": 0,
                "inline_total": 0,
                "potential_savings": 0
            },
            "js": {
                "inline_minified": 0,
                "inline_total": 0,
                "potential_savings": 0
            },
            "recommendations": []
        }
        
        # HTML минификация
        if not analysis["html"]["is_minified"]:
            minified_html = self._minify_html_estimate(html)
            analysis["html"]["potential_savings"] = len(html) - len(minified_html)
            analysis["recommendations"].append("Минифицируйте HTML для уменьшения размера")
        
        # CSS минификация
        style_tags = soup.find_all("style")
        for style in style_tags:
            content = style.get_text()
            analysis["css"]["inline_total"] += 1
            if self._is_css_minified(content):
                analysis["css"]["inline_minified"] += 1
            else:
                savings = len(content) - len(self._minify_css_estimate(content))
                analysis["css"]["potential_savings"] += savings
        
        # JavaScript минификация
        inline_scripts = soup.find_all("script", src=False)
        for script in inline_scripts:
            content = script.get_text().strip()
            if content:
                analysis["js"]["inline_total"] += 1
                if self._is_js_minified(content):
                    analysis["js"]["inline_minified"] += 1
                else:
                    savings = len(content) - len(self._minify_js_estimate(content))
                    analysis["js"]["potential_savings"] += savings
        
        return analysis
    
    def _analyze_lazy_loading(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Анализ отложенной загрузки"""
        analysis = {
            "images": {
                "total": 0,
                "lazy_loaded": 0,
                "percentage": 0,
                "recommendations": []
            },
            "iframes": {
                "total": 0,
                "lazy_loaded": 0,
                "percentage": 0,
                "recommendations": []
            },
            "score": 0
        }
        
        # Анализ изображений
        images = soup.find_all("img")
        analysis["images"]["total"] = len(images)
        
        lazy_images = 0
        for img in images:
            if img.get("loading") == "lazy":
                lazy_images += 1
        
        analysis["images"]["lazy_loaded"] = lazy_images
        if analysis["images"]["total"] > 0:
            analysis["images"]["percentage"] = (lazy_images / analysis["images"]["total"]) * 100
        
        # Рекомендации для изображений
        if analysis["images"]["total"] > 3 and analysis["images"]["percentage"] < 50:
            analysis["images"]["recommendations"].append(
                "Используйте loading='lazy' для изображений ниже фолда"
            )
        
        # Анализ iframe
        iframes = soup.find_all("iframe")
        analysis["iframes"]["total"] = len(iframes)
        
        lazy_iframes = 0
        for iframe in iframes:
            if iframe.get("loading") == "lazy":
                lazy_iframes += 1
        
        analysis["iframes"]["lazy_loaded"] = lazy_iframes
        if analysis["iframes"]["total"] > 0:
            analysis["iframes"]["percentage"] = (lazy_iframes / analysis["iframes"]["total"]) * 100
        
        # Рекомендации для iframe
        if analysis["iframes"]["total"] > 0 and analysis["iframes"]["percentage"] < 100:
            analysis["iframes"]["recommendations"].append(
                "Используйте loading='lazy' для всех iframe"
            )
        
        # Общая оценка lazy loading
        total_elements = analysis["images"]["total"] + analysis["iframes"]["total"]
        lazy_elements = analysis["images"]["lazy_loaded"] + analysis["iframes"]["lazy_loaded"]
        
        if total_elements > 0:
            analysis["score"] = (lazy_elements / total_elements) * 100
        
        return analysis
    
    def _analyze_critical_css(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Анализ критического CSS"""
        analysis = {
            "has_critical_css": False,
            "inline_css_size": 0,
            "external_css_count": 0,
            "blocking_css_count": 0,
            "recommendations": []
        }
        
        # Проверяем инлайн CSS в head
        head = soup.find("head")
        if head:
            style_tags = head.find_all("style")
            for style in style_tags:
                content = style.get_text()
                analysis["inline_css_size"] += len(content.encode('utf-8'))
                
                # Проверяем наличие критических селекторов
                for selector in self.critical_css_selectors:
                    if selector in content:
                        analysis["has_critical_css"] = True
                        break
        
        # Анализируем внешний CSS
        css_links = soup.find_all("link", rel="stylesheet")
        analysis["external_css_count"] = len(css_links)
        
        for link in css_links:
            media = link.get("media", "all")
            if media == "all" or not media:
                analysis["blocking_css_count"] += 1
        
        # Рекомендации
        if not analysis["has_critical_css"] and analysis["external_css_count"] > 0:
            analysis["recommendations"].append(
                "Выделите критический CSS и встройте его инлайн в <head>"
            )
        
        if analysis["blocking_css_count"] > 2:
            analysis["recommendations"].append(
                "Уменьшите количество блокирующих CSS файлов"
            )
        
        if analysis["inline_css_size"] > 50 * 1024:  # 50KB
            analysis["recommendations"].append(
                "Инлайн CSS слишком большой, оптимизируйте критический CSS"
            )
        
        return analysis
    
    def _analyze_dom_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Анализ DOM структуры"""
        analysis = {
            "total_elements": 0,
            "depth": 0,
            "text_to_html_ratio": 0,
            "issues": []
        }
        
        # Подсчет всех элементов
        all_elements = soup.find_all()
        analysis["total_elements"] = len(all_elements)
        
        # Расчет максимальной глубины
        analysis["depth"] = self._calculate_dom_depth(soup)
        
        # Расчет соотношения текста к HTML
        text_content = soup.get_text()
        html_content = str(soup)
        if len(html_content) > 0:
            analysis["text_to_html_ratio"] = len(text_content) / len(html_content)
        
        # Проверка пороговых значений
        if analysis["total_elements"] > self.thresholds["dom_elements"]["critical"]:
            analysis["issues"].append(
                f"Слишком много DOM элементов ({analysis['total_elements']})"
            )
        elif analysis["total_elements"] > self.thresholds["dom_elements"]["warning"]:
            analysis["issues"].append(
                f"Много DOM элементов ({analysis['total_elements']})"
            )
        
        if analysis["depth"] > 15:
            analysis["issues"].append(f"Слишком глубокая DOM структура ({analysis['depth']} уровней)")
        
        if analysis["text_to_html_ratio"] < 0.1:
            analysis["issues"].append("Низкое соотношение текста к HTML разметке")
        
        return analysis
    
    def _analyze_compression(self, html: str, resource_analysis: Dict) -> Dict[str, Any]:
        """Анализ сжатия ресурсов"""
        analysis = {
            "html": {
                "original_size": len(html.encode('utf-8')),
                "gzip_size": 0,
                "compression_ratio": 0,
                "savings": 0
            },
            "recommendations": []
        }
        
        # Симуляция gzip сжатия HTML
        try:
            compressed = gzip.compress(html.encode('utf-8'))
            analysis["html"]["gzip_size"] = len(compressed)
            analysis["html"]["compression_ratio"] = analysis["html"]["gzip_size"] / analysis["html"]["original_size"]
            analysis["html"]["savings"] = analysis["html"]["original_size"] - analysis["html"]["gzip_size"]
        except:
            analysis["html"]["gzip_size"] = analysis["html"]["original_size"]
            analysis["html"]["compression_ratio"] = 1.0
        
        # Рекомендации по сжатию
        if analysis["html"]["compression_ratio"] > 0.7:
            analysis["recommendations"].append(
                "Включите gzip/brotli сжатие на сервере для лучшей производительности"
            )
        
        return analysis
    
    def _analyze_caching_headers(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Анализ заголовков кэширования"""
        analysis = {
            "meta_cache_control": None,
            "meta_expires": None,
            "recommendations": []
        }
        
        # Проверяем meta теги для кэширования
        cache_control = soup.find("meta", attrs={"http-equiv": "Cache-Control"})
        if cache_control:
            analysis["meta_cache_control"] = cache_control.get("content")
        
        expires = soup.find("meta", attrs={"http-equiv": "Expires"})
        if expires:
            analysis["meta_expires"] = expires.get("content")
        
        # Рекомендации
        if not analysis["meta_cache_control"]:
            analysis["recommendations"].append(
                "Настройте заголовки кэширования для статических ресурсов"
            )
        
        return analysis
    
    def _analyze_blocking_resources(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Анализ блокирующих ресурсов"""
        analysis = {
            "blocking_css": 0,
            "blocking_js": 0,
            "render_blocking_score": 100,
            "recommendations": []
        }
        
        # Блокирующий CSS
        css_links = soup.find_all("link", rel="stylesheet")
        for link in css_links:
            media = link.get("media", "all")
            if media == "all" or not media:
                analysis["blocking_css"] += 1
        
        # Блокирующий JavaScript
        head = soup.find("head")
        if head:
            js_scripts = head.find_all("script", src=True)
            for script in js_scripts:
                if not (script.has_attr("async") or script.has_attr("defer")):
                    analysis["blocking_js"] += 1
        
        # Расчет оценки блокирования рендеринга
        total_blocking = analysis["blocking_css"] + analysis["blocking_js"]
        if total_blocking > 5:
            analysis["render_blocking_score"] = max(0, 100 - (total_blocking - 5) * 10)
        
        # Рекомендации
        if analysis["blocking_css"] > 2:
            analysis["recommendations"].append(
                f"Уменьшите количество блокирующих CSS файлов ({analysis['blocking_css']})"
            )
        
        if analysis["blocking_js"] > 0:
            analysis["recommendations"].append(
                f"Добавьте async/defer к JavaScript в <head> ({analysis['blocking_js']} файлов)"
            )
        
        return analysis
    
    def _generate_performance_recommendations(
        self, resources: Dict, minification: Dict, lazy_loading: Dict,
        critical_css: Dict, dom: Dict, compression: Dict,
        caching: Dict, blocking: Dict
    ) -> List[Dict[str, Any]]:
        """Генерация рекомендаций по производительности"""
        recommendations = []
        
        # Рекомендации по ресурсам
        for issue in resources.get("issues", []):
            recommendations.append({
                "type": "warning",
                "category": "performance",
                "subcategory": "resources",
                "issue": issue,
                "recommendation": "Оптимизируйте размеры ресурсов",
                "impact": "high"
            })
        
        # Рекомендации по минификации
        for rec in minification.get("recommendations", []):
            recommendations.append({
                "type": "suggestion",
                "category": "performance",
                "subcategory": "minification",
                "issue": rec,
                "recommendation": "Включите минификацию ресурсов",
                "impact": "medium"
            })
        
        # Рекомендации по lazy loading
        for rec in lazy_loading["images"].get("recommendations", []):
            recommendations.append({
                "type": "suggestion",
                "category": "performance",
                "subcategory": "lazy_loading",
                "issue": rec,
                "recommendation": "Реализуйте отложенную загрузку изображений",
                "impact": "medium"
            })
        
        # Рекомендации по критическому CSS
        for rec in critical_css.get("recommendations", []):
            recommendations.append({
                "type": "suggestion",
                "category": "performance",
                "subcategory": "critical_css",
                "issue": rec,
                "recommendation": "Оптимизируйте критический CSS",
                "impact": "high"
            })
        
        # Рекомендации по DOM
        for issue in dom.get("issues", []):
            recommendations.append({
                "type": "warning",
                "category": "performance",
                "subcategory": "dom_structure",
                "issue": issue,
                "recommendation": "Упростите структуру DOM",
                "impact": "medium"
            })
        
        # Рекомендации по сжатию
        for rec in compression.get("recommendations", []):
            recommendations.append({
                "type": "critical",
                "category": "performance",
                "subcategory": "compression",
                "issue": rec,
                "recommendation": "Настройте сжатие на сервере",
                "impact": "high"
            })
        
        # Рекомендации по блокирующим ресурсам
        for rec in blocking.get("recommendations", []):
            recommendations.append({
                "type": "warning",
                "category": "performance",
                "subcategory": "blocking_resources",
                "issue": rec,
                "recommendation": "Устраните блокирование рендеринга",
                "impact": "high"
            })
        
        return recommendations
    
    # Вспомогательные методы
    
    def _estimate_resource_size(self, url: str, resource_type: str) -> int:
        """Оценка размера ресурса по URL"""
        # Простая эвристика для оценки размеров
        size_estimates = {
            "css": 15 * 1024,    # 15KB средний CSS файл
            "js": 30 * 1024,     # 30KB средний JS файл
            "font": 25 * 1024    # 25KB средний шрифт
        }
        
        return size_estimates.get(resource_type, 10 * 1024)
    
    def _estimate_image_size(self, src: str, img_tag) -> int:
        """Оценка размера изображения"""
        # Базовая оценка по формату
        format_sizes = {
            ".jpg": 80 * 1024,
            ".jpeg": 80 * 1024,
            ".png": 120 * 1024,
            ".gif": 50 * 1024,
            ".webp": 60 * 1024,
            ".svg": 5 * 1024
        }
        
        for ext, size in format_sizes.items():
            if ext in src.lower():
                return size
        
        return 100 * 1024  # Значение по умолчанию
    
    def _calculate_base64_size(self, data_url: str) -> int:
        """Расчет размера base64 изображения"""
        try:
            header, data = data_url.split(',', 1)
            return len(base64.b64decode(data))
        except:
            return 0
    
    def _get_image_format(self, src: str) -> str:
        """Определение формата изображения"""
        formats = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"]
        for fmt in formats:
            if fmt in src.lower():
                return fmt[1:]  # Убираем точку
        return "unknown"
    
    def _is_html_minified(self, html: str) -> bool:
        """Проверка минификации HTML"""
        # Простая проверка: много пробелов и переносов = не минифицирован
        return len(html.split()) / len(html) > 0.1
    
    def _is_css_minified(self, css: str) -> bool:
        """Проверка минификации CSS"""
        # Проверяем наличие комментариев и лишних пробелов
        has_comments = "/*" in css
        has_newlines = "\n" in css.strip()
        has_multiple_spaces = "  " in css
        
        return not (has_comments or has_newlines or has_multiple_spaces)
    
    def _is_js_minified(self, js: str) -> bool:
        """Проверка минификации JavaScript"""
        # Аналогично CSS
        has_comments = "//" in js or "/*" in js
        has_newlines = "\n" in js.strip()
        has_multiple_spaces = "  " in js
        
        return not (has_comments or has_newlines or has_multiple_spaces)
    
    def _minify_html_estimate(self, html: str) -> str:
        """Примерная минификация HTML для оценки"""
        # Удаляем лишние пробелы и переносы
        minified = re.sub(r'\s+', ' ', html)
        minified = re.sub(r'>\s+<', '><', minified)
        return minified.strip()
    
    def _minify_css_estimate(self, css: str) -> str:
        """Примерная минификация CSS для оценки"""
        # Удаляем комментарии и лишние пробелы
        minified = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
        minified = re.sub(r'\s+', ' ', minified)
        minified = re.sub(r';\s*}', '}', minified)
        return minified.strip()
    
    def _minify_js_estimate(self, js: str) -> str:
        """Примерная минификация JavaScript для оценки"""
        # Базовая минификация
        minified = re.sub(r'//.*?\n', '', js)
        minified = re.sub(r'/\*.*?\*/', '', minified, flags=re.DOTALL)
        minified = re.sub(r'\s+', ' ', minified)
        return minified.strip()
    
    def _calculate_dom_depth(self, element, current_depth=0) -> int:
        """Расчет максимальной глубины DOM"""
        max_depth = current_depth
        for child in element.find_all(recursive=False):
            child_depth = self._calculate_dom_depth(child, current_depth + 1)
            max_depth = max(max_depth, child_depth)
        return max_depth
    
    def _check_resource_thresholds(self, analysis: Dict):
        """Проверка превышения пороговых значений ресурсов"""
        issues = analysis.setdefault("issues", [])
        
        # Проверка общего количества запросов
        total_requests = analysis["total_requests"]
        if total_requests > self.thresholds["total_requests"]["critical"]:
            issues.append(f"Критично много HTTP запросов ({total_requests})")
        elif total_requests > self.thresholds["total_requests"]["warning"]:
            issues.append(f"Много HTTP запросов ({total_requests})")
        
        # Проверка размеров CSS
        for css_file in analysis["css"]["external"]:
            size = css_file["size_estimate"]
            if size > self.thresholds["css_size"]["critical"]:
                issues.append(f"Критично большой CSS файл ({size // 1024}KB)")
        
        # Проверка размеров JS
        for js_file in analysis["js"]["external"]:
            size = js_file["size_estimate"]
            if size > self.thresholds["js_size"]["critical"]:
                issues.append(f"Критично большой JS файл ({size // 1024}KB)")
    
    def _calculate_total_size(self, resource_analysis: Dict) -> Dict[str, int]:
        """Расчет общих размеров всех ресурсов"""
        return {
            "css": resource_analysis["css"]["total_size"],
            "js": resource_analysis["js"]["total_size"],
            "images": resource_analysis["images"]["total_size"],
            "fonts": resource_analysis["fonts"]["total_size"],
            "total": (
                resource_analysis["css"]["total_size"] +
                resource_analysis["js"]["total_size"] +
                resource_analysis["images"]["total_size"] +
                resource_analysis["fonts"]["total_size"]
            )
        }
    
    def _estimate_load_time(self, resource_analysis: Dict, dom_analysis: Dict) -> Dict[str, float]:
        """Примерная оценка времени загрузки"""
        # Простая модель: размер / скорость + количество запросов * latency
        connection_speed = 1.5 * 1024 * 1024  # 1.5 Mbps средняя скорость
        request_latency = 0.1  # 100ms на запрос
        
        total_size = self._calculate_total_size(resource_analysis)["total"]
        total_requests = resource_analysis["total_requests"]
        
        download_time = total_size / connection_speed
        latency_time = total_requests * request_latency
        dom_processing_time = dom_analysis["total_elements"] / 10000  # 10k элементов в секунду
        
        return {
            "download_time": download_time,
            "latency_time": latency_time,
            "dom_processing_time": dom_processing_time,
            "total_estimated_time": download_time + latency_time + dom_processing_time
        }
    
    def _calculate_performance_score(
        self, resources: Dict, minification: Dict, lazy_loading: Dict,
        critical_css: Dict, dom: Dict, blocking: Dict
    ) -> int:
        """Расчет общей оценки производительности"""
        score = 100
        
        # Штрафы за проблемы с ресурсами
        score -= len(resources.get("issues", [])) * 10
        
        # Штрафы за отсутствие минификации
        if not minification["html"]["is_minified"]:
            score -= 5
        if minification["css"]["potential_savings"] > 5000:
            score -= 5
        if minification["js"]["potential_savings"] > 5000:
            score -= 5
        
        # Штрафы за отсутствие lazy loading
        if lazy_loading["score"] < 50:
            score -= 10
        
        # Штрафы за проблемы с DOM
        score -= len(dom.get("issues", [])) * 5
        
        # Штрафы за блокирующие ресурсы
        score = min(score, blocking["render_blocking_score"])
        
        return max(0, score)
