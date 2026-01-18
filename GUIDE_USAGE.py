"""
GUIA DE USO - NOVAS CLASSES DA REFATORAÇÃO

Exemplos práticos de como usar as classes refatoradas.
"""

# ============================================================================
# 1. IMAGEUTIL - Converter e manipular imagens
# ============================================================================

from utils.ImageUtil import ImageUtil, ImageFormats

# Exemplo 1: Converter imagem para ICO
ImageUtil.convert_image_to_ico(
    input_path='imagem.png',
    output_path='icone.ico',
    sizes=[16, 32, 48, 64, 128, 256]
)

# Exemplo 2: Converter entre formatos
ImageUtil.convert_image_format(
    input_path='imagem.png',
    output_path='imagem.jpg'
)

# Exemplo 3: Redimensionar imagem
ImageUtil.resize_image(
    input_path='imagem.png',
    output_path='imagem_pequena.png',
    width=256,
    height=256
)

# Exemplo 4: Obter informações da imagem
info = ImageUtil.get_image_info('imagem.png')
# Retorna: {'width': ..., 'height': ..., 'format': ..., 'mode': ...}

# Exemplo 5: Usar constantes de formatos
extensoes_entrada = ImageFormats.get_supported_extensions()
# Retorna: ['.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp', '.gif', '.webp']

formatos_saida = ImageFormats.get_output_formats()
# Retorna: ['ico', 'png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'tiff']

formato_pil = ImageFormats.get_pil_format('.png')  # Retorna: 'PNG'


# ============================================================================
# 2. FILEEXPLORER - Explorar e filtrar arquivos
# ============================================================================

from utils.FileExplorer import FileExplorer
from utils.ImageUtil import ImageFormats

# Exemplo 1: Buscar imagens em pasta
explorer = FileExplorer(
    extensions=ImageFormats.get_supported_extensions(),
    recursive=True
)
imagens = explorer.find_files('caminho/da/pasta')

# Exemplo 2: Buscar apenas PNG
explorer_png = FileExplorer(['.png'])
pngs = explorer_png.find_files('caminho/da/pasta')

# Exemplo 3: Buscar com padrão de nome
explorer = FileExplorer(['.png', '.jpg', '.jpeg'])
logos = explorer.find_files_by_name('caminho/da/pasta', 'logo')

# Exemplo 4: Buscar extensão específica
pngs_apenas = explorer.get_files_by_extension('caminho/da/pasta', '.png')

# Exemplo 5: Listar extensões disponíveis
extensoes = FileExplorer.get_available_extensions('caminho/da/pasta')

# Exemplo 6: Alterar configuração após criar
explorer = FileExplorer(['.png'])
explorer.set_extensions(['.png', '.jpg', '.jpeg'])
explorer.set_recursive(False)  # Agora busca apenas no nível atual


# ============================================================================
# 3. ICONVERTERSTYLES - Usar estilos em componentes PySide6
# ============================================================================

from src.styles.ICOConverterStyles import ICOConverterStyles
from PySide6.QtWidgets import QPushButton, QLabel, QProgressBar

# Exemplo 1: Aplicar estilo a botão
botao = QPushButton("Converter")
botao.setStyleSheet(ICOConverterStyles.get_button_style())

# Exemplo 2: Aplicar estilo customizado
botao_custom = QPushButton("Buscar")
botao_custom.setStyleSheet(ICOConverterStyles.get_button_style(
    color="#FF6B6B",
    hover="#FF4444",
    pressed="#CC0000"
))

# Exemplo 3: Aplicar estilo a label
label = QLabel("Arquivos encontrados:")
label.setStyleSheet(ICOConverterStyles.get_folder_label_style())

# Exemplo 4: Aplicar estilo a barra de progresso
progress = QProgressBar()
progress.setStyleSheet(ICOConverterStyles.get_progress_bar_style())

# Exemplo 5: Usar cores constantes
cor_primaria = ICOConverterStyles.COLOR_PRIMARY  # "#0e639c"
cor_background = ICOConverterStyles.COLOR_BG_MAIN  # "#2d2d30"
espacamento = ICOConverterStyles.SPACING_NORMAL  # 8

# Exemplo 6: Obter todos os estilos
todos_estilos = ICOConverterStyles.get_all_styles()
for nome, stylesheet in todos_estilos.items():
    print(f"Estilo: {nome} ({len(stylesheet)} caracteres)")


# ============================================================================
# 4. INTEGRAÇÃO COMPLETA - Exemplo prático
# ============================================================================

from utils.ImageUtil import ImageUtil, ImageFormats
from utils.FileExplorer import FileExplorer

def converter_imagens_em_lote(pasta_entrada, pasta_saida):
    """Converte todas as imagens em uma pasta para ICO."""
    
    # 1. Criar explorador com extensões suportadas
    explorer = FileExplorer(ImageFormats.get_supported_extensions())
    
    # 2. Encontrar todas as imagens
    imagens = explorer.find_files(pasta_entrada)
    print(f"Encontradas {len(imagens)} imagens")
    
    # 3. Converter cada uma
    for imagem_path in imagens:
        nome_arquivo = imagem_path.split('\\')[-1].split('.')[0]
        saida_ico = f"{pasta_saida}\\{nome_arquivo}.ico"
        
        sucesso = ImageUtil.convert_image_to_ico(
            input_path=imagem_path,
            output_path=saida_ico,
            sizes=[16, 32, 48, 64, 128]
        )
        
        if sucesso:
            print(f"✓ {nome_arquivo}.ico criado")
        else:
            print(f"✗ Erro ao converter {nome_arquivo}")


# ============================================================================
# 5. REUTILIZAR PARA OUTROS TIPOS DE ARQUIVO
# ============================================================================

# Exemplo: Buscar documentos
docs_explorer = FileExplorer(['.pdf', '.docx', '.txt'])
documentos = docs_explorer.find_files('Meus Documentos')

# Exemplo: Buscar áudio
audio_explorer = FileExplorer(['.mp3', '.wav', '.flac', '.aac'])
musicas = audio_explorer.find_files('Minha Música')

# Exemplo: Buscar vídeos
video_explorer = FileExplorer(['.mp4', '.avi', '.mkv', '.mov'])
videos = video_explorer.find_files('Meus Vídeos')


# ============================================================================
# DICAS IMPORTANTES
# ============================================================================

"""
1. ImageFormats é uma classe de constantes
   - Use ImageFormats.get_supported_extensions() para obter extensões
   - Use ImageFormats.get_pil_format() para converter para formato PIL

2. FileExplorer é reutilizável
   - Crie um explorador com as extensões desejadas
   - Use find_files() para busca recursiva ou não-recursiva
   - Configure com set_recursive() e set_extensions()

3. ICOConverterStyles centraliza todos os estilos
   - Cores, espaçamentos, tamanhos - tudo em um único lugar
   - Fácil manter consistência visual
   - Use get_all_styles() para listar disponíveis

4. Todas as classes podem ser importadas de qualquer lugar do projeto
   - São independentes da UI
   - Podem ser testadas isoladamente
   - Podem ser reutilizadas em outros plugins
"""
