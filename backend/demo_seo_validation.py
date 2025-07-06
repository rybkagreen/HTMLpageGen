#!/usr/bin/env python3
"""
Демонстрационный SEO валидатор
==============================

Упрощенная версия для демонстрации функционала кросс-тестирования SEO.
"""

import asyncio
import json
import requests
import time
from datetime import datetime
import re
from urllib.parse import urlparse
from typing import Dict, List, Any

class SimpleSEOValidator:
    """Упрощенный SEO валидатор для демонстрации"""
    
    def __init__(self):
        self.timeout = 10
    
    def validate_url(self, url: str) -> Dict[str, Any]:
        """Валидация URL с базовыми SEO проверками"""
        
        print(f"🔍 Анализ URL: {url}")
        start_time = time.time()
        
        try:
            # Получаем HTML страницы
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            html_content = response.text
            load_time = time.time() - start_time
            
            # Проводим анализ
            results = {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'load_time': round(load_time, 3),
                'status_code': response.status_code,
                'content_length': len(html_content),
                'analysis': {}
            }
            
            # Анализ основных SEO элементов
            results['analysis'] = {
                'title': self._analyze_title(html_content),
                'meta_description': self._analyze_meta_description(html_content),
                'headings': self._analyze_headings(html_content),
                'images': self._analyze_images(html_content),
                'links': self._analyze_links(html_content, url),
                'structured_data': self._analyze_structured_data(html_content),
                'technical': self._analyze_technical_aspects(url, response.headers),
                'content_quality': self._analyze_content_quality(html_content)
            }
            
            # Рассчитываем общую оценку
            results['seo_score'] = self._calculate_seo_score(results['analysis'])
            results['recommendations'] = self._generate_recommendations(results['analysis'])
            results['issues'] = self._extract_issues(results['analysis'])
            
            print(f"✅ Анализ завершен за {load_time:.2f} сек")
            return results
            
        except Exception as e:
            print(f"❌ Ошибка анализа: {str(e)}")
            return {
                'url': url,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _analyze_title(self, html_content: str) -> Dict[str, Any]:
        """Анализ title тега"""
        
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
        
        if not title_match:
            return {
                'exists': False,
                'content': '',
                'length': 0,
                'issues': ['Отсутствует title тег'],
                'score': 0
            }
        
        title = title_match.group(1).strip()
        title_length = len(title)
        
        issues = []
        score = 100
        
        if title_length < 30:
            issues.append('Title слишком короткий (менее 30 символов)')
            score -= 30
        elif title_length > 60:
            issues.append('Title слишком длинный (более 60 символов)')
            score -= 20
        
        if not title:
            issues.append('Пустой title тег')
            score = 0
        
        return {
            'exists': True,
            'content': title,
            'length': title_length,
            'issues': issues,
            'score': max(0, score)
        }
    
    def _analyze_meta_description(self, html_content: str) -> Dict[str, Any]:
        """Анализ meta description"""
        
        meta_desc_pattern = r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']'
        match = re.search(meta_desc_pattern, html_content, re.IGNORECASE)
        
        if not match:
            return {
                'exists': False,
                'content': '',
                'length': 0,
                'issues': ['Отсутствует meta description'],
                'score': 0
            }
        
        description = match.group(1).strip()
        desc_length = len(description)
        
        issues = []
        score = 100
        
        if desc_length < 120:
            issues.append('Meta description слишком короткий (менее 120 символов)')
            score -= 30
        elif desc_length > 160:
            issues.append('Meta description слишком длинный (более 160 символов)')
            score -= 20
        
        return {
            'exists': True,
            'content': description,
            'length': desc_length,
            'issues': issues,
            'score': max(0, score)
        }
    
    def _analyze_headings(self, html_content: str) -> Dict[str, Any]:
        """Анализ структуры заголовков"""
        
        headings = {}
        issues = []
        score = 100
        
        for i in range(1, 7):
            pattern = f'<h{i}[^>]*>(.*?)</h{i}>'
            matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
            headings[f'h{i}'] = {
                'count': len(matches),
                'content': [match.strip() for match in matches]
            }
        
        # Проверяем H1
        if headings['h1']['count'] == 0:
            issues.append('Отсутствует H1 заголовок')
            score -= 40
        elif headings['h1']['count'] > 1:
            issues.append('Несколько H1 заголовков на странице')
            score -= 20
        
        # Проверяем структуру заголовков
        if headings['h2']['count'] == 0:
            issues.append('Отсутствуют H2 заголовки для структурирования контента')
            score -= 15
        
        return {
            'structure': headings,
            'issues': issues,
            'score': max(0, score)
        }
    
    def _analyze_images(self, html_content: str) -> Dict[str, Any]:
        """Анализ изображений"""
        
        img_tags = re.findall(r'<img[^>]*>', html_content, re.IGNORECASE)
        
        total_images = len(img_tags)
        images_with_alt = 0
        
        for img in img_tags:
            if 'alt=' in img.lower():
                images_with_alt += 1
        
        images_without_alt = total_images - images_with_alt
        
        issues = []
        score = 100
        
        if images_without_alt > 0:
            issues.append(f'{images_without_alt} изображений без alt атрибута')
            score -= min(50, images_without_alt * 10)
        
        return {
            'total_images': total_images,
            'images_with_alt': images_with_alt,
            'images_without_alt': images_without_alt,
            'issues': issues,
            'score': max(0, score)
        }
    
    def _analyze_links(self, html_content: str, base_url: str) -> Dict[str, Any]:
        """Анализ ссылок"""
        
        link_pattern = r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>'
        links = re.findall(link_pattern, html_content, re.IGNORECASE | re.DOTALL)
        
        total_links = len(links)
        internal_links = 0
        external_links = 0
        empty_anchor_links = 0
        
        base_domain = urlparse(base_url).netloc
        
        for href, anchor_text in links:
            # Классифицируем ссылки
            if href.startswith('http'):
                link_domain = urlparse(href).netloc
                if link_domain == base_domain:
                    internal_links += 1
                else:
                    external_links += 1
            else:
                internal_links += 1
            
            # Проверяем anchor text
            if not anchor_text.strip():
                empty_anchor_links += 1
        
        issues = []
        score = 100
        
        if empty_anchor_links > 0:
            issues.append(f'{empty_anchor_links} ссылок с пустым anchor text')
            score -= min(30, empty_anchor_links * 5)
        
        return {
            'total_links': total_links,
            'internal_links': internal_links,
            'external_links': external_links,
            'empty_anchor_links': empty_anchor_links,
            'issues': issues,
            'score': max(0, score)
        }
    
    def _analyze_structured_data(self, html_content: str) -> Dict[str, Any]:
        """Анализ структурированных данных"""
        
        # JSON-LD
        json_ld_pattern = r'<script type="application/ld\+json"[^>]*>(.*?)</script>'
        json_ld_matches = re.findall(json_ld_pattern, html_content, re.IGNORECASE | re.DOTALL)
        
        valid_schemas = 0
        errors = []
        
        for match in json_ld_matches:
            try:
                data = json.loads(match.strip())
                if '@type' in data:
                    valid_schemas += 1
            except json.JSONDecodeError:
                errors.append('Невалидный JSON-LD')
        
        # Микроданные
        microdata_pattern = r'itemscope[^>]*itemtype="([^"]*)"'
        microdata_matches = re.findall(microdata_pattern, html_content, re.IGNORECASE)
        
        issues = []
        score = 50  # Базовая оценка
        
        if valid_schemas > 0:
            score += min(30, valid_schemas * 15)
        else:
            issues.append('Отсутствует JSON-LD разметка')
        
        if microdata_matches:
            score += 10
        
        if errors:
            score -= len(errors) * 10
            issues.extend(errors)
        
        return {
            'json_ld_count': len(json_ld_matches),
            'valid_schemas': valid_schemas,
            'microdata_count': len(microdata_matches),
            'errors': errors,
            'issues': issues,
            'score': max(0, min(100, score))
        }
    
    def _analyze_technical_aspects(self, url: str, headers: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ технических аспектов"""
        
        issues = []
        score = 100
        
        # Проверяем HTTPS
        is_https = url.startswith('https://')
        if not is_https:
            issues.append('Сайт не использует HTTPS')
            score -= 30
        
        # Проверяем заголовки
        content_type = headers.get('content-type', '').lower()
        if 'charset=utf-8' not in content_type:
            issues.append('Не указана кодировка UTF-8')
            score -= 10
        
        return {
            'is_https': is_https,
            'content_type': content_type,
            'headers': dict(headers),
            'issues': issues,
            'score': max(0, score)
        }
    
    def _analyze_content_quality(self, html_content: str) -> Dict[str, Any]:
        """Анализ качества контента"""
        
        # Извлекаем текст
        text_content = re.sub(r'<[^>]+>', ' ', html_content)
        text_content = re.sub(r'\s+', ' ', text_content).strip()
        
        words = text_content.split()
        sentences = text_content.split('.')
        
        word_count = len(words)
        sentence_count = len(sentences)
        
        issues = []
        score = 100
        
        if word_count < 300:
            issues.append('Недостаточно контента (менее 300 слов)')
            score -= 40
        
        if sentence_count > 0:
            avg_sentence_length = word_count / sentence_count
            if avg_sentence_length > 25:
                issues.append('Слишком длинные предложения (ухудшает читаемость)')
                score -= 20
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_sentence_length': round(word_count / sentence_count, 1) if sentence_count > 0 else 0,
            'issues': issues,
            'score': max(0, score)
        }
    
    def _calculate_seo_score(self, analysis: Dict[str, Any]) -> float:
        """Рассчитываем общую SEO оценку"""
        
        # Веса для различных категорий
        weights = {
            'title': 0.2,
            'meta_description': 0.15,
            'headings': 0.15,
            'images': 0.1,
            'links': 0.1,
            'structured_data': 0.1,
            'technical': 0.1,
            'content_quality': 0.1
        }
        
        total_score = 0
        total_weight = 0
        
        for category, weight in weights.items():
            if category in analysis and 'score' in analysis[category]:
                total_score += analysis[category]['score'] * weight
                total_weight += weight
        
        return round(total_score / total_weight if total_weight > 0 else 0, 2)
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Генерируем рекомендации по улучшению"""
        
        recommendations = []
        
        # Рекомендации по title
        if analysis['title']['score'] < 70:
            recommendations.append('Оптимизируйте title тег (30-60 символов)')
        
        # Рекомендации по meta description
        if analysis['meta_description']['score'] < 70:
            recommendations.append('Добавьте или улучшите meta description (120-160 символов)')
        
        # Рекомендации по заголовкам
        if analysis['headings']['score'] < 70:
            recommendations.append('Улучшите структуру заголовков (обязательно H1, добавьте H2-H3)')
        
        # Рекомендации по изображениям
        if analysis['images']['score'] < 80:
            recommendations.append('Добавьте alt атрибуты ко всем изображениям')
        
        # Рекомендации по структурированным данным
        if analysis['structured_data']['score'] < 50:
            recommendations.append('Добавьте JSON-LD разметку Schema.org')
        
        # Рекомендации по техническим аспектам
        if analysis['technical']['score'] < 80:
            recommendations.append('Исправьте технические проблемы (HTTPS, кодировка)')
        
        # Рекомендации по контенту
        if analysis['content_quality']['score'] < 70:
            recommendations.append('Увеличьте объем и улучшите качество контента')
        
        return recommendations
    
    def _extract_issues(self, analysis: Dict[str, Any]) -> List[str]:
        """Извлекаем все найденные проблемы"""
        
        all_issues = []
        
        for category, data in analysis.items():
            if 'issues' in data:
                all_issues.extend(data['issues'])
        
        return all_issues

def format_results(results: Dict[str, Any]) -> str:
    """Форматирование результатов для вывода"""
    
    if 'error' in results:
        return f"❌ Ошибка: {results['error']}"
    
    output = []
    output.append(f"📊 SEO Анализ: {results['url']}")
    output.append(f"⏱️  Время загрузки: {results['load_time']} сек")
    output.append(f"📈 SEO оценка: {results['seo_score']}/100")
    
    # Детальные результаты
    analysis = results['analysis']
    
    output.append(f"\n📝 Детальный анализ:")
    output.append(f"  Title: {analysis['title']['score']}/100 ({analysis['title']['length']} символов)")
    output.append(f"  Meta Description: {analysis['meta_description']['score']}/100 ({analysis['meta_description']['length']} символов)")
    output.append(f"  Заголовки: {analysis['headings']['score']}/100")
    output.append(f"  Изображения: {analysis['images']['score']}/100 ({analysis['images']['images_without_alt']} без alt)")
    output.append(f"  Ссылки: {analysis['links']['score']}/100 ({analysis['links']['total_links']} всего)")
    output.append(f"  Структурированные данные: {analysis['structured_data']['score']}/100")
    output.append(f"  Технические аспекты: {analysis['technical']['score']}/100")
    output.append(f"  Качество контента: {analysis['content_quality']['score']}/100 ({analysis['content_quality']['word_count']} слов)")
    
    # Проблемы
    if results['issues']:
        output.append(f"\n❌ Найденные проблемы:")
        for issue in results['issues'][:5]:  # Показываем первые 5
            output.append(f"  • {issue}")
    
    # Рекомендации
    if results['recommendations']:
        output.append(f"\n💡 Рекомендации:")
        for rec in results['recommendations'][:5]:  # Показываем первые 5
            output.append(f"  + {rec}")
    
    return '\n'.join(output)

def save_results(results: Dict[str, Any], filename: str):
    """Сохранение результатов в JSON файл"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Результаты сохранены в: {filename}")

def main():
    """Главная функция демонстрации"""
    
    # Тестовые URL
    test_urls = [
        "http://localhost:8000/good_seo_test.html",
        "http://localhost:8000/bad_seo_test.html",
        "http://localhost:8000/ecommerce_test.html"
    ]
    
    validator = SimpleSEOValidator()
    all_results = []
    
    print("🚀 Запуск демонстрационного SEO тестирования")
    print("=" * 60)
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n[{i}/{len(test_urls)}] Тестирование: {url}")
        print("-" * 50)
        
        # Проводим анализ
        results = validator.validate_url(url)
        all_results.append(results)
        
        # Выводим результаты
        print(format_results(results))
        
        # Сохраняем индивидуальные результаты
        if 'error' not in results:
            filename = f"seo_demo_{url.split('/')[-1].replace('.html', '')}.json"
            save_results(results, filename)
    
    # Сводка по всем тестам
    print(f"\n{'='*60}")
    print("📋 СВОДКА ПО ВСЕМ ТЕСТАМ")
    print("=" * 60)
    
    successful_tests = [r for r in all_results if 'error' not in r]
    failed_tests = [r for r in all_results if 'error' in r]
    
    print(f"✅ Успешных тестов: {len(successful_tests)}")
    print(f"❌ Неудачных тестов: {len(failed_tests)}")
    
    if successful_tests:
        avg_score = sum(r['seo_score'] for r in successful_tests) / len(successful_tests)
        best_url = max(successful_tests, key=lambda x: x['seo_score'])
        worst_url = min(successful_tests, key=lambda x: x['seo_score'])
        
        print(f"📈 Средняя SEO оценка: {avg_score:.1f}/100")
        print(f"🏆 Лучший результат: {best_url['url']} ({best_url['seo_score']}/100)")
        print(f"🔴 Требует внимания: {worst_url['url']} ({worst_url['seo_score']}/100)")
        
        # Общие рекомендации
        all_issues = []
        for result in successful_tests:
            all_issues.extend(result['issues'])
        
        if all_issues:
            from collections import Counter
            common_issues = Counter(all_issues).most_common(3)
            
            print(f"\n🎯 Наиболее частые проблемы:")
            for issue, count in common_issues:
                print(f"  • {issue} (встречается {count} раз)")
    
    # Сохраняем общий отчет
    full_report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_tests': len(all_results),
            'successful': len(successful_tests),
            'failed': len(failed_tests),
            'average_score': avg_score if successful_tests else 0
        },
        'results': all_results
    }
    
    save_results(full_report, 'seo_demo_full_report.json')
    
    print(f"\n🎉 Демонстрационное тестирование завершено!")

if __name__ == "__main__":
    main()
