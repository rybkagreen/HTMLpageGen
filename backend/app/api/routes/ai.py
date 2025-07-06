from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.modules.ai_integration.service import AIService
from app.modules.structured_data.generator import StructuredDataGenerator

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


class StructuredDataRequest(BaseModel):
    content: str
    schema_type: str  # faq, product, breadcrumb, article, organization
    data: Optional[Dict[str, Any]] = None
    auto_extract: bool = True


class StructuredDataResponse(BaseModel):
    schema_data: Dict[str, Any]
    schema_type: str
    json_ld: str


class StructuredDataInjectionRequest(BaseModel):
    html: str
    schema_types: Optional[List[str]] = None
    auto_detect: bool = True
    schema_params: Optional[Dict[str, Dict[str, Any]]] = None


class StructuredDataInjectionResponse(BaseModel):
    html: str
    schemas_added: int
    schemas_list: List[str]


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


@router.post("/generate-structured-data", response_model=StructuredDataResponse)
async def generate_structured_data(
    request: StructuredDataRequest, ai_service: AIService = Depends()
) -> StructuredDataResponse:
    """
    Generate structured data for content
    """
    try:
        structured_data_generator = StructuredDataGenerator(ai_service)
        
        schema_data = await structured_data_generator.generate_structured_data(
            schema_type=request.schema_type,
            content=request.content,
            data=request.data,
            auto_extract=request.auto_extract
        )
        
        # Convert to JSON-LD string
        import json
        json_ld = json.dumps(schema_data, ensure_ascii=False, indent=2)
        
        return StructuredDataResponse(
            schema_data=schema_data,
            schema_type=request.schema_type,
            json_ld=json_ld
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/inject-structured-data", response_model=StructuredDataInjectionResponse)
async def inject_structured_data(
    request: StructuredDataInjectionRequest, ai_service: AIService = Depends()
) -> StructuredDataInjectionResponse:
    """
    Inject structured data into HTML
    """
    try:
        structured_data_generator = StructuredDataGenerator(ai_service)
        
        if request.auto_detect:
            # Auto-detect and generate suitable schemas
            enhanced_html = await structured_data_generator.auto_generate_for_content(
                html=request.html,
                content_type="auto",
                include_schemas=request.schema_types
            )
        else:
            # Generate specific schemas
            enhanced_html = request.html
            schemas_added = 0
            schemas_list = []
            
            if request.schema_types:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(request.html, 'html.parser')
                text_content = soup.get_text()
                
                for schema_type in request.schema_types:
                    schema_params = request.schema_params.get(schema_type, {}) if request.schema_params else {}
                    
                    schema = await structured_data_generator.generate_structured_data(
                        schema_type=schema_type,
                        content=text_content,
                        data=schema_params,
                        auto_extract=True
                    )
                    
                    if schema:
                        enhanced_html = structured_data_generator.inject_into_html(enhanced_html, schema)
                        schemas_added += 1
                        schemas_list.append(schema_type)
            
            # Count schemas in final HTML
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(enhanced_html, 'html.parser')
            ld_scripts = soup.find_all('script', {'type': 'application/ld+json'})
            schemas_added = len(ld_scripts)
        
        # Count total schemas
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(enhanced_html, 'html.parser')
        ld_scripts = soup.find_all('script', {'type': 'application/ld+json'})
        
        return StructuredDataInjectionResponse(
            html=enhanced_html,
            schemas_added=len(ld_scripts),
            schemas_list=request.schema_types or ["auto-detected"]
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
        "structured_data_types": [
            {
                "id": "faq",
                "name": "FAQ Page",
                "description": "Frequently Asked Questions schema",
            },
            {
                "id": "product",
                "name": "Product",
                "description": "Product information schema",
            },
            {
                "id": "breadcrumb",
                "name": "Breadcrumb",
                "description": "Navigation breadcrumb schema",
            },
            {
                "id": "article",
                "name": "Article",
                "description": "Article/blog post schema",
            },
            {
                "id": "organization",
                "name": "Organization",
                "description": "Organization/company schema",
            },
        ],
        "features": [
            "Content enhancement",
            "Meta tag generation",
            "HTML improvement suggestions",
            "SEO optimization",
            "Structured data generation",
            "Schema.org JSON-LD injection",
        ],
    }
