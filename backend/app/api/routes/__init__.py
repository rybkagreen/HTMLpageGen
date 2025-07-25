from fastapi import APIRouter

from app.api.routes import ai, pages, plugins, seo, seo_realtime

api_router = APIRouter()

# Include all route modules
api_router.include_router(pages.router, prefix="/pages", tags=["pages"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(seo.router, prefix="/seo", tags=["seo"])
api_router.include_router(seo_realtime.router, prefix="/seo-realtime", tags=["seo-realtime"])
api_router.include_router(plugins.router, prefix="/plugins", tags=["plugins"])
