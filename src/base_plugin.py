from PySide6.QtWidgets import QWidget


class BasePlugin:
    """Interface/base class para plugins.

    Plugins devem herdar desta classe e implementar `create_widget`.
    Suporta recepção de sinais da aplicação principal.
    """

    name = "BasePlugin"
    icon_name = "plugins"  # Nome do ícone SVG a usar

    def create_widget(self, parent=None) -> QWidget:
        """Retorna o widget principal do plugin (deve ser um QWidget)."""
        raise NotImplementedError()
    
    def on_base_path_changed(self, new_path: str) -> None:
        """Chamado quando o caminho base é alterado.
        
        Args:
            new_path: Novo caminho base
        """
        pass  # Implementar em subclasses se necessário
