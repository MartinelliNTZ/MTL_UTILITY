"""
Image Merger Plugin - Mescla múltiplas imagens em PDF ou PNG redimensionado.

Plugin para mesclar imagens em PDF, com suporte a exportação em PNG
redimensionado proporcionalmente. Inclui:
- Seleção de pasta ou arquivo individual
- Drag & drop para reordenar imagens
- Pré-visualização de imagem selecionada
- Configurações de largura máxima
- Opções de saída (PDF e/ou PNG)
- Barra de progresso com logging estruturado
"""

import os
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from pathlib import Path
from PIL import Image

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QProgressBar, QFileDialog, QListWidget, QListWidgetItem,
    QSplitter, QGroupBox, QMessageBox, QSpinBox, QApplication
)
from PySide6.QtGui import QPixmap, QImage, QFont
from PySide6.QtCore import Qt, QTimer, QSize

from src.base_plugin import BasePlugin
from src.plugin_ui_helper import PluginUIHelper, PluginContainer, PluginStyleSheet
from src.styles.ImageMergerStyles import ImageMergerStyles
from utils.PDFUtil import PDFUtil
from utils.FileExplorer import FileExplorer
from utils.ToolKey import ToolKey
from utils.LogUtils import logger
from config.preferences import Preferences


class ReorderableListWidget(QListWidget):
    """QListWidget customizado com suporte a drag & drop para reordenação."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QListWidget.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setIconSize(QSize(120, 80))

    def dragEnterEvent(self, event):
        """Aceita drag de URLs (arquivos)."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        """Move aceita drag de URLs."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        """Drop: se URLs, adiciona arquivos; senão reordena."""
        if event.mimeData().hasUrls():
            paths = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    paths.append(url.toLocalFile())
            self.add_files(paths)
            event.acceptProposedAction()
        else:
            super().dropEvent(event)

    def add_files(self, paths: List[str]) -> None:
        """Adiciona arquivos ou pasta à lista (filtra imagens)."""
        exts = {'.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp', '.gif', '.webp'}
        for p in paths:
            if os.path.isdir(p):
                # Adicionar todos os arquivos da pasta
                for fname in sorted(os.listdir(p)):
                    fp = os.path.join(p, fname)
                    if os.path.isfile(fp) and os.path.splitext(fname)[1].lower() in exts:
                        self._add_item(fp)
            else:
                if os.path.isfile(p) and os.path.splitext(p)[1].lower() in exts:
                    self._add_item(p)

    def _add_item(self, path: str) -> None:
        """Adiciona um item à lista (evita duplicatas)."""
        # Evitar duplicatas
        for i in range(self.count()):
            if self.item(i).data(Qt.UserRole) == path:
                return

        item = QListWidgetItem(os.path.basename(path))
        item.setToolTip(path)
        item.setData(Qt.UserRole, path)

        # Tentar gerar thumbnail
        try:
            img = Image.open(path)
            img.thumbnail((120, 80), Image.LANCZOS)
            bio = BytesIO()
            img.convert("RGBA").save(bio, format="PNG")
            qimg = QImage.fromData(bio.getvalue())
            pix = QPixmap.fromImage(qimg)
            item.setIcon(QPixmap(pix))
        except Exception:
            pass  # Se falhar, apenas não mostra ícone

        self.addItem(item)

    def get_ordered_paths(self) -> List[str]:
        """Retorna lista ordenada de caminhos."""
        return [self.item(i).data(Qt.UserRole) for i in range(self.count())]


class ImageMerger(BasePlugin, PluginContainer):
    """Plugin para mesclar imagens em PDF ou PNG redimensionado."""

    name = "Image Merger"
    icon_name = "image_merger"
    TOOL_KEY = ToolKey.IMAGE_MERGER

    def __init__(self):
        BasePlugin.__init__(self)
        PluginContainer.__init__(self)
        self.preferences = None
        self.current_folder = None
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.file_explorer = None
        self.futures = {}
        logger.info(self.TOOL_KEY, "ImageMerger", "Plugin Image Merger inicializado")

    def create_widget(self, parent=None) -> QWidget:
        """Cria o widget principal do plugin."""
        logger.debug(self.TOOL_KEY, "ImageMerger", "Criando widget")

        # Inicializar preferências
        if self.preferences is None:
            self.preferences = Preferences()

        self.current_folder = self.preferences.get_base_path()
        self.file_explorer = FileExplorer(
            extensions=['.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp', '.gif', '.webp'],
            recursive=False
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

        # Lista de imagens (esquerda)
        self.setup_image_list(splitter)

        # Painel de controle (direita)
        self.setup_control_panel(splitter)

        splitter.setSizes([850, 150])
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 1)

        # Carregar imagens automaticamente
        QTimer.singleShot(100, self.load_images_from_current_folder)

        logger.info(self.TOOL_KEY, "ImageMerger", "Widget criado com sucesso")
        return w

    def setup_folder_section(self, layout: QVBoxLayout) -> None:
        """Configura a seção de seleção de pasta."""
        folder_layout = QHBoxLayout()
        folder_layout.setSpacing(8)
        folder_layout.setContentsMargins(0, 0, 0, 0)

        self.folder_label = QLabel(self.current_folder)
        self.folder_label.setStyleSheet(ImageMergerStyles.get_folder_label_style())
        folder_layout.addWidget(self.folder_label, 1)

        btn_select_file = QPushButton("📄 Arquivo")
        btn_select_file.setMinimumHeight(28)
        btn_select_file.setMaximumWidth(90)
        btn_select_file.setStyleSheet(ImageMergerStyles.get_button_style())
        btn_select_file.clicked.connect(self.add_files_dialog)
        folder_layout.addWidget(btn_select_file)

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

    def setup_image_list(self, splitter: QSplitter) -> None:
        """Configura a lista de imagens (esquerda)."""
        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(8)

        self.image_list = ReorderableListWidget()
        self.image_list.setStyleSheet(ImageMergerStyles.get_image_list_style())
        list_layout.addWidget(self.image_list, 1)

        # Botões compactos
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(6)

        btn_refresh = QPushButton("↻")
        btn_refresh.setMinimumHeight(28)
        btn_refresh.setMaximumWidth(40)
        btn_refresh.setToolTip("Atualizar")
        btn_refresh.setStyleSheet(ImageMergerStyles.get_button_style())
        btn_refresh.clicked.connect(self.load_images_from_current_folder)
        btn_layout.addWidget(btn_refresh)

        btn_clear = QPushButton("✕")
        btn_clear.setMinimumHeight(28)
        btn_clear.setMaximumWidth(40)
        btn_clear.setToolTip("Limpar")
        btn_clear.setStyleSheet(ImageMergerStyles.get_button_style())
        btn_clear.clicked.connect(self.clear_image_list)
        btn_layout.addWidget(btn_clear)

        btn_layout.addStretch()
        list_layout.addLayout(btn_layout)

        list_widget = QWidget()
        list_widget.setLayout(list_layout)
        splitter.addWidget(list_widget)

    def setup_control_panel(self, splitter: QSplitter) -> None:
        """Configura o painel de controle (direita)."""
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        control_layout.setContentsMargins(8, 8, 8, 8)
        control_layout.setSpacing(8)
        control_widget.setStyleSheet(ImageMergerStyles.get_control_panel_style())

        # Seção: Configurações
        config_group = QGroupBox("Configurações")
        config_layout = QVBoxLayout(config_group)
        config_layout.setContentsMargins(6, 10, 6, 6)
        config_layout.setSpacing(6)

        # Max width
        width_layout = QHBoxLayout()
        width_label = QLabel("Max largura (px):")
        width_label.setStyleSheet(ImageMergerStyles.get_label_style())
        self.spin_width = QSpinBox()
        self.spin_width.setRange(200, 10000)
        self.spin_width.setValue(
            self.preferences.get("merger_max_width", 3000)
        )
        self.spin_width.setStyleSheet(ImageMergerStyles.get_spinbox_style())
        self.spin_width.valueChanged.connect(
            lambda v: self.preferences.set("merger_max_width", v)
        )
        width_layout.addWidget(width_label)
        width_layout.addWidget(self.spin_width)
        config_layout.addLayout(width_layout)

        control_layout.addWidget(config_group)

        # Seção: Saída
        output_group = QGroupBox("Formato de Saída")
        output_layout = QVBoxLayout(output_group)
        output_layout.setContentsMargins(6, 10, 6, 6)
        output_layout.setSpacing(3)

        self.chk_pdf = QCheckBox("Gerar PDF (único arquivo)")
        self.chk_pdf.setChecked(self.preferences.get("merger_export_pdf", True))
        self.chk_pdf.stateChanged.connect(
            lambda state: self.preferences.set(
                "merger_export_pdf", state == Qt.Checked
            )
        )
        output_layout.addWidget(self.chk_pdf)

        self.chk_png = QCheckBox("Exportar PNGs redimensionados")
        self.chk_png.setChecked(self.preferences.get("merger_export_png", False))
        self.chk_png.stateChanged.connect(
            lambda state: self.preferences.set(
                "merger_export_png", state == Qt.Checked
            )
        )
        output_layout.addWidget(self.chk_png)

        control_layout.addWidget(output_group)

        # Botão mesclar
        self.btn_merge = QPushButton("▶️ Mesclar")
        self.btn_merge.setMinimumHeight(36)
        self.btn_merge.setFont(QFont("Arial", 10, QFont.Bold))
        self.btn_merge.setStyleSheet(ImageMergerStyles.get_button_style())
        self.btn_merge.clicked.connect(self.start_merge)
        control_layout.addWidget(self.btn_merge)

        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(18)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(ImageMergerStyles.get_progress_bar_style())
        control_layout.addWidget(self.progress_bar)

        control_layout.addStretch()
        splitter.addWidget(control_widget)
        splitter.setSizes([850, 200])

    def select_folder(self) -> None:
        """Seleciona nova pasta."""
        folder = QFileDialog.getExistingDirectory(
            QApplication.activeWindow(),
            "Selecionar pasta com imagens",
            self.current_folder
        )
        if folder:
            self.set_current_folder(folder)
            self.load_images_from_current_folder()
            logger.info(self.TOOL_KEY, "ImageMerger", f"Pasta selecionada: {folder}")

    def reset_to_base_folder(self) -> None:
        """Reseta para a pasta base."""
        base_path = self.preferences.get_base_path()
        self.set_current_folder(base_path)
        self.load_images_from_current_folder()
        logger.info(self.TOOL_KEY, "ImageMerger", f"Resetado para pasta base: {base_path}")

    def set_current_folder(self, folder: str) -> None:
        """Define a pasta atual."""
        if os.path.isdir(folder):
            self.current_folder = folder
            self.folder_label.setText(folder)
            self.preferences.set_base_path(folder)
            logger.debug(self.TOOL_KEY, "ImageMerger", f"Pasta atual: {folder}")

    def load_images_from_current_folder(self) -> None:
        """Carrega imagens da pasta atual."""
        self.image_list.clear()
        if self.current_folder and os.path.isdir(self.current_folder):
            files = self.file_explorer.find_files(self.current_folder)
            for file_path in files:
                self.image_list.add_files([file_path])
            logger.info(
                self.TOOL_KEY, "ImageMerger",
                f"Carregadas {self.image_list.count()} imagens de {self.current_folder}"
            )

    def add_files_dialog(self) -> None:
        """Abre dialog para selecionar arquivos."""
        files, _ = QFileDialog.getOpenFileNames(
            QApplication.activeWindow(),
            "Selecione imagens",
            self.current_folder,
            "Imagens (*.png *.jpg *.jpeg *.tif *.tiff *.bmp *.gif *.webp)"
        )
        if files:
            self.image_list.add_files(files)
            logger.info(self.TOOL_KEY, "ImageMerger", f"Adicionados {len(files)} arquivos")

    def clear_image_list(self) -> None:
        """Limpa a lista de imagens."""
        self.image_list.clear()
        logger.debug(self.TOOL_KEY, "ImageMerger", "Lista limpa")

    def start_merge(self) -> None:
        """Inicia o processo de mesclagem."""
        paths = self.image_list.get_ordered_paths()

        if not paths:
            QMessageBox.warning(QApplication.activeWindow(), "Aviso", "Nenhuma imagem na lista.")
            logger.warning(self.TOOL_KEY, "ImageMerger", "Tentativa de mesclar sem imagens")
            return

        export_pdf = self.chk_pdf.isChecked()
        export_png = self.chk_png.isChecked()

        if not (export_pdf or export_png):
            QMessageBox.warning(
                QApplication.activeWindow(), "Aviso",
                "Escolha pelo menos um formato de saída (PDF e/ou PNG)."
            )
            logger.warning(self.TOOL_KEY, "ImageMerger", "Nenhum formato de saída selecionado")
            return

        max_width = self.spin_width.value()

        # Escolher local de saída
        output_dir = QFileDialog.getExistingDirectory(
            QApplication.activeWindow(),
            "Escolha pasta para salvar resultado:",
            self.current_folder
        )

        if not output_dir:
            logger.debug(self.TOOL_KEY, "ImageMerger", "Operação cancelada pelo usuário")
            return

        logger.info(
            self.TOOL_KEY, "ImageMerger",
            f"Iniciando mesclagem: {len(paths)} imagens, PDF={export_pdf}, PNG={export_png}"
        )

        # Desabilitar botão e mostrar progresso
        self.btn_merge.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        # Submeter trabalho ao executor
        future = self.executor.submit(
            self._merge_images_worker,
            paths, output_dir, max_width, export_pdf, export_png
        )
        self.futures[future] = (len(paths), output_dir)

        # Monitorar progresso
        QTimer.singleShot(100, self.check_merge_progress)

    def _merge_images_worker(
        self,
        paths: List[str],
        output_dir: str,
        max_width: int,
        export_pdf: bool,
        export_png: bool
    ) -> Tuple[bool, str]:
        """Worker que executa a mesclagem (roda em thread)."""
        try:
            pdf_filename = "documento.pdf"
            success, message = PDFUtil.process_images_batch(
                paths, output_dir, max_width,
                export_pdf=export_pdf,
                export_png=export_png,
                pdf_filename=pdf_filename
            )
            return success, message
        except Exception as e:
            logger.error(self.TOOL_KEY, "ImageMerger", f"Erro no worker: {e}")
            return False, f"✗ Erro: {str(e)}"

    def check_merge_progress(self) -> None:
        """Monitora o progresso da mesclagem."""
        completed_futures = []

        for future in self.futures:
            if future.done():
                completed_futures.append(future)
                try:
                    success, message = future.result()
                    num_images, output_dir = self.futures[future]

                    if success:
                        logger.info(self.TOOL_KEY, "ImageMerger", f"Mesclagem concluída: {message}")
                        msg_box = QMessageBox(QApplication.activeWindow())
                        msg_box.setWindowTitle("Concluído")
                        msg_box.setText(f"{message}\n\nSalvo em: {output_dir}")
                        msg_box.setIcon(QMessageBox.Information)
                        open_btn = msg_box.addButton("Abrir Pasta", QMessageBox.ActionRole)
                        msg_box.addButton("OK", QMessageBox.AcceptRole)
                        msg_box.exec()
                        if msg_box.clickedButton() == open_btn:
                            import subprocess
                            import os
                            subprocess.Popen(f'explorer /select,"{output_dir}"')
                        self.progress_bar.setValue(100)
                    else:
                        logger.error(self.TOOL_KEY, "ImageMerger", f"Erro na mesclagem: {message}")
                        QMessageBox.critical(
                            QApplication.activeWindow(),
                            "Erro",
                            f"Erro na mesclagem:\n{message}"
                        )

                except Exception as e:
                    logger.error(self.TOOL_KEY, "ImageMerger", f"Erro ao recuperar resultado: {e}")
                    QMessageBox.critical(
                        QApplication.activeWindow(),
                        "Erro",
                        f"Erro ao processar resultado: {e}"
                    )

        # Remover futures completadas
        for future in completed_futures:
            del self.futures[future]

        # Se ainda há futures, continuar monitorando
        if self.futures:
            # Atualizar progresso (simples: incremento linear)
            current = self.progress_bar.value()
            if current < 90:
                self.progress_bar.setValue(current + 5)
            QTimer.singleShot(200, self.check_merge_progress)
        else:
            # Finalizado
            self.btn_merge.setEnabled(True)
            self.progress_bar.setVisible(False)
            logger.info(self.TOOL_KEY, "ImageMerger", "Processos de mesclagem finalizados")

    def on_base_path_changed(self, new_path: str) -> None:
        """Hook chamado quando pasta base muda."""
        self.set_current_folder(new_path)
        self.load_images_from_current_folder()


def get_plugin():
    """Função obrigatória para carregamento do plugin."""
    return ImageMerger()
