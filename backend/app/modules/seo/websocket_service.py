"""
WebSocket Service for Real-time SEO Optimization

Обеспечивает real-time обмен данными между клиентом и сервером
во время процесса SEO оптимизации.
"""

import asyncio
import json
import uuid
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import logging

from fastapi import WebSocket, WebSocketDisconnect
from app.modules.seo.realtime_integration import realtime_integrator


logger = logging.getLogger(__name__)


class SEOWebSocketManager:
    """
    Менеджер WebSocket соединений для real-time SEO оптимизации
    """
    
    def __init__(self):
        # Активные WebSocket соединения
        self.active_connections: Dict[str, WebSocket] = {}
        
        # Маппинг session_id -> connection_id
        self.session_connections: Dict[str, str] = {}
        
        # Очередь сообщений для каждого соединения
        self.message_queues: Dict[str, asyncio.Queue] = {}
        
        # Статистика соединений
        self.connection_stats = {
            "total_connections": 0,
            "active_connections": 0,
            "sessions_created": 0,
            "optimizations_completed": 0
        }
        
        # Настройка обработчиков событий
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        """Настройка обработчиков событий от realtime_integrator"""
        
        # Подписываемся на события оптимизации
        realtime_integrator.add_event_callback(
            "analysis_complete", 
            self._on_analysis_complete
        )
        
        realtime_integrator.add_event_callback(
            "optimization_applied", 
            self._on_optimization_applied
        )
        
        realtime_integrator.add_event_callback(
            "ai_suggestion_generated", 
            self._on_ai_suggestion_generated
        )
        
        realtime_integrator.add_event_callback(
            "error_occurred", 
            self._on_error_occurred
        )
    
    async def connect(self, websocket: WebSocket, client_id: Optional[str] = None) -> str:
        """
        Подключение нового WebSocket клиента
        
        Args:
            websocket: WebSocket соединение
            client_id: Опциональный ID клиента
        
        Returns:
            Уникальный connection_id
        """
        await websocket.accept()
        
        connection_id = client_id or str(uuid.uuid4())
        
        self.active_connections[connection_id] = websocket
        self.message_queues[connection_id] = asyncio.Queue()
        
        self.connection_stats["total_connections"] += 1
        self.connection_stats["active_connections"] += 1
        
        logger.info(f"WebSocket клиент подключен: {connection_id}")
        
        # Отправляем приветственное сообщение
        await self._send_to_connection(connection_id, {
            "type": "connection_established",
            "connection_id": connection_id,
            "timestamp": datetime.now().isoformat(),
            "server_info": {
                "version": "1.0.0",
                "features": ["real_time_seo", "ai_optimization", "progress_tracking"]
            }
        })
        
        # Запускаем обработчик сообщений для этого соединения
        asyncio.create_task(self._handle_connection_messages(connection_id))
        
        return connection_id
    
    async def disconnect(self, connection_id: str):
        """Отключение WebSocket клиента"""
        
        if connection_id in self.active_connections:
            # Отменяем активные сессии для этого соединения
            session_id = None
            for sid, cid in self.session_connections.items():
                if cid == connection_id:
                    session_id = sid
                    break
            
            if session_id:
                await realtime_integrator.cancel_session(session_id)
                del self.session_connections[session_id]
            
            # Удаляем соединение
            del self.active_connections[connection_id]
            
            if connection_id in self.message_queues:
                del self.message_queues[connection_id]
            
            self.connection_stats["active_connections"] -= 1
            
            logger.info(f"WebSocket клиент отключен: {connection_id}")
    
    async def start_optimization_session(
        self, 
        connection_id: str,
        html: str,
        context: Optional[Dict[str, Any]] = None,
        target_keywords: Optional[List[str]] = None
    ) -> str:
        """
        Запуск сессии оптимизации для WebSocket клиента
        
        Args:
            connection_id: ID WebSocket соединения
            html: HTML для оптимизации
            context: Контекст контента
            target_keywords: Целевые ключевые слова
        
        Returns:
            session_id созданной сессии
        """
        
        if connection_id not in self.active_connections:
            raise ValueError(f"Соединение {connection_id} не найдено")
        
        session_id = str(uuid.uuid4())
        self.session_connections[session_id] = connection_id
        self.connection_stats["sessions_created"] += 1
        
        # Создаем callback для отправки прогресса
        async def progress_callback(progress_data: Dict[str, Any]):
            await self._send_to_connection(connection_id, {
                "type": "optimization_progress",
                "session_id": session_id,
                **progress_data
            })
        
        try:
            # Уведомляем о начале оптимизации
            await self._send_to_connection(connection_id, {
                "type": "optimization_started",
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            })
            
            # Запускаем оптимизацию в фоновом режиме
            asyncio.create_task(
                self._run_optimization_session(
                    session_id, connection_id, html, context, 
                    target_keywords, progress_callback
                )
            )
            
            return session_id
            
        except Exception as e:
            logger.error(f"Ошибка при запуске сессии оптимизации: {str(e)}")
            await self._send_to_connection(connection_id, {
                "type": "error",
                "session_id": session_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            raise
    
    async def _run_optimization_session(
        self,
        session_id: str,
        connection_id: str,
        html: str,
        context: Optional[Dict[str, Any]],
        target_keywords: Optional[List[str]],
        progress_callback: Callable
    ):
        """Выполнение сессии оптимизации в фоновом режиме"""
        
        try:
            # Запускаем real-time оптимизацию
            result = await realtime_integrator.start_realtime_optimization(
                session_id=session_id,
                initial_html=html,
                context=context,
                target_keywords=target_keywords,
                progress_callback=progress_callback
            )
            
            # Отправляем результат клиенту
            await self._send_to_connection(connection_id, {
                "type": "optimization_completed",
                "session_id": session_id,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })
            
            self.connection_stats["optimizations_completed"] += 1
            
        except Exception as e:
            logger.error(f"Ошибка в сессии оптимизации {session_id}: {str(e)}")
            await self._send_to_connection(connection_id, {
                "type": "optimization_error",
                "session_id": session_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
        finally:
            # Очищаем связь сессии с соединением
            if session_id in self.session_connections:
                del self.session_connections[session_id]
    
    async def _handle_connection_messages(self, connection_id: str):
        """Обработка входящих сообщений от WebSocket клиента"""
        
        websocket = self.active_connections[connection_id]
        
        try:
            while connection_id in self.active_connections:
                # Получаем сообщение от клиента
                data = await websocket.receive_text()
                message = json.loads(data)
                
                await self._process_client_message(connection_id, message)
                
        except WebSocketDisconnect:
            await self.disconnect(connection_id)
        except Exception as e:
            logger.error(f"Ошибка при обработке сообщений для {connection_id}: {str(e)}")
            await self.disconnect(connection_id)
    
    async def _process_client_message(self, connection_id: str, message: Dict[str, Any]):
        """Обработка сообщения от клиента"""
        
        message_type = message.get("type")
        
        if message_type == "start_optimization":
            # Запуск новой сессии оптимизации
            try:
                session_id = await self.start_optimization_session(
                    connection_id=connection_id,
                    html=message.get("html", ""),
                    context=message.get("context"),
                    target_keywords=message.get("target_keywords")
                )
                
                await self._send_to_connection(connection_id, {
                    "type": "session_created",
                    "session_id": session_id,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                await self._send_to_connection(connection_id, {
                    "type": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        elif message_type == "cancel_optimization":
            # Отмена активной сессии
            session_id = message.get("session_id")
            if session_id:
                cancelled = await realtime_integrator.cancel_session(session_id)
                
                await self._send_to_connection(connection_id, {
                    "type": "optimization_cancelled",
                    "session_id": session_id,
                    "cancelled": cancelled,
                    "timestamp": datetime.now().isoformat()
                })
        
        elif message_type == "get_session_status":
            # Запрос статуса сессии
            session_id = message.get("session_id")
            if session_id:
                status = await realtime_integrator.get_session_status(session_id)
                
                await self._send_to_connection(connection_id, {
                    "type": "session_status",
                    "session_id": session_id,
                    "status": status,
                    "timestamp": datetime.now().isoformat()
                })
        
        elif message_type == "get_system_stats":
            # Запрос статистики системы
            stats = realtime_integrator.get_system_stats()
            
            await self._send_to_connection(connection_id, {
                "type": "system_stats",
                "stats": stats,
                "connection_stats": self.connection_stats.copy(),
                "timestamp": datetime.now().isoformat()
            })
        
        elif message_type == "ping":
            # Ping-pong для поддержания соединения
            await self._send_to_connection(connection_id, {
                "type": "pong",
                "timestamp": datetime.now().isoformat()
            })
        
        else:
            logger.warning(f"Неизвестный тип сообщения: {message_type}")
            await self._send_to_connection(connection_id, {
                "type": "error",
                "error": f"Unknown message type: {message_type}",
                "timestamp": datetime.now().isoformat()
            })
    
    async def _send_to_connection(self, connection_id: str, message: Dict[str, Any]):
        """Отправка сообщения конкретному соединению"""
        
        if connection_id in self.active_connections:
            try:
                websocket = self.active_connections[connection_id]
                await websocket.send_text(json.dumps(message, ensure_ascii=False))
            except Exception as e:
                logger.error(f"Ошибка при отправке сообщения {connection_id}: {str(e)}")
                await self.disconnect(connection_id)
    
    async def broadcast_message(self, message: Dict[str, Any], exclude_connections: List[str] = None):
        """Отправка сообщения всем подключенным клиентам"""
        
        exclude_connections = exclude_connections or []
        
        for connection_id in list(self.active_connections.keys()):
            if connection_id not in exclude_connections:
                await self._send_to_connection(connection_id, message)
    
    # Event handlers для событий от realtime_integrator
    
    async def _on_analysis_complete(self, data: Dict[str, Any]):
        """Обработчик события завершения анализа"""
        
        # Находим соединения, заинтересованные в этом событии
        session_id = data.get("session_id")
        if session_id and session_id in self.session_connections:
            connection_id = self.session_connections[session_id]
            
            await self._send_to_connection(connection_id, {
                "type": "analysis_complete",
                "data": data,
                "timestamp": datetime.now().isoformat()
            })
    
    async def _on_optimization_applied(self, data: Dict[str, Any]):
        """Обработчик события применения оптимизации"""
        
        session_id = data.get("session_id")
        if session_id and session_id in self.session_connections:
            connection_id = self.session_connections[session_id]
            
            await self._send_to_connection(connection_id, {
                "type": "optimization_applied",
                "data": data,
                "timestamp": datetime.now().isoformat()
            })
    
    async def _on_ai_suggestion_generated(self, data: Dict[str, Any]):
        """Обработчик события генерации AI предложения"""
        
        session_id = data.get("session_id")
        if session_id and session_id in self.session_connections:
            connection_id = self.session_connections[session_id]
            
            await self._send_to_connection(connection_id, {
                "type": "ai_suggestion_generated",
                "data": data,
                "timestamp": datetime.now().isoformat()
            })
    
    async def _on_error_occurred(self, data: Dict[str, Any]):
        """Обработчик события ошибки"""
        
        session_id = data.get("session_id")
        if session_id and session_id in self.session_connections:
            connection_id = self.session_connections[session_id]
            
            await self._send_to_connection(connection_id, {
                "type": "error_occurred",
                "data": data,
                "timestamp": datetime.now().isoformat()
            })
    
    # Методы для управления и мониторинга
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Получение статистики соединений"""
        return {
            **self.connection_stats,
            "active_connections_list": list(self.active_connections.keys()),
            "active_sessions": list(self.session_connections.keys()),
            "server_uptime": datetime.now().isoformat()
        }
    
    async def close_all_connections(self):
        """Закрытие всех WebSocket соединений"""
        
        for connection_id in list(self.active_connections.keys()):
            try:
                websocket = self.active_connections[connection_id]
                await websocket.close()
            except Exception as e:
                logger.error(f"Ошибка при закрытии соединения {connection_id}: {str(e)}")
            finally:
                await self.disconnect(connection_id)
    
    async def send_system_notification(self, notification: str, notification_type: str = "info"):
        """Отправка системного уведомления всем клиентам"""
        
        message = {
            "type": "system_notification",
            "notification": notification,
            "notification_type": notification_type,
            "timestamp": datetime.now().isoformat()
        }
        
        await self.broadcast_message(message)


# Глобальный экземпляр WebSocket менеджера
websocket_manager = SEOWebSocketManager()


# Утилитарные функции для интеграции с FastAPI

async def websocket_endpoint(websocket: WebSocket, client_id: Optional[str] = None):
    """
    FastAPI endpoint для WebSocket соединений
    
    Использование:
    @app.websocket("/ws/seo-optimization")
    async def websocket_seo_optimization(websocket: WebSocket, client_id: str = None):
        await websocket_endpoint(websocket, client_id)
    """
    
    connection_id = await websocket_manager.connect(websocket, client_id)
    
    try:
        # Соединение будет обрабатываться менеджером
        while connection_id in websocket_manager.active_connections:
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        pass
    finally:
        await websocket_manager.disconnect(connection_id)


def get_websocket_manager() -> SEOWebSocketManager:
    """Получение экземпляра WebSocket менеджера"""
    return websocket_manager
