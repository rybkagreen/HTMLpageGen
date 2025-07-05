import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes import api_router
from app.core.config import settings
from app.core.logging import get_logger, setup_logging
from app.core.middleware import (
    ErrorHandlingMiddleware,
    RateLimitMiddleware,
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
)
from app.core.monitoring import health, metrics

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting HTML Page Generator API")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"AI Provider: {settings.AI_PROVIDER}")

    yield

    # Shutdown
    logger.info("Shutting down HTML Page Generator API")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-ready HTML Page Generation API with AI Integration",
    openapi_url=(
        f"{settings.API_V1_STR}/openapi.json" if settings.OPENAPI_DOCS_ENABLED else None
    ),
    docs_url="/docs" if settings.DOCS_ENABLED else None,
    redoc_url="/redoc" if settings.DOCS_ENABLED else None,
    lifespan=lifespan,
)

# Add middleware (order matters!)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)

if settings.RATE_LIMIT_ENABLED:
    app.add_middleware(
        RateLimitMiddleware, requests_per_minute=settings.RATE_LIMIT_REQUESTS
    )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_hosts_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
)


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.warning(
        "Validation error",
        extra={
            "request_id": getattr(request.state, "request_id", "unknown"),
            "errors": exc.errors(),
        },
    )
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "details": exc.errors(),
            "request_id": getattr(request.state, "request_id", "unknown"),
        },
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "request_id": getattr(request.state, "request_id", "unknown"),
        },
    )


# Health check endpoints
@app.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "healthy", "version": settings.VERSION}


@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with all dependencies"""
    return await health.get_health_status()


@app.get("/metrics")
async def get_metrics():
    """Get application metrics"""
    return metrics.get_metrics()


# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    # Static directory doesn't exist
    logger.warning("Static directory not found, skipping static file mounting")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API information"""
    docs_link = "/docs" if settings.DOCS_ENABLED else "#"

    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>{settings.PROJECT_NAME}</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .status {{ color: green; font-weight: bold; }}
                .info {{ background: #f5f5f5; padding: 20px; border-radius: 5px; }}
                a {{ color: #007bff; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{settings.PROJECT_NAME}</h1>
                <p class="status">✅ API is running</p>
                
                <div class="info">
                    <h3>API Information</h3>
                    <ul>
                        <li><strong>Version:</strong> {settings.VERSION}</li>
                        <li><strong>Environment:</strong> {settings.ENVIRONMENT}</li>
                        <li><strong>AI Provider:</strong> {settings.AI_PROVIDER}</li>
                    </ul>
                    
                    <h3>Available Endpoints</h3>
                    <ul>
                        <li><a href="{docs_link}">API Documentation</a></li>
                        <li><a href="/health">Health Check</a></li>
                        <li><a href="/health/detailed">Detailed Health</a></li>
                        <li><a href="/metrics">Metrics</a></li>
                    </ul>
                </div>
            </div>
        </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        workers=1 if settings.DEBUG else settings.MAX_WORKERS,
    )
