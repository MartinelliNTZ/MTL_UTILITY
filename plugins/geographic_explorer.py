"""
Geographic Explorer - Visualizador de arquivos geográficos (SHP, KML, TIFF, ECW, etc)

Plugin para explorar arquivos geográficos com suporte a:
- Formatos vetoriais: SHP, KML, GeoJSON, GPX, etc
- Formatos raster: TIFF, ECW, HDF, JP2, etc
- Seleção dinâmica de formatos com dialog flutuante
- Preferências de formatos personalizadas
- Preview de arquivos selecionados com miniatura de geometrias/raster
"""

import os
from typing import List
from pathlib import Path
from io import BytesIO

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QSplitter, QGroupBox,
    QFileDialog, QDialog, QCheckBox, QScrollArea, QMessageBox,
    QApplication
)
from PySide6.QtGui import QPixmap, QIcon, QImage, QFont, QPainter, QPen, QColor, QBrush
from PySide6.QtCore import Qt, QSize, QTimer, QRect

from src.base_plugin import BasePlugin
from src.plugin_ui_helper import PluginContainer
from src.styles.ImageMergerStyles import ImageMergerStyles
from utils.VectorUtils import VECTOR_FORMATS, get_format_name as get_vector_name
from utils.RasterUtils import RASTER_FORMATS, get_format_name as get_raster_name
from utils.FileExplorer import FileExplorer
from utils.ToolKey import ToolKey
from utils.LogUtils import logger
from utils.GeoMetadataReader import get_file_metadata, format_metadata_text
from config.preferences import Preferences


