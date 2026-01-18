"""
Plugin UI Helper - Módulo reutilizável para componentes comuns em plugins.

Fornece métodos para criar componentes padronizados seguindo o design system
da aplicação, reduzindo duplicação de código entre plugins.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTextEdit, QListWidget
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from typing import Optional, Callable, Tuple
from src.animations import AnimatedButton
from utils.ToolKey import ToolKey
from utils.LogUtils import logger


class PluginStyleSheet:
    """Constantes de estilo reutilizáveis."""
    TOOL_KEY = ToolKey.SYSTEM  # Como é uma classe utilitária
    """Constantes de estilo reutilizáveis."""
    
    # Colors
    COLOR_PRIMARY = "#0e639c"
    COLOR_SUCCESS = "#4ec9b0"
    COLOR_WARNING = "#f48771"
    COLOR_ORANGE = "#f48771"
    COLOR_DANGER = "#ce9178"
    COLOR_TEXT = "#e0e0e0"
    COLOR_TEXT_MUTED = "#858585"
    COLOR_BG = "#252526"
    COLOR_BORDER = "#3e3e3e"
    
    # Input fields
    INPUT_FIELD = """
        QLineEdit {{
            background-color: {bg};
            color: {text};
            border: 1px solid {border};
            border-radius: 4px;
            padding: 6px;
            font-size: 11pt;
        }}
        QLineEdit:focus {{
            border: 1px solid {focus};
        }}
    """
    
    TEXT_EDIT = """
        QTextEdit {{
            background-color: {bg};
            color: {text};
            border: 1px solid {border};
            border-radius: 4px;
            padding: 12px;
            font-size: 10pt;
            font-family: 'Consolas', 'Monaco', monospace;
        }}
        QTextEdit:focus {{
            border: 1px solid {focus};
        }}
    """
    
    # Buttons
    BUTTON_PRIMARY = """
        QPushButton {{
            background-color: {color};
            color: white;
            border: none;
            border-radius: 4px;
            font-weight: bold;
            padding: {padding};
        }}
        QPushButton:hover {{
            background-color: {hover};
        }}
        QPushButton:pressed {{
            background-color: {pressed};
        }}
    """
    
    # Labels
    PATH_LABEL = """
        QLabel {{
            background-color: {bg};
            color: {text};
            border: 1px solid {border};
            padding: 6px;
            border-radius: 3px;
        }}
    """
    
    LIST_WIDGET = """
        QListWidget {{
            background-color: {bg};
            color: {text};
            border: 1px solid {border};
            border-radius: 4px;
        }}
        QListWidget::item {{
            padding: 10px;
            border-radius: 3px;
            margin: 2px;
        }}
        QListWidget::item:hover {{
            background-color: {border};
        }}
        QListWidget::item:selected {{
            background-color: {focus};
        }}
    """


class PluginUIHelper:
    """Helper para criação de componentes UI padronizados em plugins."""
    
    @staticmethod
    def create_title(text: str, color: str = PluginStyleSheet.COLOR_PRIMARY) -> QLabel:
        """
        Cria um título padronizado.
        
        Args:
            text: Texto do título
            color: Cor em hex (padrão: cor primária)
            
        Returns:
            QLabel estilizado como título
        """
        title = QLabel(text)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        title.setStyleSheet(f"color: {color};")
        return title
    
    @staticmethod
    def create_base_path_widget() -> Tuple[QWidget, QLabel]:
        """
        Cria widget padronizado para exibir pasta base.
        
        Returns:
            Tupla (container_widget, label_para_atualizar)
        """
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label_title = QLabel("Pasta Base:")
        label_title.setStyleSheet("color: #858585; font-size: 9pt;")
        
        base_path_label = QLabel("C:/")
        base_path_label.setStyleSheet(PluginStyleSheet.PATH_LABEL.format(
            bg=PluginStyleSheet.COLOR_BG,
            text="#9cdcfe",
            border=PluginStyleSheet.COLOR_BORDER
        ))
        
        layout.addWidget(label_title)
        layout.addWidget(base_path_label)
        
        return container, base_path_label
    
    @staticmethod
    def create_input_field(
        placeholder: str = "",
        focus_color: str = PluginStyleSheet.COLOR_PRIMARY
    ) -> QLineEdit:
        """
        Cria um campo de entrada padronizado.
        
        Args:
            placeholder: Texto de placeholder
            focus_color: Cor quando em foco
            
        Returns:
            QLineEdit estilizado
        """
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setMinimumHeight(36)
        field.setStyleSheet(PluginStyleSheet.INPUT_FIELD.format(
            bg=PluginStyleSheet.COLOR_BG,
            text=PluginStyleSheet.COLOR_TEXT,
            border=PluginStyleSheet.COLOR_BORDER,
            focus=focus_color
        ))
        return field
    
    @staticmethod
    def create_button(
        text: str,
        color: str = PluginStyleSheet.COLOR_PRIMARY,
        hover_color: Optional[str] = None,
        pressed_color: Optional[str] = None,
        width: Optional[int] = None,
        height: int = 36
    ) -> QPushButton:
        """
        Cria um botão padronizado.
        
        Args:
            text: Texto do botão
            color: Cor de fundo
            hover_color: Cor ao passar mouse (padrão: mais claro)
            pressed_color: Cor quando pressionado (padrão: mais escuro)
            width: Largura mínima (opcional)
            height: Altura mínima
            
        Returns:
            QPushButton estilizado
        """
        btn = AnimatedButton(text)
        btn.setMinimumHeight(height)
        
        if width:
            btn.setMinimumWidth(width)
        
        # Calcula cores derivadas se não especificadas
        if hover_color is None:
            hover_color = PluginUIHelper._lighten_color(color, 10)
        if pressed_color is None:
            pressed_color = PluginUIHelper._darken_color(color, 20)
        
        btn.setStyleSheet(PluginStyleSheet.BUTTON_PRIMARY.format(
            color=color,
            hover=hover_color,
            pressed=pressed_color,
            padding="8px 16px"
        ))
        
        return btn
    
    @staticmethod
    def create_text_editor(
        placeholder_text: str = "",
        read_only: bool = False,
        focus_color: str = PluginStyleSheet.COLOR_PRIMARY
    ) -> QTextEdit:
        """
        Cria um editor de texto padronizado.
        
        Args:
            placeholder_text: Texto inicial
            read_only: Se é somente leitura
            focus_color: Cor quando em foco
            
        Returns:
            QTextEdit estilizado
        """
        editor = QTextEdit()
        editor.setPlainText(placeholder_text)
        editor.setReadOnly(read_only)
        editor.setStyleSheet(PluginStyleSheet.TEXT_EDIT.format(
            bg=PluginStyleSheet.COLOR_BG,
            text=PluginStyleSheet.COLOR_TEXT,
            border=PluginStyleSheet.COLOR_BORDER,
            focus=focus_color
        ))
        return editor
    
    @staticmethod
    def create_list_widget(focus_color: str = PluginStyleSheet.COLOR_PRIMARY) -> QListWidget:
        """
        Cria uma lista padronizada.
        
        Args:
            focus_color: Cor quando selecionado
            
        Returns:
            QListWidget estilizado
        """
        lst = QListWidget()
        lst.setStyleSheet(PluginStyleSheet.LIST_WIDGET.format(
            bg=PluginStyleSheet.COLOR_BG,
            text=PluginStyleSheet.COLOR_TEXT,
            border=PluginStyleSheet.COLOR_BORDER,
            focus=focus_color
        ))
        return lst
    
    @staticmethod
    def create_horizontal_buttons(buttons: list) -> QHBoxLayout:
        """
        Cria um layout horizontal com botões.
        
        Args:
            buttons: Lista de tuplas (QPushButton, callback opcional)
            
        Returns:
            QHBoxLayout com os botões
        """
        layout = QHBoxLayout()
        for btn in buttons:
            if isinstance(btn, tuple):
                button, callback = btn
                if callback:
                    button.clicked.connect(callback)
                layout.addWidget(button)
            else:
                layout.addWidget(btn)
        layout.addStretch()
        return layout
    
    @staticmethod
    def _lighten_color(hex_color: str, percent: int) -> str:
        """Esclarece uma cor em hex."""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        r = min(255, int(r + (255 - r) * percent / 100))
        g = min(255, int(g + (255 - g) * percent / 100))
        b = min(255, int(b + (255 - b) * percent / 100))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    @staticmethod
    def _darken_color(hex_color: str, percent: int) -> str:
        """Escurece uma cor em hex."""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        r = max(0, int(r * (100 - percent) / 100))
        g = max(0, int(g * (100 - percent) / 100))
        b = max(0, int(b * (100 - percent) / 100))
        
        return f"#{r:02x}{g:02x}{b:02x}"


class PluginContainer:
    """Classe base para plugins que usam o helper UI."""
    
    def __init__(self):
        self.base_path_label: Optional[QLabel] = None
    
    def setup_base_path_section(self, layout: QVBoxLayout) -> None:
        """
        Adiciona seção de pasta base ao layout do plugin.
        
        Args:
            layout: Layout principal onde adicionar
        """
        container, self.base_path_label = PluginUIHelper.create_base_path_widget()
        layout.addWidget(container)
        layout.addSpacing(8)
    
    def update_base_path(self, new_path: str) -> None:
        """Atualiza o label da pasta base."""
        if self.base_path_label:
            self.base_path_label.setText(new_path)
