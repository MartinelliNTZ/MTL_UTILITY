import os
import sys
from pathlib import Path
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from PIL import Image

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QProgressBar, QFileDialog, QListWidget, QListWidgetItem,
    QSplitter, QGroupBox, QMessageBox, QScrollArea
)
from PySide6.QtGui import QPixmap, QImage, QFont
from PySide6.QtCore import Qt, QTimer, QSize

from src.base_plugin import BasePlugin
from src.plugin_ui_helper import PluginUIHelper, PluginContainer, PluginStyleSheet
from styles.ICOConverterStyles import ICOConverterStyles
from utils.ImageUtil import ImageUtil, ImageFormats
from utils.FileExplorer import FileExplorer
from utils.ToolKey import ToolKey
from utils.LogUtils import logger


class ICOConverter(BasePlugin, PluginContainer):
    name = "ICO Converter"
    icon_name = "ico_converter"
    TOOL_KEY = ToolKey.ICO_CONVERTER

    def __init__(self):
        BasePlugin.__init__(self)
        PluginContainer.__init__(self)
        self.preferences = None
        self.current_folder = None
        self.executor = None
        self.file_explorer = None
        logger.info(self.TOOL_KEY, "ICOConverter", "Plugin ICO Converter inicializado")

    def create_widget(self, parent=None) -> QWidget:
        logger.debug(self.TOOL_KEY, "ICOConverter", "Criando widget do conversor ICO")
        
        # Inicializar preferências aqui
        if self.preferences is None:
            from config.preferences import Preferences
            self.preferences = Preferences()
            self.current_folder = self.preferences.get("ico_converter_current_folder", self.preferences.get_base_path())
            from concurrent.futures import ThreadPoolExecutor
            self.executor = ThreadPoolExecutor(max_workers=4)
            # Inicializar FileExplorer com extensões suportadas
            self.file_explorer = FileExplorer(ImageFormats.get_supported_extensions(), recursive=True)
        
        w = QWidget(parent)
        layout = QVBoxLayout(w)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Seção Pasta (compacta)
        self.setup_folder_section(layout)

        # Splitter principal: lista (85%) | controles (15%)
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet(ICOConverterStyles.get_splitter_style())
        layout.addWidget(splitter, 1)

        # Lista de imagens (principal)
        self.setup_image_list(splitter)

        # Painel de controles (lateral)
        self.setup_control_panel(splitter)
        
        splitter.setSizes([850, 150])
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 1)

        # Carregar imagens automaticamente
        QTimer.singleShot(100, self.load_images_from_current_folder)

        logger.info(self.TOOL_KEY, "ICOConverter", "Widget do conversor ICO criado com sucesso")
        return w

    def setup_folder_section(self, layout: QVBoxLayout) -> None:
        """Configura a seção compacta de pasta."""
        folder_layout = QHBoxLayout()
        folder_layout.setSpacing(8)
        folder_layout.setContentsMargins(0, 0, 0, 0)

        # Label da pasta
        self.folder_label = QLabel(self.current_folder)
        self.folder_label.setStyleSheet(ICOConverterStyles.get_folder_label_style())
        folder_layout.addWidget(self.folder_label, 1)

        # Botão Selecionar Arquivo
        btn_select_file = QPushButton("📄 Arquivo")
        btn_select_file.setMinimumHeight(28)
        btn_select_file.setMaximumWidth(90)
        btn_select_file.setStyleSheet(ICOConverterStyles.get_button_style())
        btn_select_file.clicked.connect(self.add_files_dialog)
        folder_layout.addWidget(btn_select_file)

        # Botão Selecionar Pasta
        btn_select_folder = QPushButton("📁 Pasta")
        btn_select_folder.setMinimumHeight(28)
        btn_select_folder.setMaximumWidth(90)
        btn_select_folder.setStyleSheet(ICOConverterStyles.get_button_style())
        btn_select_folder.clicked.connect(self.select_folder)
        folder_layout.addWidget(btn_select_folder)

        # Botão Resetar
        btn_reset = QPushButton("↻ Resetar")
        btn_reset.setMinimumHeight(28)
        btn_reset.setMaximumWidth(90)
        btn_reset.setStyleSheet(ICOConverterStyles.get_button_style())
        btn_reset.clicked.connect(self.reset_to_base_folder)
        folder_layout.addWidget(btn_reset)

        layout.addLayout(folder_layout)

    def setup_image_list(self, splitter: QSplitter) -> None:
        """Configura a lista de imagens (principal)."""
        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(8)

        # Lista com ícones
        self.image_list = QListWidget()
        self.image_list.setIconSize(QSize(100, 80))
        self.image_list.setSpacing(8)
        self.image_list.setStyleSheet(ICOConverterStyles.get_image_list_style())
        list_layout.addWidget(self.image_list, 1)

        # Botões compactos
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(6)
        
        btn_refresh = QPushButton("↻")
        btn_refresh.setMinimumHeight(28)
        btn_refresh.setMaximumWidth(40)
        btn_refresh.setToolTip("Atualizar")
        btn_refresh.setStyleSheet(ICOConverterStyles.get_button_style())
        btn_refresh.clicked.connect(self.load_images_from_current_folder)
        btn_layout.addWidget(btn_refresh)

        btn_clear = QPushButton("✕")
        btn_clear.setMinimumHeight(28)
        btn_clear.setMaximumWidth(40)
        btn_clear.setToolTip("Limpar")
        btn_clear.setStyleSheet(ICOConverterStyles.get_button_style())
        btn_clear.clicked.connect(self.clear_image_list)
        btn_layout.addWidget(btn_clear)

        btn_layout.addStretch()
        list_layout.addLayout(btn_layout)

        list_widget = QWidget()
        list_widget.setLayout(list_layout)
        splitter.addWidget(list_widget)

    def setup_control_panel(self, splitter: QSplitter) -> None:
        """Configura o painel de controle compacto (tema escuro)."""
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        control_layout.setContentsMargins(8, 8, 8, 8)
        control_layout.setSpacing(8)

        control_widget.setStyleSheet(ICOConverterStyles.get_control_panel_style())

        # ===== SEÇÃO: TAMANHOS =====
        size_group = QGroupBox("Tamanhos (px)")
        size_layout = QVBoxLayout(size_group)
        size_layout.setContentsMargins(6, 10, 6, 6)
        size_layout.setSpacing(3)

        self.size_checkboxes = {}
        sizes = [16, 32, 48, 64, 128, 256]
        for size in sizes:
            cb = QCheckBox(f"{size}x{size}")
            checked = self.preferences.get(f"ico_converter_chk_{size}", size in [16, 32, 48, 64, 128])
            cb.setChecked(checked)
            cb.stateChanged.connect(lambda state, s=size: self._on_checkbox_changed(s, state))
            self.size_checkboxes[size] = cb
            size_layout.addWidget(cb)

        control_layout.addWidget(size_group)

        # ===== SEÇÃO: FORMATO =====
        format_group = QGroupBox("Formato")
        format_layout = QVBoxLayout(format_group)
        format_layout.setContentsMargins(6, 10, 6, 6)
        format_layout.setSpacing(3)

        self.keep_original = QCheckBox("Manter")
        self.keep_original.setChecked(self.preferences.get("ico_converter_keep_original", False))
        format_layout.addWidget(self.keep_original)

        self.remove_source = QCheckBox("Remover")
        self.remove_source.setChecked(self.preferences.get("ico_converter_remove_source", False))
        format_layout.addWidget(self.remove_source)

        control_layout.addWidget(format_group)

        # ===== BOTÃO DE CONVERSÃO =====
        self.btn_convert = QPushButton("🔄 Converter")
        self.btn_convert.setMinimumHeight(36)
        self.btn_convert.setFont(QFont("Arial", 10, QFont.Bold))
        self.btn_convert.setStyleSheet(ICOConverterStyles.get_button_style())
        self.btn_convert.clicked.connect(self.start_conversion)
        control_layout.addWidget(self.btn_convert)

        # ===== BARRA DE PROGRESSO =====
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(18)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(ICOConverterStyles.get_progress_bar_style())
        control_layout.addWidget(self.progress_bar)

        control_layout.addStretch()
        splitter.addWidget(control_widget)
        splitter.setSizes([850, 200])

    def _on_checkbox_changed(self, size: int, state) -> None:
        """Callback quando checkboxes mudam."""
        is_checked = state == Qt.Checked
        self.preferences.set(f"ico_converter_chk_{size}", is_checked)
        logger.debug(self.TOOL_KEY, "ICOConverter", f"Tamanho {size}x{size}: {is_checked}")

    def select_folder(self) -> None:
        """Seleciona uma nova pasta."""
        from PySide6.QtWidgets import QApplication
        folder = QFileDialog.getExistingDirectory(
            QApplication.activeWindow(), "Selecionar pasta com imagens", self.current_folder
        )
        if folder:
            self.set_current_folder(folder)
            self.load_images_from_current_folder()
            logger.info(self.TOOL_KEY, "ICOConverter", f"Pasta selecionada: {folder}")

    def reset_to_base_folder(self) -> None:
        """Reseta para a pasta base."""
        base_path = self.preferences.get_base_path()
        self.set_current_folder(base_path)
        self.load_images_from_current_folder()
        logger.info(self.TOOL_KEY, "ICOConverter", f"Resetado para pasta base: {base_path}")

    def set_current_folder(self, folder: str) -> None:
        """Define a pasta atual."""
        self.current_folder = folder
        self.folder_label.setText(f"Pasta atual: {folder}")
        self.preferences.set("ico_converter_current_folder", folder)

    def load_images_from_current_folder(self) -> None:
        """Carrega imagens da pasta atual usando FileExplorer."""
        logger.info(self.TOOL_KEY, "ICOConverter", f"Carregando imagens de: {self.current_folder}")
        self.image_list.clear()

        try:
            images = self.file_explorer.find_files(self.current_folder)
            for img_path in images:
                self.add_image_to_list(img_path)

            logger.info(self.TOOL_KEY, "ICOConverter", f"Carregadas {len(images)} imagens")
        except Exception as e:
            logger.error(self.TOOL_KEY, "ICOConverter", f"Erro ao carregar imagens: {e}")

    def _create_thumbnail(self, file_path: str, size: tuple = (160, 120)) -> QPixmap:
        """
        Gera thumbnail de uma imagem.
        
        Args:
            file_path: Caminho do arquivo de imagem
            size: Tamanho do thumbnail (width, height)
            
        Returns:
            QPixmap com a miniatura ou None se erro
        """
        try:
            img = Image.open(file_path)
            img.thumbnail(size, Image.LANCZOS)
            bio = BytesIO()
            img.convert("RGBA").save(bio, format="PNG")
            qimg = QImage.fromData(bio.getvalue())
            return QPixmap.fromImage(qimg)
        except Exception as e:
            logger.warning(self.TOOL_KEY, "ICOConverter", f"Erro ao gerar thumbnail: {e}")
            return None

    def add_image_to_list(self, path: str) -> None:
        """Adiciona uma imagem à lista."""
        try:
            item = QListWidgetItem(os.path.basename(path))
            item.setToolTip(path)
            item.setData(Qt.UserRole, path)

            # Criar miniatura usando método auxiliar
            pixmap = self._create_thumbnail(path)
            if pixmap:
                item.setIcon(pixmap)

            self.image_list.addItem(item)
        except Exception as e:
            logger.warning(self.TOOL_KEY, "ICOConverter", f"Erro ao adicionar imagem {path}: {e}")

    def clear_image_list(self) -> None:
        """Limpa a lista de imagens."""
        self.image_list.clear()
        logger.info(self.TOOL_KEY, "ICOConverter", "Lista de imagens limpa")

    def add_files_dialog(self) -> None:
        """Abre diálogo para adicionar arquivos individuais."""
        from PySide6.QtWidgets import QApplication
        files, _ = QFileDialog.getOpenFileNames(
            QApplication.activeWindow(),
            "Selecionar imagens",
            self.current_folder,
            "Imagens (*.png *.jpg *.jpeg *.tif *.tiff *.bmp *.gif *.webp);;Todos os arquivos (*)"
        )
        
        if files:
            for file_path in files:
                self.add_image_to_list(file_path)
            logger.info(self.TOOL_KEY, "ICOConverter", f"Adicionados {len(files)} arquivos à lista")

    def get_selected_sizes(self) -> List[int]:
        """Retorna os tamanhos selecionados."""
        sizes = []
        for size, checkbox in self.size_checkboxes.items():
            if checkbox.isChecked():
                sizes.append(size)
        return sizes

    def start_conversion(self) -> None:
        """Inicia a conversão das imagens."""
        from PySide6.QtWidgets import QApplication
        images = []
        for i in range(self.image_list.count()):
            item = self.image_list.item(i)
            images.append(item.data(Qt.UserRole))

        if not images:
            QMessageBox.warning(QApplication.activeWindow(), "Aviso", "Nenhuma imagem na lista.")
            return

        sizes = self.get_selected_sizes()
        if not sizes:
            QMessageBox.warning(QApplication.activeWindow(), "Aviso", "Selecione ao menos um tamanho.")
            return

        # Selecionar pasta de saída
        output_dir = QFileDialog.getExistingDirectory(
            QApplication.activeWindow(), "Selecionar pasta para salvar os ICOs", self.current_folder
        )
        if not output_dir:
            return

        # Iniciar conversão em thread
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(images))
        self.progress_bar.setValue(0)
        self.btn_convert.setEnabled(False)

        # Usar ThreadPoolExecutor para conversão multithread
        futures = []
        for img_path in images:
            future = self.executor.submit(self.convert_single_image, img_path, output_dir, sizes)
            futures.append(future)

        # Monitorar progresso
        self.conversion_futures = futures
        self.check_conversion_progress()

        logger.info(self.TOOL_KEY, "ICOConverter",
                   f"Iniciada conversão de {len(images)} imagens para {output_dir}")

    def convert_single_image(self, img_path: str, output_dir: str, sizes: List[int]) -> Tuple[bool, str]:
        """
        Converte uma única imagem para ICO.
        
        Args:
            img_path: Caminho da imagem
            output_dir: Pasta de saída
            sizes: Tamanhos para o ICO
            
        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            base_name = os.path.splitext(os.path.basename(img_path))[0]
            output_path = os.path.join(output_dir, f"{base_name}.ico")
            
            success = ImageUtil.convert_image_to_ico(img_path, output_path, sizes)
            
            if success:
                return True, f"✓ {os.path.basename(img_path)}"
            else:
                return False, f"✗ Erro ao converter {os.path.basename(img_path)}"
        except Exception as e:
            return False, f"✗ {str(e)}"

    def check_conversion_progress(self) -> None:
        """Verifica o progresso da conversão."""
        completed = 0
        failed = 0
        success_count = 0

        for future in self.conversion_futures:
            if future.done():
                try:
                    success, message = future.result()
                    completed += 1
                    if success:
                        success_count += 1
                    logger.debug(self.TOOL_KEY, "ICOConverter", message)
                except Exception as e:
                    completed += 1
                    failed += 1
                    logger.error(self.TOOL_KEY, "ICOConverter", f"Erro na conversão: {e}")

        self.progress_bar.setValue(completed)

        if completed == len(self.conversion_futures):
            # Conversão completa
            self.progress_bar.setVisible(False)
            self.btn_convert.setEnabled(True)

            if success_count > 0:
                from PySide6.QtWidgets import QApplication
                QMessageBox.information(
                    QApplication.activeWindow(), "Concluído",
                    f"Conversão finalizada!\n{success_count} imagens convertidas com sucesso.\n{failed} falhas."
                )

            logger.info(self.TOOL_KEY, "ICOConverter",
                       f"Conversão concluída: {success_count} sucesso, {failed} falhas")
        else:
            # Continuar monitorando
            QTimer.singleShot(100, self.check_conversion_progress)

    def on_base_path_changed(self, new_path: str) -> None:
        """Atualiza quando a pasta base muda."""
        if self.current_folder == self.preferences.get_base_path():
            # Se estava na pasta base, atualizar
            self.set_current_folder(new_path)
            self.load_images_from_current_folder()
        logger.info(self.TOOL_KEY, "ICOConverter", f"Pasta base alterada para: {new_path}")


def get_plugin():
    return ICOConverter()