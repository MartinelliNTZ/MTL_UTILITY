"""
PDFUtil - Utilitário para operações batch com PDFs e imagens.

Classe utilitária para mesclar múltiplas imagens em PDF,
exportar imagens redimensionadas e operações batch em geral.
"""

import os
from typing import List, Tuple
from PIL import Image
from utils.LogUtils import logger
from utils.ToolKey import ToolKey
from utils.ImageUtil import ImageUtil


class PDFUtil:
    """Utilitário genérico para operações batch com PDFs e imagens."""
    
    TOOL_KEY = ToolKey.IMAGE_MERGER

    @staticmethod
    def create_pdf_from_images(
        image_paths: List[str],
        output_path: str,
        max_width: int = 3000
    ) -> Tuple[bool, str]:
        """
        Mescla múltiplas imagens em um único PDF.

        As imagens são processadas na ordem fornecida,
        redimensionadas proporcionalmente se excederem max_width,
        e convertidas para RGB antes de serem salvas no PDF.

        Args:
            image_paths: Lista de caminhos de imagens (em ordem)
            output_path: Caminho do arquivo PDF de saída
            max_width: Largura máxima (padrão 3000px)

        Returns:
            Tuple[bool, str]: (sucesso, mensagem descritiva)
        """
        if not image_paths:
            return False, "✗ Nenhuma imagem fornecida"

        try:
            logger.debug(PDFUtil.TOOL_KEY, "PDFUtil",
                        f"Iniciando mesclagem PDF: {len(image_paths)} imagens -> {output_path}")

            pil_images = []

            for idx, img_path in enumerate(image_paths, start=1):
                try:
                    # Abrir e converter para RGB
                    img = Image.open(img_path).convert("RGB")
                    
                    # Redimensionar se necessário
                    width, height = img.size
                    if width > max_width:
                        ratio = max_width / float(width)
                        new_height = int(height * ratio)
                        img = img.resize((max_width, new_height), Image.LANCZOS)
                    
                    pil_images.append(img)
                    logger.debug(PDFUtil.TOOL_KEY, "PDFUtil",
                                f"[{idx}/{len(image_paths)}] Imagem processada: {os.path.basename(img_path)}")

                except Exception as e:
                    logger.warning(PDFUtil.TOOL_KEY, "PDFUtil",
                                  f"Erro ao processar {os.path.basename(img_path)}: {e}")
                    return False, f"✗ Erro ao processar imagem: {os.path.basename(img_path)}"

            # Salvar PDF
            if pil_images:
                try:
                    first_img = pil_images[0]
                    remaining_imgs = pil_images[1:] if len(pil_images) > 1 else []
                    
                    first_img.save(
                        output_path,
                        format='PDF',
                        save_all=True,
                        append_images=remaining_imgs
                    )
                    
                    logger.info(PDFUtil.TOOL_KEY, "PDFUtil",
                               f"PDF criado com sucesso: {output_path} ({len(pil_images)} páginas)")
                    return True, f"✓ PDF criado: {os.path.basename(output_path)}"

                except Exception as e:
                    logger.error(PDFUtil.TOOL_KEY, "PDFUtil",
                                f"Erro ao salvar PDF: {e}")
                    return False, f"✗ Erro ao salvar PDF: {str(e)}"

        except Exception as e:
            logger.error(PDFUtil.TOOL_KEY, "PDFUtil",
                        f"Erro na mesclagem PDF: {e}")
            return False, f"✗ Erro na mesclagem: {str(e)}"

    @staticmethod
    def export_images_resized(
        image_paths: List[str],
        output_dir: str,
        max_width: int = 3000
    ) -> Tuple[bool, str]:
        """
        Exporta múltiplas imagens redimensionadas em PNG.

        Cada imagem é redimensionada proporcionalmente se exceder max_width
        e salva como PNG no diretório de saída.

        Args:
            image_paths: Lista de caminhos de imagens
            output_dir: Diretório de saída
            max_width: Largura máxima (padrão 3000px)

        Returns:
            Tuple[bool, str]: (sucesso, mensagem descritiva)
        """
        if not image_paths:
            return False, "✗ Nenhuma imagem fornecida"

        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
                logger.debug(PDFUtil.TOOL_KEY, "PDFUtil",
                            f"Diretório criado: {output_dir}")
            except Exception as e:
                logger.error(PDFUtil.TOOL_KEY, "PDFUtil",
                            f"Erro ao criar diretório: {e}")
                return False, f"✗ Erro ao criar diretório: {str(e)}"

        try:
            logger.debug(PDFUtil.TOOL_KEY, "PDFUtil",
                        f"Exportando {len(image_paths)} imagens em PNG para {output_dir}")

            exported_count = 0

            for idx, img_path in enumerate(image_paths, start=1):
                try:
                    # Abrir e converter para RGB
                    img = Image.open(img_path).convert("RGB")
                    
                    # Redimensionar se necessário
                    width, height = img.size
                    if width > max_width:
                        ratio = max_width / float(width)
                        new_height = int(height * ratio)
                        img = img.resize((max_width, new_height), Image.LANCZOS)
                    
                    # Salvar PNG
                    base_name = os.path.splitext(os.path.basename(img_path))[0]
                    output_path = os.path.join(output_dir, f"{base_name}.png")
                    
                    img.save(output_path, format='PNG', optimize=True)
                    exported_count += 1
                    
                    logger.debug(PDFUtil.TOOL_KEY, "PDFUtil",
                                f"[{idx}/{len(image_paths)}] PNG exportado: {output_path}")

                except Exception as e:
                    logger.warning(PDFUtil.TOOL_KEY, "PDFUtil",
                                  f"Erro ao exportar {os.path.basename(img_path)}: {e}")
                    return False, f"✗ Erro ao exportar: {os.path.basename(img_path)}"

            logger.info(PDFUtil.TOOL_KEY, "PDFUtil",
                       f"Exportação concluída: {exported_count} imagens em PNG")
            return True, f"✓ {exported_count} imagens exportadas em PNG"

        except Exception as e:
            logger.error(PDFUtil.TOOL_KEY, "PDFUtil",
                        f"Erro na exportação PNG: {e}")
            return False, f"✗ Erro na exportação: {str(e)}"

    @staticmethod
    def process_images_batch(
        image_paths: List[str],
        output_dir: str,
        max_width: int = 3000,
        export_pdf: bool = True,
        export_png: bool = False,
        pdf_filename: str = "documento.pdf"
    ) -> Tuple[bool, str]:
        """
        Processa um lote de imagens: pode gerar PDF, PNG redimensionado ou ambos.

        Este é o método principal que orquestra as operações batch.
        Ideal para uso em plugins que precisam flexibilidade de saída.

        Args:
            image_paths: Lista de caminhos de imagens (em ordem)
            output_dir: Diretório de saída
            max_width: Largura máxima (padrão 3000px)
            export_pdf: Se deve gerar PDF (padrão True)
            export_png: Se deve exportar PNGs redimensionados (padrão False)
            pdf_filename: Nome do arquivo PDF (padrão "documento.pdf")

        Returns:
            Tuple[bool, str]: (sucesso, mensagem descritiva)
        """
        if not image_paths:
            return False, "✗ Nenhuma imagem fornecida"

        if not export_pdf and not export_png:
            return False, "✗ Escolha pelo menos um formato de saída (PDF e/ou PNG)"

        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                logger.error(PDFUtil.TOOL_KEY, "PDFUtil",
                            f"Erro ao criar diretório: {e}")
                return False, f"✗ Erro ao criar diretório: {str(e)}"

        try:
            logger.debug(PDFUtil.TOOL_KEY, "PDFUtil",
                        f"Processando lote: {len(image_paths)} imagens, PDF={export_pdf}, PNG={export_png}")

            # Exportar PNGs se solicitado
            if export_png:
                success, message = PDFUtil.export_images_resized(
                    image_paths, output_dir, max_width
                )
                if not success:
                    return False, message

            # Criar PDF se solicitado
            if export_pdf:
                pdf_output = os.path.join(output_dir, pdf_filename)
                success, message = PDFUtil.create_pdf_from_images(
                    image_paths, pdf_output, max_width
                )
                if not success:
                    return False, message

            logger.info(PDFUtil.TOOL_KEY, "PDFUtil",
                       f"Processamento em lote concluído com sucesso")
            
            summary = []
            if export_pdf:
                summary.append(f"PDF: {pdf_filename}")
            if export_png:
                summary.append(f"{len(image_paths)} PNGs")
            
            return True, f"✓ Processamento concluído: {', '.join(summary)}"

        except Exception as e:
            logger.error(PDFUtil.TOOL_KEY, "PDFUtil",
                        f"Erro no processamento em lote: {e}")
            return False, f"✗ Erro no processamento: {str(e)}"

    @staticmethod
    def validate_images(image_paths: List[str]) -> Tuple[bool, List[str]]:
        """
        Valida uma lista de caminhos de imagem.

        Verifica se os arquivos existem e se são imagens válidas (PIL consegue abrir).

        Args:
            image_paths: Lista de caminhos para validar

        Returns:
            Tuple[bool, List[str]]: (válidas, lista de erros)
        """
        errors = []

        for img_path in image_paths:
            if not os.path.exists(img_path):
                errors.append(f"Arquivo não encontrado: {img_path}")
                continue

            try:
                with Image.open(img_path) as img:
                    _ = img.format  # Validar que é uma imagem
            except Exception as e:
                errors.append(f"Imagem inválida ({os.path.basename(img_path)}): {e}")

        is_valid = len(errors) == 0
        logger.debug(PDFUtil.TOOL_KEY, "PDFUtil",
                    f"Validação: {len(image_paths)} imagens, {len(errors)} erros")
        
        return is_valid, errors