class GeoPreviewCanvas(QWidget):
    """Canvas para visualizar preview de arquivos geográficos."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.current_file = None
        self.setStyleSheet("""
            GeoPreviewCanvas {
                background-color: #1e1e1e;
                border: 1px solid #3e3e3e;
                border-radius: 3px;
            }
        """)
    
    def set_file(self, file_path: str) -> None:
        """Define o arquivo a visualizar."""
        self.current_file = file_path
        self.update()
    
    def paintEvent(self, event):
        """Desenha o preview do arquivo."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fundo
        painter.fillRect(self.rect(), QColor("#1e1e1e"))
        
        if not self.current_file:
            # Placeholder
            painter.setPen(QPen(QColor("#666666"), 1))
            painter.drawText(
                self.rect(),
                Qt.AlignCenter,
                "📂 Selecione um arquivo\npara visualizar preview"
            )
            return
        
        filename = os.path.basename(self.current_file)
        ext = os.path.splitext(filename)[1].lower()
        
        # Border
        painter.setPen(QPen(QColor("#3e3e3e"), 1))
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
        
        # Info header
        painter.setPen(QPen(QColor("#9CDCFE"), 1))
        header_height = 40
        painter.drawLine(0, header_height, self.width(), header_height)
        
        # Filename
        painter.setPen(QPen(QColor("#9CDCFE")))
        painter.setFont(QFont("Courier", 9, QFont.Bold))
        painter.drawText(10, 10, self.width() - 20, 30, Qt.AlignLeft, f"📄 {filename}")
        
        # Preview area
        preview_rect = QRect(0, header_height, self.width(), self.height() - header_height)
        
        if ext in VECTOR_FORMATS:
            self._draw_vector_preview(painter, preview_rect, self.current_file, ext)
        elif ext in RASTER_FORMATS:
            self._draw_raster_preview(painter, preview_rect, self.current_file, ext)
        else:
            painter.setPen(QPen(QColor("#666666")))
            painter.drawText(preview_rect, Qt.AlignCenter, "Formato não reconhecido")
    
    def _draw_vector_preview(self, painter: QPainter, rect: QRect, filepath: str, ext: str) -> None:
        """Desenha preview para arquivo vetorial."""
        painter.setPen(QPen(QColor("#4EC9B0"), 2))
        painter.setBrush(QBrush(QColor("#4EC9B0"), Qt.NoBrush))
        
        # Desenha alguns elementos de exemplo
        center_x = rect.x() + rect.width() // 2
        center_y = rect.y() + rect.height() // 2
        
        # Simula diferentes tipos de geometrias
        if "point" in filepath.lower() or ext == ".gpx":
            # Desenha pontos
            for i in range(5):
                x = center_x - 50 + i * 25
                y = center_y - 20 + (i % 2) * 40
                painter.drawEllipse(x - 3, y - 3, 6, 6)
        
        elif "line" in filepath.lower():
            # Desenha linhas
            painter.setPen(QPen(QColor("#9CDCFE"), 2))
            points = [
                (center_x - 60, center_y - 30),
                (center_x - 30, center_y + 20),
                (center_x + 30, center_y - 20),
                (center_x + 60, center_y + 30),
            ]
            for i in range(len(points) - 1):
                painter.drawLine(int(points[i][0]), int(points[i][1]), 
                               int(points[i+1][0]), int(points[i+1][1]))
        
        else:
            # Padrão: desenha um polígono genérico
            painter.setPen(QPen(QColor("#4EC9B0"), 2))
            painter.setBrush(QBrush(QColor("#4EC9B0"), Qt.Dense6Pattern))
            polygon_points = [
                (center_x - 60, center_y - 40),
                (center_x + 60, center_y - 40),
                (center_x + 70, center_y + 40),
                (center_x - 70, center_y + 40),
                (center_x - 60, center_y - 40),
            ]
            for i in range(len(polygon_points) - 1):
                painter.drawLine(int(polygon_points[i][0]), int(polygon_points[i][1]),
                               int(polygon_points[i+1][0]), int(polygon_points[i+1][1]))
        
        # Info
        painter.setPen(QPen(QColor("#9CDCFE")))
        painter.setFont(QFont("Courier", 8))
        info = get_vector_name(ext)
        painter.drawText(rect.adjusted(10, 10, -10, -10), Qt.AlignBottom | Qt.AlignLeft, 
                        f"Vetor: {info}\n🔍 Clique para abrir com aplicativo SIG")
    
    def _draw_raster_preview(self, painter: QPainter, rect: QRect, filepath: str, ext: str) -> None:
        """Desenha preview para arquivo raster."""
        try:
            from PIL import Image
            
            # Tentar carregar imagem
            img = Image.open(filepath)
            
            # Redimensionar para caber na area
            max_size = min(rect.width() - 20, rect.height() - 40)
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Converter para QImage
            bio = BytesIO()
            img.save(bio, format="PNG")
            qimg = QImage.fromData(bio.getvalue())
            
            # Desenhar imagem centralizada
            pixmap = QPixmap.fromImage(qimg)
            x = rect.x() + (rect.width() - pixmap.width()) // 2
            y = rect.y() + (rect.height() - pixmap.height()) // 2 + 10
            painter.drawPixmap(x, y, pixmap)
            
            # Info
            painter.setPen(QPen(QColor("#9CDCFE")))
            painter.setFont(QFont("Courier", 8))
            info = get_raster_name(ext)
            painter.drawText(rect.adjusted(10, 10, -10, -10), Qt.AlignBottom | Qt.AlignLeft,
                            f"Raster: {info}\nTamanho: {img.size[0]}x{img.size[1]} px")
        
        except Exception as e:
            # Fallback se não conseguir carregar
            painter.setPen(QPen(QColor("#9CDCFE"), 2))
            painter.drawRect(rect.adjusted(30, 30, -30, -30))
            painter.setPen(QPen(QColor("#9CDCFE")))
            painter.setFont(QFont("Courier", 8))
            info = get_raster_name(ext)
            painter.drawText(rect.adjusted(10, 10, -10, -10), Qt.AlignCenter,
                            f"Raster: {info}\n(Visualização disponível apenas\ncom GDAL/Rasterio instalado)")


