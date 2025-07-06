#!/usr/bin/env python3
"""
SEO Cross-Testing System
========================

Система для проведения кросс-тестов новых возможностей SEO агента.
Включает валидацию через Lighthouse, SEO-анализаторы, Google Structured Data Testing Tool.
"""

import asyncio
import json
import os
import subprocess
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import requests
from dataclasses import dataclass
from pathlib import Path
import tempfile
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class SEOTestResult:
    """Результат SEO теста"""
    url: str
    test_type: str
    score: float
    issues: List[str]
    recommendations: List[str]
    raw_data: Dict[str, Any]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'url': self.url,
            'test_type': self.test_type,
            'score': self.score,
            'issues': self.issues,
            'recommendations': self.recommendations,
            'raw_data': self.raw_data,
            'timestamp': self.timestamp.isoformat()
        }

class LighthouseAnalyzer:
    """Анализатор Lighthouse для SEO метрик"""
    
    def __init__(self):
        self.lighthouse_cli = self._check_lighthouse_installation()
    
    def _check_lighthouse_installation(self) -> bool:
        """Проверка установки Lighthouse CLI"""
        try:
            subprocess.run(['lighthouse', '--version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("Lighthouse CLI не найден. Установите: npm install -g lighthouse")
            return False
    
    async def analyze_page(self, url: str) -> SEOTestResult:
        """Анализ страницы через Lighthouse"""
        if not self.lighthouse_cli:
            return SEOTestResult(
                url=url,
                test_type="lighthouse",
                score=0.0,
                issues=["Lighthouse CLI не установлен"],
                recommendations=["Установите Lighthouse CLI: npm install -g lighthouse"],
                raw_data={},
                timestamp=datetime.now()
            )
        
        try:
            # Создаем временный файл для результатов
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
                tmp_path = tmp_file.name
            
            # Запускаем Lighthouse
            cmd = [
                'lighthouse',
                url,
                '--output=json',
                '--output-path=' + tmp_path,
                '--only-categories=seo',
                '--chrome-flags=--headless',
                '--quiet'
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                logger.error(f"Lighthouse error: {stderr.decode()}")
                return SEOTestResult(
                    url=url,
                    test_type="lighthouse",
                    score=0.0,
                    issues=[f"Lighthouse error: {stderr.decode()}"],
                    recommendations=["Проверьте URL и доступность страницы"],
                    raw_data={},
                    timestamp=datetime.now()
                )
            
            # Читаем результаты
            with open(tmp_path, 'r') as f:
                lighthouse_data = json.load(f)
            
            # Очищаем временный файл
            os.unlink(tmp_path)
            
            return self._parse_lighthouse_results(url, lighthouse_data)
            
        except Exception as e:
            logger.error(f"Lighthouse analysis error: {str(e)}")
            return SEOTestResult(
                url=url,
                test_type="lighthouse",
                score=0.0,
                issues=[f"Ошибка анализа: {str(e)}"],
                recommendations=["Проверьте конфигурацию Lighthouse"],
                raw_data={},
                timestamp=datetime.now()
            )
    
    def _parse_lighthouse_results(self, url: str, data: Dict[str, Any]) -> SEOTestResult:
        """Парсинг результатов Lighthouse"""
        seo_category = data.get('categories', {}).get('seo', {})
        seo_score = seo_category.get('score', 0) * 100 if seo_category.get('score') else 0
        
        issues = []
        recommendations = []
        
        # Анализируем аудиты SEO
        audits = data.get('audits', {})
        seo_audits = [
            'document-title', 'meta-description', 'http-status-code',
            'link-text', 'crawlable-anchors', 'is-crawlable',
            'robots-txt', 'image-alt', 'hreflang', 'canonical'
        ]
        
        for audit_id in seo_audits:
            audit = audits.get(audit_id, {})
            if audit.get('score', 1) < 1:
                issues.append(audit.get('title', audit_id))
                if audit.get('description'):
                    recommendations.append(audit.get('description'))
        
        return SEOTestResult(
            url=url,
            test_type="lighthouse",
            score=seo_score,
            issues=issues,
            recommendations=recommendations,
            raw_data=data,
            timestamp=datetime.now()
        )

class StructuredDataAnalyzer:
    """Анализатор структурированных данных (Schema.org)"""
    
    def __init__(self):
        self.google_api_url = "https://search.google.com/structured-data/testing-tool/validate"
        self.schema_org_validator = "https://validator.schema.org/"
    
    async def analyze_page(self, url: str) -> SEOTestResult:
        """Анализ структурированных данных"""
        try:
            # Получаем HTML страницы
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            html_content = response.text
            
            # Извлекаем структурированные данные
            structured_data = self._extract_structured_data(html_content)
            
            # Валидируем структурированные данные
            validation_results = await self._validate_structured_data(structured_data)
            
            score = self._calculate_structured_data_score(validation_results)
            
            return SEOTestResult(
                url=url,
                test_type="structured_data",
                score=score,
                issues=validation_results.get('errors', []),
                recommendations=validation_results.get('recommendations', []),
                raw_data=validation_results,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Structured data analysis error: {str(e)}")
            return SEOTestResult(
                url=url,
                test_type="structured_data",
                score=0.0,
                issues=[f"Ошибка анализа: {str(e)}"],
                recommendations=["Проверьте доступность URL"],
                raw_data={},
                timestamp=datetime.now()
            )
    
    def _extract_structured_data(self, html_content: str) -> Dict[str, Any]:
        """Извлечение структурированных данных из HTML"""
        import re
        
        # Извлекаем JSON-LD
        json_ld_pattern = r'<script type="application/ld\+json"[^>]*>(.*?)</script>'
        json_ld_matches = re.findall(json_ld_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        structured_data = {
            'json_ld': [],
            'microdata': [],
            'rdfa': []
        }
        
        for match in json_ld_matches:
            try:
                data = json.loads(match.strip())
                structured_data['json_ld'].append(data)
            except json.JSONDecodeError:
                continue
        
        # Извлекаем микроданные (упрощенно)
        microdata_pattern = r'itemscope[^>]*itemtype="([^"]*)"'
        microdata_matches = re.findall(microdata_pattern, html_content, re.IGNORECASE)
        structured_data['microdata'] = list(set(microdata_matches))
        
        return structured_data
    
    async def _validate_structured_data(self, structured_data: Dict[str, Any]) -> Dict[str, Any]:
        """Валидация структурированных данных"""
        results = {
            'errors': [],
            'warnings': [],
            'recommendations': [],
            'valid_schemas': [],
            'invalid_schemas': []
        }
        
        # Проверяем JSON-LD
        for json_ld in structured_data.get('json_ld', []):
            schema_type = json_ld.get('@type', 'Unknown')
            
            # Базовая валидация
            if '@context' not in json_ld:
                results['errors'].append(f"Отсутствует @context в {schema_type}")
            
            if '@type' not in json_ld:
                results['errors'].append("Отсутствует @type в JSON-LD")
            else:
                results['valid_schemas'].append(schema_type)
        
        # Рекомендации по улучшению
        if not structured_data.get('json_ld'):
            results['recommendations'].append("Добавьте JSON-LD разметку для лучшей SEO")
        
        if len(structured_data.get('json_ld', [])) > 0:
            results['recommendations'].append("Проверьте все обязательные поля в Schema.org")
        
        return results
    
    def _calculate_structured_data_score(self, validation_results: Dict[str, Any]) -> float:
        """Расчет оценки структурированных данных"""
        base_score = 100.0
        
        # Вычитаем за ошибки
        errors_count = len(validation_results.get('errors', []))
        warnings_count = len(validation_results.get('warnings', []))
        
        score = base_score - (errors_count * 20) - (warnings_count * 5)
        
        # Бонус за наличие структурированных данных
        valid_schemas = len(validation_results.get('valid_schemas', []))
        if valid_schemas > 0:
            score += min(valid_schemas * 10, 30)
        
        return max(0.0, min(100.0, score))

class ComprehensiveSEOAnalyzer:
    """Комплексный анализатор SEO"""
    
    def __init__(self):
        self.basic_checks = [
            'title_tag', 'meta_description', 'h1_tag', 'alt_attributes',
            'canonical_url', 'robots_meta', 'sitemap_xml', 'robots_txt'
        ]
    
    async def analyze_page(self, url: str) -> SEOTestResult:
        """Комплексный анализ SEO"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            html_content = response.text
            
            # Проводим различные проверки
            analysis_results = {
                'title_analysis': self._analyze_title(html_content),
                'meta_analysis': self._analyze_meta_tags(html_content),
                'heading_analysis': self._analyze_headings(html_content),
                'image_analysis': self._analyze_images(html_content),
                'link_analysis': self._analyze_links(html_content),
                'content_analysis': self._analyze_content(html_content)
            }
            
            score = self._calculate_comprehensive_score(analysis_results)
            issues = self._extract_issues(analysis_results)
            recommendations = self._extract_recommendations(analysis_results)
            
            return SEOTestResult(
                url=url,
                test_type="comprehensive_seo",
                score=score,
                issues=issues,
                recommendations=recommendations,
                raw_data=analysis_results,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Comprehensive SEO analysis error: {str(e)}")
            return SEOTestResult(
                url=url,
                test_type="comprehensive_seo",
                score=0.0,
                issues=[f"Ошибка анализа: {str(e)}"],
                recommendations=["Проверьте доступность URL"],
                raw_data={},
                timestamp=datetime.now()
            )
    
    def _analyze_title(self, html_content: str) -> Dict[str, Any]:
        """Анализ title тега"""
        import re
        
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.DOTALL | re.IGNORECASE)
        
        if not title_match:
            return {
                'exists': False,
                'length': 0,
                'issues': ['Отсутствует title тег'],
                'recommendations': ['Добавьте title тег с описанием страницы']
            }
        
        title = title_match.group(1).strip()
        title_length = len(title)
        
        issues = []
        recommendations = []
        
        if title_length < 30:
            issues.append('Title слишком короткий')
            recommendations.append('Увеличьте длину title до 30-60 символов')
        elif title_length > 60:
            issues.append('Title слишком длинный')
            recommendations.append('Сократите title до 60 символов')
        
        if not title:
            issues.append('Пустой title тег')
            recommendations.append('Добавьте содержательный title')
        
        return {
            'exists': True,
            'content': title,
            'length': title_length,
            'issues': issues,
            'recommendations': recommendations
        }
    
    def _analyze_meta_tags(self, html_content: str) -> Dict[str, Any]:
        """Анализ meta тегов"""
        import re
        
        # Meta description
        meta_desc_pattern = r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']'
        meta_desc_match = re.search(meta_desc_pattern, html_content, re.IGNORECASE)
        
        # Meta keywords
        meta_keywords_pattern = r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\']([^"\']*)["\']'
        meta_keywords_match = re.search(meta_keywords_pattern, html_content, re.IGNORECASE)
        
        # Robots meta
        robots_pattern = r'<meta[^>]*name=["\']robots["\'][^>]*content=["\']([^"\']*)["\']'
        robots_match = re.search(robots_pattern, html_content, re.IGNORECASE)
        
        results = {
            'description': {
                'exists': bool(meta_desc_match),
                'content': meta_desc_match.group(1) if meta_desc_match else '',
                'length': len(meta_desc_match.group(1)) if meta_desc_match else 0,
                'issues': [],
                'recommendations': []
            },
            'keywords': {
                'exists': bool(meta_keywords_match),
                'content': meta_keywords_match.group(1) if meta_keywords_match else '',
                'issues': [],
                'recommendations': []
            },
            'robots': {
                'exists': bool(robots_match),
                'content': robots_match.group(1) if robots_match else '',
                'issues': [],
                'recommendations': []
            }
        }
        
        # Анализ meta description
        if not results['description']['exists']:
            results['description']['issues'].append('Отсутствует meta description')
            results['description']['recommendations'].append('Добавьте meta description 150-160 символов')
        elif results['description']['length'] < 120:
            results['description']['issues'].append('Meta description слишком короткий')
            results['description']['recommendations'].append('Увеличьте длину до 150-160 символов')
        elif results['description']['length'] > 160:
            results['description']['issues'].append('Meta description слишком длинный')
            results['description']['recommendations'].append('Сократите до 160 символов')
        
        return results
    
    def _analyze_headings(self, html_content: str) -> Dict[str, Any]:
        """Анализ заголовков"""
        import re
        
        # Находим все заголовки
        heading_pattern = r'<h([1-6])[^>]*>(.*?)</h\1>'
        headings = re.findall(heading_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        results = {
            'h1': {'count': 0, 'content': [], 'issues': [], 'recommendations': []},
            'h2': {'count': 0, 'content': [], 'issues': [], 'recommendations': []},
            'h3': {'count': 0, 'content': [], 'issues': [], 'recommendations': []},
            'h4': {'count': 0, 'content': [], 'issues': [], 'recommendations': []},
            'h5': {'count': 0, 'content': [], 'issues': [], 'recommendations': []},
            'h6': {'count': 0, 'content': [], 'issues': [], 'recommendations': []}
        }
        
        for level, content in headings:
            h_key = f'h{level}'
            results[h_key]['count'] += 1
            results[h_key]['content'].append(content.strip())
        
        # Анализ H1
        if results['h1']['count'] == 0:
            results['h1']['issues'].append('Отсутствует H1 заголовок')
            results['h1']['recommendations'].append('Добавьте один H1 заголовок на страницу')
        elif results['h1']['count'] > 1:
            results['h1']['issues'].append('Несколько H1 заголовков')
            results['h1']['recommendations'].append('Используйте только один H1 заголовок')
        
        return results
    
    def _analyze_images(self, html_content: str) -> Dict[str, Any]:
        """Анализ изображений"""
        import re
        
        # Находим все изображения
        img_pattern = r'<img[^>]*>'
        images = re.findall(img_pattern, html_content, re.IGNORECASE)
        
        results = {
            'total_images': len(images),
            'images_with_alt': 0,
            'images_without_alt': 0,
            'issues': [],
            'recommendations': []
        }
        
        for img in images:
            if 'alt=' in img.lower():
                results['images_with_alt'] += 1
            else:
                results['images_without_alt'] += 1
        
        if results['images_without_alt'] > 0:
            results['issues'].append(f'{results["images_without_alt"]} изображений без alt атрибута')
            results['recommendations'].append('Добавьте alt атрибуты ко всем изображениям')
        
        return results
    
    def _analyze_links(self, html_content: str) -> Dict[str, Any]:
        """Анализ ссылок"""
        import re
        
        # Находим все ссылки
        link_pattern = r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>'
        links = re.findall(link_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        results = {
            'total_links': len(links),
            'internal_links': 0,
            'external_links': 0,
            'empty_anchor_text': 0,
            'issues': [],
            'recommendations': []
        }
        
        for href, anchor_text in links:
            # Проверяем тип ссылки
            if href.startswith('http'):
                results['external_links'] += 1
            elif href.startswith('/') or not href.startswith('http'):
                results['internal_links'] += 1
            
            # Проверяем текст ссылки
            if not anchor_text.strip():
                results['empty_anchor_text'] += 1
        
        if results['empty_anchor_text'] > 0:
            results['issues'].append(f'{results["empty_anchor_text"]} ссылок с пустым текстом')
            results['recommendations'].append('Добавьте описательный текст ко всем ссылкам')
        
        return results
    
    def _analyze_content(self, html_content: str) -> Dict[str, Any]:
        """Анализ контента"""
        import re
        
        # Убираем HTML теги для анализа текста
        text_content = re.sub(r'<[^>]+>', ' ', html_content)
        text_content = re.sub(r'\s+', ' ', text_content).strip()
        
        words = text_content.split()
        
        results = {
            'word_count': len(words),
            'character_count': len(text_content),
            'issues': [],
            'recommendations': []
        }
        
        if results['word_count'] < 300:
            results['issues'].append('Недостаточно контента')
            results['recommendations'].append('Добавьте больше качественного контента (минимум 300 слов)')
        
        return results
    
    def _calculate_comprehensive_score(self, analysis_results: Dict[str, Any]) -> float:
        """Расчет комплексной оценки SEO"""
        score = 100.0
        
        # Вычитаем баллы за проблемы
        for category, data in analysis_results.items():
            if isinstance(data, dict):
                if 'issues' in data:
                    score -= len(data['issues']) * 5
                
                # Специфические проверки
                if category == 'title_analysis':
                    if not data.get('exists', False):
                        score -= 20
                elif category == 'meta_analysis':
                    if not data.get('description', {}).get('exists', False):
                        score -= 15
                elif category == 'heading_analysis':
                    if data.get('h1', {}).get('count', 0) == 0:
                        score -= 15
        
        return max(0.0, min(100.0, score))
    
    def _extract_issues(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Извлечение всех проблем"""
        issues = []
        
        for category, data in analysis_results.items():
            if isinstance(data, dict):
                if 'issues' in data:
                    issues.extend(data['issues'])
                
                # Рекурсивно извлекаем проблемы из подкатегорий
                for subcategory, subdata in data.items():
                    if isinstance(subdata, dict) and 'issues' in subdata:
                        issues.extend(subdata['issues'])
        
        return issues
    
    def _extract_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Извлечение всех рекомендаций"""
        recommendations = []
        
        for category, data in analysis_results.items():
            if isinstance(data, dict):
                if 'recommendations' in data:
                    recommendations.extend(data['recommendations'])
                
                # Рекурсивно извлекаем рекомендации из подкатегорий
                for subcategory, subdata in data.items():
                    if isinstance(subdata, dict) and 'recommendations' in subdata:
                        recommendations.extend(subdata['recommendations'])
        
        return recommendations

class SEOCrossTestingSystem:
    """Система кросс-тестирования SEO"""
    
    def __init__(self):
        self.lighthouse_analyzer = LighthouseAnalyzer()
        self.structured_data_analyzer = StructuredDataAnalyzer()
        self.comprehensive_analyzer = ComprehensiveSEOAnalyzer()
    
    async def run_comprehensive_test(self, url: str) -> Dict[str, SEOTestResult]:
        """Запуск комплексного теста"""
        logger.info(f"Starting comprehensive SEO test for: {url}")
        
        results = {}
        
        # Запускаем все анализаторы параллельно
        tasks = [
            self.lighthouse_analyzer.analyze_page(url),
            self.structured_data_analyzer.analyze_page(url),
            self.comprehensive_analyzer.analyze_page(url)
        ]
        
        test_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Обрабатываем результаты
        for i, result in enumerate(test_results):
            if isinstance(result, Exception):
                logger.error(f"Test {i} failed: {str(result)}")
                continue
            
            results[result.test_type] = result
        
        return results
    
    def generate_comparison_report(self, results: Dict[str, SEOTestResult]) -> Dict[str, Any]:
        """Генерация сравнительного отчета"""
        report = {
            'summary': {
                'total_tests': len(results),
                'average_score': sum(r.score for r in results.values()) / len(results) if results else 0,
                'timestamp': datetime.now().isoformat()
            },
            'detailed_results': {},
            'cross_analysis': {},
            'recommendations': []
        }
        
        # Детальные результаты
        for test_type, result in results.items():
            report['detailed_results'][test_type] = result.to_dict()
        
        # Кросс-анализ
        report['cross_analysis'] = self._perform_cross_analysis(results)
        
        # Общие рекомендации
        report['recommendations'] = self._generate_comprehensive_recommendations(results)
        
        return report
    
    def _perform_cross_analysis(self, results: Dict[str, SEOTestResult]) -> Dict[str, Any]:
        """Кросс-анализ результатов"""
        cross_analysis = {
            'score_consistency': {},
            'common_issues': [],
            'conflicting_recommendations': []
        }
        
        # Анализ согласованности оценок
        scores = {test_type: result.score for test_type, result in results.items()}
        if len(scores) > 1:
            max_score = max(scores.values())
            min_score = min(scores.values())
            score_variance = max_score - min_score
            
            cross_analysis['score_consistency'] = {
                'max_score': max_score,
                'min_score': min_score,
                'variance': score_variance,
                'is_consistent': score_variance < 20
            }
        
        # Поиск общих проблем
        all_issues = []
        for result in results.values():
            all_issues.extend(result.issues)
        
        # Подсчет частоты проблем
        issue_counts = {}
        for issue in all_issues:
            # Упрощенное сравнение проблем
            simplified_issue = issue.lower()
            if 'title' in simplified_issue:
                key = 'title_issues'
            elif 'meta' in simplified_issue:
                key = 'meta_issues'
            elif 'heading' in simplified_issue or 'h1' in simplified_issue:
                key = 'heading_issues'
            elif 'image' in simplified_issue or 'alt' in simplified_issue:
                key = 'image_issues'
            else:
                key = 'other_issues'
            
            issue_counts[key] = issue_counts.get(key, 0) + 1
        
        # Проблемы, найденные несколькими анализаторами
        cross_analysis['common_issues'] = [
            issue for issue, count in issue_counts.items() if count > 1
        ]
        
        return cross_analysis
    
    def _generate_comprehensive_recommendations(self, results: Dict[str, SEOTestResult]) -> List[Dict[str, Any]]:
        """Генерация комплексных рекомендаций"""
        recommendations = []
        
        # Собираем все рекомендации
        all_recommendations = []
        for result in results.values():
            for rec in result.recommendations:
                all_recommendations.append({
                    'text': rec,
                    'source': result.test_type,
                    'priority': self._calculate_recommendation_priority(rec)
                })
        
        # Группируем по приоритету
        priority_groups = {}
        for rec in all_recommendations:
            priority = rec['priority']
            if priority not in priority_groups:
                priority_groups[priority] = []
            priority_groups[priority].append(rec)
        
        # Сортируем по приоритету
        for priority in sorted(priority_groups.keys(), reverse=True):
            recommendations.extend(priority_groups[priority])
        
        return recommendations
    
    def _calculate_recommendation_priority(self, recommendation: str) -> int:
        """Расчет приоритета рекомендации"""
        recommendation_lower = recommendation.lower()
        
        # Высокий приоритет
        if any(keyword in recommendation_lower for keyword in ['title', 'h1', 'meta description']):
            return 3
        
        # Средний приоритет
        if any(keyword in recommendation_lower for keyword in ['alt', 'canonical', 'robots']):
            return 2
        
        # Низкий приоритет
        return 1
    
    def save_results(self, results: Dict[str, SEOTestResult], output_path: str):
        """Сохранение результатов в файл"""
        report = self.generate_comparison_report(results)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to: {output_path}")

async def main():
    """Главная функция для демонстрации"""
    # Создаем тестовые страницы
    test_urls = [
        "http://localhost:8000/good_seo_test.html",
        "http://localhost:8000/bad_seo_test.html",
        "http://localhost:8000/ecommerce_test.html"
    ]
    
    # Инициализируем систему тестирования
    testing_system = SEOCrossTestingSystem()
    
    # Запускаем тесты для каждой страницы
    for url in test_urls:
        print(f"\n{'='*60}")
        print(f"Тестирование: {url}")
        print('='*60)
        
        try:
            # Запускаем комплексный тест
            results = await testing_system.run_comprehensive_test(url)
            
            # Выводим результаты
            for test_type, result in results.items():
                print(f"\n{test_type.upper()} - Оценка: {result.score:.1f}/100")
                
                if result.issues:
                    print("Проблемы:")
                    for issue in result.issues[:5]:  # Показываем первые 5
                        print(f"  - {issue}")
                
                if result.recommendations:
                    print("Рекомендации:")
                    for rec in result.recommendations[:3]:  # Показываем первые 3
                        print(f"  + {rec}")
            
            # Сохраняем результаты
            output_file = f"seo_test_results_{url.split('/')[-1].replace('.html', '')}.json"
            testing_system.save_results(results, output_file)
            
        except Exception as e:
            print(f"Ошибка при тестировании {url}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
