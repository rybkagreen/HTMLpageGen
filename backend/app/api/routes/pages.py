from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from app.services.page_generator import PageGeneratorService
from app.modules.ai_integration.service import AIService

router = APIRouter()

class PageGenerationRequest(BaseModel):
    content: str
    template: Optional[str] = "default"
    seo_options: Optional[Dict[str, Any]] = None
    plugins: Optional[List[str]] = None
    ai_enhancements: Optional[bool] = True

class PageGenerationResponse(BaseModel):
    html: str
    meta: Dict[str, Any]
    plugins_applied: List[str]
    generation_time: float

@router.post("/generate", response_model=PageGenerationResponse)
async def generate_page(
    request: PageGenerationRequest,
    page_service: PageGeneratorService = Depends(),
    ai_service: AIService = Depends()
):
    """
    Generate HTML page from content with AI enhancements
    """
    try:
        result = await page_service.generate_page(
            content=request.content,
            template=request.template,
            seo_options=request.seo_options,
            plugins=request.plugins,
            ai_enhancements=request.ai_enhancements,
            ai_service=ai_service
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
            {"id": "default", "name": "Default Template", "description": "Basic HTML template"},
            {"id": "blog", "name": "Blog Template", "description": "Template for blog posts"},
            {"id": "landing", "name": "Landing Page", "description": "Marketing landing page"},
            {"id": "portfolio", "name": "Portfolio", "description": "Portfolio/showcase template"}
        ]
    }

@router.get("/preview/{page_id}")
async def preview_page(page_id: str):
    """
    Preview generated page
    """
    # TODO: Implement page preview functionality
    return {"message": f"Preview for page {page_id}"}

@router.delete("/pages/{page_id}")
async def delete_page(page_id: str):
    """
    Delete generated page
    """
    # TODO: Implement page deletion
    return {"message": f"Page {page_id} deleted"}
