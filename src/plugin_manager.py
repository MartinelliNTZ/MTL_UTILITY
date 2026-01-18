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

        # Handle PyInstaller bundle
        if getattr(sys, '_MEIPASS', False):
            # Running in PyInstaller bundle
            base_path = Path(sys._MEIPASS)
            plugins_path = base_path / self.plugins_dir
        else:
            # Running in development
            base_path = Path.cwd()
            plugins_path = self.plugins_dir

        logger.info(self.TOOL_KEY, "PluginManager", f"Procurando plugins em: {plugins_path}")

        if not plugins_path.exists():
            logger.warning(self.TOOL_KEY, "PluginManager", f"Diretório de plugins não encontrado: {plugins_path}")
            return

        # Ensure base path is on sys.path so plugin modules can import src
        base_str = str(base_path)
        if base_str not in sys.path:
            sys.path.insert(0, base_str)
            logger.info(self.TOOL_KEY, "PluginManager", f"Adicionado ao sys.path: {base_str}")

        for file in plugins_path.glob("*.py"):
            if file.name.startswith("__"):
                continue
            try:
                logger.debug(self.TOOL_KEY, "PluginManager", f"Carregando plugin: {file.name}")
                spec = importlib.util.spec_from_file_location(file.stem, str(file))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, "get_plugin"):
                    plugin = mod.get_plugin()
                    if isinstance(plugin, BasePlugin):
                        self.plugins[plugin.name] = plugin
                        logger.info(self.TOOL_KEY, "PluginManager", f"Plugin carregado: {plugin.name}")
                else:
                    logger.warning(self.TOOL_KEY, "PluginManager", f"Plugin {file.name} não tem função get_plugin")
            except Exception as exc:
                logger.error(self.TOOL_KEY, "PluginManager", f"Erro carregando plugin {file.name}: {exc}")

        logger.info(self.TOOL_KEY, "PluginManager", f"Total de plugins carregados: {len(self.plugins)}")

    def get_plugin_names(self):
        return list(self.plugins.keys())

    def create_widget_for(self, name: str, parent=None):
        plugin = self.plugins.get(name)
        if not plugin:
            return None
        return plugin.create_widget(parent)
