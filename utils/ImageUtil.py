"""
ImageUtil - Utilitário genérico para operações com imagens.

Classe utilitária genérica para conversão e manipulação de imagens.
Pode ser utilizada por diferentes plugins que trabalham com imagens.
"""

from typing import List
from PIL import Image
from utils.LogUtils import logger
from utils.ToolKey import ToolKey


class ImageFormats:
    """Constantes para formatos suportados."""
    
    # Formatos de entrada suportados
    INPUT_FORMATS = ['.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp', '.gif', '.webp']
    
    # Formatos de saída suportados
    OUTPUT_FORMATS = ['ico', 'png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'tiff']
    
    # Mapa de extensões para formatos PIL
    FORMAT_MAP = {
        '.png': 'PNG',
        '.jpg': 'JPEG',
        '.jpeg': 'JPEG',
        '.tif': 'TIFF',
        '.tiff': 'TIFF',
        '.bmp': 'BMP',
        '.gif': 'GIF',
        '.webp': 'WEBP',
        '.ico': 'ICO'
    }
    
    @classmethod
    def get_supported_extensions(cls) -> List[str]:
        """Retorna lista de extensões de entrada suportadas."""
        return cls.INPUT_FORMATS.copy()
    
    @classmethod
    def get_output_formats(cls) -> List[str]:
        """Retorna lista de formatos de saída suportados."""
        return cls.OUTPUT_FORMATS.copy()
    
    @classmethod
    def get_pil_format(cls, extension: str) -> str:
        """
        Retorna o formato PIL para uma extensão de arquivo.
        
        Args:
            extension: Extensão do arquivo (ex: '.png')
            
        Returns:
            Formato PIL correspondente (ex: 'PNG')
        """
        return cls.FORMAT_MAP.get(extension.lower(), None)


class ImageUtil:
    """Utilitário genérico para operações com imagens."""
    
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
            logger.debug(ImageUtil.TOOL_KEY, "ImageUtil",
                        f"Iniciando conversão: {input_path} -> {output_path}, sizes: {sizes}")

            # Carregar imagem e converter para RGBA
            img = Image.open(input_path).convert("RGBA")
            sizes_tuples = [(s, s) for s in sorted(sizes)]

            # Tentar salvar diretamente com Pillow
            try:
                img.save(output_path, format='ICO', sizes=sizes_tuples)
                logger.info(ImageUtil.TOOL_KEY, "ImageUtil",
                           f"ICO salvo com sucesso: {output_path}")
                return True
            except Exception as e:
                logger.warning(ImageUtil.TOOL_KEY, "ImageUtil",
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
                    logger.info(ImageUtil.TOOL_KEY, "ImageUtil",
                               f"ICO salvo com fallback: {output_path}")
                    return True
                except Exception as e2:
                    # Último fallback: salvar apenas o maior tamanho
                    try:
                        resized_imgs[0].save(output_path, format='ICO')
                        logger.warning(ImageUtil.TOOL_KEY, "ImageUtil",
                                      f"ICO salvo apenas com tamanho único: {output_path}, erro: {e2}")
                        return True
                    except Exception as e3:
                        logger.error(ImageUtil.TOOL_KEY, "ImageUtil",
                                    f"Falha completa na conversão: {e3}")
                        return False

        except Exception as e:
            logger.error(ImageUtil.TOOL_KEY, "ImageUtil",
                        f"Erro ao processar {input_path}: {e}")
            return False

    @staticmethod
    def convert_image_format(input_path: str, output_path: str, output_format: str = None) -> bool:
        """
        Converte uma imagem para outro formato.

        Args:
            input_path: Caminho da imagem de entrada
            output_path: Caminho da imagem de saída
            output_format: Formato de saída (ex: 'PNG', 'JPEG'). Se None, infer do output_path

        Returns:
            True se a conversão foi bem-sucedida, False caso contrário
        """
        try:
            logger.debug(ImageUtil.TOOL_KEY, "ImageUtil",
                        f"Convertendo: {input_path} -> {output_path}, formato: {output_format}")

            img = Image.open(input_path)
            
            # Se não especificou formato, tenta inferir da extensão
            if output_format is None:
                ext = output_path.split('.')[-1].lower()
                output_format = ImageFormats.get_pil_format(f'.{ext}')
                if output_format is None:
                    raise ValueError(f"Formato desconhecido: {ext}")

            # Converter para RGB se necessário (para JPEG)
            if output_format in ['JPEG', 'JPG']:
                if img.mode in ('RGBA', 'P', 'LA'):
                    img = img.convert('RGB')

            img.save(output_path, format=output_format)
            logger.info(ImageUtil.TOOL_KEY, "ImageUtil",
                       f"Imagem convertida com sucesso: {output_path}")
            return True

        except Exception as e:
            logger.error(ImageUtil.TOOL_KEY, "ImageUtil",
                        f"Erro ao converter imagem: {e}")
            return False

    @staticmethod
    def resize_image(input_path: str, output_path: str, width: int, height: int) -> bool:
        """
        Redimensiona uma imagem para as dimensões especificadas.

        Args:
            input_path: Caminho da imagem de entrada
            output_path: Caminho da imagem redimensionada
            width: Largura desejada
            height: Altura desejada

        Returns:
            True se bem-sucedido, False caso contrário
        """
        try:
            logger.debug(ImageUtil.TOOL_KEY, "ImageUtil",
                        f"Redimensionando: {input_path} para {width}x{height}")

            img = Image.open(input_path)
            img_resized = img.resize((width, height), Image.LANCZOS)
            img_resized.save(output_path)
            
            logger.info(ImageUtil.TOOL_KEY, "ImageUtil",
                       f"Imagem redimensionada: {output_path}")
            return True

        except Exception as e:
            logger.error(ImageUtil.TOOL_KEY, "ImageUtil",
                        f"Erro ao redimensionar imagem: {e}")
            return False

    @staticmethod
    def get_image_info(image_path: str) -> dict:
        """
        Obtém informações sobre uma imagem.

        Args:
            image_path: Caminho da imagem

        Returns:
            Dicionário com informações (width, height, format, mode) ou None se erro
        """
        try:
            img = Image.open(image_path)
            return {
                'width': img.width,
                'height': img.height,
                'format': img.format,
                'mode': img.mode
            }
        except Exception as e:
            logger.error(ImageUtil.TOOL_KEY, "ImageUtil",
                        f"Erro ao obter informações da imagem: {e}")
            return None
