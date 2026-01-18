import importlib.util
import sys
from pathlib import Path
from typing import Dict

from src.base_plugin import BasePlugin
from utils.ToolKey import ToolKey
from utils.LogUtils import logger


class PluginManager:
    TOOL_KEY = ToolKey.PLUGIN_MANAGER
    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = Path(plugins_dir)
        self.plugins: Dict[str, BasePlugin] = {}
        self.load_plugins()

    def load_plugins(self):
        self.plugins.clear()
        if not self.plugins_dir.exists():
            return
        # Ensure project root is on sys.path so plugin modules can import src
        project_root = str(Path.cwd())
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        for file in self.plugins_dir.glob("*.py"):
            if file.name.startswith("__"):
                continue
            try:
                spec = importlib.util.spec_from_file_location(file.stem, str(file))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, "get_plugin"):
                    plugin = mod.get_plugin()
                    if isinstance(plugin, BasePlugin):
                        self.plugins[plugin.name] = plugin
            except Exception as exc:
                print(f"Erro carregando plugin {file.name}: {exc}")

    def get_plugin_names(self):
        return list(self.plugins.keys())

    def create_widget_for(self, name: str, parent=None):
        plugin = self.plugins.get(name)
        if not plugin:
            return None
        return plugin.create_widget(parent)
