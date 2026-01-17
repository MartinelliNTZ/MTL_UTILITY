from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QHBoxLayout
from PySide6.QtCore import Qt
from src.base_plugin import BasePlugin
from src.plugin_ui_helper import PluginUIHelper, PluginContainer, PluginStyleSheet


class TodoList(BasePlugin, PluginContainer):
    name = "Todo List"
    icon_name = "checklist"
    
    def __init__(self):
        BasePlugin.__init__(self)
        PluginContainer.__init__(self)

    def create_widget(self, parent=None) -> QWidget:
        w = QWidget(parent)
        layout = QVBoxLayout(w)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Title
        layout.addWidget(PluginUIHelper.create_title("Lista de Tarefas", PluginStyleSheet.COLOR_SUCCESS))
        
        # Pasta Base
        self.setup_base_path_section(layout)
        
        # Input field
        input_layout = QHBoxLayout()
        input_field = PluginUIHelper.create_input_field("Digite uma nova tarefa...")
        
        add_btn = PluginUIHelper.create_button("+ Adicionar", PluginStyleSheet.COLOR_SUCCESS)
        add_btn.setMinimumWidth(100)
        
        input_layout.addWidget(input_field)
        input_layout.addWidget(add_btn)
        layout.addLayout(input_layout)
        
        # Todo list
        todo_list = PluginUIHelper.create_list_widget()
        
        # Add sample items
        sample_tasks = [
            "✓ Estudar PySide6",
            "○ Implementar novos plugins",
            "○ Refatorar código",
            "○ Criar testes"
        ]
        
        for task in sample_tasks:
            item = QListWidgetItem(task)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            todo_list.addItem(item)
        
        layout.addWidget(QLabel("Tarefas:"))
        layout.addWidget(todo_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        def add_task():
            text = input_field.text().strip()
            if text:
                item = QListWidgetItem("○ " + text)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                todo_list.addItem(item)
                input_field.clear()
            input_field.setFocus()
        
        add_btn.clicked.connect(add_task)
        input_field.returnPressed.connect(add_task)
        
        remove_btn = PluginUIHelper.create_button("- Remover", PluginStyleSheet.COLOR_DANGER)
        remove_btn.clicked.connect(lambda: self._remove_task(todo_list))
        
        button_layout.addWidget(remove_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        layout.addStretch()
        return w
    
    def _remove_task(self, todo_list: QListWidget) -> None:
        """Remove a tarefa selecionada."""
        current_row = todo_list.currentRow()
        if current_row >= 0:
            todo_list.takeItem(current_row)
    
    def on_base_path_changed(self, new_path: str) -> None:
        """Atualiza a pasta base quando muda."""
        self.update_base_path(new_path)


def get_plugin():
    return TodoList()
