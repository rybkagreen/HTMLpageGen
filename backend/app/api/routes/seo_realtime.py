"""
Real-time SEO API Routes

API эндпоинты для real-time интеграции SEO анализатора и AI генератора
"""

import uuid
from typing import Any, Dict, List, Optional
from datetime import datetime

from fastapi import APIRouter, WebSocket, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field

from app.modules.seo.realtime_integration import realtime_integrator
from app.modules.seo.websocket_service import websocket_manager, websocket_endpoint


router = APIRouter()


# Pydantic модели для API

class RealTimeOptimizationRequest(BaseModel):
    html: str = Field(..., description="HTML код для оптимизации")
    context: Optional[Dict[str, Any]] = Field(None, description="Контекст контента")
    target_keywords: Optional[List[str]] = Field(None, description="Целевые ключевые слова")
    auto_apply: bool = Field(True, description="Автоматически применять исправления")


class RealTimeOptimizationResponse(BaseModel):
    session_id: str
    processing_time: float
    initial_analysis: Dict[str, Any]
    optimization_result: Dict[str, Any]
    session_stats: Dict[str, Any]
    system_stats: Dict[str, Any]


class SessionStatusResponse(BaseModel):
    session_id: str
    status: Optional[Dict[str, Any]]
    found: bool


class SystemStatsResponse(BaseModel):
    optimizations_performed: int
    ai_suggestions_generated: int
    total_cycles: int
    average_processing_time: float
    average_score_improvement: float
    active_sessions_count: int
    config: Dict[str, Any]


class ConfigUpdateRequest(BaseModel):
    auto_optimization: Optional[bool] = None
    min_score_threshold: Optional[int] = None
    critical_issues_auto_fix: Optional[bool] = None
    optimization_cycles_limit: Optional[int] = None
    ai_suggestions_threshold: Optional[int] = None


# API эндпоинты

@router.post("/optimize", response_model=RealTimeOptimizationResponse)
async def start_realtime_optimization(
    request: RealTimeOptimizationRequest,
    background_tasks: BackgroundTasks
):
    """
    Запуск real-time оптимизации HTML
    
    Этот эндпоинт запускает полный цикл автоматической SEO оптимизации:
    1. Анализирует HTML на предмет SEO проблем
    2. Применяет автоматические исправления
    3. Использует AI для дополнительных улучшений
    4. Возвращает оптимизированный HTML с детальной статистикой
    """
    
    try:
        session_id = str(uuid.uuid4())
        
        # Запускаем оптимизацию
        result = await realtime_integrator.start_realtime_optimization(
            session_id=session_id,
            initial_html=request.html,
            context=request.context,
            target_keywords=request.target_keywords,
            progress_callback=None  # Для HTTP API не используем callback
        )
        
        return RealTimeOptimizationResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка оптимизации: {str(e)}")


