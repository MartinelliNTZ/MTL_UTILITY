"""
ICO Converter Util - Utilitário para conversão de imagens para formato ICO.

Classe utilitária isolada para conversão de imagens, sem dependências de UI.
"""

import os
from typing import List
from PIL import Image
from utils.ToolKey import ToolKey
from utils.LogUtils import logger


class ICOConverterUtil:
    """Utilitário para conversão de imagens para formato ICO."""

    TOOL_KEY = ToolKey.ICO_CONVERTER

    @staticmethod
    def convert_image_to_ico(input_path: str, output_path: str, sizes: List[int]) -> bool:
        """
        Converte uma imagem para formato ICO com múltiplos tamanhos.

        Args:
            input_path: Caminho da imagem de entrada
            output_path: Caminho do arquivo ICO de saída
            sizes: Lista de tamanhos para incluir no ICO

        Returns:
            True se a conversão foi bem-sucedida, False caso contrário
        """
        try:
            logger.debug(ICOConverterUtil.TOOL_KEY, "ICOConverterUtil",
                        f"Iniciando conversão: {input_path} -> {output_path}, sizes: {sizes}")

            # Carregar imagem e converter para RGBA
            img = Image.open(input_path).convert("RGBA")
            sizes_tuples = [(s, s) for s in sorted(sizes)]

            # Tentar salvar diretamente com Pillow
            try:
                img.save(output_path, format='ICO', sizes=sizes_tuples)
                logger.info(ICOConverterUtil.TOOL_KEY, "ICOConverterUtil",
                           f"ICO salvo com sucesso: {output_path}")
                return True
            except Exception as e:
                logger.warning(ICOConverterUtil.TOOL_KEY, "ICOConverterUtil",
                              f"Falha no salvamento direto, tentando fallback: {e}")

                # Fallback: redimensionar manualmente e salvar
                resized_imgs = []
                for s in sorted(sizes):
                    im2 = img.copy()
                    im2 = im2.resize((s, s), Image.LANCZOS)
                    resized_imgs.append(im2.convert("RGBA"))

                # Tentar salvar a maior imagem como ICO
                try:
                    largest = resized_imgs[-1]
                    largest.save(output_path, format='ICO', sizes=sizes_tuples)
                    logger.info(ICOConverterUtil.TOOL_KEY, "ICOConverterUtil",
                               f"ICO salvo com fallback: {output_path}")
                    return True
                except Exception as e2:
                    # Último fallback: salvar apenas o maior tamanho
                    try:
                        resized_imgs[0].save(output_path, format='ICO')
                        logger.warning(ICOConverterUtil.TOOL_KEY, "ICOConverterUtil",
                                      f"ICO salvo apenas com tamanho único: {output_path}, erro: {e2}")
                        return True
                    except Exception as e3:
                        logger.error(ICOConverterUtil.TOOL_KEY, "ICOConverterUtil",
                                    f"Falha completa na conversão: {e3}")
                        return False

        except Exception as e:
            logger.error(ICOConverterUtil.TOOL_KEY, "ICOConverterUtil",
                        f"Erro ao processar {input_path}: {e}")
            return False

    @staticmethod
    def get_supported_extensions() -> List[str]:
        """Retorna lista de extensões suportadas."""
        return ['.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp', '.gif', '.webp']

    @staticmethod
    def find_images_in_folder(folder_path: str, recursive: bool = True) -> List[str]:
        """
        Encontra todas as imagens suportadas em uma pasta.

        Args:
            folder_path: Caminho da pasta
            recursive: Se deve buscar recursivamente em subpastas

        Returns:
            Lista de caminhos absolutos das imagens encontradas
        """
        if not os.path.exists(folder_path):
            logger.warning(ICOConverterUtil.TOOL_KEY, "ICOConverterUtil",
                          f"Pasta não encontrada: {folder_path}")
            return []

        images = []
        exts = ICOConverterUtil.get_supported_extensions()

        if recursive:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in exts):
                        images.append(os.path.join(root, file))
        else:
            for file in os.listdir(folder_path):
                fp = os.path.join(folder_path, file)
                if os.path.isfile(fp) and any(file.lower().endswith(ext) for ext in exts):
                    images.append(fp)

        logger.info(ICOConverterUtil.TOOL_KEY, "ICOConverterUtil",
                   f"Encontradas {len(images)} imagens em {folder_path}")
        return images