class FormatSelectorDialog(QDialog):
    """Dialog flutuante para selecionar formatos de arquivo a visualizar."""
    
    def __init__(self, parent, selected_formats: List[str]):
        super().__init__(parent)
        self.setWindowTitle("Selecionar Formatos Geográficos")
        self.setModal(True)
        self.resize(500, 600)
        self.selected_formats = selected_formats.copy()
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura a interface do dialog."""
        layout = QVBoxLayout(self)
        
        # Scroll area para não poluir a tela
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Container para os checkboxes
        container = QWidget()
        container_layout = QVBoxLayout(container)
        
        self.checkboxes = {}
        
        # Seção Vetorial
        vector_label = QLabel("Formatos Vetoriais")
        vector_label.setStyleSheet("font-weight: bold; color: #4EC9B0; font-size: 11pt;")
        container_layout.addWidget(vector_label)
        
        for fmt in VECTOR_FORMATS:
            cb = QCheckBox(f"{fmt.upper()} - {get_vector_name(fmt)}")
            cb.setChecked(fmt in self.selected_formats)
            self.checkboxes[fmt] = cb
            container_layout.addWidget(cb)
        
        container_layout.addSpacing(20)
        
        # Seção Raster
        raster_label = QLabel("Formatos Raster")
        raster_label.setStyleSheet("font-weight: bold; color: #9CDCFE; font-size: 11pt;")
        container_layout.addWidget(raster_label)
        
        for fmt in RASTER_FORMATS:
            cb = QCheckBox(f"{fmt.upper()} - {get_raster_name(fmt)}")
            cb.setChecked(fmt in self.selected_formats)
            self.checkboxes[fmt] = cb
            container_layout.addWidget(cb)
        
        container_layout.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        # Botões
        btn_layout = QHBoxLayout()
        
        btn_ok = QPushButton("✓ Aplicar")
        btn_ok.clicked.connect(self.accept)
        btn_layout.addWidget(btn_ok)
        
        btn_cancel = QPushButton("✕ Cancelar")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)
        
        layout.addLayout(btn_layout)
    
    def get_selected_formats(self) -> List[str]:
        """Retorna lista de formatos selecionados."""
        return [fmt for fmt, cb in self.checkboxes.items() if cb.isChecked()]


class GeographicExplorer(BasePlugin, PluginContainer):
    """Plugin para visualizar arquivos geográficos."""
    
    name = "Geographic Explorer"
    icon_name = "plugins"
    TOOL_KEY = ToolKey.PLUGIN_MANAGER
    
    def __init__(self):
        BasePlugin.__init__(self)
        PluginContainer.__init__(self)
        self.preferences = None
        self.current_folder = None
        self.file_explorer = None
        self.selected_formats = []
        logger.info(self.TOOL_KEY, "GeographicExplorer", "Plugin Geographic Explorer inicializado")
    
    def create_widget(self, parent=None) -> QWidget:
        """Cria o widget principal do plugin."""
        logger.debug(self.TOOL_KEY, "GeographicExplorer", "Criando widget")
        
        # Inicializar preferências
        if self.preferences is None:
            self.preferences = Preferences()
        
        self.current_folder = self.preferences.get_base_path()
        
        # Carregar formatos salvos ou usar defaults
        all_formats = VECTOR_FORMATS + RASTER_FORMATS
        self.selected_formats = self.preferences.get(
            "geo_explorer_formats",
            VECTOR_FORMATS[:3] + RASTER_FORMATS[:3]  # Defaults: primeiros 3 de cada
        )
        
        self.file_explorer = FileExplorer(
            extensions=self.selected_formats,
            recursive=True
        )
        
        w = QWidget(parent)
        layout = QVBoxLayout(w)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        
        # Seção pasta
        self.setup_folder_section(layout)
        
        # Splitter principal
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet(ImageMergerStyles.get_splitter_style())
        layout.addWidget(splitter, 1)
        
        # Lista de arquivos (esquerda - 80%)
        self.setup_file_list(splitter)
        
        # Painel lateral (direita - 20%) - reservado para funcionalidades futuras
        self.setup_future_panel(splitter)
        
        splitter.setSizes([800, 200])
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 1)
        
        # Carregar arquivos automaticamente
        QTimer.singleShot(100, self.load_files_from_folder)
        
        logger.info(self.TOOL_KEY, "GeographicExplorer", "Widget criado com sucesso")
        return w
    
    def setup_folder_section(self, layout: QVBoxLayout) -> None:
        """Configura a seção de seleção de pasta e formatos."""
        folder_layout = QHBoxLayout()
        folder_layout.setSpacing(8)
        folder_layout.setContentsMargins(0, 0, 0, 0)
        
        self.folder_label = QLabel(self.current_folder)
        self.folder_label.setStyleSheet(ImageMergerStyles.get_folder_label_style())
        folder_layout.addWidget(self.folder_label, 1)
        
        # Botão para escolher formatos (dialog flutuante)
        btn_formats = QPushButton("🔍 Formatos")
        btn_formats.setMinimumHeight(28)
        btn_formats.setMaximumWidth(90)
        btn_formats.setStyleSheet(ImageMergerStyles.get_button_style())
        btn_formats.clicked.connect(self.show_format_selector)
        folder_layout.addWidget(btn_formats)
        
        btn_select_folder = QPushButton("📁 Pasta")
        btn_select_folder.setMinimumHeight(28)
        btn_select_folder.setMaximumWidth(90)
        btn_select_folder.setStyleSheet(ImageMergerStyles.get_button_style())
        btn_select_folder.clicked.connect(self.select_folder)
        folder_layout.addWidget(btn_select_folder)
        
        btn_reset = QPushButton("↻ Resetar")
        btn_reset.setMinimumHeight(28)
        btn_reset.setMaximumWidth(90)
        btn_reset.setStyleSheet(ImageMergerStyles.get_button_style())
        btn_reset.clicked.connect(self.reset_to_base_folder)
        folder_layout.addWidget(btn_reset)
        
        layout.addLayout(folder_layout)
    
    def setup_file_list(self, splitter: QSplitter) -> None:
        """Configura a lista de arquivos geográficos (esquerda)."""
        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(6)
        
        # Label melhorado com informações
        info_layout = QHBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(8)
        
        label_title = QLabel("Arquivos Encontrados")
        label_title.setStyleSheet("color: #4EC9B0; font-weight: bold; font-size: 10pt;")
        info_layout.addWidget(label_title)
        
        self.label_count = QLabel("(0)")
        self.label_count.setStyleSheet("color: #9CDCFE; font-size: 10pt;")
        info_layout.addWidget(self.label_count)
        
        info_layout.addStretch()
        list_layout.addLayout(info_layout)
        
        self.file_list = QListWidget()
        self.file_list.setIconSize(QSize(60, 48))  # Reduzido para 60% do tamanho original
        self.file_list.setSpacing(4)
        self.file_list.setStyleSheet(ImageMergerStyles.get_image_list_style())
        self.file_list.itemSelectionChanged.connect(self._on_file_selected)
        list_layout.addWidget(self.file_list, 1)
        
        # Botões compactos
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(6)
        
        btn_refresh = QPushButton("↻")
        btn_refresh.setMinimumHeight(28)
        btn_refresh.setMaximumWidth(40)
        btn_refresh.setToolTip("Atualizar")
        btn_refresh.setStyleSheet(ImageMergerStyles.get_button_style())
        btn_refresh.clicked.connect(self.load_files_from_folder)
        btn_layout.addWidget(btn_refresh)
        
        btn_clear = QPushButton("✕")
        btn_clear.setMinimumHeight(28)
        btn_clear.setMaximumWidth(40)
        btn_clear.setToolTip("Limpar")
        btn_clear.setStyleSheet(ImageMergerStyles.get_button_style())
        btn_clear.clicked.connect(self.clear_file_list)
        btn_layout.addWidget(btn_clear)
        
        btn_layout.addStretch()
        list_layout.addLayout(btn_layout)
        
        list_widget = QWidget()
        list_widget.setLayout(list_layout)
        splitter.addWidget(list_widget)
    
    def setup_future_panel(self, splitter: QSplitter) -> None:
        """Configura o painel lateral (direita) com preview e metadados."""
        future_widget = QWidget()
        future_layout = QVBoxLayout(future_widget)
        future_layout.setContentsMargins(8, 8, 8, 8)
        future_layout.setSpacing(8)
        
        future_widget.setStyleSheet(ImageMergerStyles.get_control_panel_style())
        
        # Canvas de preview
        preview_group = QGroupBox("📍 Preview do Arquivo")
        preview_group_layout = QVBoxLayout(preview_group)
        preview_group_layout.setContentsMargins(6, 10, 6, 6)
        preview_group_layout.setSpacing(0)
        
        self.preview_canvas = GeoPreviewCanvas(parent=None)
        preview_group_layout.addWidget(self.preview_canvas)
        
        future_layout.addWidget(preview_group, 1)
        
        # Painel de metadados
        metadata_group = QGroupBox("ℹ️ Metadados do Arquivo")
        metadata_group_layout = QVBoxLayout(metadata_group)
        metadata_group_layout.setContentsMargins(6, 10, 6, 6)
        
        self.metadata_label = QLabel("Selecione um arquivo para ver metadados")
        self.metadata_label.setStyleSheet("""
            color: #9CDCFE;
            font-family: 'Courier New';
            font-size: 8pt;
            background-color: #0d1117;
            padding: 6px;
            border-radius: 3px;
        """)
        self.metadata_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.metadata_label.setWordWrap(True)
        metadata_group_layout.addWidget(self.metadata_label)
        
        future_layout.addWidget(metadata_group, 1)
        
        splitter.addWidget(future_widget)
    
    def show_format_selector(self) -> None:
        """Abre dialog flutuante para escolher formatos."""
        dialog = FormatSelectorDialog(QApplication.activeWindow(), self.selected_formats)
        
        if dialog.exec():
            self.selected_formats = dialog.get_selected_formats()
            
            if not self.selected_formats:
                QMessageBox.warning(
                    QApplication.activeWindow(),
                    "Aviso",
                    "Selecione pelo menos um formato!"
                )
                return
            
            # Salvar preferência
            self.preferences.set("geo_explorer_formats", self.selected_formats)
            
            # Atualizar file explorer
            self.file_explorer = FileExplorer(
                extensions=self.selected_formats,
                recursive=True
            )
            
            # Recarregar lista
            self.load_files_from_folder()
            
            logger.info(
                self.TOOL_KEY, "GeographicExplorer",
                f"Formatos selecionados: {', '.join(self.selected_formats)}"
            )
    
    def select_folder(self) -> None:
        """Seleciona nova pasta."""
        folder = QFileDialog.getExistingDirectory(
            QApplication.activeWindow(),
            "Selecionar pasta com arquivos geográficos",
            self.current_folder
        )
        if folder:
            self.set_current_folder(folder)
            self.load_files_from_folder()
            logger.info(self.TOOL_KEY, "GeographicExplorer", f"Pasta selecionada: {folder}")
    
    def reset_to_base_folder(self) -> None:
        """Reseta para a pasta base."""
        base_path = self.preferences.get_base_path()
        self.set_current_folder(base_path)
        self.load_files_from_folder()
        logger.info(self.TOOL_KEY, "GeographicExplorer", f"Resetado para pasta base: {base_path}")
    
    def set_current_folder(self, folder: str) -> None:
        """Define a pasta atual."""
        if os.path.isdir(folder):
            self.current_folder = folder
            self.folder_label.setText(folder)
            logger.debug(self.TOOL_KEY, "GeographicExplorer", f"Pasta atual: {folder}")
    
    def load_files_from_folder(self) -> None:
        """Carrega arquivos da pasta atual."""
        self.file_list.clear()
        
        if not self.current_folder or not os.path.isdir(self.current_folder):
            self.label_count.setText("Pasta inválida")
            return
        
        if not self.selected_formats:
            self.label_count.setText("Nenhum formato selecionado")
            return
        
        try:
            files = self.file_explorer.find_files(self.current_folder)
            
            for file_path in sorted(files):
                self.add_file_to_list(file_path)
            
            count = self.file_list.count()
            self.label_count.setText(f"({count})")
            
            logger.info(
                self.TOOL_KEY, "GeographicExplorer",
                f"Carregados {count} arquivos de {self.current_folder}"
            )
        except Exception as e:
            logger.error(self.TOOL_KEY, "GeographicExplorer", f"Erro ao carregar arquivos: {e}")
            self.label_count.setText("(erro)")
    
    def _on_file_selected(self) -> None:
        """Chamado quando um arquivo é selecionado."""
        try:
            selected_items = self.file_list.selectedItems()
            if selected_items:
                file_path = selected_items[0].data(Qt.UserRole)
                self.preview_canvas.set_file(file_path)
                
                # Carregar e exibir metadados
                try:
                    metadata = get_file_metadata(file_path)
                    if metadata:
                        metadata_text = format_metadata_text(metadata)
                        self.metadata_label.setText(metadata_text)
                        logger.debug(self.TOOL_KEY, "GeographicExplorer", f"Metadados carregados: {file_path}")
                    else:
                        self.metadata_label.setText("❌ Formato não suportado")
                except Exception as meta_error:
                    error_msg = f"❌ Erro ao ler metadados:\n{str(meta_error)}"
                    self.metadata_label.setText(error_msg)
                    logger.error(self.TOOL_KEY, "GeographicExplorer", f"Erro ao ler metadados de {file_path}: {meta_error}")
        except Exception as e:
            logger.error(self.TOOL_KEY, "GeographicExplorer", f"Erro ao selecionar arquivo: {e}")
            self.metadata_label.setText(f"❌ Erro: {str(e)}")

    
    def add_file_to_list(self, path: str) -> None:
        """Adiciona um arquivo à lista."""
        try:
            filename = os.path.basename(path)
            ext = os.path.splitext(filename)[1].lower()
            
            # Determinar tipo
            if ext in VECTOR_FORMATS:
                tipo = f"Vetor - {get_vector_name(ext)}"
                icon_type = "📍"
            elif ext in RASTER_FORMATS:
                tipo = f"Raster - {get_raster_name(ext)}"
                icon_type = "🗺️"
            else:
                tipo = "Desconhecido"
                icon_type = "❓"
            
            self.preview_canvas.set_file(path)
            item = QListWidgetItem(f"{icon_type} {filename}")
            item.setToolTip(f"{tipo}\n{path}")
            item.setData(Qt.UserRole, path)
            
            # Tentar criar ícone de tipo
            item.setSizeHint(QSize(100, 80))
            
            self.file_list.addItem(item)
        except Exception as e:
            logger.warning(self.TOOL_KEY, "GeographicExplorer", f"Erro ao adicionar {path}: {e}")
    
    def clear_file_list(self) -> None:
        """Limpa a lista de arquivos."""
        self.file_list.clear()
        self.label_count.setText("Lista limpa")
        logger.debug(self.TOOL_KEY, "GeographicExplorer", "Lista limpa")
    
    def on_base_path_changed(self, new_path: str) -> None:
        """Hook chamado quando pasta base muda."""
        if not self.preferences:
            return  # Ainda não foi inicializado
        
        self.set_current_folder(new_path)
        self.load_files_from_folder()


def get_plugin():
    """Função obrigatória para carregamento do plugin."""
    return GeographicExplorer()
