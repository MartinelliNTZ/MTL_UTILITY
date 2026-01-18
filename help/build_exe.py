#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para compilar MTL_UTIL com PyInstaller
Extrai a versão do arquivo Anotatios.txt e inclui no nome do executável
"""

import os
import sys
import subprocess
import shutil
import re
import stat
import time
from pathlib import Path


def extract_version(annotations_file):
    """
    Extrai a versão do arquivo Anotatios.txt
    
    Args:
        annotations_file: Caminho para o arquivo Anotatios.txt
        
    Returns:
        str: Versão no formato X.Y.Z
    """
    try:
        with open(annotations_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Procura por "version = X.Y.Z"
            match = re.search(r'version\s*=\s*([\d.]+)', content)
            if match:
                version = match.group(1)
                print(f"✓ Versão encontrada: {version}")
                return version
            else:
                print("✗ Versão não encontrada no arquivo Anotatios.txt")
                return None
    except FileNotFoundError:
        print(f"✗ Arquivo não encontrado: {annotations_file}")
        return None
    except Exception as e:
        print(f"✗ Erro ao ler o arquivo: {e}")
        return None


def remove_dots(version_string):
    """
    Remove pontos da versão
    
    Args:
        version_string: Versão no formato X.Y.Z
        
    Returns:
        str: Versão sem pontos no formato XYZ
    """
    return version_string.replace('.', '_')


def handle_remove_readonly(func, path, exc):
    """
    Trata erros de permissão ao remover diretórios no Windows
    """
    import stat
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR | stat.S_IREAD)
        func(path)
    else:
        raise


def remove_directory_safe(dir_path, retries=3):
    """
    Remove um diretório de forma segura com retry
    
    Args:
        dir_path: Caminho do diretório
        retries: Número de tentativas
        
    Returns:
        bool: True se removido com sucesso
    """
    if not os.path.exists(dir_path):
        return True
    
    for attempt in range(retries):
        try:
            shutil.rmtree(dir_path, onerror=handle_remove_readonly)
            return True
        except Exception as e:
            if attempt < retries - 1:
                print(f"   Tentativa {attempt + 1} falhou, aguardando...")
                time.sleep(1)
            else:
                print(f"   ✗ Erro ao remover {dir_path}: {e}")
                return False
    
    return False


def build_executable(version):
    """
    Executa o PyInstaller para gerar o executável
    
    Args:
        version: Versão para incluir no nome do arquivo
    """
    # Diretório raiz do projeto
    project_root = Path(__file__).parent.parent
    spec_file = project_root / "MTL_UTIL.spec"
    dist_dir = project_root / "dist"
    
    print("\n" + "="*60)
    print("COMPILANDO MTL_UTIL COM PYINSTALLER")
    print("="*60)
    
    # Verifica se o arquivo .spec existe
    if not spec_file.exists():
        print(f"✗ Arquivo spec não encontrado: {spec_file}")
        return False
    
    print(f"\n1. Preparando compilação...")
    print(f"   Arquivo spec: {spec_file}")
    print(f"   Diretório de saída: {dist_dir}")
    
    print(f"   Arquivo spec: {spec_file}")
    print(f"   Diretório de saída: {dist_dir}")
    
    try:
        # Executa PyInstaller
        cmd = [
            sys.executable, 
            "-m", 
            "PyInstaller",
            str(spec_file)
        ]
        
        result = subprocess.run(cmd, cwd=str(project_root), check=True)
        print("   ✓ PyInstaller executado com sucesso")
        
    except subprocess.CalledProcessError as e:
        print(f"   ✗ Erro ao executar PyInstaller: {e}")
        return False
    except Exception as e:
        print(f"   ✗ Erro inesperado: {e}")
        return False
    
    print(f"\n3. Renomeando executável com versão...")
    # Procura o arquivo .exe gerado
    exe_pattern = dist_dir / "MTL_UTIL.exe"
    
    if exe_pattern.exists():
        # Novo nome com versão (sem pontos)
        version_no_dots = remove_dots(version)
        new_exe_name = f"MTL_UTIL_{version_no_dots}.exe"
        new_exe_path = dist_dir / new_exe_name
        
        try:
            exe_pattern.rename(new_exe_path)
            print(f"   ✓ Executável renomeado para: {new_exe_name}")
        except Exception as e:
            print(f"   ✗ Erro ao renomear: {e}")
            return False
    else:
        print(f"   ✗ Executável não encontrado em: {exe_pattern}")
        return False
    
    print("\n" + "="*60)
    print("✓ COMPILAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*60)
    print(f"\nArquivo executável gerado:")
    print(f"  {new_exe_path}")
    print(f"\nVersão: {version}")
    print(f"Versão sem pontos: {version_no_dots}")
    print("\nOs arquivos estão em:")
    print(f"  {dist_dir}")
    
    return True


def main():
    """Função principal"""
    print("\nMTL_UTIL - Build Script v1.0")
    print("="*60)
    
    # Diretório raiz do projeto
    project_root = Path(__file__).parent.parent
    annotations_file = project_root / "docs" / "Anotatios.txt"
    
    # Extrai versão
    print(f"\n1. Lendo versão do arquivo: {annotations_file}")
    version = extract_version(str(annotations_file))
    
    if not version:
        print("\n✗ Não foi possível continuar sem a versão")
        return 1
    
    # Compila o executável
    success = build_executable(version)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
