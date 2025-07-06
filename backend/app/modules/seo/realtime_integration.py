"""
Real-time SEO AI Integration Module

Обеспечивает автоматическую интеграцию между SEO Analyzer и AI генератором
для мгновенной оптимизации HTML в процессе генерации.
"""

import asyncio
import json
import time
from typing import Any, Dict, List, Optional, Callable, Tuple
from datetime import datetime
import logging

from app.modules.seo.service import SEOService
from app.modules.seo.integrator import SEOIntegrator
from app.modules.ai_integration.service import AIService
from app.modules.seo.advisor import SEOAdvisor


logger = logging.getLogger(__name__)


class RealTimeSEOAIIntegrator:
    """
    Интегратор для real-time взаимодействия SEO анализатора и AI генератора
    """
    
    def __init__(self):
        self.seo_service = SEOService()
        self.seo_integrator = SEOIntegrator()
        self.ai_service = AIService()
        self.seo_advisor = SEOAdvisor()
        
        # Настройки интеграции
        self.config = {
            "auto_optimization": True,
            "min_score_threshold": 70,  # Минимальный SEO балл для автоматической оптимизации
            "critical_issues_auto_fix": True,
            "realtime_analysis_enabled": True,
            "optimization_cycles_limit": 3,  # Максимум циклов оптимизации
            "analysis_debounce_ms": 500,  # Задержка для группировки изменений
            "ai_suggestions_threshold": 60,  # Балл ниже которого запрашиваются AI предложения
        }
        
        # Статистика и мониторинг
        self.stats = {
            "optimizations_performed": 0,
            "ai_suggestions_generated": 0,
            "seo_score_improvements": [],
            "processing_times": [],
            "total_cycles": 0
        }
        
        # Очередь для обработки изменений
        self.optimization_queue = asyncio.Queue()
        
        # Активные сессии оптимизации
        self.active_sessions = {}
        
        # Event callbacks
        self.event_callbacks = {
            "analysis_complete": [],
            "optimization_applied": [],
            "ai_suggestion_generated": [],
            "error_occurred": []
        }
    
    async def start_realtime_optimization(
        self, 
        session_id: str,
        initial_html: str,
        context: Optional[Dict[str, Any]] = None,
        target_keywords: Optional[List[str]] = None,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Запуск real-time оптимизации HTML
        
        Args:
            session_id: Уникальный идентификатор сессии
            initial_html: Исходный HTML
            context: Контекст контента
            target_keywords: Целевые ключевые слова
            progress_callback: Функция для отправки обновлений прогресса
        
        Returns:
            Результат оптимизации с подробной статистикой
        """
        start_time = time.time()
        
        try:
            # Создаем сессию оптимизации
            session = self._create_optimization_session(
                session_id, initial_html, context, target_keywords, progress_callback
            )
            
            # Первоначальный анализ
            await self._emit_progress(session, "Начальный SEO анализ...", 10)
            initial_analysis = await self._analyze_html_comprehensive(
                initial_html, target_keywords, context
            )
            
            session["current_html"] = initial_html
            session["initial_analysis"] = initial_analysis
            session["optimization_history"] = []
            
            # Если SEO балл уже высокий, минимальная оптимизация
            if initial_analysis["seo_score"] >= self.config["min_score_threshold"]:
                await self._emit_progress(session, "HTML уже хорошо оптимизирован", 90)
                minor_improvements = await self._apply_minor_improvements(
                    session, initial_analysis
                )
                return self._finalize_optimization_session(session, minor_improvements)
            
            # Запуск цикла оптимизации
            await self._emit_progress(session, "Запуск цикла оптимизации...", 20)
            optimization_result = await self._run_optimization_cycle(session)
            
            processing_time = time.time() - start_time
            self.stats["processing_times"].append(processing_time)
            
            await self._emit_progress(session, "Оптимизация завершена", 100)
            
            return self._finalize_optimization_session(session, optimization_result)
            
        except Exception as e:
            logger.error(f"Ошибка в real-time оптимизации: {str(e)}")
            await self._emit_error(session_id, str(e))
            raise
        finally:
            # Очистка сессии
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
    
    async def _run_optimization_cycle(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """Основной цикл оптимизации"""
        current_html = session["current_html"]
        cycle_count = 0
        max_cycles = self.config["optimization_cycles_limit"]
        
        optimization_steps = []
        
        while cycle_count < max_cycles:
            cycle_count += 1
            cycle_start = time.time()
            
            await self._emit_progress(
                session, f"Цикл оптимизации {cycle_count}/{max_cycles}", 
                20 + (cycle_count * 20)
            )
            
            # Анализ текущего состояния
            current_analysis = await self._analyze_html_comprehensive(
                current_html, session["target_keywords"], session["context"]
            )
            
            # Определяем критические проблемы
            critical_issues = [
                issue for issue in current_analysis["issues"] 
                if self._is_critical_issue(issue)
            ]
            
            # Если критических проблем нет и балл приемлемый - завершаем
            if (not critical_issues and 
                current_analysis["seo_score"] >= self.config["min_score_threshold"]):
                break
            
            # Применяем автоматические исправления
            auto_fixes_result = await self._apply_automatic_fixes(
                session, current_html, current_analysis
            )
            current_html = auto_fixes_result["optimized_html"]
            
            # Получаем AI предложения для оставшихся проблем
            if current_analysis["seo_score"] < self.config["ai_suggestions_threshold"]:
                ai_improvements = await self._get_ai_improvements(
                    session, current_html, current_analysis
                )
                if ai_improvements:
                    current_html = ai_improvements["improved_html"]
            
            # Записываем шаг оптимизации
            step_time = time.time() - cycle_start
            optimization_steps.append({
                "cycle": cycle_count,
                "initial_score": current_analysis["seo_score"],
                "auto_fixes": auto_fixes_result["fixes_applied"],
                "ai_improvements": ai_improvements.get("improvements_applied", []) if 'ai_improvements' in locals() else [],
                "processing_time": step_time,
                "final_html_length": len(current_html)
            })
            
            # Обновляем текущий HTML в сессии
            session["current_html"] = current_html
            session["optimization_history"].append(optimization_steps[-1])
        
        # Финальный анализ
        final_analysis = await self._analyze_html_comprehensive(
            current_html, session["target_keywords"], session["context"]
        )
        
        return {
            "optimized_html": current_html,
            "final_analysis": final_analysis,
            "optimization_steps": optimization_steps,
            "cycles_performed": cycle_count,
            "total_improvements": len([step for step in optimization_steps if step["auto_fixes"] or step["ai_improvements"]])
        }
    
    async def _apply_automatic_fixes(
        self, 
        session: Dict[str, Any], 
        html: str, 
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Применение автоматических SEO исправлений"""
        
        fixes_applied = []
        
        try:
            # Используем встроенный SEO интегратор для базовых исправлений
            integration_result = self.seo_integrator.integrate_seo_recommendations(
                html=html,
                content_context=session["context"],
                target_keywords=session["target_keywords"],
                auto_apply=True
            )
            
            optimized_html = integration_result["optimized_html"]
            fixes_applied.extend(integration_result["improvements_applied"]["improvements_list"])
            
            # Дополнительные автоматические исправления
            additional_fixes = await self._apply_advanced_auto_fixes(
                optimized_html, analysis, session["context"]
            )
            
            if additional_fixes["html_changed"]:
                optimized_html = additional_fixes["html"]
                fixes_applied.extend(additional_fixes["fixes"])
            
            await self._emit_event("optimization_applied", {
                "session_id": session["session_id"],
                "fixes_applied": fixes_applied,
                "html_length_change": len(optimized_html) - len(html)
            })
            
            return {
                "optimized_html": optimized_html,
                "fixes_applied": fixes_applied,
                "html_changed": len(fixes_applied) > 0
            }
            
        except Exception as e:
            logger.error(f"Ошибка при применении автоматических исправлений: {str(e)}")
            return {
                "optimized_html": html,
                "fixes_applied": [],
                "html_changed": False,
                "error": str(e)
            }
    
    async def _get_ai_improvements(
        self, 
        session: Dict[str, Any],
        html: str, 
        analysis: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Получение улучшений от AI"""
        
        try:
            # Формируем промпт для AI на основе проблем SEO
            seo_prompt = self._create_seo_improvement_prompt(analysis, session["context"])
            
            # Получаем предложения от AI
            ai_suggestions = await self.ai_service.suggest_improvements(html)
            
            # Генерируем улучшенный HTML с помощью AI
            improvement_prompt = f"""
            Улучши следующий HTML для лучшего SEO, основываясь на этих проблемах:
            {json.dumps(analysis['issues'], ensure_ascii=False, indent=2)}
            
            Контекст: {json.dumps(session['context'], ensure_ascii=False) if session['context'] else 'Не указан'}
            Ключевые слова: {', '.join(session['target_keywords']) if session['target_keywords'] else 'Не указаны'}
            
            HTML:
            {html}
            
            Инструкции:
            1. Исправь все критические SEO проблемы
            2. Оптимизируй заголовки и мета-теги
            3. Улучши структуру контента
            4. Добавь недостающие SEO элементы
            5. Сохрани семантику и функциональность
            
            Верни только улучшенный HTML без дополнительных комментариев:
            """
            
            improved_html = await self.ai_service.enhance_content(improvement_prompt, "seo_optimization")
            
            # Валидируем улучшения
            if self._validate_ai_improvements(html, improved_html):
                improvements_applied = await self._identify_ai_improvements(html, improved_html, analysis)
                
                await self._emit_event("ai_suggestion_generated", {
                    "session_id": session["session_id"],
                    "improvements": improvements_applied,
                    "html_length_change": len(improved_html) - len(html)
                })
                
                self.stats["ai_suggestions_generated"] += 1
                
                return {
                    "improved_html": improved_html,
                    "improvements_applied": improvements_applied,
                    "ai_suggestions": ai_suggestions
                }
            
        except Exception as e:
            logger.error(f"Ошибка при получении AI улучшений: {str(e)}")
            await self._emit_error(session["session_id"], f"AI optimization error: {str(e)}")
        
        return None
    
    async def _apply_advanced_auto_fixes(
        self, 
        html: str, 
        analysis: Dict[str, Any], 
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Применение расширенных автоматических исправлений"""
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        fixes = []
        html_changed = False
        
        # Добавление мета-тега viewport если отсутствует
        if not soup.find("meta", attrs={"name": "viewport"}):
            head = soup.find("head") or soup.new_tag("head")
            viewport_meta = soup.new_tag("meta", attrs={
                "name": "viewport",
                "content": "width=device-width, initial-scale=1.0"
            })
            head.append(viewport_meta)
            fixes.append("Добавлен meta viewport для мобильной адаптации")
            html_changed = True
        
        # Добавление lang атрибута к html тегу
        html_tag = soup.find("html")
        if html_tag and not html_tag.get("lang"):
            html_tag["lang"] = "ru"
            fixes.append("Добавлен атрибут lang='ru' к HTML тегу")
            html_changed = True
        
        # Добавление charset если отсутствует
        if not soup.find("meta", attrs={"charset": True}):
            head = soup.find("head") or soup.new_tag("head")
            charset_meta = soup.new_tag("meta", attrs={"charset": "UTF-8"})
            head.insert(0, charset_meta)
            fixes.append("Добавлен meta charset=UTF-8")
            html_changed = True
        
        # Оптимизация изображений
        images = soup.find_all("img")
        for img in images:
            img_fixed = False
            
            # Добавление loading="lazy"
            if not img.get("loading"):
                img["loading"] = "lazy"
                img_fixed = True
            
            # Генерация alt если отсутствует
            if not img.get("alt"):
                src = img.get("src", "")
                if src:
                    # Генерируем alt на основе имени файла
                    filename = src.split("/")[-1].split(".")[0]
                    alt_text = filename.replace("_", " ").replace("-", " ").title()
                    img["alt"] = alt_text
                    img_fixed = True
                else:
                    img["alt"] = "Изображение"
                    img_fixed = True
            
            if img_fixed:
                html_changed = True
        
        if images and html_changed:
            fixes.append(f"Оптимизированы изображения ({len(images)} шт.)")
        
        # Улучшение внутренней перелинковки
        links = soup.find_all("a", href=True)
        external_links = [link for link in links if link["href"].startswith("http")]
        
        # Добавляем rel="noopener" к внешним ссылкам
        for link in external_links:
            if not link.get("rel"):
                link["rel"] = "noopener"
                html_changed = True
        
        if external_links and html_changed:
            fixes.append(f"Добавлен rel='noopener' к внешним ссылкам ({len(external_links)} шт.)")
        
        # Добавление базовых Open Graph тегов если контекст предоставлен
        if context and not soup.find("meta", attrs={"property": "og:title"}):
            head = soup.find("head") or soup.new_tag("head")
            
            og_tags = [
                ("og:title", context.get("title", "")),
                ("og:description", context.get("description", "")),
                ("og:type", "website"),
                ("og:url", context.get("url", ""))
            ]
            
            for prop, content in og_tags:
                if content:
                    og_tag = soup.new_tag("meta", attrs={"property": prop, "content": content})
                    head.append(og_tag)
                    html_changed = True
            
            if html_changed:
                fixes.append("Добавлены базовые Open Graph мета-теги")
        
        return {
            "html": str(soup),
            "fixes": fixes,
            "html_changed": html_changed
        }
    
    async def _analyze_html_comprehensive(
        self, 
        html: str, 
        target_keywords: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Комплексный анализ HTML"""
        
        # Базовый SEO анализ
        seo_analysis = self.seo_service.analyze_html(html)
        
        # Расширенный анализ с учетом контекста
        if target_keywords or context:
            advisor_analysis = self.seo_advisor.analyze_and_recommend(
                html=html,
                target_keywords=target_keywords,
                target_audience=context.get("target_audience", "general") if context else "general"
            )
            
            # Объединяем результаты
            combined_analysis = {
                **seo_analysis,
                "seo_score": advisor_analysis["overall_score"],
                "recommendations": advisor_analysis["recommendations"],
                "priority_actions": advisor_analysis["priority_actions"],
                "keyword_analysis": advisor_analysis.get("keyword_analysis", {}),
                "content_quality": advisor_analysis.get("content_quality", {})
            }
        else:
            combined_analysis = seo_analysis
        
        await self._emit_event("analysis_complete", {
            "html_length": len(html),
            "seo_score": combined_analysis.get("seo_score", combined_analysis["score"]),
            "issues_count": len(combined_analysis["issues"]),
            "recommendations_count": len(combined_analysis.get("recommendations", []))
        })
        
        return combined_analysis
    
    def _create_seo_improvement_prompt(
        self, 
        analysis: Dict[str, Any], 
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Создание промпта для AI улучшений"""
        
        critical_issues = [issue for issue in analysis["issues"] if self._is_critical_issue(issue)]
        
        prompt = f"""
        Анализ SEO показал следующие проблемы:
        
        Критические проблемы:
        {json.dumps(critical_issues, ensure_ascii=False, indent=2)}
        
        Все проблемы:
        {json.dumps(analysis["issues"], ensure_ascii=False, indent=2)}
        
        Текущий SEO балл: {analysis.get('seo_score', analysis.get('score', 0))}
        
        Контекст контента:
        {json.dumps(context, ensure_ascii=False, indent=2) if context else 'Не предоставлен'}
        
        Необходимо предложить конкретные улучшения для повышения SEO качества.
        """
        
        return prompt
    
    def _is_critical_issue(self, issue: str) -> bool:
        """Определение критичности SEO проблемы"""
        critical_patterns = [
            "missing title",
            "missing meta description", 
            "missing h1",
            "missing alt",
            "отсутствует title",
            "отсутствует meta description",
            "отсутствует h1",
            "missing viewport",
            "multiple h1"
        ]
        
        return any(pattern.lower() in issue.lower() for pattern in critical_patterns)
    
    def _validate_ai_improvements(self, original_html: str, improved_html: str) -> bool:
        """Валидация улучшений от AI"""
        
        # Базовые проверки
        if not improved_html or len(improved_html.strip()) == 0:
            return False
        
        # Проверка что HTML не стал значительно больше
        if len(improved_html) > len(original_html) * 2:
            logger.warning("AI генерировал слишком большой HTML")
            return False
        
        # Проверка базовой HTML структуры
        from bs4 import BeautifulSoup
        try:
            soup = BeautifulSoup(improved_html, "html.parser")
            # Проверяем что есть базовые элементы
            if not soup.find(["html", "head", "body", "title", "div", "p", "h1", "h2"]):
                return False
        except Exception:
            return False
        
        return True
    
    async def _identify_ai_improvements(
        self, 
        original_html: str, 
        improved_html: str, 
        analysis: Dict[str, Any]
    ) -> List[str]:
        """Идентификация конкретных улучшений от AI"""
        
        improvements = []
        
        # Сравниваем анализы до и после
        try:
            improved_analysis = await self._analyze_html_comprehensive(improved_html)
            
            # Сравниваем количество проблем
            original_issues = len(analysis["issues"])
            improved_issues = len(improved_analysis["issues"])
            
            if improved_issues < original_issues:
                improvements.append(f"Исправлено {original_issues - improved_issues} SEO проблем")
            
            # Сравниваем баллы
            original_score = analysis.get("seo_score", analysis.get("score", 0))
            improved_score = improved_analysis.get("seo_score", improved_analysis.get("score", 0))
            
            if improved_score > original_score:
                improvements.append(f"SEO балл увеличен с {original_score} до {improved_score}")
            
            # Анализируем структурные изменения
            from bs4 import BeautifulSoup
            orig_soup = BeautifulSoup(original_html, "html.parser")
            impr_soup = BeautifulSoup(improved_html, "html.parser")
            
            # Проверяем добавление мета-тегов
            orig_metas = len(orig_soup.find_all("meta"))
            impr_metas = len(impr_soup.find_all("meta"))
            
            if impr_metas > orig_metas:
                improvements.append(f"Добавлено {impr_metas - orig_metas} мета-тегов")
            
            # Проверяем улучшение заголовков
            orig_title = orig_soup.find("title")
            impr_title = impr_soup.find("title")
            
            if not orig_title and impr_title:
                improvements.append("Добавлен title тег")
            elif orig_title and impr_title and orig_title.get_text() != impr_title.get_text():
                improvements.append("Улучшен title тег")
            
        except Exception as e:
            logger.error(f"Ошибка при идентификации AI улучшений: {str(e)}")
            improvements.append("AI внес улучшения (детали недоступны)")
        
        return improvements
    
    def _create_optimization_session(
        self, 
        session_id: str, 
        html: str, 
        context: Optional[Dict[str, Any]],
        target_keywords: Optional[List[str]],
        progress_callback: Optional[Callable]
    ) -> Dict[str, Any]:
        """Создание сессии оптимизации"""
        
        session = {
            "session_id": session_id,
            "start_time": datetime.now(),
            "current_html": html,
            "context": context,
            "target_keywords": target_keywords,
            "progress_callback": progress_callback,
            "status": "active"
        }
        
        self.active_sessions[session_id] = session
        return session
    
    async def _emit_progress(self, session: Dict[str, Any], message: str, progress: int):
        """Отправка обновления прогресса"""
        if session.get("progress_callback"):
            try:
                await session["progress_callback"]({
                    "session_id": session["session_id"],
                    "message": message,
                    "progress": progress,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Ошибка при отправке прогресса: {str(e)}")
    
    async def _emit_event(self, event_type: str, data: Dict[str, Any]):
        """Отправка события"""
        if event_type in self.event_callbacks:
            for callback in self.event_callbacks[event_type]:
                try:
                    await callback(data)
                except Exception as e:
                    logger.error(f"Ошибка в callback для события {event_type}: {str(e)}")
    
    async def _emit_error(self, session_id: str, error_message: str):
        """Отправка уведомления об ошибке"""
        await self._emit_event("error_occurred", {
            "session_id": session_id,
            "error": error_message,
            "timestamp": datetime.now().isoformat()
        })
    
    def _finalize_optimization_session(
        self, 
        session: Dict[str, Any], 
        result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Финализация сессии оптимизации"""
        
        end_time = datetime.now()
        processing_time = (end_time - session["start_time"]).total_seconds()
        
        # Обновляем статистику
        self.stats["optimizations_performed"] += 1
        self.stats["total_cycles"] += result.get("cycles_performed", 0)
        
        if "final_analysis" in result:
            initial_score = session.get("initial_analysis", {}).get("seo_score", 0)
            final_score = result["final_analysis"].get("seo_score", 0)
            score_improvement = final_score - initial_score
            
            if score_improvement > 0:
                self.stats["seo_score_improvements"].append(score_improvement)
        
        # Формируем финальный результат
        final_result = {
            "session_id": session["session_id"],
            "processing_time": processing_time,
            "initial_analysis": session.get("initial_analysis", {}),
            "optimization_result": result,
            "session_stats": {
                "start_time": session["start_time"].isoformat(),
                "end_time": end_time.isoformat(),
                "processing_time_seconds": processing_time,
                "optimization_cycles": result.get("cycles_performed", 0),
                "total_improvements": result.get("total_improvements", 0)
            },
            "system_stats": self.get_system_stats()
        }
        
        return final_result
    
    async def _apply_minor_improvements(
        self, 
        session: Dict[str, Any], 
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Применение минорных улучшений для уже хорошо оптимизированного HTML"""
        
        html = session["current_html"]
        
        # Применяем только базовые исправления
        minor_fixes = await self._apply_advanced_auto_fixes(html, analysis, session["context"])
        
        if minor_fixes["html_changed"]:
            optimized_html = minor_fixes["html"]
            final_analysis = await self._analyze_html_comprehensive(
                optimized_html, session["target_keywords"], session["context"]
            )
        else:
            optimized_html = html
            final_analysis = analysis
        
        return {
            "optimized_html": optimized_html,
            "final_analysis": final_analysis,
            "optimization_steps": [{
                "cycle": 1,
                "type": "minor_improvements",
                "fixes_applied": minor_fixes["fixes"],
                "processing_time": 0.1
            }],
            "cycles_performed": 1,
            "total_improvements": len(minor_fixes["fixes"])
        }
    
    # Методы для управления системой
    
    def add_event_callback(self, event_type: str, callback: Callable):
        """Добавление callback для событий"""
        if event_type in self.event_callbacks:
            self.event_callbacks[event_type].append(callback)
    
    def remove_event_callback(self, event_type: str, callback: Callable):
        """Удаление callback для событий"""
        if event_type in self.event_callbacks and callback in self.event_callbacks[event_type]:
            self.event_callbacks[event_type].remove(callback)
    
    def update_config(self, new_config: Dict[str, Any]):
        """Обновление конфигурации"""
        self.config.update(new_config)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Получение статистики системы"""
        avg_processing_time = (
            sum(self.stats["processing_times"]) / len(self.stats["processing_times"])
            if self.stats["processing_times"] else 0
        )
        
        avg_score_improvement = (
            sum(self.stats["seo_score_improvements"]) / len(self.stats["seo_score_improvements"])
            if self.stats["seo_score_improvements"] else 0
        )
        
        return {
            "optimizations_performed": self.stats["optimizations_performed"],
            "ai_suggestions_generated": self.stats["ai_suggestions_generated"],
            "total_cycles": self.stats["total_cycles"],
            "average_processing_time": avg_processing_time,
            "average_score_improvement": avg_score_improvement,
            "active_sessions_count": len(self.active_sessions),
            "config": self.config.copy()
        }
    
    async def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Получение статуса сессии"""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            return {
                "session_id": session_id,
                "status": session["status"],
                "start_time": session["start_time"].isoformat(),
                "current_progress": session.get("current_progress", 0),
                "optimization_history": session.get("optimization_history", [])
            }
        return None
    
    async def cancel_session(self, session_id: str) -> bool:
        """Отмена сессии оптимизации"""
        if session_id in self.active_sessions:
            self.active_sessions[session_id]["status"] = "cancelled"
            del self.active_sessions[session_id]
            return True
        return False


# Глобальный экземпляр интегратора
realtime_integrator = RealTimeSEOAIIntegrator()
