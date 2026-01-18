from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QToolBar,
    QDockWidget,
    QListWidget,
    QWidget,
    QVBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QFileDialog,
    QHBoxLayout,
)

from PySide6.QtGui import QAction, QPixmap, QIcon, QImage, QFont
from PySide6.QtCore import Qt, QSize

from src.plugin_manager import PluginManager
from src.icon_generator import create_icon_pixmap
from src.animations import AnimatedToolButton, AnimatedButton, AnimatedListWidget, UIAnimations
from src.draggable_tab_widget import DraggableTabWidget
from src.draggable_toolbar import DraggableToolBar
from src.log_viewer import LogViewer
from config.preferences import Preferences
from src.signal_manager import SignalManager
from src.theme import DARK_STYLESHEET


from utils.ToolKey import ToolKey
from utils.LogUtils import logger


class MainWindow(QMainWindow):
    TOOL_KEY = ToolKey.MAIN_WINDOW
    def __init__(self):
        super().__init__()
        logger.info(self.TOOL_KEY, "MainWindow", "Aplicação MTL_UTIL iniciada")
        self.setWindowTitle("Mini-IDE Inspirado no Visual Studio")
        self.resize(1200, 800)

        self.plugin_manager = PluginManager()
        self.preferences = Preferences()
        self.signal_manager = SignalManager()
        
        # Dicionário para rastrear widgets de plugins abertos
        self.open_plugins: dict = {}

        # Aplicar stylesheet dark mode
        self.setStyleSheet(DARK_STYLESHEET)

        self._create_menu()
        self._create_plugins_toolbar()
        self._create_central()
        self._create_sidebar()
        self._create_taskbar()

    def _create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        view_menu = menubar.addMenu("View")
        help_menu = menubar.addMenu("Help")

        # Ação para mudar pasta base
        change_path_action = QAction("Alterar Pasta Base", self)
        change_path_action.triggered.connect(self._change_base_path)
        file_menu.addAction(change_path_action)
        
        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

        logs_action = QAction("Logs", self)
        logs_action.triggered.connect(self._show_logs)
        help_menu.addAction(logs_action)

    def _create_plugins_toolbar(self):
        """Cria a barra de ferramentas com ícones dos plugins na parte superior."""
        self.plugins_toolbar = DraggableToolBar("Plugins")
        self.plugins_toolbar.setIconSize(QSize(24, 24))

        # Dicionário para mapear ícones aos plugins
        self.plugin_buttons = {}
        
        # Carrega plugins dinamicamente
        self.plugin_manager.load_plugins()
        plugin_names = self.plugin_manager.get_plugin_names()
        
        icon_map = {
            "Calculator": "calculator",
            "Todo List": "checklist",
            "Simple Browser": "browser",
            "Text Viewer": "text",
        }
        
        for plugin_name in plugin_names:
            icon_type = icon_map.get(plugin_name, "plugins")
            icon = QIcon(create_icon_pixmap(icon_type, size=24))
            
            # Criar AnimatedToolButton em vez de QAction
            btn = AnimatedToolButton()
            btn.setIcon(icon)
            btn.setToolTip(plugin_name)
            btn.clicked.connect(lambda checked, name=plugin_name: self._open_plugin(name))
            self.plugins_toolbar.addWidget(btn)
            self.plugin_buttons[plugin_name] = btn
        
        self.addToolBar(self.plugins_toolbar)

    def _create_central(self):
        self.tab_widget = DraggableTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.tab_widget.removeTab)
        self.setCentralWidget(self.tab_widget)

    def _open_plugin(self, plugin_name: str):
        """Abre um plugin quando o ícone é clicado. Se já estiver aberto, ativa a aba."""
        logger.debug(self.TOOL_KEY, "MainWindow", f"Tentativa de abrir plugin: {plugin_name}")
        # Verifica se o plugin já está aberto
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == plugin_name:
                # Plugin já está aberto, ativa a aba
                self.tab_widget.setCurrentIndex(i)
                logger.info(self.TOOL_KEY, "MainWindow", f"Plugin {plugin_name} já estava aberto, aba ativada")
                return
        
        # Se não estiver aberto, cria novo
        widget = self.plugin_manager.create_widget_for(plugin_name, parent=self)
        if widget is None:
            logger.error(self.TOOL_KEY, "MainWindow", f"Falha ao criar widget para plugin {plugin_name}")
            QMessageBox.warning(self, "Erro", f"Não foi possível abrir plugin {plugin_name}")
            return
        
        index = self.tab_widget.addTab(widget, plugin_name)
        self.tab_widget.setCurrentIndex(index)
        
        # Animação de fade-in para o novo plugin
        UIAnimations.animate_fade_in(widget)
        
        # Registra o widget do plugin para notificações futuras
        self.open_plugins[plugin_name] = widget
        logger.info(self.TOOL_KEY, "MainWindow", f"Plugin {plugin_name} aberto com sucesso")
        
        # Envia a pasta base atual para o novo plugin
        self._notify_plugin_base_path(widget, plugin_name)

    def _create_sidebar(self):
        """Cria a barra lateral com o navegador de plugins."""
        self.sidebar = QToolBar("Plugin Navigator")
        self.sidebar.setOrientation(Qt.Vertical)
        self.sidebar.setMovable(False)
        self.sidebar.setIconSize(QSize(32, 32))

        # Botão para abrir/fechar o navegador de plugins
        navigator_action = QAction(QIcon(create_icon_pixmap("plugins", size=32)), "", self)
        navigator_action.setToolTip("Navegador de Plugins")
        navigator_action.triggered.connect(self._toggle_explorer_dock)
        self.sidebar.addAction(navigator_action)
        
        self.addToolBar(Qt.LeftToolBarArea, self.sidebar)
        self._create_explorer_dock()

    def _create_explorer_dock(self):
        """Cria o painel lateral com configurações e lista de plugins."""
        self.explorer_dock = QDockWidget("Configurações", self)
        self.explorer_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        container = QWidget()
        layout = QVBoxLayout()
        
        # Seção de Pasta Base
        base_path_label = QLabel("Pasta Base:")
        base_path_label.setStyleSheet("font-weight: bold; color: #0e639c;")
        layout.addWidget(base_path_label)
        
        # Widget para exibir e mudar caminho base
        path_container = QWidget()
        path_layout = QHBoxLayout(path_container)
        path_layout.setContentsMargins(0, 0, 0, 0)
        
        self.base_path_display = QLabel(self.preferences.get_base_path())
        self.base_path_display.setStyleSheet("""
            QLabel {
                background-color: #252526;
                color: #9cdcfe;
                border: 1px solid #3e3e3e;
                padding: 8px;
                border-radius: 3px;
            }
        """)
        self.base_path_display.setWordWrap(True)
        self.base_path_display.setMinimumHeight(40)
        
        change_path_btn = AnimatedButton("Alterar")
        change_path_btn.setMaximumWidth(80)
        change_path_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                padding: 6px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
        """)
        change_path_btn.clicked.connect(self._change_base_path)
        
        path_layout.addWidget(self.base_path_display)
        path_layout.addWidget(change_path_btn)
        layout.addWidget(path_container)
        
        layout.addSpacing(20)
        
        # Seção de Plugins Disponíveis
        plugins_label = QLabel("Plugins Disponíveis:")
        plugins_label.setStyleSheet("font-weight: bold; color: #4ec9b0;")
        layout.addWidget(plugins_label)
        
        self.plugin_list = AnimatedListWidget()
        self.plugin_list.addItems(self.plugin_manager.get_plugin_names())
        self.plugin_list.itemDoubleClicked.connect(self._open_selected_plugin)
        layout.addWidget(self.plugin_list)
        
        layout.addStretch()
        container.setLayout(layout)
        self.explorer_dock.setWidget(container)
        self.explorer_dock.hide()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.explorer_dock)

    def _toggle_explorer_dock(self):
        """Abre/fecha o navegador lateral de plugins."""
        visible = self.explorer_dock.isVisible()
        if visible:
            self.explorer_dock.hide()
        else:
            self.plugin_manager.load_plugins()
            self.plugin_list.clear()
            self.plugin_list.addItems(self.plugin_manager.get_plugin_names())
            self.explorer_dock.show()

    def _open_selected_plugin(self, item):
        """Abre um plugin selecionado da lista."""
        name = item.text()
        self._open_plugin(name)

    def _change_base_path(self):
        """Abre o diálogo para escolher uma nova pasta base."""
        logger.debug(self.TOOL_KEY, "MainWindow", "Diálogo de mudança de pasta base aberto")
        current_path = self.preferences.get_base_path()
        
        new_path = QFileDialog.getExistingDirectory(
            self,
            "Selecione a Pasta Base",
            current_path,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if new_path:
            logger.info(self.TOOL_KEY, "MainWindow", f"Pasta base alterada de '{current_path}' para '{new_path}'")
            # Salva a nova pasta base
            self.preferences.set_base_path(new_path)
            self.base_path_display.setText(new_path)
            
            # Emite sinal para todos os plugins
            self._notify_all_plugins_base_path_changed(new_path)
        else:
            logger.debug(self.TOOL_KEY, "MainWindow", "Mudança de pasta base cancelada pelo usuário")
    
    def _notify_plugin_base_path(self, widget: QWidget, plugin_name: str) -> None:
        """Notifica um plugin individual sobre o caminho base."""
        current_path = self.preferences.get_base_path()
        
        # Busca o plugin original para chamar o método
        plugin = self.plugin_manager.plugins.get(plugin_name)
        if plugin and hasattr(plugin, 'on_base_path_changed'):
            plugin.on_base_path_changed(current_path)
    
    def _notify_all_plugins_base_path_changed(self, new_path: str) -> None:
        """Notifica todos os plugins abertos sobre mudança de caminho base."""
        # Emite o sinal Qt
        self.signal_manager.emit_base_path_changed(new_path)
        
        # Chama o método em todos os plugins carregados
        for plugin_name, plugin in self.plugin_manager.plugins.items():
            if hasattr(plugin, 'on_base_path_changed'):
                plugin.on_base_path_changed(new_path)

    def _create_taskbar(self):
        self.taskbar = QToolBar("Taskbar")
        self.taskbar.setMovable(False)
        self.addToolBar(Qt.BottomToolBarArea, self.taskbar)

        new_action = QAction(QIcon(), "New", self)
        open_action = QAction(QIcon(), "Open", self)
        save_action = QAction(QIcon(), "Save", self)

        self.taskbar.addAction(new_action)
        self.taskbar.addAction(open_action)
        self.taskbar.addAction(save_action)

    def _show_about(self):
        QMessageBox.information(self, "About", "Mini-IDE exemplo inspirado no Visual Studio\nFeito com PySide6")

    def _show_logs(self):
        """Abre a janela de visualização de logs."""
        logger.debug(self.TOOL_KEY, "MainWindow", "Abrindo visualizador de logs")
        viewer = LogViewer(self)
        viewer.exec()
