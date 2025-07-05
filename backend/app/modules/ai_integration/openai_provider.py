import json
from typing import Dict, List

import openai

from app.core.config import settings
from app.modules.ai_integration.base import AIProvider


class OpenAIProvider(AIProvider):
    """Провайдер для OpenAI API"""

    def __init__(self) -> None:
        self.client = None
        if settings.OPENAI_API_KEY:
            self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    async def enhance_content(
        self, content: str, enhancement_type: str = "general"
    ) -> str:
        """Улучшить контент с помощью OpenAI"""
        if not self.client:
            return f"Enhanced content (mock): {content}"

        prompts = {
            "general": f"Improve the following content for better clarity and readability:\n\n{content}",
            "seo": f"Optimize the following content for SEO:\n\n{content}",
            "accessibility": f"Improve the following content for accessibility and readability:\n\n{content}",
            "marketing": f"Rewrite the following content with a marketing focus:\n\n{content}",
        }

        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful content enhancement assistant.",
                    },
                    {
                        "role": "user",
                        "content": prompts.get(enhancement_type, prompts["general"]),
                    },
                ],
                max_tokens=1000,
                temperature=0.7,
            )
            content = response.choices[0].message.content
            return content.strip() if content else ""
        except Exception as e:
            return f"Error enhancing content: {str(e)}"

    async def generate_meta_tags(self, content: str) -> Dict[str, str]:
        """Генерация мета-тегов с помощью OpenAI"""
        if not self.client:
            return {
                "title": "Generated Page Title",
                "description": "Generated page description",
                "keywords": "web, page, content",
            }

        prompt = f"""Generate SEO-optimized meta tags for the following content.
        Return the result as a JSON object with 'title', 'description', and 'keywords' fields:

        {content}"""

        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an SEO expert. Return only valid JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=300,
                temperature=0.3,
            )
            content_response = response.choices[0].message.content
            result = json.loads(content_response or "{}")
            return {
                "title": str(result.get("title", "Generated Title")),
                "description": str(result.get("description", "Generated description")),
                "keywords": str(result.get("keywords", "web, content")),
            }
        except Exception as e:
            return {
                "title": f"Error generating title: {str(e)}",
                "description": "Error generating description",
                "keywords": "error, generation",
            }

    async def suggest_improvements(self, html: str) -> List[str]:
        """Предложения по улучшению HTML с помощью OpenAI"""
        if not self.client:
            return [
                "Add semantic HTML5 elements",
                "Improve accessibility with ARIA labels",
                "Optimize for mobile devices",
            ]

        prompt = f"""Analyze the following HTML code and suggest improvements.
        Focus on SEO, accessibility, performance, and best practices.
        Return suggestions as a JSON array of strings:

        {html}"""

        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a web development expert. Return only a valid JSON array of strings.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                temperature=0.3,
            )
            suggestions_response = response.choices[0].message.content
            suggestions = json.loads(suggestions_response or "[]")
            return [str(s) for s in suggestions if isinstance(s, str)]
        except Exception as e:
            return [f"Error generating suggestions: {str(e)}"]

    async def generate_html_content(
        self, prompt: str, content_type: str = "webpage"
    ) -> str:
        """Генерация HTML контента с помощью OpenAI"""
        if not self.client:
            return f"""<!DOCTYPE html>
<html>
<head>
    <title>Generated Page</title>
</head>
<body>
    <h1>Mock Generated Content</h1>
    <p>This is mock content based on: {prompt}</p>
</body>
</html>"""

        content_prompts = {
            "webpage": f"Create a complete, modern HTML webpage based on: {prompt}",
            "landing": f"Create a landing page with HTML and inline CSS based on: {prompt}",
            "blog": f"Create a blog post HTML structure based on: {prompt}",
            "portfolio": f"Create a portfolio section HTML based on: {prompt}",
        }

        system_prompt = """You are a professional web developer. Create modern, semantic HTML5 code 
        with inline CSS for styling. Make it responsive and accessible. Return only the HTML code."""

        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": content_prompts.get(
                            content_type, content_prompts["webpage"]
                        ),
                    },
                ],
                max_tokens=2000,
                temperature=0.7,
            )
            content = response.choices[0].message.content
            return content.strip() if content else ""
        except Exception as e:
            return f"""<!DOCTYPE html>
<html>
<head>
    <title>Error</title>
</head>
<body>
    <h1>Error Generating Content</h1>
    <p>Error: {str(e)}</p>
</body>
</html>"""

    async def get_provider_info(self) -> Dict[str, str]:
        """Информация о провайдере"""
        return {
            "name": "OpenAI",
            "model": settings.OPENAI_MODEL,
            "status": "configured" if self.client else "not configured",
            "api_key_set": str(bool(settings.OPENAI_API_KEY)),
        }

    async def analyze_intention(self, message: str) -> Dict[str, str]:
        """Analyze user intention from message"""
        if not self.client:
            return {
                "type": "question",
                "confidence": "0.5",
                "details": "OpenAI not configured",
            }

        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """Analyze user intention and return JSON:
{
  "type": "code_generation|code_improvement|question|consultation",
  "confidence": "0.0-1.0", 
  "details": "brief description"
}""",
                    },
                    {"role": "user", "content": message},
                ],
                max_tokens=200,
                temperature=0.3,
            )

            content = response.choices[0].message.content
            try:
                return json.loads(content or "{}")
            except json.JSONDecodeError:
                return {
                    "type": "question",
                    "confidence": "0.5",
                    "details": "Parse error",
                }

        except Exception as e:
            print(f"OpenAI intention analysis failed: {e}")
            return {
                "type": "question",
                "confidence": "0.5",
                "details": "Analysis failed",
            }

    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """Generate chat completion response"""
        if not self.client:
            return "OpenAI API не настроен"

        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=1500,
                temperature=0.7,
            )
            content = response.choices[0].message.content
            return content.strip() if content else ""
        except Exception as e:
            print(f"OpenAI chat completion failed: {e}")
            return f"Извините, произошла ошибка: {e}"
