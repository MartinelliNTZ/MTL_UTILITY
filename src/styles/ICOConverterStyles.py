"""
ICOConverterStyles - Estilos isolados para o plugin ICO Converter.

Centraliza toda a formatação e estilos utilizados pela interface do ICO Converter.
"""


class ICOConverterStyles:
    """Classe com constantes e métodos para geração de estilos do ICO Converter."""

    # ===== CORES =====
    COLOR_PRIMARY = "#0e639c"
    COLOR_PRIMARY_HOVER = "#0a4a7a"
    COLOR_PRIMARY_PRESSED = "#082f52"
    
    COLOR_BG_MAIN = "#2d2d30"
    COLOR_BG_DARK = "#252526"
    COLOR_BG_LIGHT = "#3e3e3e"
    
    COLOR_TEXT_PRIMARY = "#cccccc"
    COLOR_TEXT_SECONDARY = "#969696"
    
    COLOR_BORDER = "#3e3e3e"
    COLOR_BORDER_LIGHT = "#555555"
    
    COLOR_SPLITTER = "#3e3e3e"
    COLOR_PROGRESS = "#0e639c"

    # ===== ESPAÇAMENTOS =====
    SPACING_SMALL = 3
    SPACING_NORMAL = 8
    SPACING_MEDIUM = 10
    SPACING_LARGE = 12

    # ===== TAMANHOS =====
    BUTTON_MIN_HEIGHT = 28
    BUTTON_LARGE_HEIGHT = 36
    BUTTON_ICON_WIDTH = 40
    BUTTON_NORMAL_WIDTH = 90

    FONT_SIZE_NORMAL = "9pt"
    FONT_SIZE_SMALL = "8pt"
    FONT_SIZE_LARGE = "10pt"
    FONT_SIZE_XLARGE = "10pt"

    # ===== FOLHA DE ESTILOS COMPLETA =====

    @staticmethod
    def get_folder_label_style() -> str:
        """Retorna o stylesheet para o label de pasta."""
        return f"""
            QLabel {{
                background-color: {ICOConverterStyles.COLOR_BG_MAIN};
                color: {ICOConverterStyles.COLOR_TEXT_PRIMARY};
                border: 1px solid {ICOConverterStyles.COLOR_BORDER};
                padding: 6px 8px;
                border-radius: 3px;
                font-size: 9pt;
            }}
        """

    @staticmethod
    def get_button_style(color: str = None, hover: str = None, pressed: str = None) -> str:
        """
        Retorna o stylesheet para botões.
        
        Args:
            color: Cor de fundo (padrão: COLOR_PRIMARY)
            hover: Cor ao passar mouse (padrão: COLOR_PRIMARY_HOVER)
            pressed: Cor ao pressionar (padrão: COLOR_PRIMARY_PRESSED)
        """
        if color is None:
            color = ICOConverterStyles.COLOR_PRIMARY
        if hover is None:
            hover = ICOConverterStyles.COLOR_PRIMARY_HOVER
        if pressed is None:
            pressed = ICOConverterStyles.COLOR_PRIMARY_PRESSED

        return f"""
            QPushButton {{
                background-color: {color};
                color: {ICOConverterStyles.COLOR_TEXT_PRIMARY};
                border: none;
                border-radius: 4px;
                font-weight: 600;
                font-size: 10pt;
                padding: 6px 12px;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:pressed {{
                background-color: {pressed};
            }}
        """

    @staticmethod
    def get_splitter_style() -> str:
        """Retorna o stylesheet para splitters."""
        return f"""
            QSplitter::handle {{
                background-color: {ICOConverterStyles.COLOR_SPLITTER};
                width: 1px;
            }}
        """

    @staticmethod
    def get_image_list_style() -> str:
        """Retorna o stylesheet para a lista de imagens."""
        return f"""
            QListWidget {{
                background-color: {ICOConverterStyles.COLOR_BG_MAIN};
                color: {ICOConverterStyles.COLOR_TEXT_PRIMARY};
                border: 1px solid {ICOConverterStyles.COLOR_BORDER};
                border-radius: 4px;
                outline: none;
            }}
            QListWidget::item:selected {{
                background-color: #094771;
                border-left: 3px solid {ICOConverterStyles.COLOR_PRIMARY};
            }}
            QListWidget::item:hover {{
                background-color: {ICOConverterStyles.COLOR_BG_LIGHT};
            }}
        """

    @staticmethod
    def get_control_panel_style() -> str:
        """Retorna o stylesheet para o painel de controle."""
        return f"""
            QWidget {{
                background-color: {ICOConverterStyles.COLOR_BG_DARK};
                color: {ICOConverterStyles.COLOR_TEXT_PRIMARY};
            }}
            QGroupBox {{
                background-color: {ICOConverterStyles.COLOR_BG_MAIN};
                color: {ICOConverterStyles.COLOR_TEXT_PRIMARY};
                border: 1px solid {ICOConverterStyles.COLOR_BORDER};
                border-radius: 3px;
                margin-top: 8px;
                padding-top: 8px;
                font-weight: 600;
                font-size: 9pt;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 4px;
            }}
            QCheckBox {{
                color: {ICOConverterStyles.COLOR_TEXT_PRIMARY};
                spacing: 4px;
                font-size: 9pt;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
            }}
            QCheckBox::indicator:unchecked {{
                background-color: {ICOConverterStyles.COLOR_BG_LIGHT};
                border: 1px solid {ICOConverterStyles.COLOR_BORDER_LIGHT};
                border-radius: 2px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {ICOConverterStyles.COLOR_PRIMARY};
                border: 1px solid {ICOConverterStyles.COLOR_PRIMARY};
                border-radius: 2px;
            }}
        """

    @staticmethod
    def get_progress_bar_style() -> str:
        """Retorna o stylesheet para a barra de progresso."""
        return f"""
            QProgressBar {{
                background-color: {ICOConverterStyles.COLOR_BG_LIGHT};
                border: 1px solid {ICOConverterStyles.COLOR_BORDER_LIGHT};
                border-radius: 3px;
                text-align: center;
                color: {ICOConverterStyles.COLOR_TEXT_PRIMARY};
                font-size: 8pt;
            }}
            QProgressBar::chunk {{
                background-color: {ICOConverterStyles.COLOR_PROGRESS};
                border-radius: 2px;
            }}
        """

    @staticmethod
    def get_text_input_style() -> str:
        """Retorna o stylesheet para campos de entrada de texto."""
        return f"""
            QLineEdit {{
                background-color: {ICOConverterStyles.COLOR_BG_LIGHT};
                color: {ICOConverterStyles.COLOR_TEXT_PRIMARY};
                border: 1px solid {ICOConverterStyles.COLOR_BORDER};
                border-radius: 3px;
                padding: 4px 6px;
                font-size: 9pt;
            }}
            QLineEdit:focus {{
                border: 1px solid {ICOConverterStyles.COLOR_PRIMARY};
            }}
        """

    @staticmethod
    def get_combobox_style() -> str:
        """Retorna o stylesheet para caixas de combinação."""
        return f"""
            QComboBox {{
                background-color: {ICOConverterStyles.COLOR_BG_LIGHT};
                color: {ICOConverterStyles.COLOR_TEXT_PRIMARY};
                border: 1px solid {ICOConverterStyles.COLOR_BORDER};
                border-radius: 3px;
                padding: 4px 6px;
                font-size: 9pt;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                color: {ICOConverterStyles.COLOR_TEXT_PRIMARY};
            }}
        """

    @staticmethod
    def get_all_styles() -> dict:
        """
        Retorna um dicionário com todos os estilos disponíveis.
        
        Returns:
            Dicionário com os nomes dos estilos como chaves
        """
        return {
            'folder_label': ICOConverterStyles.get_folder_label_style(),
            'button': ICOConverterStyles.get_button_style(),
            'splitter': ICOConverterStyles.get_splitter_style(),
            'image_list': ICOConverterStyles.get_image_list_style(),
            'control_panel': ICOConverterStyles.get_control_panel_style(),
            'progress_bar': ICOConverterStyles.get_progress_bar_style(),
            'text_input': ICOConverterStyles.get_text_input_style(),
            'combobox': ICOConverterStyles.get_combobox_style(),
        }
