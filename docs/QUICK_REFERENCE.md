# Quick Reference - Image Merger Plugin

**Data:** 18 de Janeiro de 2026  
**Para:** Desenvolvedores e Integradores

---

## 🚀 Início Rápido

### Arquivos Criados
```
utils/PDFUtil.py ................... Operações batch com PDFs
plugins/image_merger.py ............ Plugin UI principal
src/styles/ImageMergerStyles.py ... Estilos centralizados
```

### Arquivos Modificados
```
utils/ToolKey.py ................... IMAGE_MERGER token
MTL_UTIL.spec ...................... Inclusão no build
```

### Carregamento Automático
O plugin é carregado automaticamente pelo `PluginManager`:
```python
# Nenhuma mudança necessária em main.py
# PluginManager descobre image_merger.py e carrega
```

---

## 📖 Documentação

```
IMAGE_MERGER_ARCHITECTURE.md ....... Análise profunda
IMAGE_MERGER_IMPLEMENTATION.md .... Detalhes técnicos
IMAGE_MERGER_ENTREGA_FINAL.md .... Resumo executivo
MUDANCAS_REALIZADAS.md ........... Este sumário
```

---

## 🔧 API do PDFUtil

### `create_pdf_from_images()`
```python
from utils.PDFUtil import PDFUtil

success, message = PDFUtil.create_pdf_from_images(
    image_paths=['img1.png', 'img2.jpg'],
    output_path='/caminho/resultado.pdf',
    max_width=3000  # redimensiona se > 3000px
)

# Retorna: (bool, str)
# Exemplo: (True, "✓ PDF criado: resultado.pdf")
```

### `export_images_resized()`
```python
success, message = PDFUtil.export_images_resized(
    image_paths=['img1.png', 'img2.jpg'],
    output_dir='/caminho/saida',
    max_width=3000
)

# Retorna: (bool, str)
# Exemplo: (True, "✓ 2 imagens exportadas em PNG")
```

### `process_images_batch()`
```python
success, message = PDFUtil.process_images_batch(
    image_paths=['img1.png', 'img2.jpg'],
    output_dir='/caminho/saida',
    max_width=3000,
    export_pdf=True,
    export_png=False,
    pdf_filename='documento.pdf'
)

# Retorna: (bool, str)
# Exemplo: (True, "✓ Processamento concluído: PDF: documento.pdf")
```

### `validate_images()`
```python
is_valid, errors = PDFUtil.validate_images(
    image_paths=['img1.png', 'img2.jpg']
)

# Retorna: (bool, List[str])
# Exemplo: (True, [])
```

---

## 🎨 API do ImageMergerStyles

### Todos os métodos
```python
from src.styles.ImageMergerStyles import ImageMergerStyles

# Retorna QSS/CSS como string
ImageMergerStyles.get_button_style()
ImageMergerStyles.get_image_list_style()
ImageMergerStyles.get_control_panel_style()
ImageMergerStyles.get_progress_bar_style()
# ... etc
```

### Cores disponíveis (constantes)
```python
ImageMergerStyles.COLOR_BG_DARK        # #1e1e1e
ImageMergerStyles.COLOR_BG_PANEL       # #252526
ImageMergerStyles.COLOR_FG_TEXT        # #d4d4d4
ImageMergerStyles.COLOR_FG_HIGHLIGHT   # #007acc
ImageMergerStyles.COLOR_BORDER         # #3e3e3e
ImageMergerStyles.COLOR_SUCCESS        # #4ec9b0
ImageMergerStyles.COLOR_WARNING        # #dcdcaa
ImageMergerStyles.COLOR_ERROR          # #f48771
```

---

## 🎯 Classes do ImageMerger

### `ImageMerger` (Plugin Principal)
```python
from plugins.image_merger import ImageMerger

# Propriedades de classe
ImageMerger.name = "Image Merger"
ImageMerger.icon_name = "image_merger"
ImageMerger.TOOL_KEY = ToolKey.IMAGE_MERGER

# Métodos principais
plugin = ImageMerger()
widget = plugin.create_widget(parent)
plugin.start_merge()
plugin.on_base_path_changed(new_path)
```

### `ReorderableListWidget` (Lista Customizada)
```python
from plugins.image_merger import ReorderableListWidget

# Herança
ReorderableListWidget(QListWidget)

# Métodos extras
list_widget = ReorderableListWidget()
list_widget.add_files(['/path/to/image.png', '/path/to/folder'])
ordered_paths = list_widget.get_ordered_paths()
```

---

## 🔌 Integração com MTL_UTIL

### PluginManager (automático)
```python
# Em main.py (sem mudanças necessárias)
plugin_manager = PluginManager()

# PluginManager descobre image_merger.py e:
# 1. Importa plugins.image_merger
# 2. Executa get_plugin()
# 3. Adiciona à UI automaticamente
```

### Preferences (automático)
```python
# Salva automaticamente:
merger_max_width
merger_export_pdf
merger_export_png

# Em config/config.json
```

### Logging (automático)
```python
# Usa ToolKey.IMAGE_MERGER
logger.info(ToolKey.IMAGE_MERGER, "ImageMerger", "mensagem")
logger.debug(ToolKey.IMAGE_MERGER, "PDFUtil", "mensagem")
```

