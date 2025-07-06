import re
import json
from typing import Any, Dict, List, Optional, Tuple
from bs4 import BeautifulSoup

from app.modules.seo.advisor import SEOAdvisor
from app.modules.seo.service import SEOService


class SEOIntegrator:
    """
    Интегратор SEO рекомендаций для автоматического встраивания 
    в процесс генерации и правки HTML
    """
    
    def __init__(self):
        self.advisor = SEOAdvisor()
        self.seo_service = SEOService()
        
        # Настройки автоматических исправлений
        self.auto_fix_config = {
            "title": {
                "auto_fix": True,
                "fallback_template": "{content_title} | Качественный контент"
            },
            "meta_description": {
                "auto_fix": True,
                "fallback_template": "Узнайте больше о {main_topic}. Полезная информация и советы."
            },
            "headings": {
                "auto_fix": True,
                "ensure_h1": True
            },
            "images": {
                "auto_fix": True,
                "default_alt": "Информативное изображение"
            },
            "internal_linking": {
                "auto_suggest": True,
                "min_links": 2
            },
            "keywords": {
                "auto_optimize": True,
                "density_target": 1.5  # %
            }
        }
    
    def integrate_seo_recommendations(
        self, 
        html: str, 
        content_context: Optional[Dict[str, Any]] = None,
        target_keywords: Optional[List[str]] = None,
        target_audience: str = "general",
        auto_apply: bool = True
    ) -> Dict[str, Any]:
        """
        Основной метод интеграции SEO рекомендаций в HTML
        
        Args:
            html: Исходный HTML
            content_context: Контекст контента (заголовок, тема, и т.д.)
            target_keywords: Целевые ключевые слова
            target_audience: Целевая аудитория
            auto_apply: Автоматически применять исправления
            
        Returns:
            Dict с улучшенным HTML и анализом
        """
        # Получение рекомендаций от SEO советника
        seo_analysis = self.advisor.analyze_and_recommend(
            html=html,
            target_keywords=target_keywords,
            target_audience=target_audience
        )
        
        # Применение автоматических исправлений
        if auto_apply:
            optimized_html = self._apply_auto_fixes(
                html, 
                seo_analysis["recommendations"], 
                content_context
            )
        else:
            optimized_html = html
        
        # Генерация дополнительных SEO улучшений
        enhanced_html = self._apply_enhanced_optimizations(
            optimized_html,
            seo_analysis,
            content_context,
            target_keywords
        )
        
        # Валидация результата
        final_analysis = self.advisor.analyze_and_recommend(
            html=enhanced_html,
            target_keywords=target_keywords,
            target_audience=target_audience
        )
        
        # Генерация отчета об изменениях
        changes_report = self._generate_changes_report(
            seo_analysis, final_analysis
        )
        
        return {
            "original_html": html,
            "optimized_html": enhanced_html,
            "original_analysis": seo_analysis,
            "final_analysis": final_analysis,
            "improvements_applied": changes_report,
            "seo_score_improvement": (
                final_analysis["overall_score"] - 
                seo_analysis["overall_score"]
            ),
            "recommendations_for_manual_review": self._get_manual_recommendations(
                final_analysis["recommendations"]
            )
        }
    
    def _apply_auto_fixes(
        self, 
        html: str, 
        recommendations: List[Dict],
        content_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Применение автоматических исправлений"""
        soup = BeautifulSoup(html, "html.parser")
        applied_fixes = []
        
        for rec in recommendations:
            if rec["type"] == "critical" or (
                rec["type"] == "warning" and rec["impact"] == "high"
            ):
                if rec["category"] == "title" and self.auto_fix_config["title"]["auto_fix"]:
                    soup = self._fix_title(soup, rec, content_context)
                    applied_fixes.append(f"Исправлен title: {rec['issue']}")
                
                elif rec["category"] == "meta_description" and self.auto_fix_config["meta_description"]["auto_fix"]:
                    soup = self._fix_meta_description(soup, rec, content_context)
                    applied_fixes.append(f"Исправлен meta description: {rec['issue']}")
                
                elif rec["category"] == "headings" and self.auto_fix_config["headings"]["auto_fix"]:
                    soup = self._fix_headings(soup, rec, content_context)
                    applied_fixes.append(f"Исправлена структура заголовков: {rec['issue']}")
                
                elif rec["category"] == "images" and self.auto_fix_config["images"]["auto_fix"]:
                    soup = self._fix_images(soup, rec)
                    applied_fixes.append(f"Исправлены изображения: {rec['issue']}")
                
                elif rec["category"] == "technical":
                    soup = self._fix_technical_issues(soup, rec)
                    applied_fixes.append(f"Исправлена техническая проблема: {rec['issue']}")
        
        return str(soup)
    
    def _fix_title(
        self, 
        soup: BeautifulSoup, 
        recommendation: Dict,
        content_context: Optional[Dict[str, Any]] = None
    ) -> BeautifulSoup:
        """Автоматическое исправление title"""
        head = soup.find("head")
        if not head:
            head = soup.new_tag("head")
            if soup.find("html"):
                soup.find("html").insert(0, head)
            else:
                soup.insert(0, head)
        
        title_tag = soup.find("title")
        
        if not title_tag:
            # Создаем новый title
            title_tag = soup.new_tag("title")
            head.insert(0, title_tag)
        
        # Генерируем улучшенный title
        new_title = self._generate_improved_title(
            current_title=title_tag.get_text() if title_tag else "",
            content_context=content_context,
            recommendation=recommendation
        )
        
        title_tag.string = new_title
        return soup
    
    def _fix_meta_description(
        self, 
        soup: BeautifulSoup, 
        recommendation: Dict,
        content_context: Optional[Dict[str, Any]] = None
    ) -> BeautifulSoup:
        """Автоматическое исправление meta description"""
        head = soup.find("head")
        if not head:
            head = soup.new_tag("head")
            if soup.find("html"):
                soup.find("html").insert(0, head)
            else:
                soup.insert(0, head)
        
        meta_desc = soup.find("meta", attrs={"name": "description"})
        
        if not meta_desc:
            meta_desc = soup.new_tag("meta", attrs={"name": "description"})
            head.append(meta_desc)
        
        # Генерируем улучшенное описание
        new_description = self._generate_improved_description(
            current_description=meta_desc.get("content", ""),
            content_context=content_context,
            recommendation=recommendation
        )
        
        meta_desc["content"] = new_description
        return soup
    
    def _fix_headings(
        self, 
        soup: BeautifulSoup, 
        recommendation: Dict,
        content_context: Optional[Dict[str, Any]] = None
    ) -> BeautifulSoup:
        """Автоматическое исправление структуры заголовков"""
        if "Отсутствует H1" in recommendation["issue"]:
            # Добавляем H1 заголовок
            h1_text = self._generate_h1_text(content_context)
            h1_tag = soup.new_tag("h1")
            h1_tag.string = h1_text
            
            # Ищем место для вставки H1
            body = soup.find("body")
            if body:
                # Вставляем в начало body
                body.insert(0, h1_tag)
            else:
                # Добавляем в начало документа
                soup.insert(0, h1_tag)
        
        elif "Multiple H1" in recommendation["issue"]:
            # Преобразуем дополнительные H1 в H2
            h1_tags = soup.find_all("h1")
            for i, h1 in enumerate(h1_tags[1:], 1):  # Оставляем первый H1
                h2_tag = soup.new_tag("h2")
                h2_tag.string = h1.get_text()
                h1.replace_with(h2_tag)
        
        return soup
    
    def _fix_images(self, soup: BeautifulSoup, recommendation: Dict) -> BeautifulSoup:
        """Автоматическое исправление изображений"""
        images = soup.find_all("img")
        
        for img in images:
            if not img.get("alt"):
                # Генерируем alt текст на основе src или контекста
                alt_text = self._generate_alt_text(img)
                img["alt"] = alt_text
            
            # Добавляем loading="lazy" для оптимизации
            if not img.get("loading"):
                img["loading"] = "lazy"
        
        return soup
    
    def _fix_technical_issues(self, soup: BeautifulSoup, recommendation: Dict) -> BeautifulSoup:
        """Исправление технических SEO проблем"""
        head = soup.find("head")
        if not head:
            head = soup.new_tag("head")
            if soup.find("html"):
                soup.find("html").insert(0, head)
            else:
                soup.insert(0, head)
        
        if "viewport" in recommendation["issue"].lower():
            if not soup.find("meta", attrs={"name": "viewport"}):
                viewport_tag = soup.new_tag("meta", attrs={
                    "name": "viewport",
                    "content": "width=device-width, initial-scale=1.0"
                })
                head.append(viewport_tag)
        
        if "lang" in recommendation["issue"].lower():
            html_tag = soup.find("html")
            if html_tag and not html_tag.get("lang"):
                html_tag["lang"] = "ru"
        
        if "charset" in recommendation["issue"].lower():
            if not soup.find("meta", attrs={"charset": True}):
                charset_tag = soup.new_tag("meta", attrs={"charset": "UTF-8"})
                head.insert(0, charset_tag)
        
        return soup
    
    def _apply_enhanced_optimizations(
        self,
        html: str,
        seo_analysis: Dict,
        content_context: Optional[Dict[str, Any]] = None,
        target_keywords: Optional[List[str]] = None
    ) -> str:
        """Применение дополнительных SEO оптимизаций"""
        soup = BeautifulSoup(html, "html.parser")
        
        # Добавление структурированных данных
        soup = self._add_structured_data(soup, content_context)
        
        # Оптимизация внутренней перелинковки
        soup = self._optimize_internal_linking(soup, content_context)
        
        # Добавление Open Graph тегов
        soup = self._add_open_graph_tags(soup, content_context)
        
        # Оптимизация заголовков для ключевых слов
        if target_keywords:
            soup = self._optimize_headings_for_keywords(soup, target_keywords)
        
        # Добавление хлебных крошек
        soup = self._add_breadcrumbs(soup, content_context)
        
        return str(soup)
    
    def _add_structured_data(
        self, 
        soup: BeautifulSoup, 
        content_context: Optional[Dict[str, Any]] = None
    ) -> BeautifulSoup:
        """Добавление структурированных данных"""
        if not content_context:
            return soup
        
        # Определяем тип контента
        content_type = content_context.get("type", "webpage")
        
        structured_data = {}
        
        if content_type == "article":
            structured_data = {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": content_context.get("title", ""),
                "description": content_context.get("description", ""),
                "author": {
                    "@type": "Person",
                    "name": content_context.get("author", "")
                },
                "datePublished": content_context.get("date_published", ""),
                "dateModified": content_context.get("date_modified", ""),
                "image": content_context.get("image", "")
            }
        else:
            structured_data = {
                "@context": "https://schema.org",
                "@type": "WebPage",
                "name": content_context.get("title", ""),
                "description": content_context.get("description", ""),
                "url": content_context.get("url", "")
            }
        
        # Создаем script тег с JSON-LD
        script_tag = soup.new_tag("script", attrs={"type": "application/ld+json"})
        script_tag.string = json.dumps(structured_data, ensure_ascii=False, indent=2)
        
        head = soup.find("head")
        if head:
            head.append(script_tag)
        
        return soup
    
    def _optimize_internal_linking(
        self, 
        soup: BeautifulSoup, 
        content_context: Optional[Dict[str, Any]] = None
    ) -> BeautifulSoup:
        """Оптимизация внутренней перелинковки"""
        # Находим все ссылки
        links = soup.find_all("a", href=True)
        internal_links = [link for link in links if not link["href"].startswith("http")]
        
        if len(internal_links) < self.auto_fix_config["internal_linking"]["min_links"]:
            # Добавляем предложения для внутренних ссылок
            suggestions = self._generate_internal_link_suggestions(content_context)
            
            # Добавляем блок с рекомендуемыми ссылками
            if suggestions:
                related_section = soup.new_tag("div", attrs={"class": "related-links"})
                related_title = soup.new_tag("h3")
                related_title.string = "Связанные статьи:"
                related_section.append(related_title)
                
                links_list = soup.new_tag("ul")
                for suggestion in suggestions:
                    li = soup.new_tag("li")
                    a = soup.new_tag("a", href=suggestion["url"])
                    a.string = suggestion["title"]
                    li.append(a)
                    links_list.append(li)
                
                related_section.append(links_list)
                
                # Вставляем в конец body
                body = soup.find("body")
                if body:
                    body.append(related_section)
        
        return soup
    
    def _add_open_graph_tags(
        self, 
        soup: BeautifulSoup, 
        content_context: Optional[Dict[str, Any]] = None
    ) -> BeautifulSoup:
        """Добавление Open Graph тегов"""
        if not content_context:
            return soup
        
        head = soup.find("head")
        if not head:
            return soup
        
        og_tags = [
            ("og:title", content_context.get("title", "")),
            ("og:description", content_context.get("description", "")),
            ("og:type", content_context.get("type", "website")),
            ("og:url", content_context.get("url", "")),
            ("og:image", content_context.get("image", "")),
            ("og:site_name", content_context.get("site_name", ""))
        ]
        
        for property_name, content in og_tags:
            if content and not soup.find("meta", attrs={"property": property_name}):
                og_tag = soup.new_tag("meta", attrs={
                    "property": property_name,
                    "content": content
                })
                head.append(og_tag)
        
        return soup
    
    def _optimize_headings_for_keywords(
        self, 
        soup: BeautifulSoup, 
        target_keywords: List[str]
    ) -> BeautifulSoup:
        """Оптимизация заголовков для ключевых слов"""
        headings = soup.find_all(["h2", "h3", "h4", "h5", "h6"])
        
        for i, heading in enumerate(headings):
            text = heading.get_text().strip()
            
            # Если заголовок не содержит ключевых слов, предлагаем улучшение
            if not any(kw.lower() in text.lower() for kw in target_keywords):
                if i < len(target_keywords):
                    # Добавляем ключевое слово в заголовок
                    improved_text = f"{target_keywords[i]}: {text}"
                    heading.string = improved_text
        
        return soup
    
    def _add_breadcrumbs(
        self, 
        soup: BeautifulSoup, 
        content_context: Optional[Dict[str, Any]] = None
    ) -> BeautifulSoup:
        """Добавление хлебных крошек"""
        if not content_context or not content_context.get("breadcrumbs"):
            return soup
        
        breadcrumbs_data = content_context["breadcrumbs"]
        
        # HTML структура хлебных крошек
        nav = soup.new_tag("nav", attrs={"aria-label": "breadcrumb"})
        ol = soup.new_tag("ol", attrs={"class": "breadcrumb"})
        
        for i, crumb in enumerate(breadcrumbs_data):
            li = soup.new_tag("li", attrs={"class": "breadcrumb-item"})
            
            if i == len(breadcrumbs_data) - 1:  # Последний элемент
                li["class"] = "breadcrumb-item active"
                li["aria-current"] = "page"
                li.string = crumb["title"]
            else:
                a = soup.new_tag("a", href=crumb["url"])
                a.string = crumb["title"]
                li.append(a)
            
            ol.append(li)
        
        nav.append(ol)
        
        # JSON-LD для хлебных крошек
        breadcrumb_ld = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "name": crumb["title"],
                    "item": crumb["url"]
                }
                for i, crumb in enumerate(breadcrumbs_data)
            ]
        }
        
        script_tag = soup.new_tag("script", attrs={"type": "application/ld+json"})
        script_tag.string = json.dumps(breadcrumb_ld, ensure_ascii=False)
        
        # Вставляем хлебные крошки в начало body
        body = soup.find("body")
        if body:
            body.insert(0, nav)
            
            # Добавляем JSON-LD в head
            head = soup.find("head")
            if head:
                head.append(script_tag)
        
        return soup
    
    # Вспомогательные методы для генерации контента
    
    def _generate_improved_title(
        self, 
        current_title: str, 
        content_context: Optional[Dict[str, Any]] = None,
        recommendation: Dict = None
    ) -> str:
        """Генерация улучшенного title"""
        if content_context and content_context.get("title"):
            base_title = content_context["title"]
        elif current_title:
            base_title = current_title
        else:
            base_title = "Новая страница"
        
        # Добавляем брендинг если есть
        if content_context and content_context.get("site_name"):
            if len(base_title) + len(content_context["site_name"]) + 3 <= 60:
                return f"{base_title} | {content_context['site_name']}"
        
        # Проверяем длину и корректируем
        if len(base_title) < 30:
            # Добавляем описательные слова
            base_title += " - Полная информация"
        elif len(base_title) > 60:
            # Сокращаем
            base_title = base_title[:57] + "..."
        
        return base_title
    
    def _generate_improved_description(
        self, 
        current_description: str, 
        content_context: Optional[Dict[str, Any]] = None,
        recommendation: Dict = None
    ) -> str:
        """Генерация улучшенного meta description"""
        if content_context and content_context.get("description"):
            base_desc = content_context["description"]
        elif current_description:
            base_desc = current_description
        else:
            # Извлекаем описание из контента
            if content_context and content_context.get("excerpt"):
                base_desc = content_context["excerpt"]
            else:
                base_desc = "Узнайте больше полезной информации на нашем сайте."
        
        # Корректируем длину
        if len(base_desc) < 120:
            base_desc += " Подробные инструкции и советы от экспертов."
        elif len(base_desc) > 160:
            base_desc = base_desc[:157] + "..."
        
        return base_desc
    
    def _generate_h1_text(self, content_context: Optional[Dict[str, Any]] = None) -> str:
        """Генерация текста для H1 заголовка"""
        if content_context and content_context.get("h1"):
            return content_context["h1"]
        elif content_context and content_context.get("title"):
            return content_context["title"]
        else:
            return "Основной заголовок страницы"
    
    def _generate_alt_text(self, img_tag) -> str:
        """Генерация alt текста для изображения"""
        src = img_tag.get("src", "")
        
        # Извлекаем имя файла
        if src:
            filename = src.split("/")[-1].split(".")[0]
            # Заменяем символы на пробелы и делаем читаемым
            alt_text = re.sub(r"[_-]", " ", filename).title()
            return alt_text
        
        return self.auto_fix_config["images"]["default_alt"]
    
    def _generate_internal_link_suggestions(
        self, 
        content_context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, str]]:
        """Генерация предложений для внутренних ссылок"""
        # В реальной реализации здесь будет обращение к базе данных или API
        # для поиска связанного контента
        
        suggestions = []
        
        if content_context and content_context.get("category"):
            suggestions.extend([
                {"url": f"/category/{content_context['category']}", 
                 "title": f"Все статьи в категории {content_context['category']}"},
                {"url": "/", "title": "Главная страница"},
                {"url": "/about", "title": "О нас"}
            ])
        
        return suggestions[:3]  # Максимум 3 предложения
    
    def _generate_changes_report(
        self, 
        original_analysis: Dict, 
        final_analysis: Dict
    ) -> Dict[str, Any]:
        """Генерация отчета об изменениях"""
        improvements = []
        
        # Сравниваем количество проблем
        original_issues = len(original_analysis["recommendations"])
        final_issues = len(final_analysis["recommendations"])
        issues_fixed = original_issues - final_issues
        
        if issues_fixed > 0:
            improvements.append(f"Исправлено {issues_fixed} SEO проблем")
        
        # Сравниваем баллы
        score_improvement = (
            final_analysis["overall_score"] - 
            original_analysis["overall_score"]
        )
        
        if score_improvement > 0:
            improvements.append(f"SEO балл увеличен на {score_improvement} пунктов")
        
        # Анализируем конкретные улучшения
        original_critical = [r for r in original_analysis["recommendations"] 
                           if r["type"] == "critical"]
        final_critical = [r for r in final_analysis["recommendations"] 
                        if r["type"] == "critical"]
        
        critical_fixed = len(original_critical) - len(final_critical)
        if critical_fixed > 0:
            improvements.append(f"Исправлено {critical_fixed} критических проблем")
        
        return {
            "total_improvements": len(improvements),
            "improvements_list": improvements,
            "score_change": score_improvement,
            "issues_remaining": final_issues
        }
    
    def _get_manual_recommendations(self, recommendations: List[Dict]) -> List[Dict]:
        """Получение рекомендаций для ручной проверки"""
        manual_review = []
        
        for rec in recommendations:
            if rec["type"] == "suggestion" or (
                rec["category"] in ["keywords", "linking", "readability"]
            ):
                manual_review.append({
                    "category": rec["category"],
                    "issue": rec["issue"],
                    "recommendation": rec["recommendation"],
                    "priority": rec["type"]
                })
        
        return manual_review
    
    def generate_seo_report(
        self, 
        html: str, 
        target_keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Генерация подробного SEO отчета"""
        analysis = self.advisor.analyze_and_recommend(
            html=html,
            target_keywords=target_keywords
        )
        
        # Группируем рекомендации по категориям
        recommendations_by_category = {}
        for rec in analysis["recommendations"]:
            category = rec["category"]
            if category not in recommendations_by_category:
                recommendations_by_category[category] = []
            recommendations_by_category[category].append(rec)
        
        # Создаем сводку
        summary = {
            "overall_score": analysis["overall_score"],
            "total_recommendations": len(analysis["recommendations"]),
            "critical_issues": len([r for r in analysis["recommendations"] 
                                  if r["type"] == "critical"]),
            "warnings": len([r for r in analysis["recommendations"] 
                           if r["type"] == "warning"]),
            "suggestions": len([r for r in analysis["recommendations"] 
                              if r["type"] == "suggestion"]),
            "top_priorities": analysis["priority_actions"]
        }
        
        return {
            "summary": summary,
            "detailed_analysis": analysis["analysis"],
            "recommendations_by_category": recommendations_by_category,
            "actionable_items": analysis["priority_actions"]
        }