@router.get("/session/{session_id}/status", response_model=SessionStatusResponse)
async def get_session_status(session_id: str):
    """
    Получение статуса сессии оптимизации
    
    Возвращает текущий статус активной сессии оптимизации,
    включая прогресс и историю изменений.
    """
    
    try:
        status = await realtime_integrator.get_session_status(session_id)
        
        return SessionStatusResponse(
            session_id=session_id,
            status=status,
            found=status is not None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения статуса: {str(e)}")


@router.delete("/session/{session_id}")
async def cancel_optimization_session(session_id: str):
    """
    Отмена активной сессии оптимизации
    
    Прерывает выполнение сессии оптимизации и освобождает ресурсы.
    """
    
    try:
        cancelled = await realtime_integrator.cancel_session(session_id)
        
        if cancelled:
            return {"message": f"Сессия {session_id} отменена", "cancelled": True}
        else:
            return {"message": f"Сессия {session_id} не найдена", "cancelled": False}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка отмены сессии: {str(e)}")


@router.get("/stats", response_model=SystemStatsResponse)
async def get_system_stats():
    """
    Получение статистики системы real-time оптимизации
    
    Возвращает общую статистику работы системы, включая:
    - Количество выполненных оптимизаций
    - Среднее время обработки
    - Средний прирост SEO баллов
    - Конфигурацию системы
    """
    
    try:
        stats = realtime_integrator.get_system_stats()
        return SystemStatsResponse(**stats)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения статистики: {str(e)}")


@router.put("/config")
async def update_system_config(request: ConfigUpdateRequest):
    """
    Обновление конфигурации системы
    
    Позволяет изменить параметры работы real-time оптимизации:
    - Пороги для автоматической оптимизации
    - Лимиты циклов оптимизации
    - Включение/выключение различных функций
    """
    
    try:
        # Фильтруем только не None значения
        config_updates = {k: v for k, v in request.dict().items() if v is not None}
        
        if not config_updates:
            raise HTTPException(status_code=400, detail="Не указаны параметры для обновления")
        
        realtime_integrator.update_config(config_updates)
        
        return {
            "message": "Конфигурация обновлена",
            "updated_config": config_updates,
            "current_config": realtime_integrator.config
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления конфигурации: {str(e)}")


@router.get("/config")
async def get_system_config():
    """
    Получение текущей конфигурации системы
    """
    
    return {
        "config": realtime_integrator.config,
        "description": {
            "auto_optimization": "Автоматическая оптимизация включена",
            "min_score_threshold": "Минимальный SEO балл для оптимизации",
            "critical_issues_auto_fix": "Автоматическое исправление критических проблем",
            "realtime_analysis_enabled": "Real-time анализ включен",
            "optimization_cycles_limit": "Максимальное количество циклов оптимизации",
            "analysis_debounce_ms": "Задержка для группировки изменений (мс)",
            "ai_suggestions_threshold": "Балл для запроса AI предложений"
        }
    }


# WebSocket эндпоинты

@router.websocket("/ws")
async def websocket_realtime_seo(websocket: WebSocket, client_id: Optional[str] = None):
    """
    WebSocket эндпоинт для real-time SEO оптимизации
    
    Обеспечивает двустороннюю связь для:
    - Отправки HTML на оптимизацию
    - Получения real-time обновлений прогресса
    - Мониторинга процесса оптимизации
    - Получения уведомлений о завершении
    
    Протокол сообщений:
    
    Клиент -> Сервер:
    {
        "type": "start_optimization",
        "html": "...",
        "context": {...},
        "target_keywords": [...]
    }
    
    Сервер -> Клиент:
    {
        "type": "optimization_progress",
        "session_id": "...",
        "message": "...",
        "progress": 50
    }
    """
    
    await websocket_endpoint(websocket, client_id)


@router.get("/ws/stats")
async def get_websocket_stats():
    """
    Получение статистики WebSocket соединений
    """
    
    try:
        stats = websocket_manager.get_connection_stats()
        return {
            "websocket_stats": stats,
            "system_stats": realtime_integrator.get_system_stats()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения статистики WebSocket: {str(e)}")


@router.post("/ws/notification")
async def send_system_notification(notification: str, notification_type: str = "info"):
    """
    Отправка системного уведомления всем подключенным WebSocket клиентам
    """
    
    try:
        await websocket_manager.send_system_notification(notification, notification_type)
        
        return {
            "message": "Уведомление отправлено",
            "notification": notification,
            "type": notification_type,
            "sent_to_connections": len(websocket_manager.active_connections)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка отправки уведомления: {str(e)}")


# Вспомогательные эндпоинты для тестирования и мониторинга

@router.post("/test/analyze")
async def test_seo_analysis(html: str):
    """
    Тестовый эндпоинт для быстрого SEO анализа без оптимизации
    """
    
    try:
        # Используем внутренний анализатор для быстрой проверки
        analysis = realtime_integrator.seo_service.analyze_html(html)
        
        return {
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка анализа: {str(e)}")


@router.post("/test/ai-suggestions")
async def test_ai_suggestions(html: str, issues: List[str]):
    """
    Тестовый эндпоинт для получения AI предложений
    """
    
    try:
        # Получаем AI предложения
        suggestions = await realtime_integrator.ai_service.suggest_improvements(html)
        
        return {
            "original_html_length": len(html),
            "issues_provided": issues,
            "ai_suggestions": suggestions,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения AI предложений: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Проверка состояния сервиса real-time SEO оптимизации
    """
    
    try:
        # Проверяем основные компоненты
        seo_service_ok = realtime_integrator.seo_service is not None
        ai_service_ok = realtime_integrator.ai_service is not None
        websocket_manager_ok = len(websocket_manager.active_connections) >= 0
        
        ai_provider_info = realtime_integrator.ai_service.get_provider_info()
        
        health_status = {
            "status": "healthy" if all([seo_service_ok, ai_service_ok, websocket_manager_ok]) else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "seo_service": "ok" if seo_service_ok else "error",
                "ai_service": "ok" if ai_service_ok else "error",
                "websocket_manager": "ok" if websocket_manager_ok else "error"
            },
            "ai_provider": ai_provider_info,
            "active_sessions": len(realtime_integrator.active_sessions),
            "active_ws_connections": len(websocket_manager.active_connections),
            "system_stats": realtime_integrator.get_system_stats()
        }
        
        return health_status
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


# Документация и примеры

@router.get("/docs/examples")
async def get_api_examples():
    """
    Примеры использования API
    """
    
    return {
        "http_optimization_example": {
            "url": "/api/seo-realtime/optimize",
            "method": "POST",
            "body": {
                "html": "<!DOCTYPE html><html><head><title>Test</title></head><body><h1>Hello World</h1></body></html>",
                "context": {
                    "title": "Test Page",
                    "description": "A test page for SEO optimization",
                    "url": "https://example.com/test"
                },
                "target_keywords": ["test", "seo", "optimization"],
                "auto_apply": True
            }
        },
        "websocket_example": {
            "url": "ws://localhost:8000/api/seo-realtime/ws",
            "messages": {
                "start_optimization": {
                    "type": "start_optimization",
                    "html": "<!DOCTYPE html>...",
                    "context": {"title": "Test"},
                    "target_keywords": ["test"]
                },
                "get_system_stats": {
                    "type": "get_system_stats"
                },
                "ping": {
                    "type": "ping"
                }
            }
        },
        "config_update_example": {
            "url": "/api/seo-realtime/config",
            "method": "PUT",
            "body": {
                "min_score_threshold": 80,
                "optimization_cycles_limit": 5,
                "ai_suggestions_threshold": 70
            }
        }
    }


@router.get("/docs/protocol")
async def get_websocket_protocol():
    """
    Документация WebSocket протокола
    """
    
    return {
        "websocket_protocol": {
            "connection": {
                "url": "ws://host/api/seo-realtime/ws",
                "optional_params": ["client_id"]
            },
            "client_messages": {
                "start_optimization": {
                    "description": "Запуск новой сессии оптимизации",
                    "fields": {
                        "type": "start_optimization",
                        "html": "HTML код для оптимизации",
                        "context": "Опциональный контекст (объект)",
                        "target_keywords": "Опциональные ключевые слова (массив)"
                    }
                },
                "cancel_optimization": {
                    "description": "Отмена сессии оптимизации",
                    "fields": {
                        "type": "cancel_optimization",
                        "session_id": "ID сессии для отмены"
                    }
                },
                "get_session_status": {
                    "description": "Запрос статуса сессии",
                    "fields": {
                        "type": "get_session_status",
                        "session_id": "ID сессии"
                    }
                },
                "get_system_stats": {
                    "description": "Запрос статистики системы",
                    "fields": {
                        "type": "get_system_stats"
                    }
                },
                "ping": {
                    "description": "Ping для поддержания соединения",
                    "fields": {
                        "type": "ping"
                    }
                }
            },
            "server_messages": {
                "connection_established": "Подтверждение подключения",
                "session_created": "Сессия создана",
                "optimization_started": "Оптимизация начата",
                "optimization_progress": "Прогресс оптимизации",
                "optimization_completed": "Оптимизация завершена",
                "optimization_cancelled": "Оптимизация отменена",
                "optimization_error": "Ошибка оптимизации",
                "analysis_complete": "Анализ завершен",
                "optimization_applied": "Оптимизация применена",
                "ai_suggestion_generated": "AI предложение сгенерировано",
                "error_occurred": "Произошла ошибка",
                "system_notification": "Системное уведомление",
                "pong": "Ответ на ping"
            }
        }
    }
