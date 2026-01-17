from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from src.base_plugin import BasePlugin
from src.plugin_ui_helper import PluginUIHelper, PluginContainer, PluginStyleSheet


class SampleBrowser(BasePlugin, PluginContainer):
    name = "Simple Browser"
    icon_name = "browser"
    
    def __init__(self):
        BasePlugin.__init__(self)
        PluginContainer.__init__(self)

    def create_widget(self, parent=None) -> QWidget:
        w = QWidget(parent)
        layout = QVBoxLayout(w)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Title
        layout.addWidget(PluginUIHelper.create_title("Navegador Simples", PluginStyleSheet.COLOR_ORANGE))
        
        # Pasta Base
        self.setup_base_path_section(layout)
        
        # URL Bar
        url_layout = QHBoxLayout()
        url_input = PluginUIHelper.create_input_field("Digite uma URL...")
        
        go_btn = PluginUIHelper.create_button("Ir", PluginStyleSheet.COLOR_ORANGE)
        go_btn.setMinimumWidth(60)
        
        url_layout.addWidget(url_input)
        url_layout.addWidget(go_btn)
        layout.addLayout(url_layout)
        
        # Content area
        content = PluginUIHelper.create_text_editor()
        content.setReadOnly(True)
        content.setStyleSheet("""
            QTextEdit {
                background-color: #252526;
                color: #9cdcfe;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                padding: 12px;
                font-size: 10pt;
                font-family: 'Consolas', monospace;
            }
        """)
        
        default_text = """
<h2 style="color: #f48771;">Bem-vindo ao Navegador Simples</h2>
<p style="color: #9cdcfe;">
Este é um navegador de exemplo. Você pode usar este espaço para:
</p>
<ul style="color: #9cdcfe;">
    <li>Visualizar conteúdo web</li>
    <li>Exibir informações de URL</li>
    <li>Renderizar HTML simples</li>
</ul>
<p style="color: #858585; font-size: 9pt;">
Digite uma URL na barra acima e clique em 'Ir' para navegar.
</p>
        """.strip()
        
        content.setHtml(default_text)
        
        def navigate():
            url = url_input.text().strip()
            if url:
                info_text = f"""
<h3 style="color: #f48771;">URL Digitada:</h3>
<p style="color: #9cdcfe; font-family: monospace;">{url}</p>
<p style="color: #858585; font-size: 9pt;">
Em um navegador real, este URL seria carregado aqui.
Este é apenas um exemplo de interface.
</p>
                """.strip()
                content.setHtml(info_text)
        
        go_btn.clicked.connect(navigate)
        url_input.returnPressed.connect(navigate)
        
        layout.addWidget(content)
        return w
    
    def on_base_path_changed(self, new_path: str) -> None:
        """Atualiza a pasta base quando muda."""
        self.update_base_path(new_path)


def get_plugin():
    return SampleBrowser()
