import re
import json
from typing import Any, Dict, List, Optional, Tuple
from collections import Counter
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import nltk
from textstat import flesch_reading_ease, flesch_kincaid_grade

# Download required NLTK data if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


class SEOAdvisor:
    """
    Интеллектуальный SEO-советник для анализа контента и генерации рекомендаций
    """
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.target_keywords = []
        
        # SEO константы
        self.IDEAL_TITLE_LENGTH = (30, 60)
        self.IDEAL_META_DESC_LENGTH = (120, 160)
        self.IDEAL_H1_COUNT = 1
        self.MIN_CONTENT_LENGTH = 300
        self.IDEAL_KEYWORD_DENSITY = (0.5, 2.5)  # в процентах
        self.IDEAL_READABILITY_SCORE = 60  # Flesch Reading Ease
        self.MAX_SENTENCE_LENGTH = 20  # слов
        self.IDEAL_PARAGRAPH_LENGTH = (50, 150)  # слов
        
    def analyze_and_recommend(
        self, 
        html: str, 
        target_keywords: Optional[List[str]] = None,
        target_audience: str = "general"
    ) -> Dict[str, Any]:
        """
        Комплексный анализ HTML с генерацией персонализированных SEO рекомендаций
        """
        self.target_keywords = target_keywords or []
        soup = BeautifulSoup(html, "html.parser")
        
        # Базовый анализ
        basic_analysis = self._basic_seo_analysis(soup)
        
        # Анализ ключевых слов
        keyword_analysis = self._analyze_keywords(soup)
        
        # Анализ читаемости
        readability_analysis = self._analyze_readability(soup)
        
        # Анализ структуры контента
        structure_analysis = self._analyze_content_structure(soup)
        
        # Анализ внутренней перелинковки
        linking_analysis = self._analyze_internal_linking(soup)
        
        # Технический SEO анализ
        technical_analysis = self._analyze_technical_seo(soup)
        
        # Генерация рекомендаций
        recommendations = self._generate_recommendations(
            basic_analysis,
            keyword_analysis,
            readability_analysis,
            structure_analysis,
            linking_analysis,
            technical_analysis,
            target_audience
        )
        
        # Расчет приоритетов рекомендаций
        prioritized_recommendations = self._prioritize_recommendations(recommendations)
        
        # Автоматическая генерация улучшенного HTML
        improved_html = self._auto_improve_html(html, recommendations)
        
        return {
            "analysis": {
                "basic": basic_analysis,
                "keywords": keyword_analysis,
                "readability": readability_analysis,
                "structure": structure_analysis,
                "linking": linking_analysis,
                "technical": technical_analysis
            },
            "recommendations": prioritized_recommendations,
            "improved_html": improved_html,
            "overall_score": self._calculate_overall_score(
                basic_analysis, keyword_analysis, readability_analysis,
                structure_analysis, technical_analysis
            ),
            "priority_actions": self._get_priority_actions(prioritized_recommendations)
        }
    
    def _basic_seo_analysis(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Базовый SEO анализ"""
        # Анализ title
        title_tag = soup.find("title")
        title_analysis = {
            "exists": bool(title_tag),
            "text": title_tag.get_text().strip() if title_tag else "",
            "length": len(title_tag.get_text().strip()) if title_tag else 0,
            "issues": []
        }
        
        if not title_tag:
            title_analysis["issues"].append("Отсутствует тег title")
        elif title_analysis["length"] < self.IDEAL_TITLE_LENGTH[0]:
            title_analysis["issues"].append(f"Title слишком короткий (< {self.IDEAL_TITLE_LENGTH[0]} символов)")
        elif title_analysis["length"] > self.IDEAL_TITLE_LENGTH[1]:
            title_analysis["issues"].append(f"Title слишком длинный (> {self.IDEAL_TITLE_LENGTH[1]} символов)")
        
        # Анализ meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        desc_analysis = {
            "exists": bool(meta_desc),
            "text": meta_desc.get("content", "").strip() if meta_desc else "",
            "length": len(meta_desc.get("content", "").strip()) if meta_desc else 0,
            "issues": []
        }
        
        if not meta_desc:
            desc_analysis["issues"].append("Отсутствует meta description")
        elif desc_analysis["length"] < self.IDEAL_META_DESC_LENGTH[0]:
            desc_analysis["issues"].append(f"Meta description слишком короткое (< {self.IDEAL_META_DESC_LENGTH[0]} символов)")
        elif desc_analysis["length"] > self.IDEAL_META_DESC_LENGTH[1]:
            desc_analysis["issues"].append(f"Meta description слишком длинное (> {self.IDEAL_META_DESC_LENGTH[1]} символов)")
        
        # Анализ заголовков
        headings_analysis = self._analyze_headings_structure(soup)
        
        # Анализ изображений
        images_analysis = self._analyze_images_seo(soup)
        
        return {
            "title": title_analysis,
            "meta_description": desc_analysis,
            "headings": headings_analysis,
            "images": images_analysis
        }
    
    def _analyze_keywords(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Анализ плотности ключевых слов и их распределения"""
        # Извлекаем текстовый контент
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalpha() and word not in self.stop_words]
        
        total_words = len(words)
        word_freq = Counter(words)
        
        # Анализ заданных ключевых слов
        keyword_analysis = {}
        for keyword in self.target_keywords:
            keyword_lower = keyword.lower()
            count = text.lower().count(keyword_lower)
            density = (count / total_words * 100) if total_words > 0 else 0
            
            keyword_analysis[keyword] = {
                "count": count,
                "density": density,
                "in_title": keyword_lower in soup.find("title").get_text().lower() if soup.find("title") else False,
                "in_h1": any(keyword_lower in h1.get_text().lower() for h1 in soup.find_all("h1")),
                "in_meta_desc": keyword_lower in (soup.find("meta", attrs={"name": "description"}).get("content", "").lower() if soup.find("meta", attrs={"name": "description"}) else ""),
                "first_occurrence": self._find_first_occurrence_position(text, keyword_lower)
            }
        
        # Топ ключевые слова в контенте
        top_keywords = [word for word, count in word_freq.most_common(10) if len(word) > 3]
        
        return {
            "total_words": total_words,
            "unique_words": len(word_freq),
            "target_keywords": keyword_analysis,
            "top_keywords": top_keywords,
            "keyword_stuffing_risk": self._detect_keyword_stuffing(word_freq, total_words)
        }
    
    def _analyze_readability(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Анализ читаемости контента"""
        # Извлекаем основной текстовый контент
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        
        # Базовые метрики
        total_sentences = len(sentences)
        total_words = len([word for word in words if word.isalpha()])
        avg_sentence_length = total_words / total_sentences if total_sentences > 0 else 0
        
        # Анализ длины предложений
        long_sentences = [s for s in sentences if len(word_tokenize(s)) > self.MAX_SENTENCE_LENGTH]
        
        # Показатели читаемости
        flesch_score = flesch_reading_ease(text) if text else 0
        fk_grade = flesch_kincaid_grade(text) if text else 0
        
        # Анализ абзацев
        paragraphs = soup.find_all("p")
        paragraph_analysis = self._analyze_paragraphs(paragraphs)
        
        return {
            "flesch_reading_ease": flesch_score,
            "flesch_kincaid_grade": fk_grade,
            "avg_sentence_length": avg_sentence_length,
            "long_sentences_count": len(long_sentences),
            "total_sentences": total_sentences,
            "readability_level": self._classify_readability(flesch_score),
            "paragraphs": paragraph_analysis
        }
    
    def _analyze_content_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Анализ структуры контента"""
        # Анализ заголовков
        headings_hierarchy = []
        current_level = 0
        
        for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
            level = int(heading.name[1])
            text = heading.get_text().strip()
            
            headings_hierarchy.append({
                "level": level,
                "text": text,
                "length": len(text),
                "has_keywords": any(kw.lower() in text.lower() for kw in self.target_keywords)
            })
            
            if level > current_level + 1:
                # Пропуск уровней заголовков
                pass
            current_level = level
        
        # Анализ списков
        lists = soup.find_all(["ul", "ol"])
        list_analysis = {
            "total_lists": len(lists),
            "unordered_lists": len(soup.find_all("ul")),
            "ordered_lists": len(soup.find_all("ol")),
            "total_list_items": len(soup.find_all("li"))
        }
        
        # Анализ таблиц
        tables = soup.find_all("table")
        table_analysis = {
            "total_tables": len(tables),
            "tables_with_headers": len([t for t in tables if t.find("th")]),
            "tables_with_captions": len([t for t in tables if t.find("caption")])
        }
        
        return {
            "headings_hierarchy": headings_hierarchy,
            "lists": list_analysis,
            "tables": table_analysis,
            "structure_score": self._calculate_structure_score(headings_hierarchy, list_analysis)
        }
    
    def _analyze_internal_linking(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Анализ внутренней перелинковки"""
        links = soup.find_all("a", href=True)
        
        internal_links = []
        external_links = []
        
        for link in links:
            href = link["href"]
            text = link.get_text().strip()
            
            if href.startswith("http"):
                parsed = urlparse(href)
                external_links.append({
                    "url": href,
                    "text": text,
                    "domain": parsed.netloc
                })
            else:
                internal_links.append({
                    "url": href,
                    "text": text,
                    "is_anchor": href.startswith("#")
                })
        
        # Анализ якорного текста
        anchor_texts = [link["text"] for link in internal_links if link["text"]]
        anchor_keyword_usage = sum(1 for text in anchor_texts 
                                  if any(kw.lower() in text.lower() for kw in self.target_keywords))
        
        return {
            "total_links": len(links),
            "internal_links": len(internal_links),
            "external_links": len(external_links),
            "anchor_links": len([l for l in internal_links if l["is_anchor"]]),
            "anchor_keyword_usage": anchor_keyword_usage,
            "link_density": len(links) / len(soup.get_text().split()) if soup.get_text() else 0,
            "internal_link_details": internal_links[:10],  # Первые 10 для анализа
            "external_domains": list(set(link["domain"] for link in external_links))
        }
    
    def _analyze_technical_seo(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Технический SEO анализ"""
        # Анализ meta тегов
        meta_tags = soup.find_all("meta")
        meta_analysis = {
            "total_meta_tags": len(meta_tags),
            "has_viewport": bool(soup.find("meta", attrs={"name": "viewport"})),
            "has_charset": bool(soup.find("meta", attrs={"charset": True})),
            "has_robots": bool(soup.find("meta", attrs={"name": "robots"})),
            "has_canonical": bool(soup.find("link", attrs={"rel": "canonical"})),
            "has_og_tags": len(soup.find_all("meta", attrs={"property": re.compile("^og:")})),
            "has_twitter_cards": len(soup.find_all("meta", attrs={"name": re.compile("^twitter:")}))
        }
        
        # Анализ структурированных данных
        json_ld_scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
        structured_data = {
            "json_ld_count": len(json_ld_scripts),
            "microdata_items": len(soup.find_all(attrs={"itemtype": True})),
            "has_schema_org": any("schema.org" in script.get_text() for script in json_ld_scripts)
        }
        
        # Анализ изображений
        images = soup.find_all("img")
        image_seo = {
            "total_images": len(images),
            "images_with_alt": len([img for img in images if img.get("alt")]),
            "images_with_title": len([img for img in images if img.get("title")]),
            "images_with_lazy_loading": len([img for img in images if img.get("loading") == "lazy"])
        }
        
        return {
            "meta_tags": meta_analysis,
            "structured_data": structured_data,
            "images": image_seo,
            "has_lang_attribute": bool(soup.find("html", attrs={"lang": True}))
        }
    
    def _generate_recommendations(
        self, 
        basic: Dict, 
        keywords: Dict, 
        readability: Dict, 
        structure: Dict, 
        linking: Dict, 
        technical: Dict,
        target_audience: str
    ) -> List[Dict[str, Any]]:
        """Генерация персонализированных рекомендаций"""
        recommendations = []
        
        # Рекомендации по title
        if basic["title"]["issues"]:
            recommendations.extend(self._generate_title_recommendations(basic["title"], keywords))
        
        # Рекомендации по meta description
        if basic["meta_description"]["issues"]:
            recommendations.extend(self._generate_meta_desc_recommendations(basic["meta_description"]))
        
        # Рекомендации по заголовкам
        recommendations.extend(self._generate_heading_recommendations(basic["headings"], structure))
        
        # Рекомендации по ключевым словам
        recommendations.extend(self._generate_keyword_recommendations(keywords))
        
        # Рекомендации по читаемости
        recommendations.extend(self._generate_readability_recommendations(readability, target_audience))
        
        # Рекомендации по внутренней перелинковке
        recommendations.extend(self._generate_linking_recommendations(linking))
        
        # Технические рекомендации
        recommendations.extend(self._generate_technical_recommendations(technical))
        
        # Рекомендации по изображениям
        recommendations.extend(self._generate_image_recommendations(basic["images"]))
        
        return recommendations
    
    def _generate_title_recommendations(self, title_analysis: Dict, keywords: Dict) -> List[Dict]:
        """Генерация рекомендаций по title"""
        recommendations = []
        
        if not title_analysis["exists"]:
            recommendations.append({
                "type": "critical",
                "category": "title",
                "issue": "Отсутствует тег title",
                "recommendation": "Добавьте уникальный и описательный тег title",
                "example": f"<title>Ваш основной заголовок - Название сайта</title>",
                "impact": "high"
            })
        elif title_analysis["length"] < self.IDEAL_TITLE_LENGTH[0]:
            recommendations.append({
                "type": "warning",
                "category": "title",
                "issue": f"Title слишком короткий ({title_analysis['length']} символов)",
                "recommendation": f"Расширьте title до {self.IDEAL_TITLE_LENGTH[0]}-{self.IDEAL_TITLE_LENGTH[1]} символов",
                "example": self._suggest_improved_title(title_analysis["text"], keywords),
                "impact": "medium"
            })
        elif title_analysis["length"] > self.IDEAL_TITLE_LENGTH[1]:
            recommendations.append({
                "type": "warning",
                "category": "title",
                "issue": f"Title слишком длинный ({title_analysis['length']} символов)",
                "recommendation": f"Сократите title до {self.IDEAL_TITLE_LENGTH[1]} символов или менее",
                "example": self._suggest_shortened_title(title_analysis["text"]),
                "impact": "medium"
            })
        
        # Проверка использования ключевых слов в title
        if self.target_keywords and not any(kw.lower() in title_analysis["text"].lower() for kw in self.target_keywords):
            recommendations.append({
                "type": "suggestion",
                "category": "title",
                "issue": "Ключевые слова не используются в title",
                "recommendation": "Включите основное ключевое слово в начало title",
                "example": f"{self.target_keywords[0]} - {title_analysis['text']}" if self.target_keywords else "",
                "impact": "medium"
            })
        
        return recommendations
    
    def _auto_improve_html(self, html: str, recommendations: List[Dict]) -> str:
        """Автоматическое улучшение HTML на основе рекомендаций"""
        soup = BeautifulSoup(html, "html.parser")
        
        for rec in recommendations:
            if rec["type"] == "critical" and rec["category"] == "title":
                # Автоматически добавляем title если его нет
                if not soup.find("title"):
                    head = soup.find("head")
                    if head:
                        title_tag = soup.new_tag("title")
                        title_tag.string = "Новая страница"  # Базовый title
                        head.insert(0, title_tag)
            
            elif rec["category"] == "meta_description":
                # Автоматически добавляем meta description
                if not soup.find("meta", attrs={"name": "description"}):
                    head = soup.find("head")
                    if head:
                        meta_tag = soup.new_tag("meta", attrs={
                            "name": "description", 
                            "content": "Описание страницы"
                        })
                        head.append(meta_tag)
            
            elif rec["category"] == "images":
                # Автоматически добавляем alt к изображениям
                for img in soup.find_all("img"):
                    if not img.get("alt"):
                        img["alt"] = "Изображение"
        
        return str(soup)
    
    # Вспомогательные методы
    
    def _analyze_headings_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Анализ структуры заголовков"""
        headings = {f"h{i}": [] for i in range(1, 7)}
        
        for i in range(1, 7):
            tags = soup.find_all(f"h{i}")
            headings[f"h{i}"] = [tag.get_text().strip() for tag in tags]
        
        issues = []
        h1_count = len(headings["h1"])
        
        if h1_count == 0:
            issues.append("Отсутствует H1 заголовок")
        elif h1_count > 1:
            issues.append(f"Найдено {h1_count} H1 заголовков (рекомендуется 1)")
        
        # Проверка логической последовательности
        prev_level = 0
        for i in range(1, 7):
            if headings[f"h{i}"]:
                if i > prev_level + 1:
                    issues.append(f"Пропущен уровень заголовка H{prev_level + 1}")
                prev_level = i
        
        return {
            "structure": headings,
            "h1_count": h1_count,
            "total_headings": sum(len(h) for h in headings.values()),
            "issues": issues,
            "keyword_usage": self._check_keyword_usage_in_headings(headings)
        }
    
    def _analyze_images_seo(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Анализ SEO изображений"""
        images = soup.find_all("img")
        
        total_images = len(images)
        missing_alt = 0
        empty_alt = 0
        missing_title = 0
        
        for img in images:
            alt = img.get("alt")
            title = img.get("title")
            
            if alt is None:
                missing_alt += 1
            elif alt.strip() == "":
                empty_alt += 1
            
            if title is None:
                missing_title += 1
        
        issues = []
        if missing_alt > 0:
            issues.append(f"{missing_alt} изображений без alt атрибута")
        if empty_alt > 0:
            issues.append(f"{empty_alt} изображений с пустым alt атрибутом")
        
        return {
            "total": total_images,
            "missing_alt": missing_alt,
            "empty_alt": empty_alt,
            "missing_title": missing_title,
            "issues": issues
        }
    
    def _find_first_occurrence_position(self, text: str, keyword: str) -> int:
        """Находит позицию первого вхождения ключевого слова в тексте (в процентах)"""
        pos = text.lower().find(keyword.lower())
        if pos == -1:
            return -1
        return int((pos / len(text)) * 100) if text else -1
    
    def _detect_keyword_stuffing(self, word_freq: Counter, total_words: int) -> Dict[str, Any]:
        """Обнаружение переспама ключевых слов"""
        risk_words = []
        
        for word, count in word_freq.most_common(20):
            density = (count / total_words * 100) if total_words > 0 else 0
            if density > self.IDEAL_KEYWORD_DENSITY[1]:
                risk_words.append({
                    "word": word,
                    "count": count,
                    "density": density
                })
        
        return {
            "risk_level": "high" if len(risk_words) > 3 else "medium" if len(risk_words) > 1 else "low",
            "problematic_words": risk_words
        }
    
    def _classify_readability(self, flesch_score: float) -> str:
        """Классификация уровня читаемости"""
        if flesch_score >= 90:
            return "Очень легко"
        elif flesch_score >= 80:
            return "Легко"
        elif flesch_score >= 70:
            return "Довольно легко"
        elif flesch_score >= 60:
            return "Стандартно"
        elif flesch_score >= 50:
            return "Довольно сложно"
        elif flesch_score >= 30:
            return "Сложно"
        else:
            return "Очень сложно"
    
    def _analyze_paragraphs(self, paragraphs) -> Dict[str, Any]:
        """Анализ структуры абзацев"""
        if not paragraphs:
            return {"count": 0, "avg_length": 0, "issues": ["Нет абзацев"]}
        
        word_counts = []
        for p in paragraphs:
            text = p.get_text().strip()
            word_count = len(text.split())
            word_counts.append(word_count)
        
        avg_length = sum(word_counts) / len(word_counts) if word_counts else 0
        
        issues = []
        if avg_length > self.IDEAL_PARAGRAPH_LENGTH[1]:
            issues.append("Слишком длинные абзацы")
        elif avg_length < self.IDEAL_PARAGRAPH_LENGTH[0]:
            issues.append("Слишком короткие абзацы")
        
        return {
            "count": len(paragraphs),
            "avg_length": avg_length,
            "max_length": max(word_counts) if word_counts else 0,
            "min_length": min(word_counts) if word_counts else 0,
            "issues": issues
        }
    
    def _calculate_structure_score(self, headings_hierarchy: List, list_analysis: Dict) -> int:
        """Расчет оценки структуры контента"""
        score = 100
        
        # Штраф за отсутствие заголовков
        if not headings_hierarchy:
            score -= 30
        
        # Штраф за неправильную иерархию
        prev_level = 0
        for heading in headings_hierarchy:
            if heading["level"] > prev_level + 1:
                score -= 10
            prev_level = heading["level"]
        
        # Бонус за использование списков
        if list_analysis["total_lists"] > 0:
            score += 5
        
        return max(0, score)
    
    def _check_keyword_usage_in_headings(self, headings: Dict) -> Dict[str, Any]:
        """Проверка использования ключевых слов в заголовках"""
        usage = {f"h{i}": 0 for i in range(1, 7)}
        
        for level, heading_list in headings.items():
            for heading_text in heading_list:
                if any(kw.lower() in heading_text.lower() for kw in self.target_keywords):
                    usage[level] += 1
        
        return usage
    
    def _suggest_improved_title(self, current_title: str, keywords: Dict) -> str:
        """Предложение улучшенного title"""
        if self.target_keywords and current_title:
            return f"{self.target_keywords[0]} | {current_title}"
        elif self.target_keywords:
            return f"{self.target_keywords[0]} - Ваше описание"
        else:
            return f"{current_title} - Дополнительное описание"
    
    def _suggest_shortened_title(self, current_title: str) -> str:
        """Предложение сокращенного title"""
        if len(current_title) <= self.IDEAL_TITLE_LENGTH[1]:
            return current_title
        return current_title[:self.IDEAL_TITLE_LENGTH[1]-3] + "..."
    
    def _generate_meta_desc_recommendations(self, meta_desc: Dict) -> List[Dict]:
        """Генерация рекомендаций по meta description"""
        recommendations = []
        
        if not meta_desc["exists"]:
            recommendations.append({
                "type": "critical",
                "category": "meta_description",
                "issue": "Отсутствует meta description",
                "recommendation": "Добавьте уникальное и привлекательное описание страницы",
                "example": '<meta name="description" content="Краткое описание содержимого страницы">',
                "impact": "high"
            })
        elif meta_desc["length"] < self.IDEAL_META_DESC_LENGTH[0]:
            recommendations.append({
                "type": "warning",
                "category": "meta_description",
                "issue": f"Meta description слишком короткое ({meta_desc['length']} символов)",
                "recommendation": f"Расширьте до {self.IDEAL_META_DESC_LENGTH[0]}-{self.IDEAL_META_DESC_LENGTH[1]} символов",
                "impact": "medium"
            })
        
        return recommendations
    
    def _generate_heading_recommendations(self, headings: Dict, structure: Dict) -> List[Dict]:
        """Генерация рекомендаций по заголовкам"""
        recommendations = []
        
        for issue in headings["issues"]:
            if "Отсутствует H1" in issue:
                recommendations.append({
                    "type": "critical",
                    "category": "headings",
                    "issue": issue,
                    "recommendation": "Добавьте единственный H1 заголовок, описывающий основную тему страницы",
                    "example": "<h1>Основной заголовок страницы</h1>",
                    "impact": "high"
                })
            elif "H1 заголовков" in issue:
                recommendations.append({
                    "type": "warning",
                    "category": "headings",
                    "issue": issue,
                    "recommendation": "Используйте только один H1 заголовок на странице",
                    "impact": "medium"
                })
        
        return recommendations
    
    def _generate_keyword_recommendations(self, keywords: Dict) -> List[Dict]:
        """Генерация рекомендаций по ключевым словам"""
        recommendations = []
        
        for keyword, analysis in keywords["target_keywords"].items():
            if analysis["density"] < self.IDEAL_KEYWORD_DENSITY[0]:
                recommendations.append({
                    "type": "suggestion",
                    "category": "keywords",
                    "issue": f"Низкая плотность ключевого слова '{keyword}' ({analysis['density']:.1f}%)",
                    "recommendation": f"Увеличьте использование ключевого слова до {self.IDEAL_KEYWORD_DENSITY[0]}-{self.IDEAL_KEYWORD_DENSITY[1]}%",
                    "impact": "medium"
                })
            elif analysis["density"] > self.IDEAL_KEYWORD_DENSITY[1]:
                recommendations.append({
                    "type": "warning",
                    "category": "keywords",
                    "issue": f"Переспам ключевого слова '{keyword}' ({analysis['density']:.1f}%)",
                    "recommendation": f"Снизьте использование ключевого слова до {self.IDEAL_KEYWORD_DENSITY[1]}% или менее",
                    "impact": "medium"
                })
        
        if keywords["keyword_stuffing_risk"]["risk_level"] == "high":
            recommendations.append({
                "type": "warning",
                "category": "keywords",
                "issue": "Высокий риск переспама ключевых слов",
                "recommendation": "Используйте синонимы и связанные термины для естественного текста",
                "impact": "high"
            })
        
        return recommendations
    
    def _generate_readability_recommendations(self, readability: Dict, target_audience: str) -> List[Dict]:
        """Генерация рекомендаций по читаемости"""
        recommendations = []
        
        target_score = 60 if target_audience == "general" else 50 if target_audience == "professional" else 70
        
        if readability["flesch_reading_ease"] < target_score:
            recommendations.append({
                "type": "suggestion",
                "category": "readability",
                "issue": f"Низкая читаемость ({readability['flesch_reading_ease']:.1f})",
                "recommendation": "Упростите текст: используйте короткие предложения и простые слова",
                "impact": "medium"
            })
        
        if readability["avg_sentence_length"] > self.MAX_SENTENCE_LENGTH:
            recommendations.append({
                "type": "suggestion",
                "category": "readability",
                "issue": f"Слишком длинные предложения (в среднем {readability['avg_sentence_length']:.1f} слов)",
                "recommendation": f"Сократите предложения до {self.MAX_SENTENCE_LENGTH} слов или менее",
                "impact": "medium"
            })
        
        return recommendations
    
    def _generate_linking_recommendations(self, linking: Dict) -> List[Dict]:
        """Генерация рекомендаций по внутренней перелинковке"""
        recommendations = []
        
        if linking["internal_links"] < 3:
            recommendations.append({
                "type": "suggestion",
                "category": "linking",
                "issue": f"Мало внутренних ссылок ({linking['internal_links']})",
                "recommendation": "Добавьте 3-5 внутренних ссылок на связанные страницы",
                "impact": "medium"
            })
        
        if linking["anchor_keyword_usage"] == 0 and self.target_keywords:
            recommendations.append({
                "type": "suggestion",
                "category": "linking",
                "issue": "Ключевые слова не используются в якорном тексте ссылок",
                "recommendation": "Используйте ключевые слова в тексте внутренних ссылок",
                "impact": "low"
            })
        
        return recommendations
    
    def _generate_technical_recommendations(self, technical: Dict) -> List[Dict]:
        """Генерация технических рекомендаций"""
        recommendations = []
        
        if not technical["meta_tags"]["has_viewport"]:
            recommendations.append({
                "type": "warning",
                "category": "technical",
                "issue": "Отсутствует viewport meta тег",
                "recommendation": "Добавьте viewport meta тег для мобильной адаптации",
                "example": '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                "impact": "high"
            })
        
        if not technical["has_lang_attribute"]:
            recommendations.append({
                "type": "warning",
                "category": "technical",
                "issue": "Отсутствует атрибут lang у тега html",
                "recommendation": "Добавьте атрибут lang для указания языка страницы",
                "example": '<html lang="ru">',
                "impact": "medium"
            })
        
        if technical["structured_data"]["json_ld_count"] == 0:
            recommendations.append({
                "type": "suggestion",
                "category": "technical",
                "issue": "Отсутствуют структурированные данные",
                "recommendation": "Добавьте JSON-LD разметку для лучшего понимания поисковиками",
                "impact": "medium"
            })
        
        return recommendations
    
    def _generate_image_recommendations(self, images: Dict) -> List[Dict]:
        """Генерация рекомендаций по изображениям"""
        recommendations = []
        
        if images["missing_alt"] > 0:
            recommendations.append({
                "type": "warning",
                "category": "images",
                "issue": f"{images['missing_alt']} изображений без alt атрибута",
                "recommendation": "Добавьте описательные alt атрибуты ко всем изображениям",
                "example": '<img src="image.jpg" alt="Описание изображения">',
                "impact": "medium"
            })
        
        return recommendations
    
    def _prioritize_recommendations(self, recommendations: List[Dict]) -> List[Dict]:
        """Приоритизация рекомендаций"""
        priority_order = {"critical": 0, "warning": 1, "suggestion": 2}
        impact_order = {"high": 0, "medium": 1, "low": 2}
        
        return sorted(recommendations, key=lambda x: (
            priority_order.get(x["type"], 3),
            impact_order.get(x["impact"], 3)
        ))
    
    def _calculate_overall_score(self, basic: Dict, keywords: Dict, readability: Dict, structure: Dict, technical: Dict) -> int:
        """Расчет общей SEO оценки"""
        score = 100
        
        # Базовые элементы (30 баллов)
        if basic["title"]["issues"]:
            score -= 15
        if basic["meta_description"]["issues"]:
            score -= 15
        
        # Заголовки (15 баллов)
        if basic["headings"]["issues"]:
            score -= 15
        
        # Ключевые слова (20 баллов)
        if keywords["keyword_stuffing_risk"]["risk_level"] == "high":
            score -= 20
        elif keywords["keyword_stuffing_risk"]["risk_level"] == "medium":
            score -= 10
        
        # Читаемость (15 баллов)
        if readability["flesch_reading_ease"] < 60:
            score -= 15
        
        # Технические аспекты (10 баллов)
        if not technical["meta_tags"]["has_viewport"]:
            score -= 5
        if not technical["has_lang_attribute"]:
            score -= 5
        
        # Изображения (10 баллов)
        if basic["images"]["missing_alt"] > 0:
            score -= 10
        
        return max(0, score)
    
    def _get_priority_actions(self, recommendations: List[Dict]) -> List[str]:
        """Получение приоритетных действий"""
        critical_actions = [rec["recommendation"] for rec in recommendations 
                           if rec["type"] == "critical"]
        high_impact_actions = [rec["recommendation"] for rec in recommendations 
                              if rec["impact"] == "high" and rec["type"] != "critical"]
        
        return critical_actions + high_impact_actions[:3]  # Максимум 3 дополнительных действия
