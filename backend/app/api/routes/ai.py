from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

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


class HTMLGenerationRequest(BaseModel):
    prompt: str
    content_type: str = "webpage"  # webpage, landing, blog, portfolio


class HTMLGenerationResponse(BaseModel):
    html_content: str
    prompt: str
    content_type: str


class ProviderInfoResponse(BaseModel):
    provider: str
    configured: bool
    ai_provider_setting: str


@router.post("/enhance-content", response_model=ContentEnhancementResponse)
async def enhance_content(
    request: ContentEnhancementRequest, ai_service: AIService = Depends()
) -> ContentEnhancementResponse:
    """
    Enhance content using AI
    """
    try:
        enhanced = await ai_service.enhance_content(
            content=request.content, enhancement_type=request.enhancement_type
        )

        return ContentEnhancementResponse(
            enhanced_content=enhanced,
            original_content=request.content,
            enhancement_type=request.enhancement_type,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-meta-tags", response_model=MetaTagsResponse)
async def generate_meta_tags(
    request: MetaTagsRequest, ai_service: AIService = Depends()
) -> MetaTagsResponse:
    """
    Generate SEO meta tags from content
    """
    try:
        meta_tags = await ai_service.generate_meta_tags(request.content)

        return MetaTagsResponse(
            title=meta_tags.get("title", ""),
            description=meta_tags.get("description", ""),
            keywords=meta_tags.get("keywords", ""),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/suggest-improvements", response_model=ImprovementSuggestionResponse)
async def suggest_improvements(
    request: ImprovementSuggestionRequest, ai_service: AIService = Depends()
) -> ImprovementSuggestionResponse:
    """
    Get AI suggestions for HTML improvements
    """
    try:
        suggestions = await ai_service.suggest_improvements(request.html)

        return ImprovementSuggestionResponse(suggestions=suggestions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-html", response_model=HTMLGenerationResponse)
async def generate_html(
    request: HTMLGenerationRequest, ai_service: AIService = Depends()
) -> HTMLGenerationResponse:
    """
    Generate HTML content from prompt
    """
    try:
        html_content = await ai_service.generate_html_content(
            prompt=request.prompt, content_type=request.content_type
        )

        return HTMLGenerationResponse(
            html_content=html_content,
            prompt=request.prompt,
            content_type=request.content_type,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/provider-info", response_model=ProviderInfoResponse)
async def get_provider_info(
    ai_service: AIService = Depends(),
) -> ProviderInfoResponse:
    """
    Get information about the AI provider
    """
    try:
        # Проверяем, есть ли async метод get_provider_info у провайдера
        if hasattr(ai_service.provider, "get_provider_info"):
            provider_info = await ai_service.provider.get_provider_info()
        else:
            provider_info = ai_service.get_provider_info()

        return ProviderInfoResponse(
            provider=provider_info.get("provider", ""),
            configured=provider_info.get("configured", False),
            ai_provider_setting=provider_info.get("ai_provider_setting", ""),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/capabilities")
async def get_ai_capabilities() -> Dict[str, Any]:
    """
    Get available AI capabilities
    """
    return {
        "enhancement_types": [
            {
                "id": "general",
                "name": "General Enhancement",
                "description": "Improve content for web presentation",
            },
            {
                "id": "seo",
                "name": "SEO Optimization",
                "description": "Optimize content for search engines",
            },
            {
                "id": "accessibility",
                "name": "Accessibility",
                "description": "Improve content accessibility",
            },
            {
                "id": "marketing",
                "name": "Marketing Focus",
                "description": "Rewrite with marketing emphasis",
            },
        ],
        "features": [
            "Content enhancement",
            "Meta tag generation",
            "HTML improvement suggestions",
            "SEO optimization",
        ],
    }
