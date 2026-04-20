# Análise Técnica dos Scripts da Pasta src/

Olá de novo! Mesma explicação **super simples**, como se você fosse burro (no bom sentido 😄). Vamos analisar **TODOS os scripts Python** da pasta `src/` (coração da app!).

**Scripts encontrados (12 arquivos .py):**
1. `animations.py`
2. `base_plugin.py`
3. `draggable_tab_widget.py`
4. `draggable_toolbar.py`
5. `icon_generator.py`
6. `main_window.py`
7. `plugin_manager.py`
8. `plugin_ui_helper.py`
9. `signal_manager.py`
10. `theme.py`
11. `log_viewer.py` (cópia do config/)
12. `styles/ImageMergerStyles.py`

**Total de classes principais: ~20**. Vou explicar **cada uma** com exemplos burros!

## 1. animations.py - Os \"Truques Mágicos\" da Interface

### `UIAnimations` (classe estática - sem criar objeto)
**O que é?** Caixa de ferramentas pra fazer botões **se mexerem** bonitinho (hover, click, fade).

**Funções principais:**
| Função | O que faz? | Exemplo |
|--------|------------|---------|
| `create_fade_animation` | Fade in/out | Widget some/aparece suave |
| `create_color_animation` | Muda cor suave | Botão azul → verde |
| `create_scale_animation` | Aumenta/diminui | Botão cresce 5% no hover |
| `animate_hover_enter/leave` | Hover mouse | Botão fica mais azul |
| `animate_click` | Clique | Botão pisca + encolhe |
| `animate_fade_in` | Aparece novo widget | Plugin novo fade-in |

**Classes filhas:**
- `AnimatedButton/ToolButton`: Botão com animações automáticas
- `AnimatedTabBar`: Abas que reagem ao mouse
- `AnimatedListWidget`: Lista com hover

**Exemplo burro:** `UIAnimations.animate_click(meu_botao)` → Botão \"pula\"!

---

## 2. base_plugin.py - O \"Contrato\" pros Plugins

### `BasePlugin`
**O que é?** **Molde vazio** que todo plugin deve seguir (como receita de bolo).

**O que tem:**
- `name`, `icon_name` (info básica)
- `create_widget()`: **OBRIGATÓRIO** - retorna tela do plugin
- `on_base_path_changed(path)`: Opcional - quando pasta muda

**Exemplo:**
```python
class MeuPlugin(BasePlugin):
    name = \"SuperCalc\"
    def create_widget(self, parent):
        return QWidget()  # Sua tela aqui!
```

**Por quê?** Padroniza todos plugins!

---

## 3. draggable_tab_widget.py - Abas que Você Arraste!

### `DraggableTabBar` (herda AnimatedTabBar)
**O que é?** Barra de abas que você **arrasta pra trocar ordem**.

**Mágica:** Mouse press → drag → drop → aba muda posição!

### `DraggableTabWidget`
**Usa DraggableTabBar** no lugar da normal.

---

## 4. draggable_toolbar.py - Toolbar Arrástavel

### `DraggableToolBar`
**O que é?** Barra de ícones que **reordena arrastando**.

- `addPluginAction(icon, name, callback)`: Adiciona botão
- Drag/drop entre botões!

---

## 5. icon_generator.py - Fábrica de Ícones SVG

**Sem classes, só funções!**
- `create_icon_pixmap(name, size=24, color)`: Pega SVG hardcoded (calculator, todo, etc.) → QPixmap

**Exemplos:** \"calculator\" → ícone azul com círculos, \"ico_converter\" → 4 círculos + \"ICO\".

---

## 6. main_window.py - A \"Casa\" Principal (ESTRELA ★)

### `MainWindow` (herda QMainWindow)
**O que é?** **App inteira**: janelas, menus, plugins, barras.

