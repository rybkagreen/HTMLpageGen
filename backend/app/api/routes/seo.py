from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.modules.seo.service import SEOService
from app.modules.seo.integrator import SEOIntegrator

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
    open_graph: Dict[str, Any]
    twitter_cards: Dict[str, Any]
    performance: Dict[str, Any]
    issues: List[str]
    recommendations: List[str]


class StructuredDataRequest(BaseModel):
    content_type: str  # article, webpage, etc.
    data: Dict[str, Any]


class StructuredDataResponse(BaseModel):
    json_ld: str


class SEOIntegrationRequest(BaseModel):
    html: str
    target_keywords: Optional[List[str]] = None
    target_audience: str = "general"
    auto_apply: bool = True
    content_context: Optional[Dict[str, Any]] = None


class SEOIntegrationResponse(BaseModel):
    original_html: str
    optimized_html: str
    seo_score_improvement: int
    improvements_applied: Dict[str, Any]
    recommendations_for_manual_review: List[Dict[str, Any]]


class SEOReportRequest(BaseModel):
    html: str
    target_keywords: Optional[List[str]] = None


class SEOReportResponse(BaseModel):
    summary: Dict[str, Any]
    detailed_analysis: Dict[str, Any]
    recommendations_by_category: Dict[str, List[Dict[str, Any]]]
    actionable_items: List[str]


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
            open_graph=analysis["open_graph"],
            twitter_cards=analysis["twitter_cards"],
            performance=analysis["performance"],
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