---

## 🧪 Testes Rápidos

### Testar imports
```python
from utils.PDFUtil import PDFUtil
from plugins.image_merger import ImageMerger, get_plugin
from src.styles.ImageMergerStyles import ImageMergerStyles

print("OK - Todos os imports funcionam")
```

### Testar PDFUtil
```python
from utils.PDFUtil import PDFUtil

# Validar imagens
is_valid, errors = PDFUtil.validate_images(['test.png'])
assert is_valid, f"Validação falhou: {errors}"

print("OK - PDFUtil funciona")
```

### Testar plugin
```python
from plugins.image_merger import get_plugin

plugin = get_plugin()
assert plugin.name == "Image Merger"
assert plugin.TOOL_KEY == "image_merger"

print("OK - Plugin carrega corretamente")
```

---

## 📊 Estrutura de Diretórios

```
MTL_UTIL/
├── plugins/
│   └── image_merger.py ........... ✅ NOVO
│
├── utils/
│   └── PDFUtil.py ............... ✅ NOVO
│
├── src/
│   └── styles/
│       └── ImageMergerStyles.py .. ✅ NOVO
│
└── docs/
    ├── IMAGE_MERGER_ARCHITECTURE.md
    ├── IMAGE_MERGER_IMPLEMENTATION.md
    ├── IMAGE_MERGER_ENTREGA_FINAL.md
    └── MUDANCAS_REALIZADAS.md
```

---

## ⚙️ Configuração

### Preferências Padrão
```python
{
    "merger_max_width": 3000,
    "merger_export_pdf": True,
    "merger_export_png": False
}
```

### Formatos Suportados
```
Entrada: .png, .jpg, .jpeg, .tif, .tiff, .bmp, .gif, .webp
Saída:   PDF (múltiplas páginas)
         PNG (redimensionado)
```

### Configuração de Threading
```python
ThreadPoolExecutor(max_workers=4)  # 4 threads paralelos
```

---

## 🐛 Troubleshooting

### "Plugin não aparece"
- ✅ Verificar se `image_merger.py` está em `plugins/`
- ✅ Verificar se tem `get_plugin()` função
- ✅ Verificar imports em `plugin_manager.py`

### "Import error: PDFUtil"
- ✅ Verificar se `PDFUtil.py` está em `utils/`
- ✅ Verificar se `from PIL import Image` funciona

### "ImageMergerStyles não carrega"
- ✅ Verificar se está em `src/styles/`
- ✅ Verificar imports em `image_merger.py`

### "Plugin carrega mas não funciona"
- ✅ Verificar logs em `config/` (arquivo .log)
- ✅ Verificar se Preferences funciona
- ✅ Verificar se FileExplorer encontra imagens

---

## 📝 Changelog

### v1.0 (18/01/2026)
- ✅ PDFUtil criado com 4 métodos
- ✅ ImageMerger plugin criado
- ✅ ImageMergerStyles criado
- ✅ Integração com MTL_UTIL
- ✅ Documentação completa
- ✅ Testes e validações

---

## 📚 Referências Rápidas

### Arquivos Principais
| Arquivo | Linhas | Responsabilidade |
|---------|--------|------------------|
| PDFUtil.py | 245 | Operações batch |
| image_merger.py | 645 | UI + Orquestração |
| ImageMergerStyles.py | 180 | Estilos |

### Métodos Principais
| Método | Classe | Retorno |
|--------|--------|---------|
| `create_pdf_from_images()` | PDFUtil | `Tuple[bool, str]` |
| `export_images_resized()` | PDFUtil | `Tuple[bool, str]` |
| `process_images_batch()` | PDFUtil | `Tuple[bool, str]` |
| `create_widget()` | ImageMerger | `QWidget` |
| `start_merge()` | ImageMerger | `None` |

### Padrões Usados
- ThreadPoolExecutor (parallelismo)
- Type hints (type safety)
- Logging estruturado (debug)
- Preferences (persistência)
- SOLID principles (arquitetura)

---

## 🎓 Conceitos-Chave

1. **PDFUtil = Batch Operations**
   - Independente de UI
   - Reutilizável
   - Testável isoladamente

2. **ImageMerger = UI + Orquestração**
   - Delega lógica para PDFUtil
   - Gerencia threading
   - Interage com usuário

3. **ReorderableListWidget = Drag-Drop**
   - Suporta arrastar do SO
   - Reordena internamente
   - Gera thumbnails

4. **Separação Clara**
   - UI em ImageMerger
   - Lógica em PDFUtil
   - Estilos em ImageMergerStyles

---

## ✅ Checklist de Implementação

- [x] PDFUtil implementado
- [x] ImageMerger implementado
- [x] ImageMergerStyles implementado
- [x] ToolKey atualizado
- [x] MTL_UTIL.spec atualizado
- [x] Testes de import
- [x] Documentação completa
- [x] Validações passadas
- [x] Plugin carrega automaticamente
- [x] Logging funciona

---

**Última Atualização:** 18/01/2026  
**Status:** 🟢 PRONTO PARA PRODUÇÃO
