#!/usr/bin/env python3
"""
Автономный SEO валидатор
========================

Работает с локальными HTML файлами для демонстрации функционала кросс-тестирования SEO.
"""

import json
import time
from datetime import datetime
import re
from pathlib import Path
from typing import Dict, List, Any

class OfflineSEOValidator:
    """Автономный SEO валидатор для локальных файлов"""
    
    def __init__(self):
        self.timestamp = datetime.now()
    
    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """Валидация HTML файла с базовыми SEO проверками"""
        
        print(f"🔍 Анализ файла: {file_path}")
        start_time = time.time()
        
        try:
            # Читаем HTML файл
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            load_time = time.time() - start_time
            
            # Проводим анализ
            results = {
                'file_path': file_path,
                'timestamp': datetime.now().isoformat(),
                'load_time': round(load_time, 3),
                'content_length': len(html_content),
                'analysis': {}
            }
            
            # Анализ основных SEO элементов
            results['analysis'] = {
                'title': self._analyze_title(html_content),
                'meta_description': self._analyze_meta_description(html_content),
                'meta_viewport': self._analyze_meta_viewport(html_content),
                'headings': self._analyze_headings(html_content),
                'images': self._analyze_images(html_content),
                'links': self._analyze_links(html_content),
                'structured_data': self._analyze_structured_data(html_content),
                'technical': self._analyze_technical_aspects(html_content),
                'content_quality': self._analyze_content_quality(html_content),
                'open_graph': self._analyze_open_graph(html_content),
                'lang_attribute': self._analyze_lang_attribute(html_content)
            }
            
            # Рассчитываем общую оценку
            results['seo_score'] = self._calculate_seo_score(results['analysis'])
            results['recommendations'] = self._generate_recommendations(results['analysis'])
            results['issues'] = self._extract_issues(results['analysis'])
            results['grade'] = self._get_grade(results['seo_score'])
            
            print(f"✅ Анализ завершен за {load_time:.3f} сек")
            return results
            
        except Exception as e:
            print(f"❌ Ошибка анализа: {str(e)}")
            return {
                'file_path': file_path,
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
        
        # Проверяем на дублирование ключевых слов
        words = title.lower().split()
        unique_words = set(words)
        if len(words) - len(unique_words) > 2:
            issues.append('Много повторяющихся слов в title')
            score -= 15
        
        return {
            'exists': True,
            'content': title,
            'length': title_length,
            'word_count': len(words),
            'unique_words': len(unique_words),
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
        
        if not description:
            issues.append('Пустой meta description')
            score = 0
        
        return {
            'exists': True,
            'content': description,
            'length': desc_length,
            'issues': issues,
            'score': max(0, score)
        }
    
    def _analyze_meta_viewport(self, html_content: str) -> Dict[str, Any]:
        """Анализ meta viewport"""
        
        viewport_pattern = r'<meta[^>]*name=["\']viewport["\'][^>]*content=["\']([^"\']*)["\']'
        match = re.search(viewport_pattern, html_content, re.IGNORECASE)
        
        if not match:
            return {
                'exists': False,
                'content': '',
                'issues': ['Отсутствует meta viewport'],
                'score': 0
            }
        
        viewport = match.group(1).strip()
        
        issues = []
        score = 100
        
        if 'width=device-width' not in viewport.lower():
            issues.append('Meta viewport не содержит width=device-width')
            score -= 50
        
        if 'initial-scale=1' not in viewport.lower():
            issues.append('Meta viewport не содержит initial-scale=1')
            score -= 25
        
        return {
            'exists': True,
            'content': viewport,
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
            # Очищаем содержимое от HTML тегов
            clean_content = []
            for match in matches:
                clean_text = re.sub(r'<[^>]+>', '', match).strip()
                clean_content.append(clean_text)
            
            headings[f'h{i}'] = {
                'count': len(matches),
                'content': clean_content
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
        
        # Проверяем логическую структуру
        if headings['h3']['count'] > 0 and headings['h2']['count'] == 0:
            issues.append('Нарушена логическая структура заголовков (H3 без H2)')
            score -= 10
        
        return {
            'structure': headings,
            'total_headings': sum(h['count'] for h in headings.values()),
            'issues': issues,
            'score': max(0, score)
        }
    
    def _analyze_images(self, html_content: str) -> Dict[str, Any]:
        """Анализ изображений"""
        
        img_tags = re.findall(r'<img[^>]*>', html_content, re.IGNORECASE)
        
        total_images = len(img_tags)
        images_with_alt = 0
        images_with_title = 0
        images_with_lazy_loading = 0
        
        for img in img_tags:
            if 'alt=' in img.lower():
                images_with_alt += 1
            if 'title=' in img.lower():
                images_with_title += 1
            if 'loading=' in img.lower() and 'lazy' in img.lower():
                images_with_lazy_loading += 1
        
        images_without_alt = total_images - images_with_alt
        
        issues = []
        score = 100
        
        if images_without_alt > 0:
            issues.append(f'{images_without_alt} изображений без alt атрибута')
            score -= min(50, images_without_alt * 10)
        
        if total_images > 3 and images_with_lazy_loading == 0:
            issues.append('Рекомендуется использовать lazy loading для изображений')
            score -= 10
        
        return {
            'total_images': total_images,
            'images_with_alt': images_with_alt,
            'images_without_alt': images_without_alt,
            'images_with_title': images_with_title,
            'images_with_lazy_loading': images_with_lazy_loading,
            'issues': issues,
            'score': max(0, score)
        }
    
    def _analyze_links(self, html_content: str) -> Dict[str, Any]:
        """Анализ ссылок"""
        
        link_pattern = r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>'
        links = re.findall(link_pattern, html_content, re.IGNORECASE | re.DOTALL)
        
        total_links = len(links)
        internal_links = 0
        external_links = 0
        empty_anchor_links = 0
        nofollow_links = 0
        
        for href, anchor_text in links:
            # Классифицируем ссылки
            if href.startswith('http'):
                external_links += 1
            elif href.startswith('/') or href.startswith('#') or not href.startswith('http'):
                internal_links += 1
            
            # Проверяем anchor text
            clean_anchor = re.sub(r'<[^>]+>', '', anchor_text).strip()
            if not clean_anchor:
                empty_anchor_links += 1
        
        # Проверяем nofollow атрибуты
        nofollow_pattern = r'<a[^>]*rel=["\'][^"\']*nofollow[^"\']*["\']'
        nofollow_matches = re.findall(nofollow_pattern, html_content, re.IGNORECASE)
        nofollow_links = len(nofollow_matches)
        
        issues = []
        score = 100
        
        if empty_anchor_links > 0:
            issues.append(f'{empty_anchor_links} ссылок с пустым anchor text')
            score -= min(30, empty_anchor_links * 5)
        
        if external_links > 0 and nofollow_links == 0:
            issues.append('Рекомендуется добавить rel="nofollow" к внешним ссылкам')
            score -= 5
        
        return {
            'total_links': total_links,
            'internal_links': internal_links,
            'external_links': external_links,
            'empty_anchor_links': empty_anchor_links,
            'nofollow_links': nofollow_links,
            'issues': issues,
            'score': max(0, score)
        }
    
    def _analyze_structured_data(self, html_content: str) -> Dict[str, Any]:
        """Анализ структурированных данных"""
        
        # JSON-LD
        json_ld_pattern = r'<script type="application/ld\+json"[^>]*>(.*?)</script>'
        json_ld_matches = re.findall(json_ld_pattern, html_content, re.IGNORECASE | re.DOTALL)
        
        valid_schemas = 0
        schema_types = []
        errors = []
        
        for match in json_ld_matches:
            try:
                data = json.loads(match.strip())
                if '@type' in data:
                    valid_schemas += 1
                    schema_types.append(data['@type'])
            except json.JSONDecodeError:
                errors.append('Невалидный JSON-LD')
        
        # Микроданные
        microdata_pattern = r'itemscope[^>]*itemtype="([^"]*)"'
        microdata_matches = re.findall(microdata_pattern, html_content, re.IGNORECASE)
        
        # Open Graph
        og_pattern = r'<meta[^>]*property=["\']og:[^"\']*["\'][^>]*>'
        og_matches = re.findall(og_pattern, html_content, re.IGNORECASE)
        
        issues = []
        score = 50  # Базовая оценка
        
        if valid_schemas > 0:
            score += min(30, valid_schemas * 15)
        else:
            issues.append('Отсутствует JSON-LD разметка')
        
        if microdata_matches:
            score += 10
        
        if og_matches:
            score += 10
        else:
            issues.append('Отсутствует Open Graph разметка')
        
        if errors:
            score -= len(errors) * 10
            issues.extend(errors)
        
        return {
            'json_ld_count': len(json_ld_matches),
            'valid_schemas': valid_schemas,
            'schema_types': schema_types,
            'microdata_count': len(microdata_matches),
            'open_graph_count': len(og_matches),
            'errors': errors,
            'issues': issues,
            'score': max(0, min(100, score))
        }
    
    def _analyze_technical_aspects(self, html_content: str) -> Dict[str, Any]:
        """Анализ технических аспектов"""
        
        issues = []
        score = 100
        
        # Проверяем DOCTYPE
        doctype_pattern = r'<!DOCTYPE\s+html>'
        has_doctype = bool(re.search(doctype_pattern, html_content, re.IGNORECASE))
        
        if not has_doctype:
            issues.append('Отсутствует DOCTYPE HTML5')
            score -= 20
        
        # Проверяем charset
        charset_pattern = r'<meta[^>]*charset=["\']?utf-8["\']?[^>]*>'
        has_charset = bool(re.search(charset_pattern, html_content, re.IGNORECASE))
        
        if not has_charset:
            issues.append('Не указана кодировка UTF-8')
            score -= 15
        
        # Проверяем canonical URL
        canonical_pattern = r'<link[^>]*rel=["\']canonical["\'][^>]*>'
        has_canonical = bool(re.search(canonical_pattern, html_content, re.IGNORECASE))
        
        if not has_canonical:
            issues.append('Отсутствует canonical URL')
            score -= 10
        
        # Проверяем robots meta
        robots_pattern = r'<meta[^>]*name=["\']robots["\'][^>]*>'
        has_robots = bool(re.search(robots_pattern, html_content, re.IGNORECASE))
        
        return {
            'has_doctype': has_doctype,
            'has_charset': has_charset,
            'has_canonical': has_canonical,
            'has_robots_meta': has_robots,
            'issues': issues,
            'score': max(0, score)
        }
    
    def _analyze_content_quality(self, html_content: str) -> Dict[str, Any]:
        """Анализ качества контента"""
        
        # Извлекаем текст
        text_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        text_content = re.sub(r'<style[^>]*>.*?</style>', '', text_content, flags=re.DOTALL | re.IGNORECASE)
        text_content = re.sub(r'<[^>]+>', ' ', text_content)
        text_content = re.sub(r'\s+', ' ', text_content).strip()
        
        words = text_content.split()
        sentences = text_content.split('.')
        
        word_count = len(words)
        sentence_count = len([s for s in sentences if s.strip()])
        
        # Анализ ключевых слов
        word_freq = {}
        stop_words = {'и', 'в', 'на', 'с', 'по', 'для', 'не', 'что', 'это', 'как', 'от', 'до', 'из', 'у', 'за', 'то', 'же', 'мы', 'вы', 'он', 'она', 'они', 'the', 'is', 'at', 'which', 'on', 'and', 'a', 'to', 'as', 'are', 'was', 'will', 'an', 'be', 'or'}
        
        for word in words:
            word_clean = re.sub(r'[^\w]', '', word.lower())
            if len(word_clean) > 3 and word_clean not in stop_words:
                word_freq[word_clean] = word_freq.get(word_clean, 0) + 1
        
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        issues = []
        score = 100
        
        if word_count < 300:
            issues.append('Недостаточно контента (менее 300 слов)')
            score -= 40
        elif word_count < 500:
            issues.append('Рекомендуется увеличить объем контента до 500+ слов')
            score -= 20
        
        if sentence_count > 0:
            avg_sentence_length = word_count / sentence_count
            if avg_sentence_length > 25:
                issues.append('Слишком длинные предложения (ухудшает читаемость)')
                score -= 20
        
        readability_score = max(0, min(100, 100 - (avg_sentence_length - 15) * 2)) if sentence_count > 0 else 0
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_sentence_length': round(word_count / sentence_count, 1) if sentence_count > 0 else 0,
            'readability_score': round(readability_score, 1),
            'top_keywords': top_keywords,
            'keyword_density': len(set(words)) / len(words) if words else 0,
            'issues': issues,
            'score': max(0, score)
        }
    
    def _analyze_open_graph(self, html_content: str) -> Dict[str, Any]:
        """Анализ Open Graph тегов"""
        
        og_tags = {
            'title': r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']*)["\']',
            'description': r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']*)["\']',
            'image': r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']*)["\']',
            'url': r'<meta[^>]*property=["\']og:url["\'][^>]*content=["\']([^"\']*)["\']',
            'type': r'<meta[^>]*property=["\']og:type["\'][^>]*content=["\']([^"\']*)["\']'
        }
        
        found_tags = {}
        issues = []
        score = 100
        
        for tag_name, pattern in og_tags.items():
            match = re.search(pattern, html_content, re.IGNORECASE)
            found_tags[tag_name] = {
                'exists': bool(match),
                'content': match.group(1) if match else ''
            }
            
            if not match:
                issues.append(f'Отсутствует og:{tag_name}')
                score -= 20
        
        return {
            'tags': found_tags,
            'total_found': sum(1 for tag in found_tags.values() if tag['exists']),
            'issues': issues,
            'score': max(0, score)
        }
    
    def _analyze_lang_attribute(self, html_content: str) -> Dict[str, Any]:
        """Анализ атрибута lang"""
        
        lang_pattern = r'<html[^>]*lang=["\']([^"\']*)["\']'
        match = re.search(lang_pattern, html_content, re.IGNORECASE)
        
        if not match:
            return {
                'exists': False,
                'value': '',
                'issues': ['Отсутствует атрибут lang в теге html'],
                'score': 0
            }
        
        lang_value = match.group(1).strip()
        
        issues = []
        score = 100
        
        if len(lang_value) < 2:
            issues.append('Некорректное значение атрибута lang')
            score -= 50
        
        return {
            'exists': True,
            'value': lang_value,
            'issues': issues,
            'score': max(0, score)
        }
    
    def _calculate_seo_score(self, analysis: Dict[str, Any]) -> float:
        """Рассчитываем общую SEO оценку"""
        
        # Веса для различных категорий
        weights = {
            'title': 0.18,
            'meta_description': 0.15,
            'meta_viewport': 0.08,
            'headings': 0.15,
            'images': 0.08,
            'links': 0.06,
            'structured_data': 0.10,
            'technical': 0.10,
            'content_quality': 0.08,
            'open_graph': 0.02,
            'lang_attribute': 0.02
        }
        
        total_score = 0
        total_weight = 0
        
        for category, weight in weights.items():
            if category in analysis and 'score' in analysis[category]:
                total_score += analysis[category]['score'] * weight
                total_weight += weight
        
        return round(total_score / total_weight if total_weight > 0 else 0, 2)
    
    def _get_grade(self, score: float) -> str:
        """Определяем оценку буквой"""
        if score >= 90:
            return 'A+'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        elif score >= 50:
            return 'D'
        else:
            return 'F'
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Генерируем рекомендации по улучшению"""
        
        recommendations = []
        
        # Приоритетные рекомендации (критичные для SEO)
        if analysis['title']['score'] < 70:
            recommendations.append('🔴 КРИТИЧНО: Оптимизируйте title тег (30-60 символов, уникальный контент)')
        
        if analysis['meta_description']['score'] < 70:
            recommendations.append('🔴 КРИТИЧНО: Добавьте или улучшите meta description (120-160 символов)')
        
        if analysis['headings']['score'] < 70:
            recommendations.append('🔴 КРИТИЧНО: Улучшите структуру заголовков (H1 - один на страницу, добавьте H2-H3)')
        
        # Важные рекомендации
        if analysis['meta_viewport']['score'] < 80:
            recommendations.append('🟡 ВАЖНО: Добавьте корректный meta viewport для мобильной адаптации')
        
        if analysis['images']['score'] < 80:
            recommendations.append('🟡 ВАЖНО: Добавьте alt атрибуты ко всем изображениям')
        
        if analysis['structured_data']['score'] < 50:
            recommendations.append('🟡 ВАЖНО: Добавьте JSON-LD разметку Schema.org для улучшения понимания контента')
        
        if analysis['technical']['score'] < 80:
            recommendations.append('🟡 ВАЖНО: Исправьте технические проблемы (DOCTYPE, charset, canonical)')
        
        # Рекомендации по улучшению
        if analysis['content_quality']['score'] < 70:
            recommendations.append('🟢 УЛУЧШЕНИЕ: Увеличьте объем и качество контента (300+ слов)')
        
        if analysis['open_graph']['score'] < 60:
            recommendations.append('🟢 УЛУЧШЕНИЕ: Добавьте Open Graph теги для социальных сетей')
        
        if analysis['links']['score'] < 80:
            recommendations.append('🟢 УЛУЧШЕНИЕ: Улучшите качество ссылок (добавьте anchor text, используйте nofollow)')
        
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
    output.append(f"📊 SEO Анализ: {results['file_path']}")
    output.append(f"📈 SEO оценка: {results['seo_score']}/100 (Оценка: {results['grade']})")
    
    # Детальные результаты
    analysis = results['analysis']
    
    output.append(f"\n📝 Детальный анализ:")
    output.append(f"  📌 Title: {analysis['title']['score']}/100 ({analysis['title']['length']} символов)")
    if analysis['title']['content']:
        output.append(f"     \"{analysis['title']['content'][:100]}{'...' if len(analysis['title']['content']) > 100 else ''}\"")
    
    output.append(f"  📄 Meta Description: {analysis['meta_description']['score']}/100 ({analysis['meta_description']['length']} символов)")
    output.append(f"  📱 Meta Viewport: {analysis['meta_viewport']['score']}/100")
    output.append(f"  🏗️  Заголовки: {analysis['headings']['score']}/100 (H1: {analysis['headings']['structure']['h1']['count']}, H2: {analysis['headings']['structure']['h2']['count']})")
    output.append(f"  🖼️  Изображения: {analysis['images']['score']}/100 ({analysis['images']['images_without_alt']} без alt из {analysis['images']['total_images']})")
    output.append(f"  🔗 Ссылки: {analysis['links']['score']}/100 ({analysis['links']['total_links']} всего, {analysis['links']['external_links']} внешних)")
    output.append(f"  📋 Структурированные данные: {analysis['structured_data']['score']}/100 ({analysis['structured_data']['valid_schemas']} валидных схем)")
    output.append(f"  ⚙️  Технические аспекты: {analysis['technical']['score']}/100")
    output.append(f"  📝 Качество контента: {analysis['content_quality']['score']}/100 ({analysis['content_quality']['word_count']} слов)")
    output.append(f"  📲 Open Graph: {analysis['open_graph']['score']}/100 ({analysis['open_graph']['total_found']}/5 тегов)")
    
    # Топ ключевые слова
    if analysis['content_quality']['top_keywords']:
        output.append(f"\n🔑 Топ ключевые слова:")
        for word, count in analysis['content_quality']['top_keywords'][:5]:
            output.append(f"     {word}: {count} раз")
    
    # Проблемы
    if results['issues']:
        output.append(f"\n❌ Найденные проблемы ({len(results['issues'])}):")
        for i, issue in enumerate(results['issues'][:8], 1):
            output.append(f"  {i}. {issue}")
        if len(results['issues']) > 8:
            output.append(f"     ... и еще {len(results['issues']) - 8} проблем")
    
    # Рекомендации
    if results['recommendations']:
        output.append(f"\n💡 Рекомендации по улучшению:")
        for i, rec in enumerate(results['recommendations'][:6], 1):
            output.append(f"  {i}. {rec}")
        if len(results['recommendations']) > 6:
            output.append(f"     ... и еще {len(results['recommendations']) - 6} рекомендаций")
    
    return '\n'.join(output)

def save_results(results: Dict[str, Any], filename: str):
    """Сохранение результатов в JSON файл"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Результаты сохранены в: {filename}")

def main():
    """Главная функция демонстрации"""
    
    # Поиск HTML файлов в текущей директории
    html_files = list(Path('.').glob('*.html'))
    
    if not html_files:
        print("❌ HTML файлы не найдены в текущей директории")
        return
    
    validator = OfflineSEOValidator()
    all_results = []
    
    print("🚀 Запуск автономного SEO тестирования")
    print("=" * 80)
    
    for i, file_path in enumerate(html_files, 1):
        print(f"\n[{i}/{len(html_files)}] Тестирование: {file_path}")
        print("-" * 70)
        
        # Проводим анализ
        results = validator.validate_file(str(file_path))
        all_results.append(results)
        
        # Выводим результаты
        print(format_results(results))
        
        # Сохраняем индивидуальные результаты
        if 'error' not in results:
            filename = f"seo_offline_{file_path.stem}.json"
            save_results(results, filename)
    
    # Сводка по всем тестам
    print(f"\n{'='*80}")
    print("📋 СВОДКА ПО ВСЕМ ТЕСТАМ")
    print("=" * 80)
    
    successful_tests = [r for r in all_results if 'error' not in r]
    failed_tests = [r for r in all_results if 'error' in r]
    
    print(f"✅ Успешных тестов: {len(successful_tests)}")
    print(f"❌ Неудачных тестов: {len(failed_tests)}")
    
    if successful_tests:
        scores = [r['seo_score'] for r in successful_tests]
        avg_score = sum(scores) / len(scores)
        best_test = max(successful_tests, key=lambda x: x['seo_score'])
        worst_test = min(successful_tests, key=lambda x: x['seo_score'])
        
        print(f"📈 Средняя SEO оценка: {avg_score:.1f}/100")
        print(f"🏆 Лучший результат: {Path(best_test['file_path']).name} ({best_test['seo_score']}/100, {best_test['grade']})")
        print(f"🔴 Требует внимания: {Path(worst_test['file_path']).name} ({worst_test['seo_score']}/100, {worst_test['grade']})")
        
        # Распределение оценок
        grades = [r['grade'] for r in successful_tests]
        grade_count = {}
        for grade in grades:
            grade_count[grade] = grade_count.get(grade, 0) + 1
        
        print(f"\n📊 Распределение оценок:")
        for grade in ['A+', 'A', 'B', 'C', 'D', 'F']:
            if grade in grade_count:
                print(f"  {grade}: {grade_count[grade]} страниц")
        
        # Общие рекомендации
        all_issues = []
        for result in successful_tests:
            all_issues.extend(result['issues'])
        
        if all_issues:
            from collections import Counter
            common_issues = Counter(all_issues).most_common(5)
            
            print(f"\n🎯 Наиболее частые проблемы:")
            for issue, count in common_issues:
                print(f"  • {issue} (в {count} файлах)")
    
    # Сохраняем общий отчет
    timestamp = datetime.now()
    full_report = {
        'timestamp': timestamp.isoformat(),
        'summary': {
            'total_tests': len(all_results),
            'successful': len(successful_tests),
            'failed': len(failed_tests),
            'average_score': avg_score if successful_tests else 0,
            'grade_distribution': grade_count if successful_tests else {}
        },
        'results': all_results
    }
    
    save_results(full_report, f'seo_offline_full_report_{timestamp.strftime("%Y%m%d_%H%M%S")}.json')
    
    print(f"\n🎉 Автономное SEO тестирование завершено!")
    print(f"📁 Все результаты сохранены в JSON файлах")

if __name__ == "__main__":
    main()
