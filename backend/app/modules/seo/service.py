import re
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup
from .open_graph_analyzer import OpenGraphAnalyzer
from .twitter_cards_analyzer import TwitterCardsAnalyzer
from .performance_analyzer import PerformanceAnalyzer


class SEOService:
    def __init__(self):
        self.og_analyzer = OpenGraphAnalyzer()
        self.twitter_analyzer = TwitterCardsAnalyzer()
        self.performance_analyzer = PerformanceAnalyzer()

    def analyze_html(self, html: str) -> Dict[str, Any]:
        """
        Analyze HTML for SEO optimization opportunities
        """
        soup = BeautifulSoup(html, "html.parser")

        # Базовый SEO анализ
        basic_analysis = {
            "title": self._analyze_title(soup),
            "meta_description": self._analyze_meta_description(soup),
            "headings": self._analyze_headings(soup),
            "images": self._analyze_images(soup),
            "links": self._analyze_links(soup),
            "content": self._analyze_content(soup),
        }

        # Анализ Open Graph
        og_analysis = self.og_analyzer.analyze_open_graph(html)
        
        # Анализ Twitter Cards
        twitter_analysis = self.twitter_analyzer.analyze_twitter_cards(html)
        
        # Анализ производительности
        performance_analysis = self.performance_analyzer.analyze_performance(html)
        
        # Объединение всех анализов
        analysis = {
            **basic_analysis,
            "open_graph": og_analysis,
            "twitter_cards": twitter_analysis,
            "performance": performance_analysis,
            "score": 0,
            "issues": [],
            "recommendations": [],
        }

        # Сбор всех проблем
        analysis["issues"].extend(self._collect_basic_issues(basic_analysis))
        analysis["issues"].extend(og_analysis.get("issues", []))
        analysis["issues"].extend(twitter_analysis.get("issues", []))
        
        # Сбор всех рекомендаций
        analysis["recommendations"].extend(self._generate_basic_recommendations(basic_analysis))
        analysis["recommendations"].extend(og_analysis.get("recommendations", []))
        analysis["recommendations"].extend(twitter_analysis.get("recommendations", []))
        analysis["recommendations"].extend(performance_analysis.get("recommendations", []))

        # Calculate overall score
        analysis["score"] = self._calculate_enhanced_seo_score(analysis)

        return analysis

    def _analyze_title(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze page title"""
        title_tag = soup.find("title")

        if not title_tag:
            return {
                "exists": False,
                "length": 0,
                "text": "",
                "issues": ["Missing title tag"],
            }

        title_text = title_tag.get_text().strip()
        length = len(title_text)

        issues = []
        if length == 0:
            issues.append("Empty title tag")
        elif length < 30:
            issues.append("Title too short (should be 30-60 characters)")
        elif length > 60:
            issues.append("Title too long (should be 30-60 characters)")

        return {"exists": True, "length": length, "text": title_text, "issues": issues}

    def _analyze_meta_description(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze meta description"""
        meta_desc = soup.find("meta", attrs={"name": "description"})

        if not meta_desc:
            return {
                "exists": False,
                "length": 0,
                "text": "",
                "issues": ["Missing meta description"],
            }

        desc_text = meta_desc.get("content", "").strip()
        length = len(desc_text)

        issues = []
        if length == 0:
            issues.append("Empty meta description")
        elif length < 120:
            issues.append("Meta description too short (should be 120-160 characters)")
        elif length > 160:
            issues.append("Meta description too long (should be 120-160 characters)")

        return {"exists": True, "length": length, "text": desc_text, "issues": issues}

    def _analyze_headings(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze heading structure"""
        headings = {f"h{i}": [] for i in range(1, 7)}

        for i in range(1, 7):
            tags = soup.find_all(f"h{i}")
            headings[f"h{i}"] = [tag.get_text().strip() for tag in tags]

        issues = []
        if not headings["h1"]:
            issues.append("Missing H1 tag")
        elif len(headings["h1"]) > 1:
            issues.append("Multiple H1 tags found")

        return {
            "structure": headings,
            "h1_count": len(headings["h1"]),
            "total_headings": sum(len(h) for h in headings.values()),
            "issues": issues,
        }

    def _analyze_images(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze images for SEO"""
        images = soup.find_all("img")

        total_images = len(images)
        missing_alt = 0
        empty_alt = 0

        for img in images:
            alt = img.get("alt")
            if alt is None:
                missing_alt += 1
            elif alt.strip() == "":
                empty_alt += 1

        issues = []
        if missing_alt > 0:
            issues.append(f"{missing_alt} images missing alt attribute")
        if empty_alt > 0:
            issues.append(f"{empty_alt} images with empty alt attribute")

        return {
            "total": total_images,
            "missing_alt": missing_alt,
            "empty_alt": empty_alt,
            "issues": issues,
        }

    def _analyze_links(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze internal and external links"""
        links = soup.find_all("a", href=True)

        internal_links = []
        external_links = []

        for link in links:
            href = link["href"]
            if href.startswith("http"):
                external_links.append(href)
            else:
                internal_links.append(href)

        return {
            "total": len(links),
            "internal": len(internal_links),
            "external": len(external_links),
            "issues": [],
        }

    def _analyze_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze content for SEO"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text()
        word_count = len(text.split())

        issues = []
        if word_count < 300:
            issues.append("Content too short (should be at least 300 words)")

        return {
            "word_count": word_count,
            "character_count": len(text),
            "issues": issues,
        }

    def _calculate_seo_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate overall SEO score (0-100)"""
        score = 100

        # Title analysis
        if not analysis["title"]["exists"] or analysis["title"]["issues"]:
            score -= 15

        # Meta description analysis
        if (
            not analysis["meta_description"]["exists"]
            or analysis["meta_description"]["issues"]
        ):
            score -= 15

        # Headings analysis
        if analysis["headings"]["issues"]:
            score -= 10

        # Images analysis
        if analysis["images"]["issues"]:
            score -= 10

        # Content analysis
        if analysis["content"]["issues"]:
            score -= 10

        return max(0, score)
    
    def _collect_basic_issues(self, basic_analysis: Dict[str, Any]) -> List[str]:
        """Сбор проблем из базового анализа"""
        issues = []
        
        # Проблемы с title
        issues.extend(basic_analysis["title"].get("issues", []))
        
        # Проблемы с meta description
        issues.extend(basic_analysis["meta_description"].get("issues", []))
        
        # Проблемы с заголовками
        issues.extend(basic_analysis["headings"].get("issues", []))
        
        # Проблемы с изображениями
        issues.extend(basic_analysis["images"].get("issues", []))
        
        # Проблемы с контентом
        issues.extend(basic_analysis["content"].get("issues", []))
        
        return issues
    
    def _generate_basic_recommendations(self, basic_analysis: Dict[str, Any]) -> List[str]:
        """Генерация рекомендаций из базового анализа"""
        recommendations = []
        
        # Title рекомендации
        if not basic_analysis["title"]["exists"]:
            recommendations.append("Добавьте title тег на страницу")
        elif basic_analysis["title"]["issues"]:
            recommendations.append("Оптимизируйте title тег")
        
        # Meta description рекомендации
        if not basic_analysis["meta_description"]["exists"]:
            recommendations.append("Добавьте meta description")
        elif basic_analysis["meta_description"]["issues"]:
            recommendations.append("Оптимизируйте meta description")
        
        # Заголовки рекомендации
        if basic_analysis["headings"]["issues"]:
            recommendations.append("Улучшите структуру заголовков")
        
        # Изображения рекомендации
        if basic_analysis["images"]["issues"]:
            recommendations.append("Оптимизируйте изображения (добавьте alt атрибуты)")
        
        # Контент рекомендации
        if basic_analysis["content"]["issues"]:
            recommendations.append("Увеличьте объем качественного контента")
        
        return recommendations
    
    def _calculate_enhanced_seo_score(self, analysis: Dict[str, Any]) -> int:
        """Расчет улучшенной SEO оценки с учетом всех факторов"""
        score = 100
        
        # Базовый SEO анализ (40% от общей оценки)
        basic_score = self._calculate_seo_score(analysis)
        score = basic_score * 0.4
        
        # Open Graph (20% от общей оценки)
        og_score = analysis["open_graph"].get("score", 0)
        score += og_score * 0.2
        
        # Twitter Cards (15% от общей оценки)
        twitter_score = analysis["twitter_cards"].get("score", 0)
        score += twitter_score * 0.15
        
        # Производительность (25% от общей оценки)
        performance_score = analysis["performance"].get("performance_score", 0)
        score += performance_score * 0.25
        
        return max(0, min(100, int(score)))

    def generate_structured_data(self, content_type: str, data: Dict[str, Any]) -> str:
        """
        Generate JSON-LD structured data
        """
        structured_data_templates = {
            "article": {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": data.get("title", ""),
                "description": data.get("description", ""),
                "author": {"@type": "Person", "name": data.get("author", "")},
                "datePublished": data.get("date_published", ""),
                "image": data.get("image", ""),
            },
            "webpage": {
                "@context": "https://schema.org",
                "@type": "WebPage",
                "name": data.get("title", ""),
                "description": data.get("description", ""),
                "url": data.get("url", ""),
            },
        }

        template = structured_data_templates.get(
            content_type, structured_data_templates["webpage"]
        )

        import json

        return json.dumps(template, indent=2)
