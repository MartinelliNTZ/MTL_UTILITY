from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt
from typing import Callable, Dict
from src.animations import AnimatedToolButton, UIAnimations
from utils.ToolKey import ToolKey
from utils.LogUtils import logger


class DraggableToolBar(QToolBar):
    """Toolbar que permite reordenar ações via drag and drop."""
    TOOL_KEY = ToolKey.DRAGGABLE_TOOLBAR
    """Toolbar que permite reordenar ações via drag and drop."""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(title, parent)
        self.setMovable(False)
        self._dragging_action = None
        self._action_callbacks: Dict[str, Callable] = {}
    
    def addPluginAction(self, icon: QIcon, plugin_name: str, callback: Callable):
        """Adiciona uma ação de plugin com suporte a drag and drop."""
        action = QAction(icon, plugin_name, self)
        action.triggered.connect(callback)
        self.addAction(action)
        self._action_callbacks[plugin_name] = callback
        return action
    
    def mouseReleaseEvent(self, event):
        """Permite reordenação ao arrastar ações."""
        super().mouseReleaseEvent(event)
    
    def dragEnterEvent(self, event):
        """Aceita drag events."""
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        """Reordena ações no drop."""
        mime_data = event.mimeData()
        if mime_data.hasText():
            text = mime_data.text()
            drop_pos = event.position().toPoint()
            
            # Encontra a ação sobre a qual foi feito o drop
            action_at_pos = self.actionAt(drop_pos)
            
            if action_at_pos:
                actions = self.actions()
                try:
                    dragged_idx = int(text)
                    drop_idx = actions.index(action_at_pos)
                    
                    if dragged_idx != drop_idx:
                        # Remove e reinsere a ação na nova posição
                        dragged_action = actions[dragged_idx]
                        self.removeAction(dragged_action)
                        
                        if dragged_idx < drop_idx:
                            self.insertAction(action_at_pos, dragged_action)
                        else:
                            self.insertAction(action_at_pos, dragged_action)
                except (ValueError, IndexError):
                    pass
            
            event.acceptProposedAction()
