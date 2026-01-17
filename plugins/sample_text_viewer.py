from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QClipboard
from PySide6.QtWidgets import QApplication
from src.base_plugin import BasePlugin
from src.plugin_ui_helper import PluginUIHelper, PluginContainer, PluginStyleSheet


class SampleTextViewer(BasePlugin, PluginContainer):
    name = "Text Viewer"
    icon_name = "text"
    
    def __init__(self):
        BasePlugin.__init__(self)
        PluginContainer.__init__(self)

    def create_widget(self, parent=None) -> QWidget:
        w = QWidget(parent)
        layout = QVBoxLayout(w)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Title
        layout.addWidget(PluginUIHelper.create_title("Visualizador de Texto", PluginStyleSheet.COLOR_WARNING))
        
        # Pasta Base
        self.setup_base_path_section(layout)
        
        # Description
        desc = QLabel("Editor de texto simples com suporte a formatação básica")
        desc.setStyleSheet("color: #858585; font-size: 10pt;")
        layout.addWidget(desc)
        
        # Editor
        editor = PluginUIHelper.create_text_editor()
        editor.setPlainText("""Exemplo de plugin: Text Viewer

Este é um visualizador/editor de texto simples.

Você pode usar este espaço para:
• Editar documentos de texto
• Visualizar conteúdo
• Trabalhar com códigos simples

Sinta-se à vontade para adicionar mais funcionalidades!""")
        
        editor.setStyleSheet("""
            QTextEdit {
                background-color: #252526;
                color: #e0e0e0;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                padding: 12px;
                font-size: 10pt;
                font-family: 'Consolas', 'Monaco', monospace;
            }
            QTextEdit:focus {
                border: 1px solid #ce9178;
            }
        """)
        
        layout.addWidget(editor)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        clear_btn = PluginUIHelper.create_button("Limpar", PluginStyleSheet.COLOR_WARNING)
        clear_btn.clicked.connect(editor.clear)
        
        copy_btn = PluginUIHelper.create_button("Copiar", PluginStyleSheet.COLOR_PRIMARY)
        
        def copy_text():
            clipboard = QApplication.clipboard()
            clipboard.setText(editor.toPlainText())
        
        copy_btn.clicked.connect(copy_text)
        
        button_layout.addWidget(copy_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        return w
    
    def on_base_path_changed(self, new_path: str) -> None:
        """Atualiza a pasta base quando muda."""
        self.update_base_path(new_path)


def get_plugin():
    return SampleTextViewer()
