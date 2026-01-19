# Análise Arquitetural: Image Merger Plugin

**Data:** 18 de Janeiro de 2026  
**Análise de:** UNIR_PNG_EM_PDF_COMPLETO.py vs Arquitetura MTL_UTIL  

---

## 1. Comparação de Cenários

### ICO Converter (5 cenários)
1. ✅ Usuário abre plugin
2. ✅ Seleciona pasta  
3. ✅ Seleciona arquivos individuais
4. 🔄 **Converte** (específico: ICO com múltiplos tamanhos)
5. ✅ Preferências salvas

### Image Merger (esperado)
1. ✅ Usuário abre plugin
2. ✅ Seleciona pasta  
3. ✅ Seleciona arquivos individuais (+ drag-drop)
4. 🔄 **Mescla** (específico: PDF ou PNG redimensionado)
5. ✅ Preferências salvas

**Conclusão:** 80% dos cenários são idênticos. Diferença principal está no **Cenário 4** (operação específica).

---

## 2. Análise de Responsabilidades

### UNIR_PNG_EM_PDF_COMPLETO.py
```
action_generate():
  ├─ Para cada imagem:
  │  ├─ Image.open() + convert("RGB")
  │  ├─ Redimensionar se > max_width
  │  ├─ Salvar PNG se pedido
  │  └─ Acumular para PDF
  └─ PIL.Image.save(format='PDF', append_images=...)
```

**Operação:** Mesclar N imagens em PDF (mantendo ordem)

---

### ImageUtil Atual
```
Métodos existentes:
├─ convert_image_to_ico() ... específico ICO
├─ convert_image_format() .. genérico, múltiplos formatos
├─ resize_image() ......... genérico
└─ get_image_info() ...... genérico
```

**Observação:** ImageUtil NÃO tem operações de "PDF" explicitamente.

---

## 3. Decisão: PDFUtil vs Estender ImageUtil?

### Análise SOLID:

**Single Responsibility Principle:**
- `ImageUtil` = Operações COM UMA imagem
- `PDFUtil` = Operações COM MÚLTIPLAS imagens (mescla, batch)

**Open/Closed:**
- Se adicionar ao ImageUtil: Fica "responsável por tudo"
- Se criar PDFUtil: Extensível para futuras operações batch

**Dependency Inversion:**
- ImageUtil não deve conhecer PDFUtil
- PDFUtil PODE usar ImageUtil internamente

---

## 4. RECOMENDAÇÃO: Criar PDFUtil

### Justificativa

1. **Separação Clara:**
   - `ImageUtil` = Operações elementares (PIL direto)
   - `PDFUtil` = Orquestração de operações batch

2. **Coesão Melhorada:**
   ```python
   # ImageUtil
   resize_image(input, output, w, h) → bool
   
   # PDFUtil
   create_pdf_from_images(images: List[str], output, max_width) → bool
   ```

3. **Reutilização:**
   - PDFUtil pode usar `ImageUtil.resize_image()` internamente
   - Outro plugin (batch processing) pode usar PDFUtil sem conhecer ImageUtil

4. **Testabilidade:**
   - ImageUtil: testa manipulação de 1 imagem
   - PDFUtil: testa lógica de mescla

5. **Código Limpo:**
   ```python
   # Em image_merger.py (plugin)
   success, message = PDFUtil.create_pdf_from_images(
       image_paths,
       output_path,
       max_width=self.preferences.get("merger_max_width", 3000)
   )
   ```

---

## 5. Arquitetura Proposta para Image Merger

### Estrutura de Arquivos
```
plugins/
  image_merger.py ......... Plugin principal (UI)

utils/
  ImageUtil.py ........... Existente (mantém-se igual)
  PDFUtil.py ............ NOVO (operações batch PDF)

src/
  styles/
    ImageMergerStyles.py .. NOVO (estilos específicos)
```

### Hierarquia de Responsabilidades

```
ImageMerger (Plugin)
├─ UI: Layouts, eventos, dialogs
├─ FileExplorer: Encontrar imagens
├─ PDFUtil: Mesclar em PDF
├─ ImageUtil: Redimensionar (via PDFUtil)
├─ Preferences: Salvar config (max_width, etc)
└─ ToolKey.IMAGE_MERGER: Logging

PDFUtil (Util)
├─ ImageUtil.resize_image() (internamente)
└─ PIL.Image.save(format='PDF')

ImageMergerStyles (Styles)
├─ Cores, fontes
└─ Layouts específicos
```

---

## 6. Métodos do PDFUtil (Proposto)

```python
class PDFUtil:
    """Utilitário para operações batch com PDFs."""
    
    @staticmethod
    def create_pdf_from_images(
        image_paths: List[str],
        output_path: str,
        max_width: int = 3000
    ) -> Tuple[bool, str]:
        """Mescla múltiplas imagens em um PDF."""
        # Lógica do action_generate()
    
    @staticmethod
    def export_images_resized(
        image_paths: List[str],
        output_dir: str,
        max_width: int = 3000
    ) -> Tuple[bool, str]:
        """Exporta imagens redimensionadas em PNG."""
        # Lógica do action_generate() (parte PNG)
    
    @staticmethod
    def process_images_batch(
        image_paths: List[str],
        output_dir: str,
        max_width: int = 3000,
        export_pdf: bool = True,
        export_png: bool = False
    ) -> Tuple[bool, str]:
        """Processa lote: pode gerar PDF, PNG ou ambos."""
```

---

## 7. Cenários Image Merger (Mapeado)

