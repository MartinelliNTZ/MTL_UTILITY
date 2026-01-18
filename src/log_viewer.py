"""
LogViewer - Ferramenta para visualização e análise de logs da aplicação.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QLineEdit, QPushButton, QLabel, QComboBox, QSplitter,
    QTextEdit, QGroupBox, QCheckBox, QWidget, QMenu, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QAction
from utils.LogUtils import logger, LogLevel


class LogEntry:
    """Representa uma entrada de log."""
    def __init__(self, data: Dict[str, Any]):
        self.timestamp = data.get('timestamp', '')
        self.level = data.get('level', 'INFO')
        self.tool_key = data.get('tool_key', 'unknown')
        self.class_name = data.get('class_name', 'Unknown')
        self.message = data.get('message', '')
        self.extra_data = data.get('extra_data', {})


class LogViewer(QDialog):
    """Janela para visualização de logs com filtros e pesquisa."""

    # Cores para tool_keys (inspirado no Android Studio)
    TOOL_KEY_COLORS = {
        'system': '#FF6B6B',      # Vermelho
        'main_window': '#4ECDC4', # Turquesa
        'calculator': '#45B7D1',  # Azul claro
        'todo_list': '#96CEB4',   # Verde menta
        'simple_browser': '#FFEAA7', # Amarelo
        'text_viewer': '#DDA0DD', # Plum
        'plugin_manager': '#98D8C8', # Verde água
        'preferences': '#F7DC6F', # Amarelo ouro
        'signal_manager': '#BB8FCE', # Roxo claro
        'animations': '#85C1E9',  # Azul céu
        'theme': '#F8C471',      # Laranja
        'icon_generator': '#82E0AA', # Verde limão
        'draggable_tab': '#F1948A', # Coral
        'draggable_toolbar': '#AED6F1' # Azul gelo
    }

    # Cores para níveis de log
    LEVEL_COLORS = {
        'DEBUG': '#9CA3AF',      # Cinza
        'INFO': '#10B981',       # Verde
        'WARNING': '#F59E0B',    # Âmbar
        'ERROR': '#EF4444',      # Vermelho
        'CRITICAL': '#7C2D12'    # Marrom escuro
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info('main_window', 'LogViewer', 'Janela de visualização de logs aberta')
        self.setWindowTitle("Visualizador de Logs - MTL_UTIL")
        self.resize(1200, 800)

        self.log_entries: List[LogEntry] = []
        self.filtered_entries: List[LogEntry] = []
        self.current_log_file = None

        # Coletar tool keys e classes disponíveis
        self.available_toolkeys = set()
        self.available_classes = set()

        self._setup_ui()
        self._load_logs()
        self._apply_filters()

    def _setup_ui(self):
        """Configura a interface da janela."""
        layout = QVBoxLayout(self)

        # Splitter principal
        splitter = QSplitter(Qt.Vertical)
        layout.addWidget(splitter)

        # Painel superior - Filtros e tabela
        top_widget = self._create_top_panel()
        splitter.addWidget(top_widget)

        # Painel inferior - Detalhes do log selecionado
        bottom_widget = self._create_bottom_panel()
        splitter.addWidget(bottom_widget)

        splitter.setSizes([600, 200])

    def _create_top_panel(self):
        """Cria o painel superior com filtros e tabela."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Seletor de arquivo de log
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Arquivo de Log:"))
        self.file_combo = QComboBox()
        self.file_combo.currentTextChanged.connect(self._on_file_changed)
        file_layout.addWidget(self.file_combo)
        file_layout.addStretch()
        layout.addLayout(file_layout)

        # Filtros
        filters_group = QGroupBox("Filtros")
        filters_layout = QVBoxLayout(filters_group)

        # Linha 1: ToolKey, Classe, Nível
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("ToolKey:"))
        self.toolkey_filter = QComboBox()
        self.toolkey_filter.addItem("Todos", "")
        self.toolkey_filter.currentTextChanged.connect(self._apply_filters)
        row1.addWidget(self.toolkey_filter)

        row1.addWidget(QLabel("Classe:"))
        self.class_filter = QComboBox()
        self.class_filter.addItem("Todos", "")
        self.class_filter.currentTextChanged.connect(self._apply_filters)
        row1.addWidget(self.class_filter)

        row1.addWidget(QLabel("Nível:"))
        self.level_combo = QComboBox()
        self.level_combo.addItem("Todos", "")
        for level in LogLevel:
            self.level_combo.addItem(level.value, level.value)
        self.level_combo.currentTextChanged.connect(self._apply_filters)
        row1.addWidget(self.level_combo)

        filters_layout.addLayout(row1)

        # Linha 2: Pesquisa geral e botões
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Pesquisar:"))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Buscar em todos os campos...")
        self.search_edit.textChanged.connect(self._apply_filters)
        row2.addWidget(self.search_edit)

        self.clear_btn = QPushButton("Limpar Filtros")
        self.clear_btn.clicked.connect(self._clear_filters)
        row2.addWidget(self.clear_btn)

        filters_layout.addLayout(row2)

        layout.addWidget(filters_group)

        # Tabela de logs
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Data/Hora", "ToolKey", "Classe", "Nível", "Mensagem"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        # Tema escuro com linhas alternadas
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #000000;
                alternate-background-color: #202124;
                color: #ffffff;
                gridline-color: #555555;
            }
            QTableWidget::item {
                border: none;
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #404040;
            }
            QHeaderView::section {
                background-color: #404040;
                color: #ffffff;
                padding: 8px;
                border: 1px solid #555555;
                font-weight: bold;
            }
        """)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        layout.addWidget(self.table)

        return widget

    def _create_bottom_panel(self):
        """Cria o painel inferior com detalhes do log."""
        group = QGroupBox("Detalhes do Log Selecionado")
        layout = QVBoxLayout(group)

        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMaximumHeight(150)
        layout.addWidget(self.details_text)

        return group

    def _load_logs(self):
        """Carrega a lista de arquivos de log disponíveis."""
        log_dir = Path("config")
        log_files = sorted(log_dir.glob("mtl_util_*.log"), key=lambda x: x.stat().st_mtime, reverse=True)

        self.file_combo.clear()
        for log_file in log_files:
            # Formatar nome do arquivo para exibição
            name = log_file.name.replace("mtl_util_", "").replace(".log", "").replace("_", " ")
            self.file_combo.addItem(f"{name} ({log_file.name})", str(log_file))

        if log_files:
            self.file_combo.setCurrentIndex(0)
            self._load_log_file(log_files[0])

    def _on_file_changed(self):
        """Chamado quando o arquivo selecionado muda."""
        current_data = self.file_combo.currentData()
        if current_data:
            self._load_log_file(Path(current_data))

    def _load_log_file(self, log_file: Path):
        """Carrega as entradas de log de um arquivo específico."""
        self.log_entries.clear()
        self.available_toolkeys.clear()
        self.available_classes.clear()
        self.current_log_file = log_file

        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            data = json.loads(line)
                            entry = LogEntry(data)
                            self.log_entries.append(entry)
                            # Coletar tool keys e classes
                            self.available_toolkeys.add(entry.tool_key)
                            self.available_classes.add(entry.class_name)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            logger.error('main_window', 'LogViewer', f'Erro ao carregar arquivo de log: {e}')

        # Atualizar filtros com os valores disponíveis
        self._update_filter_options()
        self._apply_filters()

    def _update_filter_options(self):
        """Atualiza as opções dos filtros com os valores disponíveis nos logs."""
        # ToolKey filter
        self.toolkey_filter.clear()
        self.toolkey_filter.addItem("Todos", "")
        for toolkey in sorted(self.available_toolkeys):
            self.toolkey_filter.addItem(toolkey, toolkey)

        # Class filter
        self.class_filter.clear()
        self.class_filter.addItem("Todos", "")
        for class_name in sorted(self.available_classes):
            self.class_filter.addItem(class_name, class_name)

    def _apply_filters(self):
        """Aplica os filtros atuais e atualiza a tabela."""
        toolkey_filter = self.toolkey_filter.currentData() or ""
        class_filter = self.class_filter.currentData() or ""
        level_filter = self.level_combo.currentData() or ""
        search_text = self.search_edit.text().lower()

        self.filtered_entries = []
        for entry in self.log_entries:
            # Aplicar filtros
            if toolkey_filter and entry.tool_key != toolkey_filter:
                continue
            if class_filter and entry.class_name != class_filter:
                continue
            if level_filter and entry.level != level_filter:
                continue

            # Filtro de pesquisa geral
            if search_text:
                searchable = f"{entry.timestamp} {entry.tool_key} {entry.class_name} {entry.level} {entry.message}".lower()
                if search_text not in searchable:
                    continue

            self.filtered_entries.append(entry)

        self._update_table()

    def _update_table(self):
        """Atualiza a tabela com as entradas filtradas."""
        self.table.setRowCount(0)
        self.table.setSortingEnabled(False)  # Desabilitar durante atualização

        for row, entry in enumerate(self.filtered_entries):
            self.table.insertRow(row)

            # Data/Hora
            time_item = QTableWidgetItem(entry.timestamp)
            self.table.setItem(row, 0, time_item)

            # ToolKey (texto colorido)
            toolkey_item = QTableWidgetItem(entry.tool_key)
            color = QColor(self.TOOL_KEY_COLORS.get(entry.tool_key, '#FFFFFF'))
            toolkey_item.setForeground(color)
            self.table.setItem(row, 1, toolkey_item)

            # Classe
            class_item = QTableWidgetItem(entry.class_name)
            self.table.setItem(row, 2, class_item)

            # Nível (texto colorido)
            level_item = QTableWidgetItem(entry.level)
            level_color = QColor(self.LEVEL_COLORS.get(entry.level, '#FFFFFF'))
            level_item.setForeground(level_color)
            self.table.setItem(row, 3, level_item)

            # Mensagem
            message_item = QTableWidgetItem(entry.message)
            self.table.setItem(row, 4, message_item)

        self.table.setSortingEnabled(True)  # Reabilitar ordenação
        self.table.resizeColumnsToContents()

    def _clear_filters(self):
        """Limpa todos os filtros."""
        self.toolkey_filter.setCurrentIndex(0)
        self.class_filter.setCurrentIndex(0)
        self.level_combo.setCurrentIndex(0)
        self.search_edit.clear()

    def _on_selection_changed(self):
        """Chamado quando a seleção da tabela muda."""
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())

        if len(selected_rows) == 1:
            row = list(selected_rows)[0]
            if row < len(self.filtered_entries):
                entry = self.filtered_entries[row]
                details = f"""Timestamp: {entry.timestamp}
Tool Key: {entry.tool_key}
Classe: {entry.class_name}
Nível: {entry.level}
Mensagem: {entry.message}"""

                if entry.extra_data:
                    details += f"\nDados Extras: {json.dumps(entry.extra_data, indent=2, ensure_ascii=False)}"

                self.details_text.setPlainText(details)
        else:
            self.details_text.clear()