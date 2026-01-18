"""
ToolKey - Identificadores únicos para componentes do sistema.

Cada classe/componente deve ter um TOOL_KEY único para identificação em logs.
"""

class ToolKey:
    """Constantes de identificação para ferramentas e plugins."""

    # Sistema principal
    SYSTEM = "system"

    # Plugins
    CALCULATOR = "calculator"
    TODO_LIST = "todo_list"
    SIMPLE_BROWSER = "simple_browser"
    TEXT_VIEWER = "text_viewer"
    ICO_CONVERTER = "ico_converter"

    # Outros componentes
    MAIN_WINDOW = "main_window"
    PLUGIN_MANAGER = "plugin_manager"
    PREFERENCES = "preferences"
    SIGNAL_MANAGER = "signal_manager"
    ANIMATIONS = "animations"
    THEME = "theme"
    ICON_GENERATOR = "icon_generator"
    DRAGGABLE_TAB = "draggable_tab"
    DRAGGABLE_TOOLBAR = "draggable_toolbar"