@router.post("/integrate", response_model=SEOIntegrationResponse)
async def integrate_seo_recommendations(
    request: SEOIntegrationRequest,
    seo_integrator: SEOIntegrator = Depends()
):
    """
    Интеграция SEO рекомендаций в HTML с автоматическими исправлениями
    """
    try:
        result = seo_integrator.integrate_seo_recommendations(
            html=request.html,
            content_context=request.content_context,
            target_keywords=request.target_keywords,
            target_audience=request.target_audience,
            auto_apply=request.auto_apply
        )
        
        return SEOIntegrationResponse(
            original_html=result["original_html"],
            optimized_html=result["optimized_html"],
            seo_score_improvement=result["seo_score_improvement"],
            improvements_applied=result["improvements_applied"],
            recommendations_for_manual_review=result["recommendations_for_manual_review"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/report", response_model=SEOReportResponse)
async def generate_seo_report(
    request: SEOReportRequest,
    seo_integrator: SEOIntegrator = Depends()
):
    """
    Генерация подробного SEO отчета
    """
    try:
        report = seo_integrator.generate_seo_report(
            html=request.html,
            target_keywords=request.target_keywords
        )
        
        return SEOReportResponse(
            summary=report["summary"],
            detailed_analysis=report["detailed_analysis"],
            recommendations_by_category=report["recommendations_by_category"],
            actionable_items=report["actionable_items"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/keywords/analysis")
async def get_keyword_analysis_tips():
    """
    Советы по анализу ключевых слов
    """
    return {
        "keyword_research": {
            "primary_keywords": {
                "definition": "Основные ключевые слова, описывающие главную тему страницы",
                "recommendations": [
                    "Используйте 1-2 основных ключевых слова на страницу",
                    "Размещайте в title, H1, meta description",
                    "Плотность 1-2% от общего текста"
                ]
            },
            "secondary_keywords": {
                "definition": "Дополнительные ключевые слова и синонимы",
                "recommendations": [
                    "Используйте в заголовках H2-H6",
                    "Распределяйте естественно по тексту",
                    "Включайте связанные термины и синонимы"
                ]
            },
            "long_tail_keywords": {
                "definition": "Длинные фразы из 3+ слов",
                "benefits": [
                    "Меньше конкуренции",
                    "Более точное намерение пользователя",
                    "Выше конверсия"
                ]
            }
        },
        "keyword_placement": {
            "critical_locations": [
                "Title (начало)",
                "H1 заголовок",
                "Meta description",
                "Первый абзац",
                "Alt текст изображений"
            ],
            "supporting_locations": [
                "Подзаголовки H2-H6",
                "Якорный текст ссылок",
                "Имена файлов изображений",
                "URL страницы"
            ]
        },
        "keyword_density": {
            "optimal_range": "1-2%",
            "warning_threshold": "3%+",
            "calculation": "(количество_упоминаний / общее_количество_слов) * 100"
        }
    }


@router.get("/technical/checklist")
async def get_technical_seo_checklist():
    """
    Технический SEO чеклист
    """
    return {
        "html_structure": {
            "required_tags": [
                {
                    "tag": "<!DOCTYPE html>",
                    "description": "Объявление типа документа",
                    "critical": True
                },
                {
                    "tag": "<html lang='...'>",
                    "description": "Язык страницы",
                    "critical": True
                },
                {
                    "tag": "<title>",
                    "description": "Заголовок страницы (30-60 символов)",
                    "critical": True
                },
                {
                    "tag": "<meta name='description'>",
                    "description": "Описание страницы (120-160 символов)",
                    "critical": True
                },
                {
                    "tag": "<meta name='viewport'>",
                    "description": "Мобильная адаптация",
                    "critical": True
                }
            ]
        },
        "structured_data": {
            "formats": [
                {
                    "name": "JSON-LD",
                    "recommended": True,
                    "description": "Предпочтительный формат Google"
                },
                {
                    "name": "Microdata",
                    "recommended": False,
                    "description": "Встроенная разметка в HTML"
                }
            ],
            "common_schemas": [
                "Article", "WebPage", "Organization", 
                "Product", "Event", "BreadcrumbList"
            ]
        },
        "performance": {
            "image_optimization": [
                "Используйте современные форматы (WebP, AVIF)",
                "Добавляйте loading='lazy'",
                "Оптимизируйте размеры",
                "Всегда указывайте alt атрибуты"
            ],
            "loading_speed": [
                "Минифицируйте CSS и JavaScript",
                "Используйте сжатие gzip/brotli",
                "Оптимизируйте Critical Rendering Path",
                "Используйте CDN"
            ]
        },
        "mobile_seo": {
            "requirements": [
                "Responsive дизайн",
                "Viewport meta тег",
                "Touch-friendly элементы",
                "Быстрая загрузка на мобильных"
            ],
            "testing_tools": [
                "Google Mobile-Friendly Test",
                "PageSpeed Insights Mobile",
                "Chrome DevTools Device Mode"
            ]
        }
    }


@router.post("/analyze/open-graph")
async def analyze_open_graph(request: SEOAnalysisRequest, seo_service: SEOService = Depends()):
    """
    Специализированный анализ Open Graph метатегов
    """
    try:
        analysis = seo_service.og_analyzer.analyze_open_graph(request.html)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/twitter-cards")
async def analyze_twitter_cards(request: SEOAnalysisRequest, seo_service: SEOService = Depends()):
    """
    Специализированный анализ Twitter Cards метатегов
    """
    try:
        analysis = seo_service.twitter_analyzer.analyze_twitter_cards(request.html)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/performance")
async def analyze_performance(request: SEOAnalysisRequest, seo_service: SEOService = Depends()):
    """
    Специализированный анализ производительности
    """
    try:
        analysis = seo_service.performance_analyzer.analyze_performance(request.html)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class GenerateMetaTagsRequest(BaseModel):
    content_data: Dict[str, Any]
    include_og: bool = True
    include_twitter: bool = True


@router.post("/generate/meta-tags")
async def generate_meta_tags(request: GenerateMetaTagsRequest, seo_service: SEOService = Depends()):
    """
    Генерация оптимизированных метатегов
    """
    try:
        result = {"tags": []}
        
        # Генерация Open Graph тегов
        if request.include_og:
            og_tags = seo_service.og_analyzer.generate_og_tags(request.content_data)
            result["open_graph_tags"] = og_tags
            result["tags"].extend(og_tags)
        
        # Генерация Twitter Cards тегов
        if request.include_twitter:
            twitter_tags = seo_service.twitter_analyzer.generate_twitter_tags(request.content_data)
            result["twitter_cards_tags"] = twitter_tags
            result["tags"].extend(twitter_tags)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/performance/thresholds")
async def get_performance_thresholds():
    """
    Получение пороговых значений для анализа производительности
    """
    return {
        "html_size": {
            "good": "50KB",
            "warning": "100KB",
            "critical": "200KB",
            "description": "Рекомендуемые размеры HTML документа"
        },
        "css_size": {
            "good": "30KB per file",
            "warning": "75KB per file",
            "critical": "150KB per file",
            "description": "Рекомендуемые размеры CSS файлов"
        },
        "js_size": {
            "good": "50KB per file",
            "warning": "100KB per file",
            "critical": "200KB per file",
            "description": "Рекомендуемые размеры JavaScript файлов"
        },
        "image_size": {
            "good": "100KB per image",
            "warning": "500KB per image",
            "critical": "1MB per image",
            "description": "Рекомендуемые размеры изображений"
        },
        "total_requests": {
            "good": "30 requests",
            "warning": "50 requests",
            "critical": "100 requests",
            "description": "Рекомендуемое количество HTTP запросов"
        },
        "dom_elements": {
            "good": "1500 elements",
            "warning": "3000 elements",
            "critical": "5000 elements",
            "description": "Рекомендуемое количество DOM элементов"
        }
    }


@router.get("/social-media/best-practices")
async def get_social_media_best_practices():
    """
    Лучшие практики для социальных сетей
    """
    return {
        "open_graph": {
            "required_tags": [
                "og:title",
                "og:description",
                "og:type",
                "og:url",
                "og:image"
            ],
            "image_requirements": {
                "min_size": "1200x630 pixels",
                "max_size": "5MB",
                "formats": ["JPG", "PNG", "GIF", "WebP"],
                "aspect_ratio": "1.91:1 recommended"
            },
            "title_length": "30-60 characters",
            "description_length": "120-300 characters"
        },
        "twitter_cards": {
            "card_types": {
                "summary": "Standard card with image and text",
                "summary_large_image": "Card with large image",
                "app": "Card for mobile app promotion",
                "player": "Card for video/audio content"
            },
            "image_requirements": {
                "summary": "120x120 pixels minimum",
                "summary_large_image": "300x157 pixels minimum",
                "max_size": "5MB",
                "formats": ["JPG", "PNG", "GIF", "WebP"]
            },
            "title_length": "70 characters maximum",
            "description_length": "200 characters maximum"
        },
        "general_tips": [
            "Use high-quality, relevant images",
            "Keep titles concise and compelling",
            "Write descriptions that encourage clicks",
            "Test your cards using social media debuggers",
            "Update meta tags when content changes",
            "Use consistent branding across platforms"
        ]
    }


@router.get("/readability/guidelines")
async def get_readability_guidelines():
    """
    Рекомендации по читаемости контента
    """
    return {
        "flesch_reading_ease": {
            "score_ranges": {
                "90-100": "Очень легко (5-й класс)",
                "80-89": "Легко (6-й класс)",
                "70-79": "Довольно легко (7-й класс)",
                "60-69": "Стандартно (8-9 класс)",
                "50-59": "Довольно сложно (10-12 класс)",
                "30-49": "Сложно (университет)",
                "0-29": "Очень сложно (аспирантура)"
            },
            "target_scores": {
                "general_audience": "60-70",
                "technical_content": "50-60",
                "academic_content": "30-50"
            }
        },
        "sentence_structure": {
            "optimal_length": "15-20 слов",
            "maximum_recommended": "25 слов",
            "tips": [
                "Используйте активный залог",
                "Избегайте сложных конструкций",
                "Разбивайте длинные предложения",
                "Используйте переходные слова"
            ]
        },
        "paragraph_structure": {
            "optimal_length": "50-150 слов",
            "sentences_per_paragraph": "2-4 предложения",
            "tips": [
                "Одна идея на абзац",
                "Используйте подзаголовки",
                "Добавляйте списки и маркеры",
                "Выделяйте ключевые моменты"
            ]
        },
        "formatting_for_readability": {
            "headings": "Используйте H2-H6 для структуры",
            "lists": "Применяйте маркированные и нумерованные списки",
            "bold_italic": "Выделяйте важные термины",
            "white_space": "Обеспечьте достаточные отступы",
            "line_length": "45-75 символов на строку"
        }
    }
