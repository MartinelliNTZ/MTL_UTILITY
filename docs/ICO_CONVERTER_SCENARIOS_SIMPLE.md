# Análise de Cenários - ICO Converter (Simples e Prático)

**Data:** 18 de Janeiro de 2026  
**Enfoque:** Simplicidade + Boas Práticas

---

## 📋 Cenários de Uso

### Cenário 1: Usuário abre plugin
```
1. create_widget() é chamado
2. Preferências carregadas (pasta anterior, tamanhos selecionados)
3. FileExplorer configurado com extensões de imagem
4. UI construída
5. QTimer dispara → load_images_from_current_folder()
6. Imagens aparecem na lista com thumbnails
```
**Responsável:** `ico_converter.py`  
**Usa:** `FileExplorer`, `ICOConverterStyles`, `Preferences`

---

### Cenário 2: Usuário seleciona pasta
```
1. Clica "📁 Pasta"
2. QFileDialog abre
3. select_folder() chamado com novo caminho
4. set_current_folder() atualiza label + preferências
5. load_images_from_current_folder() recarrega lista
6. Thumbnails regeneradas
```
**Responsável:** `ico_converter.py`  
**Usa:** `FileExplorer` para encontrar arquivos

---

### Cenário 3: Usuário seleciona arquivos individuais
```
1. Clica "📄 Arquivo"
2. QFileDialog.getOpenFileNames() abre (multi-select)
3. Para cada arquivo:
   - add_image_to_list() é chamado
   - PIL abre imagem
   - Thumbnail gerado
   - QListWidgetItem criado
```
**Responsável:** `ico_converter.py`  
**Usa:** `PIL` (via `add_image_to_list`)

---

### Cenário 4: Usuário converte imagens
```
1. Seleciona tamanhos (16, 32, 48, 64, 128, 256)
2. Marca "Manter original" e/ou "Remover fonte"
3. Clica "🔄 Converter"
4. Dialog: escolhe pasta de saída
5. Para cada imagem em thread pool:
   - ImageUtil.convert_image_to_ico() processa
   - Salva em output_dir
6. Progress bar atualiza
7. Resultado final exibido
```
**Responsável:** `ico_converter.py` + `ImageUtil`  
**Threading:** ThreadPoolExecutor (4 workers)

---

### Cenário 5: Preferências salvas
```
1. Usuário marca checkbox tamanho
2. _on_checkbox_changed() salva em Preferences
3. Próxima abertura carrega preferência
4. Checkbox já marcado
```
**Responsável:** `ico_converter.py` + `Preferences`

---

## 🎯 Responsabilidades Atuais

### `ICOConverter` (PLUGIN)
**Faz:**
- ✅ Criar layouts
- ✅ Responder a cliques
- ✅ Atualizar UI
- ✅ Orquestrar operações

**Deveria fazer:**
- ✓ Apenas UI (layouts, event handlers)
- ✓ Usar helpers de UI comum
- ✓ Delegar lógica para utils

**Problema:** Mistura UI + lógica  
**Solução:** Separar melhor + usar helpers existentes

---

### `FileExplorer`
**Responsabilidade:** Encontrar arquivos em pasta  
**Status:** ✅ Bom - faz isso bem

**Métodos:**
- `find_files(folder)` - retorna lista de caminhos
- `find_files_by_name(folder, pattern)` - filtra por nome
- `get_files_by_extension(folder, ext)` - filtra por extensão

---

### `ImageUtil`
**Responsabilidade:** Processar imagens (PIL operations)  
**Status:** ✅ Bom - "classe burra" que recebe dados

**Métodos:**
- `convert_image_to_ico(input, output, sizes)` - converte
- `convert_image_format(input, output, format)` - muda formato
- `resize_image(input, output, w, h)` - redimensiona
- `get_image_info(path)` - extrai metadados

---

### `ICOConverterStyles`
**Responsabilidade:** Centralizar CSS/QSS  
**Status:** ✅ Bom - reduz código duplicado

**Métodos:**
- `get_folder_label_style()`
- `get_button_style()`
- `get_image_list_style()`
- `get_control_panel_style()`
- etc...

---

### `PluginUIHelper`
**Responsabilidade:** UI comum a todos os plugins  
**Status:** ⚠️ Incompleto - faltam helpers úteis

**Métodos existentes:**
- `create_title()`
- `create_input_field()`
- `create_button()`
- `create_text_editor()`
- `create_list_widget()`

**Métodos que faltam:**
- `create_groupbox()` - para seções com título
- `create_checkbox_group()` - para grupos de checkboxes

---

## 🔧 Melhorias Propostas (SIMPLES)

### 1. Expandir `PluginUIHelper` com helpers ausentes

