"""
Testes de integração para as novas classes refatoradas.

Testa ImageUtil, FileExplorer e ICOConverterStyles.
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ImageUtil import ImageUtil, ImageFormats
from utils.FileExplorer import FileExplorer
from src.styles.ICOConverterStyles import ICOConverterStyles
from utils.LogUtils import logger
from utils.ToolKey import ToolKey


def test_image_formats():
    """Testa a classe ImageFormats e suas constantes."""
    print("\n" + "="*50)
    print("TESTE 1: ImageFormats - Constantes de formatos")
    print("="*50)
    
    # Teste de extensões de entrada
    extensions = ImageFormats.get_supported_extensions()
    print(f"✓ Extensões suportadas (entrada): {extensions}")
    assert len(extensions) > 0, "Deve haver extensões suportadas"
    assert '.png' in extensions, "PNG deve estar na lista"
    
    # Teste de formatos de saída
    output_formats = ImageFormats.get_output_formats()
    print(f"✓ Formatos de saída: {output_formats}")
    assert 'ico' in output_formats, "ICO deve estar nos formatos de saída"
    
    # Teste de mapeamento PIL
    pil_format = ImageFormats.get_pil_format('.png')
    print(f"✓ Formato PIL para .png: {pil_format}")
    assert pil_format == 'PNG', "Deve retornar 'PNG'"
    
    pil_format_ico = ImageFormats.get_pil_format('.ico')
    print(f"✓ Formato PIL para .ico: {pil_format_ico}")
    assert pil_format_ico == 'ICO', "Deve retornar 'ICO'"
    
    print("✅ TESTE 1 PASSOU")


def test_file_explorer():
    """Testa a classe FileExplorer."""
    print("\n" + "="*50)
    print("TESTE 2: FileExplorer - Exploração de arquivos")
    print("="*50)
    
    # Criar explorador com extensões de imagem
    explorer = FileExplorer(['.png', '.jpg', '.jpeg'], recursive=False)
    print(f"✓ FileExplorer criado com extensões: {explorer.get_extensions()}")
    
    # Teste de configuração
    assert explorer.is_recursive() == False, "Deve ser não-recursivo"
    print("✓ Modo não-recursivo confirmado")
    
    # Teste de atualização de configuração
    explorer.set_recursive(True)
    assert explorer.is_recursive() == True, "Deve ser recursivo após configuração"
    print("✓ Modo recursivo alterado com sucesso")
    
    # Teste de busca em pasta do projeto
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"✓ Buscando em: {project_root}")
    
    # Buscar em docs (que pode ter imagens)
    docs_path = os.path.join(project_root, 'docs')
    if os.path.exists(docs_path):
        files = explorer.find_files(docs_path)
        print(f"✓ Encontrados {len(files)} arquivo(s) com extensões .png/.jpg/.jpeg em docs/")
    
    # Teste de obtém extensões disponíveis
    available_exts = FileExplorer.get_available_extensions(project_root, max_depth=1)
    print(f"✓ Extensões encontradas no projeto: {available_exts[:5]}..." if len(available_exts) > 5 else f"✓ Extensões encontradas: {available_exts}")
    
    print("✅ TESTE 2 PASSOU")


def test_image_util():
    """Testa a classe ImageUtil."""
    print("\n" + "="*50)
    print("TESTE 3: ImageUtil - Métodos de utilidade")
    print("="*50)
    
    # Criar pasta temporária para testes
    import tempfile
    from PIL import Image
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Criar imagem de teste
        test_image_path = os.path.join(tmpdir, "test.png")
        img = Image.new('RGB', (256, 256), color='red')
        img.save(test_image_path)
        print(f"✓ Imagem de teste criada: {test_image_path}")
        
        # Teste de obter informações
        info = ImageUtil.get_image_info(test_image_path)
        print(f"✓ Informações da imagem: {info}")
        assert info['width'] == 256, "Largura deve ser 256"
        assert info['height'] == 256, "Altura deve ser 256"
        
        # Teste de redimensionar
        resized_path = os.path.join(tmpdir, "test_resized.png")
        success = ImageUtil.resize_image(test_image_path, resized_path, 128, 128)
        print(f"✓ Redimensionamento: {'Sucesso' if success else 'Falha'}")
        assert success, "Redimensionamento deve ter sucesso"
        
        # Verificar dimensões da imagem redimensionada
        info_resized = ImageUtil.get_image_info(resized_path)
        print(f"✓ Dimensões redimensionadas: {info_resized['width']}x{info_resized['height']}")
        assert info_resized['width'] == 128, "Largura redimensionada deve ser 128"
        
        # Teste de conversão de formato
        jpg_path = os.path.join(tmpdir, "test_converted.jpg")
        success = ImageUtil.convert_image_format(test_image_path, jpg_path)
        print(f"✓ Conversão PNG->JPG: {'Sucesso' if success else 'Falha'}")
        assert success, "Conversão deve ter sucesso"
        assert os.path.exists(jpg_path), "Arquivo JPG deve existir"
        
        # Teste de conversão para ICO
        ico_path = os.path.join(tmpdir, "test.ico")
        success = ImageUtil.convert_image_to_ico(test_image_path, ico_path, [16, 32, 48])
        print(f"✓ Conversão para ICO: {'Sucesso' if success else 'Falha'}")
        assert success, "Conversão para ICO deve ter sucesso"
        assert os.path.exists(ico_path), "Arquivo ICO deve existir"
        print(f"✓ Arquivo ICO criado: {os.path.getsize(ico_path)} bytes")
    
    print("✅ TESTE 3 PASSOU")


def test_ico_converter_styles():
    """Testa a classe ICOConverterStyles."""
    print("\n" + "="*50)
    print("TESTE 4: ICOConverterStyles - Estilos isolados")
    print("="*50)
    
    # Teste de constantes de cor
    print(f"✓ Cor primária: {ICOConverterStyles.COLOR_PRIMARY}")
    assert ICOConverterStyles.COLOR_PRIMARY == "#0e639c", "Cor primária incorreta"
    
    # Teste de constantes de espaçamento
    print(f"✓ Espaçamento normal: {ICOConverterStyles.SPACING_NORMAL}px")
    assert ICOConverterStyles.SPACING_NORMAL == 8, "Espaçamento incorreto"
    
    # Teste de métodos de stylesheet
    button_style = ICOConverterStyles.get_button_style()
    print(f"✓ Stylesheet de botão gerado ({len(button_style)} caracteres)")
    assert len(button_style) > 0, "Stylesheet deve ter conteúdo"
    assert "QPushButton" in button_style, "Deve conter definição de QPushButton"
    
    # Teste de todos os estilos
    all_styles = ICOConverterStyles.get_all_styles()
    print(f"✓ Estilos disponíveis: {list(all_styles.keys())}")
    assert 'button' in all_styles, "Deve ter estilo de botão"
    assert 'progress_bar' in all_styles, "Deve ter estilo de barra de progresso"
    assert 'image_list' in all_styles, "Deve ter estilo de lista de imagens"
    
    # Verificar que todos os estilos têm conteúdo
    for name, style in all_styles.items():
        assert len(style) > 0, f"Estilo '{name}' deve ter conteúdo"
        print(f"  ✓ Estilo '{name}': {len(style)} caracteres")
    
    print("✅ TESTE 4 PASSOU")


def test_integration():
    """Testa integração de todas as classes."""
    print("\n" + "="*50)
    print("TESTE 5: Integração geral")
    print("="*50)
    
    # Verificar que ImageFormats pode ser usado pelo FileExplorer
    extensions = ImageFormats.get_supported_extensions()
    explorer = FileExplorer(extensions)
    print(f"✓ FileExplorer inicializado com ImageFormats.get_supported_extensions()")
    print(f"  Extensões: {explorer.get_extensions()}")
    
    # Verificar que todos os imports funcionam corretamente
    print("✓ Todos os imports funcionam corretamente")
    
    # Verificar estrutura de diretórios
    project_root = Path(__file__).parent
    utils_path = project_root / 'utils'
    styles_path = project_root / 'src' / 'styles'
    
    assert utils_path.exists(), f"Pasta utils deve existir em {utils_path}"
    assert (utils_path / 'ImageUtil.py').exists(), "ImageUtil.py deve existir"
    assert (utils_path / 'FileExplorer.py').exists(), "FileExplorer.py deve existir"
    print(f"✓ Arquivo ImageUtil.py existe em utils/")
    print(f"✓ Arquivo FileExplorer.py existe em utils/")
    
    assert styles_path.exists(), f"Pasta styles deve existir em {styles_path}"
    assert (styles_path / 'ICOConverterStyles.py').exists(), "ICOConverterStyles.py deve existir"
    print(f"✓ Pasta src/styles/ criada")
    print(f"✓ Arquivo ICOConverterStyles.py existe em src/styles/")
    
    # Verificar que ico_converter_util.py foi removido
    old_path = project_root / 'src' / 'ico_converter_util.py'
    assert not old_path.exists(), "ico_converter_util.py deve ter sido removido"
    print(f"✓ Arquivo antigo ico_converter_util.py removido")
    
    print("✅ TESTE 5 PASSOU")


def main():
    """Executa todos os testes."""
    print("\n")
    print("╔" + "="*48 + "╗")
    print("║" + " "*10 + "TESTES DE INTEGRAÇÃO REFATORAÇÃO" + " "*6 + "║")
    print("╚" + "="*48 + "╝")
    
    try:
        test_image_formats()
        test_file_explorer()
        test_image_util()
        test_ico_converter_styles()
        test_integration()
        
        print("\n" + "="*50)
        print("🎉 TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("="*50 + "\n")
        
        return 0
    except AssertionError as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
