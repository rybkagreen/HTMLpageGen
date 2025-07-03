from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from app.modules.ai_integration.service import AIService

router = APIRouter()

class ContentEnhancementRequest(BaseModel):
    content: str
    enhancement_type: str = "general"  # general, seo, accessibility, marketing

class ContentEnhancementResponse(BaseModel):
    enhanced_content: str
    original_content: str
    enhancement_type: str

class MetaTagsRequest(BaseModel):
    content: str

class MetaTagsResponse(BaseModel):
    title: str
    description: str
    keywords: str

class ImprovementSuggestionRequest(BaseModel):
    html: str

class ImprovementSuggestionResponse(BaseModel):
    suggestions: List[str]

@router.post("/enhance-content", response_model=ContentEnhancementResponse)
async def enhance_content(
    request: ContentEnhancementRequest,
    ai_service: AIService = Depends()
):
    """
    Enhance content using AI
    """
    try:
        enhanced = await ai_service.enhance_content(
            content=request.content,
            enhancement_type=request.enhancement_type
        )
        
        return ContentEnhancementResponse(
            enhanced_content=enhanced,
            original_content=request.content,
            enhancement_type=request.enhancement_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-meta-tags", response_model=MetaTagsResponse)
async def generate_meta_tags(
    request: MetaTagsRequest,
    ai_service: AIService = Depends()
):
    """
    Generate SEO meta tags from content
    """
    try:
        meta_tags = await ai_service.generate_meta_tags(request.content)
        
        return MetaTagsResponse(
            title=meta_tags.get("title", ""),
            description=meta_tags.get("description", ""),
            keywords=meta_tags.get("keywords", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/suggest-improvements", response_model=ImprovementSuggestionResponse)
async def suggest_improvements(
    request: ImprovementSuggestionRequest,
    ai_service: AIService = Depends()
):
    """
    Get AI suggestions for HTML improvements
    """
    try:
        suggestions = await ai_service.suggest_improvements(request.html)
        
        return ImprovementSuggestionResponse(suggestions=suggestions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/capabilities")
async def get_ai_capabilities():
    """
    Get available AI capabilities
    """
    return {
        "enhancement_types": [
            {"id": "general", "name": "General Enhancement", "description": "Improve content for web presentation"},
            {"id": "seo", "name": "SEO Optimization", "description": "Optimize content for search engines"},
            {"id": "accessibility", "name": "Accessibility", "description": "Improve content accessibility"},
            {"id": "marketing", "name": "Marketing Focus", "description": "Rewrite with marketing emphasis"}
        ],
        "features": [
            "Content enhancement",
            "Meta tag generation",
            "HTML improvement suggestions",
            "SEO optimization"
        ]
    }
