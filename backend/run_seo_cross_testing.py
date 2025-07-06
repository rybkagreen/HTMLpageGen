#!/usr/bin/env python3
"""
SEO Cross-Testing Runner
========================

Основной скрипт для запуска комплексного кросс-тестирования SEO агента.
Включает все валидации: Lighthouse, PageSpeed, Schema.org, техническое SEO.
"""

import asyncio
import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
import logging

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from seo_cross_testing import SEOCrossTestingSystem
from seo_performance_validator import SEOPerformanceValidator

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SEOTestingOrchestrator:
    """Оркестратор для управления всеми SEO тестами"""
    
    def __init__(self, pagespeed_api_key=None):
        self.cross_testing_system = SEOCrossTestingSystem()
        self.performance_validator = SEOPerformanceValidator(pagespeed_api_key)
        self.results_dir = Path("seo_test_results")
        self.results_dir.mkdir(exist_ok=True)
    
    async def run_complete_validation(self, urls: list, output_format='json'):
        """Запуск полной валидации для списка URL"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Создаем папку для результатов этого запуска
        session_dir = self.results_dir / f"session_{timestamp}"
        session_dir.mkdir(exist_ok=True)
        
        logger.info(f"Начинаем комплексное тестирование {len(urls)} URL")
        logger.info(f"Результаты будут сохранены в: {session_dir}")
        
        all_results = {
            'session_info': {
                'timestamp': timestamp,
                'urls_count': len(urls),
                'test_types': ['lighthouse', 'pagespeed_mobile', 'pagespeed_desktop', 'schema_validation', 'technical_seo', 'content_quality']
            },
            'results': {},
            'summary': {},
            'comparison': {}
        }
        
        # Тестируем каждый URL
        for i, url in enumerate(urls, 1):
            logger.info(f"[{i}/{len(urls)}] Тестирование: {url}")
            
            try:
                # Запускаем оба типа тестирования параллельно
                cross_test_task = self.cross_testing_system.run_comprehensive_test(url)
                performance_test_task = self.performance_validator.comprehensive_validation(url)
                
                cross_results, performance_results = await asyncio.gather(
                    cross_test_task, performance_test_task, return_exceptions=True
                )
                
                # Обрабатываем результаты
                url_results = {
                    'url': url,
                    'timestamp': datetime.now().isoformat(),
                    'cross_testing': cross_results if not isinstance(cross_results, Exception) else {'error': str(cross_results)},
                    'performance_validation': performance_results if not isinstance(performance_results, Exception) else {'error': str(performance_results)}
                }
                
                # Добавляем комбинированный анализ
                url_results['combined_analysis'] = self._combine_results(cross_results, performance_results)
                
                all_results['results'][url] = url_results
                
                # Сохраняем индивидуальные результаты
                url_filename = url.replace('/', '_').replace(':', '_').replace('?', '_')
                individual_file = session_dir / f"{url_filename}.json"
                
                with open(individual_file, 'w', encoding='utf-8') as f:
                    json.dump(url_results, f, indent=2, ensure_ascii=False, default=str)
                
                logger.info(f"✓ Тестирование {url} завершено")
                
            except Exception as e:
                logger.error(f"✗ Ошибка при тестировании {url}: {str(e)}")
                all_results['results'][url] = {
                    'url': url,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
        
        # Генерируем сводку и сравнительный анализ
        all_results['summary'] = self._generate_summary(all_results['results'])
        all_results['comparison'] = self._generate_comparison(all_results['results'])
        
        # Сохраняем полный отчет
        full_report_file = session_dir / "full_report.json"
        with open(full_report_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
        
        # Генерируем HTML отчет
        if output_format in ['html', 'both']:
            html_report = self._generate_html_report(all_results)
            html_file = session_dir / "report.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_report)
        
        logger.info(f"🎉 Комплексное тестирование завершено!")
        logger.info(f"📊 Полный отчет: {full_report_file}")
        
        return all_results
    
    def _combine_results(self, cross_results, performance_results):
        """Объединение результатов различных тестов"""
        
        if isinstance(cross_results, Exception) or isinstance(performance_results, Exception):
            return {'error': 'Не удалось объединить результаты из-за ошибок в тестах'}
        
        combined = {
            'overall_health_score': 0,
            'critical_issues': [],
            'improvement_priorities': [],
            'seo_readiness': 'unknown'
        }
        
        # Собираем все оценки
        scores = []
        
        # Из кросс-тестирования
        for test_type, result in cross_results.items():
            if hasattr(result, 'score'):
                scores.append(result.score)
        
        # Из валидации производительности
        if 'overall_score' in performance_results:
            scores.append(performance_results['overall_score'])
        
        # Рассчитываем общую оценку здоровья
        if scores:
            combined['overall_health_score'] = round(sum(scores) / len(scores), 2)
        
        # Определяем критические проблемы
        critical_issues = set()
        
        # Из кросс-тестирования
        for test_type, result in cross_results.items():
            if hasattr(result, 'issues'):
                for issue in result.issues:
                    if any(keyword in issue.lower() for keyword in ['отсутствует title', 'отсутствует h1', 'отсутствует meta description']):
                        critical_issues.add(issue)
        
        # Из валидации производительности
        perf_recommendations = performance_results.get('recommendations', [])
        for rec in perf_recommendations:
            if rec.get('priority') == 'high':
                critical_issues.add(rec['text'])
        
        combined['critical_issues'] = list(critical_issues)
        
        # Определяем приоритеты улучшений
        priorities = []
        
        if combined['overall_health_score'] < 60:
            priorities.append('Критическое улучшение SEO основ')
        elif combined['overall_health_score'] < 80:
            priorities.append('Оптимизация производительности и SEO')
        else:
            priorities.append('Тонкая настройка и мониторинг')
        
        # Проверяем мобильную производительность
        mobile_perf = performance_results.get('mobile_performance', {})
        if mobile_perf.get('performance_score', 100) < 70:
            priorities.append('Улучшение мобильной производительности')
        
        # Проверяем структурированные данные
        schema_validation = performance_results.get('schema_validation', {})
        if not schema_validation.get('valid_schemas'):
            priorities.append('Добавление структурированных данных')
        
        combined['improvement_priorities'] = priorities
        
        # Определяем готовность к SEO
        if combined['overall_health_score'] >= 90:
            combined['seo_readiness'] = 'excellent'
        elif combined['overall_health_score'] >= 80:
            combined['seo_readiness'] = 'good'
        elif combined['overall_health_score'] >= 60:
            combined['seo_readiness'] = 'fair'
        else:
            combined['seo_readiness'] = 'poor'
        
        return combined
    
    def _generate_summary(self, results):
        """Генерация сводки результатов"""
        
        summary = {
            'total_urls': len(results),
            'successful_tests': 0,
            'failed_tests': 0,
            'average_scores': {},
            'common_issues': [],
            'best_performing_url': None,
            'worst_performing_url': None
        }
        
        all_scores = []
        all_issues = []
        url_scores = {}
        
        for url, result in results.items():
            if 'error' in result:
                summary['failed_tests'] += 1
                continue
            
            summary['successful_tests'] += 1
            
            # Собираем оценки
            combined = result.get('combined_analysis', {})
            score = combined.get('overall_health_score', 0)
            
            if score > 0:
                all_scores.append(score)
                url_scores[url] = score
            
            # Собираем проблемы
            critical_issues = combined.get('critical_issues', [])
            all_issues.extend(critical_issues)
        
        # Рассчитываем средние оценки
        if all_scores:
            summary['average_scores']['overall'] = round(sum(all_scores) / len(all_scores), 2)
        
        # Находим самые частые проблемы
        from collections import Counter
        issue_counts = Counter(all_issues)
        summary['common_issues'] = [
            {'issue': issue, 'count': count}
            for issue, count in issue_counts.most_common(5)
        ]
        
        # Находим лучший и худший URL
        if url_scores:
            best_url = max(url_scores, key=url_scores.get)
            worst_url = min(url_scores, key=url_scores.get)
            
            summary['best_performing_url'] = {
                'url': best_url,
                'score': url_scores[best_url]
            }
            
            summary['worst_performing_url'] = {
                'url': worst_url,
                'score': url_scores[worst_url]
            }
        
        return summary
    
    def _generate_comparison(self, results):
        """Генерация сравнительного анализа"""
        
        comparison = {
            'score_distribution': {
                'excellent': 0,  # 90-100
                'good': 0,       # 80-89
                'fair': 0,       # 60-79
                'poor': 0        # 0-59
            },
            'test_consistency': {},
            'improvement_recommendations': []
        }
        
        # Анализируем распределение оценок
        for url, result in results.items():
            if 'error' in result:
                continue
            
            combined = result.get('combined_analysis', {})
            score = combined.get('overall_health_score', 0)
            
            if score >= 90:
                comparison['score_distribution']['excellent'] += 1
            elif score >= 80:
                comparison['score_distribution']['good'] += 1
            elif score >= 60:
                comparison['score_distribution']['fair'] += 1
            else:
                comparison['score_distribution']['poor'] += 1
        
        # Анализируем согласованность тестов
        lighthouse_scores = []
        pagespeed_scores = []
        
        for url, result in results.items():
            if 'error' in result:
                continue
            
            cross_results = result.get('cross_testing', {})
            perf_results = result.get('performance_validation', {})
            
            # Lighthouse оценки
            lighthouse_result = cross_results.get('lighthouse')
            if lighthouse_result and hasattr(lighthouse_result, 'score'):
                lighthouse_scores.append(lighthouse_result.score)
            
            # PageSpeed оценки
            overall_score = perf_results.get('overall_score', 0)
            if overall_score > 0:
                pagespeed_scores.append(overall_score)
        
        if lighthouse_scores and pagespeed_scores:
            import statistics
            
            comparison['test_consistency'] = {
                'lighthouse_avg': round(statistics.mean(lighthouse_scores), 2),
                'pagespeed_avg': round(statistics.mean(pagespeed_scores), 2),
                'score_variance': round(abs(statistics.mean(lighthouse_scores) - statistics.mean(pagespeed_scores)), 2)
            }
        
        # Генерируем рекомендации по улучшению
        poor_count = comparison['score_distribution']['poor']
        fair_count = comparison['score_distribution']['fair']
        
        if poor_count > 0:
            comparison['improvement_recommendations'].append(
                f"🔴 Критично: {poor_count} страниц требуют немедленного улучшения SEO"
            )
        
        if fair_count > 0:
            comparison['improvement_recommendations'].append(
                f"🟡 Внимание: {fair_count} страниц нуждаются в оптимизации"
            )
        
        if comparison['test_consistency'].get('score_variance', 0) > 20:
            comparison['improvement_recommendations'].append(
                "⚠️ Обнаружены значительные расхождения между различными SEO инструментами"
            )
        
        return comparison
    
    def _generate_html_report(self, results):
        """Генерация HTML отчета"""
        
        html_template = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Cross-Testing Report</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #eee;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #007bff;
        }
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }
        .metric-label {
            color: #666;
            margin-top: 5px;
        }
        .url-results {
            margin-top: 30px;
        }
        .url-card {
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-bottom: 20px;
            overflow: hidden;
        }
        .url-header {
            background: #f8f9fa;
            padding: 15px 20px;
            border-bottom: 1px solid #ddd;
        }
        .url-content {
            padding: 20px;
        }
        .score-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            margin-right: 10px;
        }
        .score-excellent { background: #28a745; }
        .score-good { background: #ffc107; color: #212529; }
        .score-fair { background: #fd7e14; }
        .score-poor { background: #dc3545; }
        .issues-list {
            list-style: none;
            padding: 0;
        }
        .issues-list li {
            padding: 5px 0;
            border-bottom: 1px solid #eee;
        }
        .priority-high { color: #dc3545; font-weight: bold; }
        .priority-medium { color: #fd7e14; font-weight: bold; }
        .priority-low { color: #28a745; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 SEO Cross-Testing Report</h1>
            <p>Комплексный анализ SEO производительности</p>
            <p><strong>Дата создания:</strong> {timestamp}</p>
        </div>
        
        <div class="summary-grid">
            <div class="metric-card">
                <div class="metric-value">{total_urls}</div>
                <div class="metric-label">Протестировано URL</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{successful_tests}</div>
                <div class="metric-label">Успешных тестов</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{average_score:.1f}</div>
                <div class="metric-label">Средняя оценка</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{excellent_count}</div>
                <div class="metric-label">Отличных страниц</div>
            </div>
        </div>
        
        <h2>📊 Результаты по URL</h2>
        <div class="url-results">
            {url_results_html}
        </div>
        
        <h2>🎯 Общие рекомендации</h2>
        <ul>
            {recommendations_html}
        </ul>
    </div>
</body>
</html>
        """
        
        # Заполняем данные для шаблона
        summary = results.get('summary', {})
        comparison = results.get('comparison', {})
        
        # URL результаты
        url_results_html = ""
        for url, result in results.get('results', {}).items():
            if 'error' in result:
                continue
            
            combined = result.get('combined_analysis', {})
            score = combined.get('overall_health_score', 0)
            
            # Определяем класс для оценки
            if score >= 90:
                score_class = 'score-excellent'
            elif score >= 80:
                score_class = 'score-good'
            elif score >= 60:
                score_class = 'score-fair'
            else:
                score_class = 'score-poor'
            
            # Формируем список проблем
            issues_html = ""
            for issue in combined.get('critical_issues', [])[:5]:
                issues_html += f"<li>❌ {issue}</li>"
            
            url_results_html += f"""
            <div class="url-card">
                <div class="url-header">
                    <h3>{url}</h3>
                    <span class="score-badge {score_class}">{score:.1f}/100</span>
                </div>
                <div class="url-content">
                    <h4>Критические проблемы:</h4>
                    <ul class="issues-list">
                        {issues_html}
                    </ul>
                </div>
            </div>
            """
        
        # Рекомендации
        recommendations_html = ""
        for rec in comparison.get('improvement_recommendations', []):
            recommendations_html += f"<li>{rec}</li>"
        
        # Заполняем шаблон
        html_content = html_template.format(
            timestamp=datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            total_urls=summary.get('total_urls', 0),
            successful_tests=summary.get('successful_tests', 0),
            average_score=summary.get('average_scores', {}).get('overall', 0),
            excellent_count=comparison.get('score_distribution', {}).get('excellent', 0),
            url_results_html=url_results_html,
            recommendations_html=recommendations_html
        )
        
        return html_content

