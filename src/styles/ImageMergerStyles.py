"""
ImageMergerStyles - Estilos centralizados para o plugin Image Merger.

Define todas as stylesheets (QSS) e constantes de aparência
específicas do plugin Image Merger.
"""


class ImageMergerStyles:
    """Estilos CSS/QSS centralizados para o Image Merger."""

    # Cores do tema (escuro)
    COLOR_BG_DARK = "#1e1e1e"
    COLOR_BG_PANEL = "#252526"
    COLOR_FG_TEXT = "#d4d4d4"
    COLOR_FG_HIGHLIGHT = "#007acc"
    COLOR_BORDER = "#3e3e3e"
    COLOR_SUCCESS = "#4ec9b0"
    COLOR_WARNING = "#dcdcaa"
    COLOR_ERROR = "#f48771"

    @staticmethod
    def get_folder_label_style() -> str:
        """Estilo do label que exibe a pasta atual."""
        return f"""
            QLabel {{
                color: {ImageMergerStyles.COLOR_FG_TEXT};
                background-color: {ImageMergerStyles.COLOR_BG_PANEL};
                border: 1px solid {ImageMergerStyles.COLOR_BORDER};
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 10pt;
                font-family: 'Consolas', monospace;
            }}
        """

    @staticmethod
    def get_button_style() -> str:
        """Estilo dos botões principais."""
        return f"""
            QPushButton {{
                background-color: {ImageMergerStyles.COLOR_BG_PANEL};
                color: {ImageMergerStyles.COLOR_FG_TEXT};
                border: 1px solid {ImageMergerStyles.COLOR_BORDER};
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 9pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {ImageMergerStyles.COLOR_FG_HIGHLIGHT};
                color: white;
                border: 1px solid {ImageMergerStyles.COLOR_FG_HIGHLIGHT};
            }}
            QPushButton:pressed {{
                background-color: #005a9e;
                color: white;
            }}
            QPushButton:disabled {{
                background-color: #333333;
                color: #666666;
                border: 1px solid #3e3e3e;
            }}
        """

    @staticmethod
    def get_image_list_style() -> str:
        """Estilo da QListWidget de imagens."""
        return f"""
            QListWidget {{
                background-color: {ImageMergerStyles.COLOR_BG_DARK};
                color: {ImageMergerStyles.COLOR_FG_TEXT};
                border: 1px solid {ImageMergerStyles.COLOR_BORDER};
                border-radius: 4px;
                padding: 6px;
                outline: none;
            }}
            QListWidget::item {{
                padding: 8px;
                border-radius: 4px;
                margin: 4px 0px;
            }}
            QListWidget::item:selected {{
                background-color: {ImageMergerStyles.COLOR_FG_HIGHLIGHT};
                color: white;
            }}
            QListWidget::item:hover {{
                background-color: {ImageMergerStyles.COLOR_BORDER};
            }}
        """

    @staticmethod
    def get_preview_label_style() -> str:
        """Estilo do label de pré-visualização."""
        return f"""
            QLabel {{
                background-color: {ImageMergerStyles.COLOR_BG_DARK};
                border: 1px solid {ImageMergerStyles.COLOR_BORDER};
                border-radius: 4px;
                padding: 10px;
            }}
        """

    @staticmethod
    def get_control_panel_style() -> str:
        """Estilo do painel de controle (lateral)."""
        return f"""
            QWidget {{
                background-color: {ImageMergerStyles.COLOR_BG_DARK};
                color: {ImageMergerStyles.COLOR_FG_TEXT};
            }}
            QGroupBox {{
                color: {ImageMergerStyles.COLOR_FG_TEXT};
                border: 1px solid {ImageMergerStyles.COLOR_BORDER};
                border-radius: 4px;
                padding: 8px;
                margin-top: 8px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 2px 0 2px;
            }}
            QCheckBox {{
                color: {ImageMergerStyles.COLOR_FG_TEXT};
                spacing: 6px;
                padding: 4px;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
            }}
            QCheckBox::indicator:unchecked {{
                background-color: {ImageMergerStyles.COLOR_BG_PANEL};
                border: 1px solid {ImageMergerStyles.COLOR_BORDER};
                border-radius: 2px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {ImageMergerStyles.COLOR_FG_HIGHLIGHT};
                border: 1px solid {ImageMergerStyles.COLOR_FG_HIGHLIGHT};
                color: white;
                image: url(:/checkmark);
            }}
        """

    @staticmethod
    def get_progress_bar_style() -> str:
        """Estilo da barra de progresso."""
        return f"""
            QProgressBar {{
                background-color: {ImageMergerStyles.COLOR_BG_PANEL};
                color: {ImageMergerStyles.COLOR_FG_TEXT};
                border: 1px solid {ImageMergerStyles.COLOR_BORDER};
                border-radius: 4px;
                height: 20px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {ImageMergerStyles.COLOR_FG_HIGHLIGHT};
                border-radius: 3px;
                margin: 1px;
            }}
        """

    @staticmethod
    def get_spinbox_style() -> str:
        """Estilo do QSpinBox (max_width)."""
        return f"""
            QSpinBox {{
                background-color: {ImageMergerStyles.COLOR_BG_PANEL};
                color: {ImageMergerStyles.COLOR_FG_TEXT};
                border: 1px solid {ImageMergerStyles.COLOR_BORDER};
                border-radius: 4px;
                padding: 4px;
                min-width: 60px;
            }}
            QSpinBox::up-button {{
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 18px;
                background-color: {ImageMergerStyles.COLOR_BG_PANEL};
                border-left: 1px solid {ImageMergerStyles.COLOR_BORDER};
            }}
            QSpinBox::down-button {{
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 18px;
                background-color: {ImageMergerStyles.COLOR_BG_PANEL};
                border-left: 1px solid {ImageMergerStyles.COLOR_BORDER};
            }}
        """

    @staticmethod
    def get_splitter_style() -> str:
        """Estilo do QSplitter."""
        return f"""
            QSplitter::handle {{
                background-color: {ImageMergerStyles.COLOR_BORDER};
                width: 2px;
            }}
            QSplitter::handle:hover {{
                background-color: {ImageMergerStyles.COLOR_FG_HIGHLIGHT};
            }}
        """

    @staticmethod
    def get_label_style() -> str:
        """Estilo padrão de labels."""
        return f"""
            QLabel {{
                color: {ImageMergerStyles.COLOR_FG_TEXT};
                background-color: transparent;
            }}
        """

    @staticmethod
    def get_title_style() -> str:
        """Estilo de titles/headings."""
        return f"""
            QLabel {{
                color: {ImageMergerStyles.COLOR_SUCCESS};
                background-color: transparent;
                font-size: 12pt;
                font-weight: bold;
            }}
        """
