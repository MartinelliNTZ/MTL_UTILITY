"""
FileExplorer - Utilitário para exploração de arquivos com filtros de extensão.

Classe auxiliar genérica para buscar arquivos em pastas baseado em lista de extensões.
Pode ser utilizada por diferentes plugins que trabalham com diferentes tipos de arquivos.
"""

import os
from typing import List, Optional
from utils.LogUtils import logger
from utils.ToolKey import ToolKey


class FileExplorer:
    """Utilitário genérico para exploração de arquivos em pastas."""
    
    TOOL_KEY = ToolKey.ICO_CONVERTER

    def __init__(self, extensions: List[str], recursive: bool = True):
        """
        Inicializa o FileExplorer.

        Args:
            extensions: Lista de extensões para filtrar (ex: ['.png', '.jpg'])
            recursive: Se deve buscar recursivamente em subpastas (padrão: True)
        """
        # Normalizar extensões (adicionar ponto se necessário)
        self.extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
        self.recursive = recursive
        
        logger.debug(self.TOOL_KEY, "FileExplorer",
                    f"FileExplorer criado com extensões: {self.extensions}, recursivo: {recursive}")

    def find_files(self, folder_path: str) -> List[str]:
        """
        Encontra todos os arquivos com extensões especificadas em uma pasta.

        Args:
            folder_path: Caminho da pasta para buscar
            
        Returns:
            Lista de caminhos absolutos dos arquivos encontrados
        """
        # Normalizar o caminho para usar separadores consistentes do sistema
        folder_path = os.path.normpath(folder_path)
        
        if not os.path.exists(folder_path):
            logger.warning(self.TOOL_KEY, "FileExplorer",
                          f"Pasta não encontrada: {folder_path}")
            return []

        if not os.path.isdir(folder_path):
            logger.warning(self.TOOL_KEY, "FileExplorer",
                          f"Caminho não é uma pasta: {folder_path}")
            return []

        files = []

        if self.recursive:
            # Busca recursiva
            for root, dirs, filelist in os.walk(folder_path):
                for file in filelist:
                    if self._matches_extensions(file):
                        files.append(os.path.join(root, file))
        else:
            # Busca apenas no nível atual
            try:
                for file in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file)
                    if os.path.isfile(file_path) and self._matches_extensions(file):
                        files.append(file_path)
            except PermissionError:
                logger.warning(self.TOOL_KEY, "FileExplorer",
                              f"Permissão negada ao acessar: {folder_path}")
                return []

        logger.info(self.TOOL_KEY, "FileExplorer",
                   f"Encontrados {len(files)} arquivos em {folder_path}")
        return files

    def find_files_by_name(self, folder_path: str, pattern: str) -> List[str]:
        """
        Encontra arquivos que correspondem aos critérios: extensão E nome contém padrão.

        Args:
            folder_path: Caminho da pasta para buscar
            pattern: Padrão de nome a filtrar (case-insensitive)
            
        Returns:
            Lista de caminhos absolutos dos arquivos encontrados
        """
        all_files = self.find_files(folder_path)
        pattern_lower = pattern.lower()
        
        filtered = [f for f in all_files if pattern_lower in os.path.basename(f).lower()]
        
        logger.info(self.TOOL_KEY, "FileExplorer",
                   f"Encontrados {len(filtered)} arquivos com padrão '{pattern}'")
        return filtered

    def get_files_by_extension(self, folder_path: str, extension: str) -> List[str]:
        """
        Encontra arquivos de uma extensão específica.

        Args:
            folder_path: Caminho da pasta para buscar
            extension: Extensão específica para filtrar
            
        Returns:
            Lista de caminhos absolutos dos arquivos encontrados
        """
        # Normalizar extensão
        ext = extension if extension.startswith('.') else f'.{extension}'
        
        all_files = self.find_files(folder_path)
        filtered = [f for f in all_files if f.lower().endswith(ext.lower())]
        
        logger.debug(self.TOOL_KEY, "FileExplorer",
                    f"Encontrados {len(filtered)} arquivos com extensão '{ext}'")
        return filtered

    def _matches_extensions(self, filename: str) -> bool:
        """
        Verifica se o arquivo tem uma das extensões permitidas.

        Args:
            filename: Nome do arquivo

        Returns:
            True se o arquivo corresponde às extensões, False caso contrário
        """
        filename_lower = filename.lower()
        return any(filename_lower.endswith(ext.lower()) for ext in self.extensions)

    def set_extensions(self, extensions: List[str]) -> None:
        """
        Atualiza a lista de extensões a filtrar.

        Args:
            extensions: Nova lista de extensões
        """
        self.extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
        logger.debug(self.TOOL_KEY, "FileExplorer",
                    f"Extensões atualizadas para: {self.extensions}")

    def set_recursive(self, recursive: bool) -> None:
        """
        Define se a busca deve ser recursiva.

        Args:
            recursive: True para busca recursiva, False para apenas nível atual
        """
        self.recursive = recursive
        logger.debug(self.TOOL_KEY, "FileExplorer",
                    f"Modo recursivo alterado para: {recursive}")

    def get_extensions(self) -> List[str]:
        """Retorna as extensões atualmente configuradas."""
        return self.extensions.copy()

    def is_recursive(self) -> bool:
        """Retorna se a busca é recursiva."""
        return self.recursive

    @staticmethod
    def get_available_extensions(folder_path: str, max_depth: Optional[int] = None) -> List[str]:
        """
        Obtém todas as extensões de arquivo encontradas em uma pasta.

        Args:
            folder_path: Caminho da pasta
            max_depth: Profundidade máxima de busca (None = ilimitada)

        Returns:
            Lista de extensões únicas encontradas
        """
        extensions = set()

        try:
            if max_depth is None or max_depth > 0:
                next_depth = None if max_depth is None else max_depth - 1
                
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        _, ext = os.path.splitext(file)
                        if ext:
                            extensions.add(ext.lower())
                    
                    if max_depth is not None and next_depth == 0:
                        dirs.clear()  # Não descender mais
        except PermissionError:
            logger.warning(ToolKey.ICO_CONVERTER, "FileExplorer",
                          f"Permissão negada ao analisar: {folder_path}")

        return sorted(list(extensions))
