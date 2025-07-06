from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.modules.ai_integration.service import AIService
from app.services.page_generator import PageGeneratorService

router = APIRouter()


class PageGenerationRequest(BaseModel):
    content: str
    template: Optional[str] = "default"
    seo_options: Optional[Dict[str, Any]] = None
    plugins: Optional[List[str]] = None
    ai_enhancements: Optional[bool] = True
    structured_data: Optional[bool] = True
    structured_data_types: Optional[List[str]] = None
    structured_data_params: Optional[Dict[str, Any]] = None


class PageGenerationResponse(BaseModel):
    html: str
    meta: Dict[str, Any]
    plugins_applied: List[str]
    generation_time: float


@router.post("/generate", response_model=PageGenerationResponse)
async def generate_page(
    request: PageGenerationRequest,
    page_service: PageGeneratorService = Depends(),
    ai_service: AIService = Depends(),
):
    """
    Generate HTML page from content with AI enhancements
    """
    try:
        result = await page_service.generate_page(
            content=request.content,
            template=request.template or "default",
            seo_options=request.seo_options,
            plugins=request.plugins,
            ai_enhancements=(
                request.ai_enhancements if request.ai_enhancements is not None else True
            ),
            ai_service=ai_service,
            structured_data=(
                request.structured_data if request.structured_data is not None else True
            ),
            structured_data_types=request.structured_data_types,
            structured_data_params=request.structured_data_params,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates")
async def get_templates():
    """
    Get available page templates
    """
    return {
        "templates": [
            {
                "id": "default",
                "name": "Default Template",
                "description": "Basic HTML template",
            },
            {
                "id": "blog",
                "name": "Blog Template",
                "description": "Template for blog posts",
            },
            {
                "id": "landing",
                "name": "Landing Page",
                "description": "Marketing landing page",
            },
            {
                "id": "portfolio",
                "name": "Portfolio",
                "description": "Portfolio/showcase template",
            },
        ]
    }


@router.get("/preview/{page_id}")
async def preview_page(page_id: str):
    """
    Preview generated page
    """
    try:
        # В реальной реализации здесь бы был поиск в базе данных
        # Пока возвращаем тестовый HTML
        preview_html = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" 
                  content="width=device-width, initial-scale=1.0">
            <title>Предварительный просмотр страницы {page_id}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .preview-container {{ max-width: 800px; margin: 0 auto; }}
                .header {{ text-align: center; color: #333; }}
            </style>
        </head>
        <body>
            <div class="preview-container">
                <h1 class="header">Предварительный просмотр</h1>
                <p>ID страницы: {page_id}</p>
                <p>Здесь будет отображаться сгенерированный контент.</p>
            </div>
        </body>
        </html>
        """
        return {"html": preview_html, "page_id": page_id, "status": "success"}
    except Exception:
        raise HTTPException(status_code=404, detail=f"Page {page_id} not found")


@router.delete("/pages/{page_id}")
async def delete_page(page_id: str):
    """
    Delete generated page
    """
    try:
        # В реальной реализации здесь бы было удаление из базы данных
        # Пока просто возвращаем успешный результат
        return {
            "message": f"Page {page_id} successfully deleted",
            "page_id": page_id,
            "status": "success",
        }
    except Exception:
        raise HTTPException(
            status_code=404, detail=f"Page {page_id} not found or cannot be deleted"
        )
