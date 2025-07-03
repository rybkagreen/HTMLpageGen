from typing import Dict, Any, List, Optional, Callable
import importlib
import os
from abc import ABC, abstractmethod


class PluginInterface(ABC):
    """
    Base interface for all plugins
    """
    
    @abstractmethod
    def get_name(self) -> str:
        """Return plugin name"""
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """Return plugin version"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Return plugin description"""
        pass
    
    @abstractmethod
    def process(self, content: str, options: Dict[str, Any] = None) -> str:
        """Process content and return modified version"""
        pass
    
    def initialize(self, config: Dict[str, Any] = None) -> None:
        """Initialize plugin with configuration"""
        pass
    
    def cleanup(self) -> None:
        """Cleanup plugin resources"""
        pass


class PluginManager:
    def __init__(self, plugins_dir: str = "./plugins"):
        self.plugins_dir = plugins_dir
        self.loaded_plugins: Dict[str, PluginInterface] = {}
        self.enabled_plugins: List[str] = []
    
    def load_plugin(self, plugin_name: str) -> bool:
        """
        Load a plugin by name
        """
        try:
            plugin_path = os.path.join(self.plugins_dir, plugin_name)
            if not os.path.exists(plugin_path):
                print(f"Plugin directory not found: {plugin_path}")
                return False
            
            # Import plugin module
            spec = importlib.util.spec_from_file_location(
                plugin_name, 
                os.path.join(plugin_path, "__init__.py")
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get plugin class
            plugin_class = getattr(module, 'Plugin', None)
            if not plugin_class:
                print(f"Plugin class not found in {plugin_name}")
                return False
            
            # Instantiate plugin
            plugin_instance = plugin_class()
            if not isinstance(plugin_instance, PluginInterface):
                print(f"Plugin {plugin_name} does not implement PluginInterface")
                return False
            
            self.loaded_plugins[plugin_name] = plugin_instance
            print(f"Plugin {plugin_name} loaded successfully")
            return True
            
        except Exception as e:
            print(f"Failed to load plugin {plugin_name}: {e}")
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """
        Unload a plugin
        """
        if plugin_name in self.loaded_plugins:
            try:
                self.loaded_plugins[plugin_name].cleanup()
                del self.loaded_plugins[plugin_name]
                if plugin_name in self.enabled_plugins:
                    self.enabled_plugins.remove(plugin_name)
                return True
            except Exception as e:
                print(f"Failed to unload plugin {plugin_name}: {e}")
                return False
        return False
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """
        Enable a loaded plugin
        """
        if plugin_name in self.loaded_plugins and plugin_name not in self.enabled_plugins:
            self.enabled_plugins.append(plugin_name)
            return True
        return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """
        Disable a plugin
        """
        if plugin_name in self.enabled_plugins:
            self.enabled_plugins.remove(plugin_name)
            return True
        return False
    
    def process_content(self, content: str, plugin_names: List[str] = None, options: Dict[str, Any] = None) -> tuple[str, List[str]]:
        """
        Process content through specified plugins or all enabled plugins
        """
        if plugin_names is None:
            plugin_names = self.enabled_plugins
        
        processed_content = content
        applied_plugins = []
        
        for plugin_name in plugin_names:
            if plugin_name in self.loaded_plugins and plugin_name in self.enabled_plugins:
                try:
                    plugin = self.loaded_plugins[plugin_name]
                    processed_content = plugin.process(processed_content, options)
                    applied_plugins.append(plugin_name)
                except Exception as e:
                    print(f"Plugin {plugin_name} failed to process content: {e}")
        
        return processed_content, applied_plugins
    
    def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, str]]:
        """
        Get information about a plugin
        """
        if plugin_name in self.loaded_plugins:
            plugin = self.loaded_plugins[plugin_name]
            return {
                "name": plugin.get_name(),
                "version": plugin.get_version(),
                "description": plugin.get_description(),
                "enabled": plugin_name in self.enabled_plugins
            }
        return None
    
    def list_plugins(self) -> Dict[str, Dict[str, Any]]:
        """
        List all loaded plugins with their information
        """
        plugins_info = {}
        for plugin_name in self.loaded_plugins:
            plugins_info[plugin_name] = self.get_plugin_info(plugin_name)
        return plugins_info
    
    def discover_plugins(self) -> List[str]:
        """
        Discover available plugins in the plugins directory
        """
        discovered = []
        if not os.path.exists(self.plugins_dir):
            return discovered
        
        for item in os.listdir(self.plugins_dir):
            plugin_path = os.path.join(self.plugins_dir, item)
            if os.path.isdir(plugin_path) and os.path.exists(os.path.join(plugin_path, "__init__.py")):
                discovered.append(item)
        
        return discovered


# Built-in plugins
class SEOPlugin(PluginInterface):
    """
    Built-in SEO enhancement plugin
    """
    
    def get_name(self) -> str:
        return "SEO Enhancer"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "Enhances HTML with SEO optimizations"
    
    def process(self, content: str, options: Dict[str, Any] = None) -> str:
        """
        Add SEO enhancements to HTML content
        """
        if not options:
            options = {}
        
        # Add meta viewport if not present
        if 'viewport' not in content:
            viewport_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            if '<head>' in content:
                content = content.replace('<head>', f'<head>\n    {viewport_meta}')
        
        # Add charset if not present
        if 'charset' not in content:
            charset_meta = '<meta charset="UTF-8">'
            if '<head>' in content:
                content = content.replace('<head>', f'<head>\n    {charset_meta}')
        
        return content


class AnalyticsPlugin(PluginInterface):
    """
    Built-in analytics plugin
    """
    
    def get_name(self) -> str:
        return "Analytics Injector"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "Injects analytics tracking code"
    
    def process(self, content: str, options: Dict[str, Any] = None) -> str:
        """
        Add analytics tracking code
        """
        if not options or 'tracking_id' not in options:
            return content
        
        tracking_id = options['tracking_id']
        
        analytics_script = f"""
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={tracking_id}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());
          gtag('config', '{tracking_id}');
        </script>
        """
        
        if '</head>' in content:
            content = content.replace('</head>', f'{analytics_script}\n</head>')
        
        return content


class SocialMetaPlugin(PluginInterface):
    """
    Built-in social media meta tags plugin
    """
    
    def get_name(self) -> str:
        return "Social Meta Tags"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "Adds Open Graph and Twitter Card meta tags"
    
    def process(self, content: str, options: Dict[str, Any] = None) -> str:
        """
        Add social media meta tags
        """
        if not options:
            options = {}
        
        title = options.get('title', 'Default Title')
        description = options.get('description', 'Default Description')
        image = options.get('image', '')
        url = options.get('url', '')
        
        social_meta = f"""
        <!-- Open Graph / Facebook -->
        <meta property="og:type" content="website">
        <meta property="og:url" content="{url}">
        <meta property="og:title" content="{title}">
        <meta property="og:description" content="{description}">
        <meta property="og:image" content="{image}">

        <!-- Twitter -->
        <meta property="twitter:card" content="summary_large_image">
        <meta property="twitter:url" content="{url}">
        <meta property="twitter:title" content="{title}">
        <meta property="twitter:description" content="{description}">
        <meta property="twitter:image" content="{image}">
        """
        
        if '</head>' in content:
            content = content.replace('</head>', f'{social_meta}\n</head>')
        
        return content
