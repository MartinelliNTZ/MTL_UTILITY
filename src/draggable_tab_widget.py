from PySide6.QtWidgets import QTabWidget
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag
from src.animations import AnimatedTabBar


class DraggableTabBar(AnimatedTabBar):
    """TabBar que permite reordenar abas via drag and drop."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self._dragging_index = -1
        self._drag_start_pos = None
    
    def mousePressEvent(self, event):
        """Inicia o drag ao clicar em uma aba."""
        if event.button() == Qt.LeftButton:
            self._dragging_index = self.tabAt(event.position().toPoint())
            self._drag_start_pos = event.position().toPoint()
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Inicia o drag ao mover o mouse e também lida com hover."""
        # Primeiro, lida com o drag
        if (event.buttons() == Qt.LeftButton and 
            self._dragging_index >= 0 and 
            self._drag_start_pos is not None):
            
            delta = (event.position().toPoint() - self._drag_start_pos).manhattanLength()
            if delta > 20:  # Threshold para iniciar drag
                drag = QDrag(self)
                mime_data = QMimeData()
                mime_data.setText(str(self._dragging_index))
                drag.setMimeData(mime_data)
                drag.exec(Qt.MoveAction)
                self._dragging_index = -1
                return  # Não continua para hover se está dragging
        
        # Se não está dragging, lida com hover
        super().mouseMoveEvent(event)
    
    def dragEnterEvent(self, event):
        """Aceita drag events."""
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        """Reordena as abas no drop."""
        if not event.mimeData().hasText():
            return
        
        try:
            source_index = int(event.mimeData().text())
        except ValueError:
            return
        
        target_index = self.tabAt(event.position().toPoint())
        
        if target_index < 0 or source_index == target_index:
            return
        
        # Movimenta a aba da posição source para a posição target
        if source_index < target_index:
            target_index -= 1
        
        # Pega a referência da aba (widget e texto)
        widget = self.parent().widget(source_index)
        icon = self.tabIcon(source_index)
        text = self.tabText(source_index)
        
        # Remove a aba original
        self.parent().removeTab(source_index)
        
        # Insere na nova posição
        self.parent().insertTab(target_index, widget, icon, text)
        
        # Define como a aba atual
        self.parent().setCurrentIndex(target_index)
        
        event.acceptProposedAction()


class DraggableTabWidget(QTabWidget):
    """TabWidget que permite reordenar abas via drag and drop."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Substitui a tab bar padrão pela customizada
        self.setTabBar(DraggableTabBar(self))