async def main():
    """Главная функция"""
    
    parser = argparse.ArgumentParser(description='SEO Cross-Testing System')
    parser.add_argument('--urls', nargs='+', help='URLs для тестирования')
    parser.add_argument('--urls-file', help='Файл с URLs (по одному на строку)')
    parser.add_argument('--output-format', choices=['json', 'html', 'both'], default='both', help='Формат вывода')
    parser.add_argument('--pagespeed-api-key', help='API ключ для PageSpeed Insights')
    
    args = parser.parse_args()
    
    # Определяем URLs для тестирования
    test_urls = []
    
    if args.urls:
        test_urls.extend(args.urls)
    
    if args.urls_file:
        try:
            with open(args.urls_file, 'r') as f:
                file_urls = [line.strip() for line in f if line.strip()]
                test_urls.extend(file_urls)
        except FileNotFoundError:
            logger.error(f"Файл {args.urls_file} не найден")
            return
    
    # Если URLs не указаны, используем тестовые
    if not test_urls:
        test_urls = [
            "http://localhost:8000/good_seo_test.html",
            "http://localhost:8000/bad_seo_test.html", 
            "http://localhost:8000/ecommerce_test.html"
        ]
        logger.info("Используются тестовые URLs")
    
    # Запускаем тестирование
    orchestrator = SEOTestingOrchestrator(args.pagespeed_api_key)
    
    try:
        results = await orchestrator.run_complete_validation(test_urls, args.output_format)
        
        # Выводим краткую сводку
        summary = results.get('summary', {})
        print(f"\n{'='*60}")
        print("🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
        print(f"{'='*60}")
        print(f"📊 Всего URL: {summary.get('total_urls', 0)}")
        print(f"✅ Успешных тестов: {summary.get('successful_tests', 0)}")
        print(f"❌ Неудачных тестов: {summary.get('failed_tests', 0)}")
        print(f"📈 Средняя оценка: {summary.get('average_scores', {}).get('overall', 0):.1f}/100")
        
        best_url = summary.get('best_performing_url')
        if best_url:
            print(f"🏆 Лучший URL: {best_url['url']} ({best_url['score']:.1f}/100)")
        
        worst_url = summary.get('worst_performing_url')
        if worst_url:
            print(f"🔴 Требует внимания: {worst_url['url']} ({worst_url['score']:.1f}/100)")
        
        print(f"\n📁 Результаты сохранены в: {orchestrator.results_dir}/session_*")
        
    except Exception as e:
        logger.error(f"Ошибка при выполнении тестирования: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(asyncio.run(main()))