**Faz TUDO:**
1. Carrega `PluginManager`, `Preferences`, `SignalManager`
2. Menu: File (pasta base), Help (logs/about)
3. **Toolbar superior**: Ícones plugins (arrastáveis, animados)
4. **Central**: Abas arrastáveis (DraggableTabWidget)
5. **Sidebar**: Lista plugins + pasta base
6. `_open_plugin(name)`: Abre/ativa plugin
7. Notifica plugins de mudanças (base_path)

**Exemplo:** Clica ícone Calculator → abre aba animada!

---

## 7. plugin_manager.py - O \"Carregador de Plugins\"

### `PluginManager`
**O que é?** **Leitor de mágica**: vasculha `plugins/*.py`, importa dinamicamente.

**Fluxo:**
1. `load_plugins()`: Para cada `plugins/*.py` → `mod.get_plugin()` → salva em `self.plugins`
2. `create_widget_for(name)`: Chama `plugin.create_widget()`
3. `get_plugin_names()`: Lista nomes

**Suporta PyInstaller (bundle exe)!**

---

## 8. plugin_ui_helper.py - \"Canivete Suíço\" da UI

### `PluginStyleSheet` (constantes)
Cores: azul `#0e639c`, verde `#4ec9b0`, etc. + templates QSS.

### `PluginUIHelper` (estática)
**Fabrica widgets prontos:**
- `create_title(text)` → Título grande
- `create_button(text, color)` → Botão animado
- `create_input_field()` → Caixa texto dark
- `create_text_editor()` → Editor código
- `create_list_widget()` → Lista hover
- `create_groupbox(title, widgets)` → Caixa agrupada
- `create_checkbox_group()` → Checkboxes

### `PluginContainer`
Base pra plugins: `setup_base_path_section()`, `update_base_path()`.

---

## 9. signal_manager.py - O \"Correio\" da App

### `SignalManager` (singleton)
**O que é?** Central de **mensagens** entre partes.

- Sinais Qt: `base_path_changed`
- Custom: `subscribe('nome', func)`, `emit('nome', data)`
- `emit_base_path_changed(path)`: Notifica TODOS plugins!

**Exemplo:** Main muda pasta → Signal avisa plugins → eles atualizam!

---

## 10. theme.py - O \"Maquiador Dark Mode\"

**Sem classes:** `DARK_STYLESHEET` gigante (CSS pro Qt).
- Cores VSCode: `#1e1e1e` bg, `#0e639c` azul, etc.
- Botões, tabs, lists, scrollbars TUDO estilizado!

---

## 11. log_viewer.py - Cópia do config/ (LogEntry + LogViewer)

**Mesmo código:** Tabela logs filtrada/colorida. Ignorar duplicata?

---

## 12. styles/ImageMergerStyles.py - Estilos pro Plugin Image Merger

### `ImageMergerStyles` (estática)
**Cores + getters QSS:**
- `get_button_style()` → Botões hover
- `get_image_list_style()` → Lista imagens
- `get_folder_label_style()` → Pasta atual
- Progressbar, spinbox, splitter, etc.

---

## Resumo Final (Pra Decorar!):
| Arquivo | Função Principal | Classes |
|---------|------------------|---------|
| animations | Animações UI | UIAnimations, Animated* |
| base_plugin | Molde plugins | BasePlugin |
| draggable_* | Drag/drop tabs/toolbar | Draggable* |
| main_window | App inteira ★ | MainWindow |
| plugin_manager | Carrega plugins | PluginManager |
| plugin_ui_helper | Fabrica UI | PluginUIHelper |
| signal_manager | Sinais/mensagens | SignalManager |
| theme | Dark stylesheet | - |
| icon_generator | Ícones SVG | Funções |

**Arquitetura:** MainWindow → PluginManager → BasePlugin → Seu plugin!
App **moderna**: animações, drag/drop, plugins dinâmicos, dark theme VSCode.

Abra **docs/src_scripts_analysis.md** pra ver formatado! Tarefa src/ ✅

