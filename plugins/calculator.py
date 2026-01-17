from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout
from src.base_plugin import BasePlugin
from src.plugin_ui_helper import PluginUIHelper, PluginContainer, PluginStyleSheet


class Calculator(BasePlugin, PluginContainer):
    name = "Calculator"
    icon_name = "calculator"
    
    def __init__(self):
        BasePlugin.__init__(self)
        PluginContainer.__init__(self)

    def create_widget(self, parent=None) -> QWidget:
        w = QWidget(parent)
        layout = QVBoxLayout(w)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Título
        layout.addWidget(PluginUIHelper.create_title("Calculadora", PluginStyleSheet.COLOR_PRIMARY))
        
        # Pasta Base
        self.setup_base_path_section(layout)
        
        # Display
        display = PluginUIHelper.create_text_editor()
        display.setPlainText("0")
        display.setReadOnly(True)
        display.setStyleSheet("""
            QTextEdit {
                background-color: #252526;
                color: #4ec9b0;
                border: 1px solid #3e3e3e;
                border-radius: 6px;
                padding: 16px;
                font-size: 28px;
                font-weight: bold;
                text-align: right;
            }
        """)
        display.setMinimumHeight(60)
        layout.addWidget(display)
        
        # Grid de botões
        self._create_buttons_grid(layout, display)
        
        # Botão Limpar
        clear_btn = PluginUIHelper.create_button("C (Limpar)", PluginStyleSheet.COLOR_DANGER)
        clear_btn.clicked.connect(lambda: display.setPlainText("0"))
        layout.addWidget(clear_btn)
        
        layout.addStretch()
        return w
    
    def _create_buttons_grid(self, layout: QVBoxLayout, display) -> None:
        """Cria a grid de botões da calculadora."""
        buttons = [
            ("7", "8", "9", "/"),
            ("4", "5", "6", "*"),
            ("1", "2", "3", "-"),
            ("0", ".", "=", "+")
        ]
        
        def button_click(val):
            if val == "=":
                try:
                    result = eval(display.toPlainText())
                    display.setPlainText(str(result))
                except:
                    display.setPlainText("Erro")
            else:
                current = display.toPlainText()
                if current == "0":
                    display.setPlainText(val)
                else:
                    display.setPlainText(current + val)
        
        grid = QGridLayout()
        grid.setSpacing(8)
        
        for row_idx, row in enumerate(buttons):
            for col_idx, btn_text in enumerate(row):
                # Determina cor baseado no tipo de botão
                if btn_text in "/*-+":
                    btn_color = PluginStyleSheet.COLOR_PRIMARY
                elif btn_text == "=":
                    btn_color = PluginStyleSheet.COLOR_SUCCESS
                else:
                    btn_color = PluginStyleSheet.COLOR_BORDER  # neutro
                
                btn = PluginUIHelper.create_button(btn_text, btn_color, height=50)
                btn.clicked.connect(lambda checked, val=btn_text: button_click(val))
                grid.addWidget(btn, row_idx, col_idx)
        
        layout.addLayout(grid)
    
    def on_base_path_changed(self, new_path: str) -> None:
        """Atualiza a pasta base quando muda."""
        self.update_base_path(new_path)


def get_plugin():
    return Calculator()
