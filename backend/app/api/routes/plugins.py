from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.modules.plugins.manager import (
    AnalyticsPlugin,
    PluginManager,
    SEOPlugin,
    SocialMetaPlugin,
)

router = APIRouter()

# Initialize plugin manager with built-in plugins
plugin_manager = PluginManager()

# Load built-in plugins
plugin_manager.loaded_plugins["seo"] = SEOPlugin()
plugin_manager.loaded_plugins["analytics"] = AnalyticsPlugin()
plugin_manager.loaded_plugins["social"] = SocialMetaPlugin()

# Enable built-in plugins by default
plugin_manager.enabled_plugins = ["seo", "analytics", "social"]


class PluginProcessRequest(BaseModel):
    content: str
    plugins: Optional[List[str]] = None
    options: Optional[Dict[str, Any]] = None


class PluginProcessResponse(BaseModel):
    processed_content: str
    applied_plugins: List[str]
    original_content: str


class PluginInfoResponse(BaseModel):
    name: str
    version: str
    description: str
    enabled: bool


class PluginActionRequest(BaseModel):
    plugin_name: str


@router.post("/process", response_model=PluginProcessResponse)
async def process_content_with_plugins(request: PluginProcessRequest):
    """
    Process content through specified plugins
    """
    try:
        processed_content, applied_plugins = plugin_manager.process_content(
            content=request.content,
            plugin_names=request.plugins,
            options=request.options,
        )

        return PluginProcessResponse(
            processed_content=processed_content,
            applied_plugins=applied_plugins,
            original_content=request.content,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_plugins():
    """
    List all available plugins
    """
    return {
        "plugins": plugin_manager.list_plugins(),
        "enabled_plugins": plugin_manager.enabled_plugins,
    }


@router.get("/info/{plugin_name}", response_model=PluginInfoResponse)
async def get_plugin_info(plugin_name: str):
    """
    Get information about a specific plugin
    """
    plugin_info = plugin_manager.get_plugin_info(plugin_name)
    if not plugin_info:
        raise HTTPException(status_code=404, detail="Plugin not found")

    return PluginInfoResponse(**plugin_info)


@router.post("/enable")
async def enable_plugin(request: PluginActionRequest):
    """
    Enable a plugin
    """
    success = plugin_manager.enable_plugin(request.plugin_name)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to enable plugin")

    return {"message": f"Plugin {request.plugin_name} enabled successfully"}


@router.post("/disable")
async def disable_plugin(request: PluginActionRequest):
    """
    Disable a plugin
    """
    success = plugin_manager.disable_plugin(request.plugin_name)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to disable plugin")

    return {"message": f"Plugin {request.plugin_name} disabled successfully"}


@router.post("/load")
async def load_plugin(request: PluginActionRequest):
    """
    Load a plugin from the plugins directory
    """
    success = plugin_manager.load_plugin(request.plugin_name)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to load plugin")

    return {"message": f"Plugin {request.plugin_name} loaded successfully"}


@router.post("/unload")
async def unload_plugin(request: PluginActionRequest):
    """
    Unload a plugin
    """
    success = plugin_manager.unload_plugin(request.plugin_name)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to unload plugin")

    return {"message": f"Plugin {request.plugin_name} unloaded successfully"}


@router.get("/discover")
async def discover_plugins():
    """
    Discover available plugins in the plugins directory
    """
    discovered = plugin_manager.discover_plugins()
    return {"discovered_plugins": discovered}


@router.get("/built-in")
async def get_builtin_plugins():
    """
    Get information about built-in plugins
    """
    return {
        "built_in_plugins": [
            {
                "id": "seo",
                "name": "SEO Enhancer",
                "description": "Enhances HTML with SEO optimizations",
                "features": [
                    "Meta viewport",
                    "Charset declaration",
                    "Basic SEO structure",
                ],
            },
            {
                "id": "analytics",
                "name": "Analytics Injector",
                "description": "Injects analytics tracking code",
                "features": ["Google Analytics", "Custom tracking", "Event tracking"],
            },
            {
                "id": "social",
                "name": "Social Meta Tags",
                "description": "Adds Open Graph and Twitter Card meta tags",
                "features": [
                    "Open Graph tags",
                    "Twitter Cards",
                    "Social sharing optimization",
                ],
            },
        ]
    }


@router.get("/templates")
async def get_plugin_templates():
    """
    Get templates for creating custom plugins
    """
    return {
        "plugin_template": {
            "structure": {
                "plugin_directory/": {
                    "__init__.py": "Main plugin file",
                    "config.json": "Plugin configuration",
                    "README.md": "Plugin documentation",
                }
            },
            "example_code": """
from app.modules.plugins.manager import PluginInterface
from typing import Dict, Any

class Plugin(PluginInterface):
    def get_name(self) -> str:
        return "My Custom Plugin"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "Description of what this plugin does"
    
    def process(self, content: str, options: Dict[str, Any] = None) -> str:
        # Your plugin logic here
        return content
            """,
            "config_example": {
                "name": "plugin_name",
                "version": "1.0.0",
                "description": "Plugin description",
                "author": "Plugin author",
                "dependencies": [],
            },
        }
    }
