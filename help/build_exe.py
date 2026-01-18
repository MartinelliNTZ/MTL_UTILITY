#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script para compilar MTL_UTIL com PyInstaller.

Funcionalidades:
  - Extrai versão do arquivo Anotatios.txt
  - Limpa artifacts da build anterior (build/, dist/, __pycache__)
  - Gera executável com versão no nome do arquivo
  - Valida dependências necessárias
"""

import logging
import os
import re
import shutil
import stat
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)-8s | %(message)s'
)
logger = logging.getLogger(__name__)

# Constantes de configuração
PROJECT_CONFIG = {
    'spec_file': 'MTL_UTIL.spec',
    'main_module': 'main.py',
    'version_file': 'docs/Anotatios.txt',
    'build_dirs': ['build', 'dist', '__pycache__', '.pytest_cache'],
    'pyinstaller_timeout': 300,  # segundos
}


def extract_version(annotations_file: Path) -> Optional[str]:
    """
    Extrai a versão do arquivo Anotatios.txt.
    
    Args:
        annotations_file: Caminho para o arquivo Anotatios.txt
        
    Returns:
        Versão no formato X.Y.Z, ou None se não encontrado
        
    Raises:
        FileNotFoundError: Se o arquivo não existir
        Exception: Outros erros ao ler o arquivo
    """
    if not annotations_file.exists():
        logger.error(f"Arquivo não encontrado: {annotations_file}")
        return None
    
    try:
        with open(annotations_file, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'version\s*=\s*([\d.]+)', content)
            if match:
                version = match.group(1)
                logger.info(f"Versão encontrada: {version}")
                return version
            else:
                logger.warning("Padrão de versão não encontrado em Anotatios.txt")
                return None
    except Exception as e:
        logger.error(f"Erro ao ler arquivo: {e}")
        return None


def remove_dots(version_string: str) -> str:
    """
    Remove pontos da versão para usar no nome do arquivo.
    
    Args:
        version_string: Versão no formato X.Y.Z
        
    Returns:
        Versão sem pontos no formato XYZ
    """
    return version_string.replace('.', '_')


def handle_remove_readonly(func, path: str, exc_info) -> None:
    """
    Trata erros de permissão ao remover diretórios no Windows.
    
    Parâmetro de callback para shutil.rmtree(onexc=...)
    
    Args:
        func: Função que falhou
        path: Caminho do arquivo/diretório
        exc_info: Tuple com informações da exceção (type, value, traceback)
    """
    try:
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR | stat.S_IREAD)
            func(path)
        else:
            logger.debug(f"Permissões OK, mas ainda não foi possível remover: {path}")
    except Exception as e:
        logger.debug(f"Não foi possível ajustar permissões para {path}: {e}")


def remove_directory_safe(dir_path: str, retries: int = 3) -> bool:
    """
    Remove um diretório de forma segura com retry.
    
    Tenta remover o diretório até 3 vezes em caso de erros de permissão.
    Útil no Windows onde arquivos podem estar temporariamente bloqueados.
    
    Args:
        dir_path: Caminho do diretório a remover
        retries: Número de tentativas (padrão: 3)
        
    Returns:
        bool: True se removido com sucesso, False caso contrário
    """
    if not os.path.exists(dir_path):
        return True
    
    for attempt in range(retries):
        try:
            shutil.rmtree(dir_path, onexc=handle_remove_readonly)
            logger.info(f"✓ Removido: {dir_path}")
            return True
        except Exception as e:
            if attempt < retries - 1:
                logger.warning(f"Tentativa {attempt + 1}/{retries} falhou ao remover {dir_path}, aguardando...")
                time.sleep(1)
            else:
                logger.warning(f"Ignorando falha ao remover {dir_path}: {e}")
                logger.info(f"⚠️  Continuando compilação mesmo com diretórios antigos presentes")
                return True  # Retorna True para não bloquear a compilação
    
    return True


def build_executable(version: str) -> bool:
    """
    Executa o PyInstaller para gerar o executável.
    
    Processa:
    1. Verifica arquivo spec do PyInstaller
    2. Limpa compilações anteriores
    3. Executa compilação com PyInstaller
    4. Renomeia executável com número de versão
    
    Args:
        version: Versão no formato X.Y.Z para incluir no executável
        
    Returns:
        bool: True se compilação bem-sucedida, False caso contrário
    """
    project_root = Path(__file__).parent.parent
    dist_dir = project_root / "dist"
    spec_file = project_root / "MTL_UTIL.spec"
    build_dir = project_root / "build"
    
    logger.info("="*60)
    logger.info("COMPILANDO MTL_UTIL COM PYINSTALLER")
    logger.info("="*60)
    
    # Verifica se o arquivo .spec existe
    if not spec_file.exists():
        logger.error(f"Arquivo spec não encontrado: {spec_file}")
        return False
    
    logger.info(f"Arquivo spec: {spec_file}")
    logger.info(f"Diretório de saída: {dist_dir}")
    
    # Limpa compilações anteriores
    logger.info("Limpando compilações anteriores...")
    remove_directory_safe(str(build_dir))
    remove_directory_safe(str(dist_dir))
    
    try:
        logger.info("Executando PyInstaller...")
        cmd = [sys.executable, "-m", "PyInstaller", str(spec_file)]
        result = subprocess.run(cmd, cwd=str(project_root), check=True, capture_output=True, text=True)
        logger.info("✓ PyInstaller executado com sucesso")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao executar PyInstaller: {e}")
        if e.stderr:
            logger.error(f"Saída de erro: {e.stderr}")
        return False
    except FileNotFoundError:
        logger.error("PyInstaller não encontrado. Instale com: pip install pyinstaller")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado ao compilar: {e}")
        return False
    
    # Renomeia executável com versão
    logger.info("Renomeando executável com versão...")
    exe_path = dist_dir / "MTL_UTIL.exe"
    
    if not exe_path.exists():
        logger.error(f"Executável não encontrado em: {exe_path}")
        return False
    
    version_no_dots = remove_dots(version)
    new_exe_name = f"MTL_UTIL_{version_no_dots}.exe"
    new_exe_path = dist_dir / new_exe_name
    
    try:
        exe_path.rename(new_exe_path)
        logger.info(f"✓ Executável renomeado para: {new_exe_name}")
    except Exception as e:
        logger.error(f"Erro ao renomear executável: {e}")
        return False
    
    logger.info("="*60)
    logger.info("✓ COMPILAÇÃO CONCLUÍDA COM SUCESSO!")
    logger.info("="*60)
    logger.info(f"Arquivo: {new_exe_path}")
    logger.info(f"Versão: {version}")
    
    return True


def main() -> int:
    """
    Função principal para compilar e empacotar a aplicação.
    
    Processa:
    1. Lê versão do arquivo Anotatios.txt
    2. Executa compilação com PyInstaller
    3. Retorna código de saída apropriado
    
    Returns:
        int: 0 se sucesso, 1 se erro
    """
    logger.info("="*60)
    logger.info("MTL_UTIL - Build Script v2.0")
    logger.info("="*60)
    
    project_root = Path(__file__).parent.parent
    annotations_file = project_root / "docs" / "Anotatios.txt"
    
    # Verifica se arquivo de anotações existe
    if not annotations_file.exists():
        logger.error(f"Arquivo não encontrado: {annotations_file}")
        return 1
    
    # Extrai versão
    logger.info(f"Lendo versão de: {annotations_file}")
    version = extract_version(annotations_file)
    
    if not version:
        logger.error("Não foi possível extrair a versão do arquivo")
        return 1
    
    logger.info(f"Versão detectada: {version}")
    
    # Compila o executável
    success = build_executable(version)
    
    if success:
        dist_dir = project_root / "dist"
        exe_path = dist_dir / f"MTL_UTIL_{remove_dots(version)}.exe"
        logger.info(f"Executável pronto em: {exe_path}")
        return 0
    else:
        logger.error("Falha na compilação")
        return 1


if __name__ == "__main__":
    sys.exit(main())
