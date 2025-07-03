from typing import Dict, Any, Optional, List
import time
import uuid
from jinja2 import Environment, FileSystemLoader, Template
from app.modules.ai_integration.service import AIService
from app.modules.seo.service import SEOService
from app.modules.plugins.manager import PluginManager
from app.core.config import settings


class PageGeneratorService:
    def __init__(self):
        self.templates_dir = "templates"
        self.jinja_env = Environment(loader=FileSystemLoader(self.templates_dir))
        self.seo_service = SEOService()
        
        # Initialize plugin manager with default plugins
        self.plugin_manager = PluginManager()
        self._load_default_plugins()
    
    def _load_default_plugins(self):
        """Load default plugins"""
        from app.modules.plugins.manager import SEOPlugin, AnalyticsPlugin, SocialMetaPlugin
        
        # Load built-in plugins
        self.plugin_manager.loaded_plugins["seo"] = SEOPlugin()
        self.plugin_manager.loaded_plugins["analytics"] = AnalyticsPlugin()
        self.plugin_manager.loaded_plugins["social"] = SocialMetaPlugin()
        
        # Enable plugins based on settings
        for plugin_name in settings.ENABLED_PLUGINS:
            if plugin_name in self.plugin_manager.loaded_plugins:
                self.plugin_manager.enable_plugin(plugin_name)
    
    async def generate_page(
        self,
        content: str,
        template: str = "default",
        seo_options: Optional[Dict[str, Any]] = None,
        plugins: Optional[List[str]] = None,
        ai_enhancements: bool = True,
        ai_service: Optional[AIService] = None
    ) -> Dict[str, Any]:
        """
        Generate HTML page from content
        """
        start_time = time.time()
        
        try:
            # Step 1: AI Enhancement (if enabled)
            enhanced_content = content
            if ai_enhancements and ai_service:
                enhanced_content = await ai_service.enhance_content(content, "general")
            
            # Step 2: Generate meta tags using AI (if available)
            meta_tags = {}
            if ai_service:
                meta_tags = await ai_service.generate_meta_tags(enhanced_content)
            
            # Step 3: Apply template
            html = self._apply_template(enhanced_content, template, meta_tags, seo_options)
            
            # Step 4: Apply plugins
            applied_plugins = []
            if plugins or self.plugin_manager.enabled_plugins:
                plugin_options = self._prepare_plugin_options(meta_tags, seo_options)
                html, applied_plugins = self.plugin_manager.process_content(
                    html, plugins, plugin_options
                )
            
            # Step 5: SEO Analysis
            seo_analysis = self.seo_service.analyze_html(html)
            
            generation_time = time.time() - start_time
            
            return {
                "html": html,
                "meta": {
                    "generation_time": generation_time,
                    "template_used": template,
                    "ai_enhanced": ai_enhancements,
                    "seo_score": seo_analysis["score"],
                    "word_count": seo_analysis["content"]["word_count"],
                    "meta_tags": meta_tags
                },
                "plugins_applied": applied_plugins,
                "generation_time": generation_time
            }
            
        except Exception as e:
            raise Exception(f"Page generation failed: {str(e)}")
    
    def _apply_template(
        self, 
        content: str, 
        template_name: str, 
        meta_tags: Dict[str, str],
        seo_options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Apply HTML template to content
        """
        if seo_options is None:
            seo_options = {}
        
        # Default template if file doesn't exist
        default_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <meta name="description" content="{{ description }}">
    {% if keywords %}
    <meta name="keywords" content="{{ keywords }}">
    {% endif %}
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }
        .header {
            background-color: #f4f4f4;
            padding: 1rem;
            margin-bottom: 2rem;
            border-radius: 5px;
        }
        .content {
            background-color: white;
            padding: 2rem;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }
        h2 {
            color: #555;
            margin-top: 2rem;
        }
        p {
            margin-bottom: 1rem;
        }
        .footer {
            text-align: center;
            margin-top: 2rem;
            padding: 1rem;
            background-color: #f8f9fa;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ title }}</h1>
    </div>
    
    <div class="content">
        {{ content | safe }}
    </div>
    
    <div class="footer">
        <p>Generated by HTML Page Generator</p>
    </div>
</body>
</html>"""
        
        try:
            # Try to load custom template
            template = self.jinja_env.get_template(f"{template_name}.html")
        except:
            # Use default template
            template = Template(default_template)
        
        # Prepare template variables
        template_vars = {
            "content": content,
            "title": meta_tags.get("title", seo_options.get("title", settings.DEFAULT_META_TITLE)),
            "description": meta_tags.get("description", seo_options.get("description", settings.DEFAULT_META_DESCRIPTION)),
            "keywords": meta_tags.get("keywords", seo_options.get("keywords", "")),
            "author": seo_options.get("author", ""),
            "canonical_url": seo_options.get("canonical_url", ""),
        }
        
        return template.render(**template_vars)
    
    def _prepare_plugin_options(self, meta_tags: Dict[str, str], seo_options: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Prepare options for plugins
        """
        if seo_options is None:
            seo_options = {}
        
        return {
            "title": meta_tags.get("title", seo_options.get("title", "")),
            "description": meta_tags.get("description", seo_options.get("description", "")),
            "image": seo_options.get("image", ""),
            "url": seo_options.get("url", ""),
            "tracking_id": seo_options.get("tracking_id", ""),
            "author": seo_options.get("author", ""),
        }
    
    def get_available_templates(self) -> List[Dict[str, str]]:
        """
        Get list of available templates
        """
        # This would scan the templates directory in a real implementation
        return [
            {"id": "default", "name": "Default Template", "description": "Basic HTML template"},
            {"id": "blog", "name": "Blog Template", "description": "Template for blog posts"},
            {"id": "landing", "name": "Landing Page", "description": "Marketing landing page"},
            {"id": "portfolio", "name": "Portfolio", "description": "Portfolio/showcase template"}
        ]
