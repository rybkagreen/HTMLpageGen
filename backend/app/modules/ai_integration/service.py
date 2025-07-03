from typing import Dict, Any, Optional, List
import openai
from app.core.config import settings


class AIService:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        
    async def enhance_content(self, content: str, enhancement_type: str = "general") -> str:
        """
        Enhance content using AI
        """
        if not settings.OPENAI_API_KEY:
            return content
            
        prompts = {
            "general": f"Improve and enhance the following content for web presentation:\n\n{content}",
            "seo": f"Optimize the following content for SEO while maintaining readability:\n\n{content}",
            "accessibility": f"Improve the following content for accessibility and readability:\n\n{content}",
            "marketing": f"Rewrite the following content with a marketing focus:\n\n{content}"
        }
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful content enhancement assistant."},
                    {"role": "user", "content": prompts.get(enhancement_type, prompts["general"])}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"AI enhancement failed: {e}")
            return content
    
    async def generate_meta_tags(self, content: str) -> Dict[str, str]:
        """
        Generate SEO meta tags from content
        """
        if not settings.OPENAI_API_KEY:
            return {
                "title": settings.DEFAULT_META_TITLE,
                "description": settings.DEFAULT_META_DESCRIPTION
            }
            
        prompt = f"""
        Based on the following content, generate SEO-optimized meta tags:
        
        Content:
        {content}
        
        Please provide:
        1. A compelling title (max 60 characters)
        2. A meta description (max 160 characters)
        3. Relevant keywords (comma-separated)
        
        Format your response as JSON with keys: title, description, keywords
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an SEO specialist. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.5
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            print(f"Meta tag generation failed: {e}")
            return {
                "title": settings.DEFAULT_META_TITLE,
                "description": settings.DEFAULT_META_DESCRIPTION,
                "keywords": ""
            }
    
    async def suggest_improvements(self, html: str) -> List[str]:
        """
        Suggest improvements for generated HTML
        """
        if not settings.OPENAI_API_KEY:
            return []
            
        prompt = f"""
        Analyze the following HTML and suggest improvements for:
        1. SEO optimization
        2. Accessibility
        3. Performance
        4. User experience
        
        HTML:
        {html}
        
        Provide suggestions as a bullet-pointed list.
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a web development expert providing improvement suggestions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.6
            )
            
            suggestions = response.choices[0].message.content.strip().split('\n')
            return [s.strip('- ').strip() for s in suggestions if s.strip()]
        except Exception as e:
            print(f"Suggestion generation failed: {e}")
            return []