```python
@staticmethod
def create_groupbox(title: str, items: List[QWidget]) -> QGroupBox:
    """Cria GroupBox padronizado com itens."""
    group = QGroupBox(title)
    layout = QVBoxLayout(group)
    layout.setContentsMargins(6, 10, 6, 6)
    layout.setSpacing(3)
    for item in items:
        layout.addWidget(item)
    return group

@staticmethod
def create_checkbox_group(options: Dict[str, bool], callback=None) -> Tuple[QGroupBox, Dict[str, QCheckBox]]:
    """Cria grupo de checkboxes."""
    checkboxes = {}
    items = []
    for label, checked in options.items():
        cb = QCheckBox(label)
        cb.setChecked(checked)
        if callback:
            cb.stateChanged.connect(lambda state, lbl=label: callback(lbl, state))
        checkboxes[label] = cb
        items.append(cb)
    
    group = QGroupBox("Opções")
    layout = QVBoxLayout(group)
    for cb in items:
        layout.addWidget(cb)
    return group, checkboxes
```

### 2. Simplificar `ICOConverter.setup_control_panel()`

```python
# Usar PluginUIHelper para criar GroupBoxes
size_items = [QCheckBox(f"{s}x{s}") for s in [16, 32, 48, 64, 128, 256]]
size_group = PluginUIHelper.create_groupbox("Tamanhos (px)", size_items)

format_items = [
    QCheckBox("Manter"),
    QCheckBox("Remover")
]
format_group = PluginUIHelper.create_groupbox("Formato", format_items)
```

### 3. Mover lógica de thumbnail para método auxiliar

```python
def _create_thumbnail(self, file_path: str) -> QPixmap:
    """Gera thumbnail de uma imagem."""
    try:
        img = Image.open(file_path)
        img.thumbnail((160, 120), Image.LANCZOS)
        bio = BytesIO()
        img.convert("RGBA").save(bio, format="PNG")
        qimg = QImage.fromData(bio.getvalue())
        return QPixmap.fromImage(qimg)
    except Exception as e:
        logger.warning(self.TOOL_KEY, "ICOConverter", f"Erro ao gerar thumbnail: {e}")
        return None
```

### 4. Extrair lógica de conversão para método focado

```python
def _do_convert_single(self, img_path: str, output_dir: str, sizes: List[int]) -> Tuple[bool, str]:
    """Converte uma imagem, retorna (sucesso, mensagem)."""
    try:
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}.ico")
        
        success = ImageUtil.convert_image_to_ico(img_path, output_path, sizes)
        
        if success:
            return True, f"✓ {os.path.basename(img_path)}"
        else:
            return False, f"✗ Erro ao converter {os.path.basename(img_path)}"
    except Exception as e:
        return False, f"✗ {str(e)}"
```

---

## 📊 Estrutura Resultante (Simples)

```
ICOConverter (~350 linhas, organizado)
├─ create_widget() .................... Setup principal
├─ setup_folder_section() ........... UI: seleção de pasta
├─ setup_image_list() ............... UI: lista de imagens
├─ setup_control_panel() ............ UI: configurações + botão converter
│
├─ select_folder() ................... Handler: diálogo pasta
├─ add_files_dialog() ............... Handler: diálogo arquivos
├─ load_images_from_current_folder() Handler: recarrega lista
├─ add_image_to_list(path) ......... Handler: adiciona imagem
├─ clear_image_list() ............... Handler: limpa lista
│
├─ get_selected_sizes() ............ Getter: tamanhos marcados
├─ start_conversion() .............. Handler: inicia conversão
├─ convert_single_image() ......... Worker: converte uma imagem
├─ check_conversion_progress() .... Monitor: atualiza progresso
│
├─ on_base_path_changed() .......... Hook: quando pasta base muda
│
├─ _create_thumbnail(path) ......... Auxiliar: gera thumbnail
├─ _do_convert_single(path, dir, sizes) Auxiliar: converte e retorna status
└─ set_current_folder(path) ........ Auxiliar: atualiza pasta + UI + prefs
```

---

## ✅ Regra Simples para Organização

1. **`PluginUIHelper`** → Coisas que **TODOS os plugins precisam**
   - Criar buttons, inputs, lists padronizados
   - Cores, fontes, espaçamentos

2. **`ICOConverterStyles`** → Coisas **ESPECÍFICAS** do ICO Converter
   - Cores especiais, layouts complexos
   - Estilo do splitter, progress bar

3. **`ico_converter.py`** → **Orquestração UI** + **Lógica específica**
   - Como os componentes se conectam
   - Fluxo de eventos
   - Integração com FileExplorer + ImageUtil

4. **`FileExplorer`** → **Responsável APENAS** por encontrar arquivos
   - Agnóstico a UI, pode ser usado em CLI

5. **`ImageUtil`** → **Responsável APENAS** por processar imagens
   - Agnóstico a UI, pode ser usado em CLI
   - Recebe path → retorna sucesso/falha

---

## 🎓 Boas Práticas (Simples)

✅ **Nomes Claros:**
- `load_images_from_current_folder()` (claro o que faz)
- `_create_thumbnail()` (privado, auxiliar)
- `_do_convert_single()` (privado, conversor)

✅ **Separação:**
- UI methods (sem `_`) e Helpers (com `_`)
- Métodos com callback (eventos) e métodos puros (dados)

✅ **Documentação:**
- Docstring em métodos complexos
- Logging em pontos críticos
- Type hints em métodos públicos

✅ **Error Handling:**
- Try/except em operações de arquivo
- Return (sucesso, mensagem) para fácil feedback
- Log de erros para debug

---

**Próximo passo:** Implementar esses ajustes simples de forma prática?
