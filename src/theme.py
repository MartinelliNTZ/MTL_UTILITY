# Stylesheet Dark Mode - Inspirado em Visual Studio, QGIS e IntelliJ

DARK_STYLESHEET = """
QMainWindow {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

QMenuBar {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border-bottom: 1px solid #3e3e3e;
}

QMenuBar::item:selected {
    background-color: #3e3e3e;
}

QMenu {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #3e3e3e;
}

QMenu::item:selected {
    background-color: #0e639c;
}

QToolBar {
    background-color: #252526;
    border: none;
    border-bottom: 1px solid #3e3e3e;
    padding: 6px 2px;
    spacing: 4px;
}

QToolButton {
    color: #e0e0e0;
    background-color: transparent;
    border: none;
    padding: 4px;
    margin: 2px;
    border-radius: 3px;
}

QToolButton:hover {
    background-color: #3e3e3e;
    border-radius: 3px;
}

QToolButton:pressed {
    background-color: #0e639c;
}

QTabWidget::pane {
    border: none;
    background-color: #1e1e1e;
}

QTabBar {
    background-color: #252526;
    border-bottom: 1px solid #3e3e3e;
}

QTabBar::tab {
    background-color: #2d2d2d;
    color: #858585;
    padding: 8px 20px;
    margin-right: 2px;
    border: none;
    border-bottom: 2px solid transparent;
}

QTabBar::tab:hover {
    background-color: #3e3e3e;
}

QTabBar::tab:selected {
    color: #e0e0e0;
    background-color: #1e1e1e;
    border-bottom: 2px solid #0e639c;
}

QTabBar::close-button {
    background-color: transparent;
    border: none;
    padding: 2px;
    margin: 0px 2px;
}

QTabBar::close-button:hover {
    background-color: #ff4444;
    border-radius: 2px;
}

QDockWidget {
    color: #e0e0e0;
    background-color: #1e1e1e;
    border: none;
}

QDockWidget::title {
    background-color: #252526;
    color: #e0e0e0;
    padding: 8px;
    border-bottom: 1px solid #3e3e3e;
}

QListWidget {
    background-color: #252526;
    color: #e0e0e0;
    border: none;
    outline: none;
}

QListWidget::item {
    padding: 6px;
    border-radius: 3px;
    margin: 2px;
}

QListWidget::item:hover {
    background-color: #3e3e3e;
}

QListWidget::item:selected {
    background-color: #0e639c;
}

QListWidget::item:selected:active {
    background-color: #0e639c;
}

QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

QLabel {
    color: #e0e0e0;
    background-color: transparent;
}

QPushButton {
    background-color: #0e639c;
    color: #ffffff;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1177bb;
}

QPushButton:pressed {
    background-color: #094a7a;
}

QPushButton:disabled {
    background-color: #3e3e3e;
    color: #858585;
}

QTextEdit {
    background-color: #252526;
    color: #e0e0e0;
    border: 1px solid #3e3e3e;
    border-radius: 4px;
    padding: 8px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 10pt;
}

QTextEdit:focus {
    border: 1px solid #0e639c;
}

QLineEdit {
    background-color: #3e3e3e;
    color: #e0e0e0;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 6px;
}

QLineEdit:focus {
    border: 1px solid #0e639c;
}

QScrollBar:vertical {
    background-color: #252526;
    width: 12px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #3e3e3e;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #555555;
}

QScrollBar:horizontal {
    background-color: #252526;
    height: 12px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #3e3e3e;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #555555;
}

QScrollBar::add-line, QScrollBar::sub-line {
    border: none;
    background-color: none;
}

QMessageBox {
    background-color: #1e1e1e;
}

QMessageBox QLabel {
    color: #e0e0e0;
}

QMessageBox QPushButton {
    min-width: 60px;
    min-height: 24px;
}

QInputDialog {
    background-color: #1e1e1e;
}

QComboBox {
    background-color: #3e3e3e;
    color: #e0e0e0;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 6px;
}

QComboBox:focus {
    border: 1px solid #0e639c;
}

QComboBox::drop-down {
    border: none;
}

QCheckBox {
    color: #e0e0e0;
    spacing: 6px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
}

QCheckBox::indicator:unchecked {
    background-color: #3e3e3e;
    border: 1px solid #555555;
    border-radius: 3px;
}

QCheckBox::indicator:checked {
    background-color: #0e639c;
    border: 1px solid #0e639c;
    border-radius: 3px;
}

QGroupBox {
    color: #e0e0e0;
    border: 1px solid #3e3e3e;
    border-radius: 4px;
    margin-top: 12px;
    padding-top: 8px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px 0 3px;
}
"""