### Cenário 1: Usuário abre plugin
```
1. create_widget() é chamado
2. Preferências carregadas (pasta, max_width, export_pdf/png)
3. FileExplorer configurado com extensões de imagem
4. UI construída (lista reordenável, preview, botão mesclar)
5. QTimer dispara → load_images_from_current_folder()
```
**Responsável:** `image_merger.py`

---

### Cenário 2: Usuário seleciona pasta
```
1. Clica "📁 Pasta"
2. QFileDialog abre
3. select_folder() chamado
4. load_images_from_current_folder() via FileExplorer
5. Lista atualiza com thumbnails
```
**Responsável:** `image_merger.py` + `FileExplorer`

---

### Cenário 3: Usuário arrasta imagens / seleciona arquivos
```
1. Drag-drop na lista OU clica "📄 Arquivo"
2. ReorderableListWidget trata drop
3. add_image_to_list() para cada imagem
4. Thumbnail gerado
5. Usuário pode reordenar
```
**Responsável:** `image_merger.py`

---

### Cenário 4: Usuário mescla em PDF ⭐ (DIFERENTE)
```
1. Marca: "Gerar PDF" e/ou "Exportar PNG"
2. Define max_width (preferências)
3. Clica "▶️ Mesclar"
4. Dialog: escolhe pasta de saída
5. Para cada imagem em thread pool:
   - PDFUtil.process_images_batch() processa
   - Redimensiona, salva PNG ou acumula para PDF
6. Progress bar atualiza
7. PDF final criado via PDFUtil
```
**Responsável:** `image_merger.py` + `PDFUtil`

---

### Cenário 5: Preferências salvas
```
1. Usuário muda max_width ou checkboxes
2. Preferences.set() salva
3. Próxima abertura carrega valores
```
**Responsável:** `image_merger.py` + `Preferences`

---

## 8. Comparação Visual: ICO Converter vs Image Merger

### ICO Converter
```python
def convert_single_image(self, img_path, output_dir, sizes) → Tuple[bool, str]:
    success = ImageUtil.convert_image_to_ico(img_path, output_path, sizes)
    return (success, message)

def check_conversion_progress(self):
    # Monitora futures do executor
    # Chama convert_single_image() em cada thread
```

### Image Merger (Proposto)
```python
def merge_images(self, img_paths, output_dir, max_width) → Tuple[bool, str]:
    success, message = PDFUtil.process_images_batch(
        img_paths, output_dir, max_width,
        export_pdf=self.chk_pdf.isChecked(),
        export_png=self.chk_png.isChecked()
    )
    return (success, message)

def check_merge_progress(self):
    # Monitora futures do executor
    # Chama merge_images() em cada thread
```

**Diferença Principal:** 
- ICO: Uma operação por imagem
- Merger: Uma operação por LOTE (todas as imagens)

---

## 9. UI Layout Proposto para Image Merger

```
┌─────────────────────────────────────────┐
│  📁 /pasta/atual     [📁] [📄] [↻]      │
├─────────────────────────────────┬───────┤
│                                 │       │
│  Imagens (arraste p/ reordenar) │Prévia │
│  [img1.png] [img2.jpg] ...      │       │
│                                 │   🖼   │
│  [➕] [📁] [🗑] [✖]             │       │
│                                 │       │
├─────────────────────────────────┼───────┤
│                                 │ Opções│
│                                 ├───────┤
│                                 │☑ PDF  │
│                                 │☐ PNG  │
│                                 │       │
│                                 │Max: 3000px
│                                 │       │
│                                 │[▶️ Mesclar]
│                                 │[████    ] 0%
└─────────────────────────────────┴───────┘
```

**Similitudes com ICO Converter:**
- ✅ Seleção de pasta
- ✅ Seleção de arquivos  
- ✅ Lista reordenável
- ✅ Preview
- ✅ Opções de saída
- ✅ Barra de progresso

**Diferenças:**
- ❌ Sem tabs (simples)
- ❌ Max width em vez de múltiplos tamanhos
- ✅ Drag-drop nativo na lista

---

## 10. Conclusão Arquitetural

| Aspecto | Decisão | Justificativa |
|---------|---------|-------------|
| **Novo Plugin** | Substituir `sample_browser.py` | Mesmo padrão ICO Converter |
| **Novo Util** | Criar `PDFUtil` | Responsabilidade única (batch) |
| **Novo Style** | Criar `ImageMergerStyles` | Estilos específicos |
| **UI Pattern** | Similar ICO Converter | Reutilizar padrões |
| **Threading** | ThreadPoolExecutor | Mesmo do ICO Converter |
| **Logging** | ToolKey.IMAGE_MERGER | Nova entrada em ToolKey |
| **Preferences** | Sistema existente | Guardar max_width, opções |

---

## 11. Benefícios da Arquitetura Proposta

✅ **Coesão:**
- Cada classe tem responsabilidade clara
- PDFUtil = batch, ImageUtil = elementar

✅ **Acoplamento Baixo:**
- ImageMerger usa FileExplorer + PDFUtil + Preferences
- PDFUtil usa ImageUtil internamente (apenas)

✅ **Reutilização:**
- PDFUtil pode ser usado por outro plugin
- ImageUtil continua genérico

✅ **Testabilidade:**
- PDFUtil testável isoladamente
- ImageMerger testável sem PDFUtil

✅ **Manutenibilidade:**
- Lógica PDF centralizada em PDFUtil
- UI centralizada em ImageMerger
- Estilos centralizados em ImageMergerStyles

---

**Próximo Passo:** Implementar PDFUtil, ImageMerger e atualizar ToolKey/referências.
