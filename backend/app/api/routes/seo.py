from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.modules.seo.service import SEOService

router = APIRouter()


class SEOAnalysisRequest(BaseModel):
    html: str


class SEOAnalysisResponse(BaseModel):
    score: int
    title: Dict[str, Any]
    meta_description: Dict[str, Any]
    headings: Dict[str, Any]
    images: Dict[str, Any]
    links: Dict[str, Any]
    content: Dict[str, Any]
    issues: List[str]
    recommendations: List[str]


class StructuredDataRequest(BaseModel):
    content_type: str  # article, webpage, etc.
    data: Dict[str, Any]


class StructuredDataResponse(BaseModel):
    json_ld: str


@router.post("/analyze", response_model=SEOAnalysisResponse)
async def analyze_seo(request: SEOAnalysisRequest, seo_service: SEOService = Depends()):
    """
    Analyze HTML for SEO optimization opportunities
    """
    try:
        analysis = seo_service.analyze_html(request.html)

        return SEOAnalysisResponse(
            score=analysis["score"],
            title=analysis["title"],
            meta_description=analysis["meta_description"],
            headings=analysis["headings"],
            images=analysis["images"],
            links=analysis["links"],
            content=analysis["content"],
            issues=analysis["issues"],
            recommendations=analysis["recommendations"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/structured-data", response_model=StructuredDataResponse)
async def generate_structured_data(
    request: StructuredDataRequest, seo_service: SEOService = Depends()
):
    """
    Generate JSON-LD structured data
    """
    try:
        json_ld = seo_service.generate_structured_data(
            content_type=request.content_type, data=request.data
        )

        return StructuredDataResponse(json_ld=json_ld)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/meta-tags/best-practices")
async def get_meta_tags_best_practices():
    """
    Get SEO best practices for meta tags
    """
    return {
        "title": {
            "min_length": 30,
            "max_length": 60,
            "recommendations": [
                "Include primary keyword near the beginning",
                "Make it compelling and clickable",
                "Avoid keyword stuffing",
                "Each page should have unique title",
            ],
        },
        "meta_description": {
            "min_length": 120,
            "max_length": 160,
            "recommendations": [
                "Include primary and secondary keywords",
                "Write compelling copy that encourages clicks",
                "Include a call-to-action when appropriate",
                "Each page should have unique description",
            ],
        },
        "meta_keywords": {
            "status": "deprecated",
            "note": "Meta keywords tag is no longer used by search engines",
        },
    }


@router.get("/heading-structure/guidelines")
async def get_heading_guidelines():
    """
    Get guidelines for proper heading structure
    """
    return {
        "h1": {
            "count": "exactly_one",
            "purpose": "Main page topic",
            "recommendations": [
                "Use only one H1 per page",
                "Include primary keyword",
                "Make it descriptive of page content",
            ],
        },
        "h2_h6": {
            "purpose": "Content hierarchy",
            "recommendations": [
                "Use headings in logical order (H2 after H1, H3 after H2, etc.)",
                "Include relevant keywords naturally",
                "Make headings descriptive of the content that follows",
                "Don't skip heading levels",
            ],
        },
    }


@router.get("/content-optimization/tips")
async def get_content_optimization_tips():
    """
    Get content optimization tips for SEO
    """
    return {
        "word_count": {
            "minimum": 300,
            "recommended": 1000,
            "note": "Longer content tends to rank better, but quality is more important than quantity",
        },
        "keyword_optimization": [
            "Use primary keyword in title, meta description, and H1",
            "Include secondary keywords in subheadings",
            "Maintain 1-2% keyword density",
            "Use semantic keywords and synonyms",
            "Focus on user intent, not just keywords",
        ],
        "readability": [
            "Use short paragraphs (2-3 sentences)",
            "Include bullet points and numbered lists",
            "Use transition words",
            "Write for your target audience",
            "Include relevant images and media",
        ],
        "technical": [
            "Use descriptive alt text for images",
            "Include internal links to related content",
            "Use external links to authoritative sources",
            "Optimize page loading speed",
            "Ensure mobile responsiveness",
        ],
    }
