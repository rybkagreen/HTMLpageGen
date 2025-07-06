import time
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class MetricsCollector:
    """Collect and store application metrics"""

    def __init__(self):
        self.request_count = defaultdict(int)
        self.response_times = deque(maxlen=1000)
        self.error_count = defaultdict(int)
        self.ai_request_count = defaultdict(int)
        self.ai_response_times = deque(maxlen=1000)
        self.start_time = datetime.now(timezone.utc)

    def record_request(
        self, method: str, path: str, status_code: int, response_time: float
    ):
        """Record a request metric"""
        self.request_count[f"{method}:{path}"] += 1
        self.response_times.append(response_time)

        if status_code >= 400:
            self.error_count[status_code] += 1

    def record_ai_request(
        self, provider: str, model: str, response_time: float, success: bool
    ):
        """Record AI request metrics"""
        key = f"{provider}:{model}"
        self.ai_request_count[key] += 1
        self.ai_response_times.append(response_time)

        if not success:
            self.error_count["ai_error"] += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        uptime = datetime.now(timezone.utc) - self.start_time

        # Calculate average response time
        avg_response_time = (
            sum(self.response_times) / len(self.response_times)
            if self.response_times
            else 0
        )

        # Calculate AI average response time
        avg_ai_response_time = (
            sum(self.ai_response_times) / len(self.ai_response_times)
            if self.ai_response_times
            else 0
        )

        return {
            "uptime_seconds": uptime.total_seconds(),
            "total_requests": sum(self.request_count.values()),
            "requests_by_endpoint": dict(self.request_count),
            "avg_response_time": round(avg_response_time, 4),
            "errors_by_status": dict(self.error_count),
            "ai_requests": dict(self.ai_request_count),
            "avg_ai_response_time": round(avg_ai_response_time, 4),
            "memory_usage_mb": self._get_memory_usage(),
        }

    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            import psutil

            process = psutil.Process()
            return round(process.memory_info().rss / 1024 / 1024, 2)
        except ImportError:
            return 0.0


# Global metrics collector instance
metrics = MetricsCollector()


class HealthChecker:
    """Application health checker"""

    def __init__(self):
        self.checks = {}

    async def check_database(self) -> Dict[str, Any]:
        """Check database connectivity"""
        import time
        from app.db.database import SessionLocal
        
        start_time = time.time()
        try:
            # Test database connection
            from sqlalchemy import text
            db = SessionLocal()
            db.execute(text("SELECT 1"))
            db.close()
            
            response_time = time.time() - start_time
            return {"status": "healthy", "response_time": round(response_time, 4)}
        except Exception as e:
            response_time = time.time() - start_time
            return {
                "status": "unhealthy", 
                "error": str(e),
                "response_time": round(response_time, 4)
            }

    async def check_redis(self) -> Dict[str, Any]:
        """Check Redis connectivity"""
        try:
            # Placeholder for Redis check
            # In real app, check actual Redis connection
            return {"status": "healthy", "response_time": 0.001}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def check_ai_providers(self) -> Dict[str, Any]:
        """Check AI providers status"""
        try:
            # Basic check - verify API keys are present
            providers = {}

            if settings.DEEPSEEK_API_KEY:
                providers["deepseek"] = {"status": "configured"}
            else:
                providers["deepseek"] = {"status": "not_configured"}

            if settings.OPENAI_API_KEY:
                providers["openai"] = {"status": "configured"}
            else:
                providers["openai"] = {"status": "not_configured"}

            return {"providers": providers}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status"""
        checks = {
            "database": await self.check_database(),
            "redis": await self.check_redis(),
            "ai_providers": await self.check_ai_providers(),
        }

        # Determine overall status
        overall_status = "healthy"
        for check_name, check_result in checks.items():
            if isinstance(check_result, dict):
                if check_result.get("status") == "unhealthy":
                    overall_status = "degraded"
                elif "error" in check_result:
                    overall_status = "unhealthy"

        return {
            "status": overall_status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "checks": checks,
            "metrics": metrics.get_metrics(),
        }


# Global health checker instance
health = HealthChecker()
